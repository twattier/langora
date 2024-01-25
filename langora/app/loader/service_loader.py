from datetime import datetime
from alive_progress import alive_bar

from config.env import Config
from db.dbvector import DbVector, STORE
from db.datamodel import Knowledge, Search, Source, SearchSource
from llm.service_model import ServiceModel
from loader.google_search import google_search
from utils.functions import get_url_hostname

class ServiceLoader():

    def __init__(self, model:ServiceModel,
                 up_to_store:STORE = None,
                 use_task_mode=False) -> None:
        self.model = model
        self.db = model.db
        self.stage_store = None
        self.up_to_store = up_to_store
        self.use_task_mode = use_task_mode
        self.init_loader()

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
    
    def continue_loading(self)->bool:
        if not self.up_to_store:
            return False
        if not self.stage_store:
            return True
        return self.up_to_store.value>self.stage_store

    def init_knowledge(self, agent:str, topics:list[str])->None:
        """Create the database 
            + Create the Knowledge object
            + Add recommended search
            + (optional create source -> extract -> summarized them)
        """
        self.db.recreate_database()        
        knowledge = Knowledge(agent=agent, topics=topics)
        self.db.add(knowledge)
        self.db.save()        
        
        # self.model.db = self.db
        # self.model.init_model()
        self.add_search_recommendations()

    def add_search_recommendations(self)->None:
        self.model.init_model() 

        print(f'Add search recommendations')
        new_searches = []
        for query in self.model.get_knowledge_recommendations(self.model):
            search = self.db.select_search_by_query(query)
            if search:
                continue
            search=Search(query=query.strip(), from_user=False)
            self.db.add(search)
            new_searches.append(search)
            self.db.store_search_embeddings(search)
        self.db.save()
        
        if self.continue_loading():
            for search in new_searches:            
                self.import_google_search(search)
    
    def import_search_recommendations(self)->None:        
        for search in self.db.select_searches_recommended():
            self.import_google_search(search)

    # ---------------------------------------------------------------------------
    # Google research
    # ---------------------------------------------------------------------------

    def import_google_search(self, search:Search)->None:
        print(f'Google search : "{search.query}"')
        self.stage_store = STORE.SEARCH

        results = google_search(search.query)
        nb_results = len(results)
        new_sources = []
        with alive_bar(nb_results) as bar:
            for rank in range(nb_results):
                res = results[rank]
                url = res['link']
                site = get_url_hostname(url)
                title = res['title']
                source = self.db.select_source_by_url(url)
                if source:                    
                    print(f'- Skip : {source.get_name()}')
                    if search.contains_source(source.id):
                        bar()
                        continue
                else:                    
                    source = Source(url=url, 
                                site=site,
                                title=title,
                                snippet= res['snippet']
                                )
                    print(f'- Add : {source.get_name()}')
                    new_sources.append(source)
                search.search_sources.append(
                    SearchSource(source=source, rank=rank+1)
                )                
                bar()
            
        self.db.save()
        
        if self.continue_loading():
            self.extract_sources(new_sources)

    def extract_sources(self, sources:list[Source])->None:
        nb = len(sources)
        if nb == 0:
            return        
        print('Extract Sources :')
        self.stage_store = STORE.EXTRACT
        with alive_bar(nb) as bar:
            for source in sources:
                if source.extract:
                    print(f'- Skip : {source.get_name()}')
                    bar()
                    continue
                print(f'- Extract : {source.get_name()}')
                source.extract = self.loader.load_web(source.url).page_content
                source.date_extract = datetime.now()                
                self.db.save()
                self.db.store_source_embeddings(source, STORE.EXTRACT)
                bar()
        
        if self.continue_loading():
            self.summarize_sources(sources)

    def summarize_sources(self, sources:list[Source]):
        nb = len(sources)
        if nb == 0:
            return
        print(f'Summarize sources :') 
        self.stage_store = STORE.SUMMARY
        with alive_bar(nb) as bar:
            for source in sources:
                if source.summary:
                    print(f'- Skip : {source.get_name()}')
                    bar()
                    continue
                print(f'- Summary : {source.get_name()}')
                try:
                    doc = source.document_extract()
                    source.summary = self.model.summarize(doc)
                    source.date_summary = datetime.now()                    
                    self.db.save()
                    self.db.store_source_embeddings(source, STORE.SUMMARY)
                except Exception as error:
                    print("An error occurred:", error)
                bar()