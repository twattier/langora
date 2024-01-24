from datetime import datetime
from alive_progress import alive_bar

from config.env import Config
from db.datamodel import Knowledge, Search, Source, SearchSource
from llm.service_model import ServiceModel
from loader.google_search import google_search
from utils.functions import get_url_hostname

class ServiceLoader():

    def __init__(self, svc_model:ServiceModel) -> None:
        self.svc_model = svc_model
        self.db = svc_model.db

    def init_loader(self):
        loader = None
        if Config.USE_APIFY:            
            from loader.loader_apify import LoaderApify
            loader = LoaderApify()
        else:
            from loader.loader_html2text import LoaderHtml2Text
            loader = LoaderHtml2Text()
        self.loader=loader

    # ---------------------------------------------------------------------------
    # Source import
    # ---------------------------------------------------------------------------
        
    def init_knowledge(self, agent:str, topics:list[str])->None:
        self.db.recreate_database()        
        knowledge = Knowledge(agent=agent, topics=topics)
        self.db.add(knowledge)
        self.add_knowledge_recommendations()

    def add_knowledge_recommendations(self)->None:
        self.model_build()        
        new_searches = []
        for query in self.svc_model.get_knowledge_recommendations(self.model):
            search = self.db.select_search_by_query(query)
            if search:
                continue
            search=Search(query=query.strip(), from_user=False)
            self.db.add(search)
            new_searches.append(search)
        self.db.save()
        for search in new_searches:
            print(f'Store embeddings')        
            self.db.store_search_embeddings(search)
            self.import_google_search(search)        
    
    def update_knowledge_recommendations(self)->None:        
        for search in self.db.select_searches_recommended():
            self.import_google_search(search)

    # ---------------------------------------------------------------------------
    # Google research
    # ---------------------------------------------------------------------------

    def import_google_search(self, search:Search, 
                             with_summarize=False)->None:
        print(f'Google search : "{search.query}"')
        results = google_search(search.query)
        nb_results = len(results)
        new_sources = []
        with alive_bar(nb_results) as bar:
            for rank in range(nb_results):
                res = results[rank]
                url = res['link']
                site = get_url_hostname(url)
                title = res['title']
                src = self.db.select_source_by_url(url)
                if src:                    
                    print(f'- Skip : {title} [{site}]')
                    if search.contains_source(src.id):
                        bar()
                        continue
                else:
                    print(f'- Import : {title} [{site}]')
                    src = Source(url=url, 
                                site=site,
                                title=title,
                                snippet= res['snippet']
                                )                    
                    src.extract = self.loader.load_web(url).page_content
                    new_sources.append(src)
                search.search_sources.append(
                    SearchSource(source=src, rank=rank+1)
                )
                self.db.save()
                bar()

        print(f'Store embeddings')
        for source in new_sources:
            self.db.store_source_embeddings(source)
        
        if with_summarize:
            self.summarize_search(search)        
            self.db.save()

    # ---------------------------------------------------------------------------
    # Summarize
    # ---------------------------------------------------------------------------

    def summarize_search(self, search:Search)->None:      
        print(f'Summarize search results :')
        with alive_bar(len(search.search_sources)) as bar:       
            for sbs in search.search_sources:            
                self.summarize_source(sbs.source)
                bar()

    def summarize_sources(self):
        print(f'Summarize sources :') 
        sources = self.db.select_sources()
        with alive_bar(len(sources)) as bar:
            for source in sources:
                self.summarize_source(source)
                bar()
    
    def summarize_source(self, source:Source):   
        if source.summary:
            print(f'- Skip : {source.title} [{source.site}]')
            return
        print(f'- Summarize : {source.title} [{source.site}]')
        try:
            doc = source.document_extract()
            source.summary = self.svc_model.summarize(doc)
            source.date_summary = datetime.now()
            self.db.save()
        except Exception as error:
            print("An error occurred:", error)