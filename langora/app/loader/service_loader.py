from datetime import datetime
from alive_progress import alive_bar

from config.env import Config
from db.dbvector import DbVector, STORE
from db.datamodel import Knowledge, Topic, Search, Source, SearchSource
from llm.service_model import ServiceModel
from loader.google_search import google_search
from utils.functions import get_url_hostname

class ServiceLoader():

    def __init__(self, model:ServiceModel,
                 up_to_store:STORE = None,
                 use_task_mode=False) -> None:
        self.model = model
        self.db = model.db        
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
    
    def continue_loading(self, step:STORE)->bool:
        if not self.up_to_store:
            return False        
        return self.up_to_store.value>=step.value

    def init_knowledge(self, agent:str, topics:list[str])->None:
        """Create the database 
            + Create the Knowledge object
            + Add recommended search + recommended topic
            + (optional create source -> extract -> summarized them)
        """
        self.db.recreate_database()        
        knowledge = Knowledge(agent=agent)
        self.db.add(knowledge)
        self.db.save()
        
        self.add_topics(topics)

    # ---------------------------------------------------------------------------
    # Topics
        
    def add_topics(self, names:list[str])->None:        
        print('Add topics :')
        new_topics = []
        for name in names:
            #TODO check duplicate similarity
            print(f'- Add : {name}')
            topic = Topic(name=name)
            self.db.add(topic)            
            new_topics.append(topic)        
        self.db.save()
        
        print('Embeddings topics :')
        for topic in new_topics:
            self.db.store_topic_embeddings(topic) #TODO manage list

        if self.continue_loading(STORE.SEARCH):
            for topic in new_topics:
                self.add_topic_searches_recommended(topic)

    # ---------------------------------------------------------------------------
    # Search

    def add_topic_searches_recommended(self, topic:Topic)->None:
        print(f'Add searches recommended for : {topic.name}')     
        queries = self.model.get_topic_searches_recommended(topic.name)
        self.add_searches(queries, topic=topic)

    def add_searches(self, queries:list[str], topic:Topic=None)->None:
        print(f'Add searches :')
        new_searches = []
        with alive_bar(len(queries)) as bar:        
            for query in queries:
                #TODO check duplicate similarity query
                search = self.db.select_search_by_query(query)
                if search:
                    print(f'- Skip : {query}')
                else:
                    print(f'- Add : {query}')
                    search=Search(query=query)
                    self.db.add(search)
                    new_searches.append(search)                    
                if topic and topic not in search.topics:
                    search.topics.append(topic)
                    #TODO complete with identified topics (handle similarity topic)
                bar()

        self.db.save()
        print('Embeddings searches :')
        for search in new_searches:
            self.db.store_search_embeddings(search) #TODO manage list
        
        if not self.continue_loading(STORE.SOURCE):
            return
        new_sources = []
        for search in new_searches:
            new_sources.extend(self.add_sources(search))

        if not self.continue_loading(STORE.SRC_EXTRACT):
            return
        update_sources = self.extract_sources(new_sources)

        if not self.continue_loading(STORE.SRC_SUMMARY):
            return
        self.summarize_sources(update_sources)

    # ---------------------------------------------------------------------------
    # Source
                
    def update_sources(self)->None:        
        for search in self.db.select_searches():
            self.add_sources(search)

    def add_sources(self, search:Search)->None:
        print(f'Add sources for : "{search.query}"')
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
        return new_sources

    def extract_sources(self, sources:list[Source])->list[Source]:
        update_sources = []
        nb = len(sources)
        if nb == 0:
            return update_sources
        print('Extract Sources :')
        with alive_bar(nb) as bar:
            for source in sources:
                if source.extract:
                    print(f'- Skip : {source.get_name()}')
                    bar()
                    continue
                print(f'- Extract : {source.get_name()}')
                source.extract = self.loader.load_web(source.url).page_content
                source.date_extract = datetime.now()                
                update_sources.append(source)
                self.db.save()
                self.db.store_source_embeddings(source, STORE.SRC_EXTRACT)
                bar()
        return update_sources
        
    def summarize_sources(self, sources:list[Source])->list[Source]:
        update_sources = []
        nb = len(sources)
        if nb == 0:
            return update_sources
        print(f'Summarize sources :') 
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
                    update_sources.append(source)              
                    self.db.save()
                    self.db.store_source_embeddings(source, STORE.SRC_SUMMARY)
                except Exception as error:
                    print("An error occurred:", error)
                bar()
        return update_sources