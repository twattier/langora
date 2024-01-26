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
                 use_task_mode=False) -> None:
        self.model = model
        self.db = model.db        
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
    # Import chain
    # ---------------------------------------------------------------------------
    
    def chain_loader(self, inputs:list, from_store:STORE, to_store:STORE)->list:
        order = [STORE.TOPIC, STORE.SEARCH, STORE.SOURCE, STORE.SRC_EXTRACT, STORE.SRC_SUMMARY]
        list = inputs
        for store in order:
            if store.value<=from_store.value:
                continue
            elif store.value>to_store.value:
                break
            if store == STORE.TOPIC:
                list = self.add_topics(list)
            elif store == STORE.SEARCH:
                if from_store == STORE.TOPIC:
                    list = self.add_searches_recommended(list)
                else:
                    list = self.add_searches(list)
            elif store == STORE.SOURCE:
                list = self.add_sources(list)
            elif store == STORE.SRC_EXTRACT:
                list = self.extract_sources(list)
            elif store == STORE.SRC_SUMMARY:
                list = self.summarize_sources(list)
        return list

    # ---------------------------------------------------------------------------
    # knowledge

    def init_knowledge(self, agent:str, names:list[str], up_to_store:STORE)->None:
        """Create the database 
            + Create the Knowledge object
            + Add recommended search + recommended topic
            + (optional create source -> extract -> summarized them)
        """
        self.db.recreate_database()        
        knowledge = Knowledge(agent=agent)
        self.db.add(knowledge)
        self.db.save()
        
        self.add_topics(names, up_to_store)

    # ---------------------------------------------------------------------------
    # Topics
        
    def add_topics(self, names:list[str],
                   up_to_store:STORE=None)->list[Topic]:        
        print('Add topics :')
        new_topics = []
        for name in names:
            #TODO check duplicate similarity
            print(f'- Add : {name}')
            topic = Topic(name=name)
            self.db.add(topic)            
            new_topics.append(topic)        
        self.db.save()

        print('Embeddings topics')
        for topic in new_topics:
            self.db.store_topic_embeddings(topic) #TODO manage list

        if up_to_store:
            self.chain_loader(new_topics, STORE.TOPIC, up_to_store)

        return new_topics

    # ---------------------------------------------------------------------------
    # Search

    def add_searches_recommended(self, topics:list[Topic]
                                 , up_to_store:STORE=None)->list[Search]:        
        print(f'Add searches recommended')
        searches = []
        with alive_bar(len(topics)) as bar:
            for topic in topics:
                print(f'Recommended for : {topic.name}')
                queries = self.model.get_topic_searches_recommended(topic.name)
                searches.extend(self.add_searches(queries, topic))
                bar()

        if up_to_store:
            self.chain_loader(searches, STORE.SEARCH, up_to_store)

        return searches

    def add_searches(self, queries:list[str], topic:Topic=None
                     , up_to_store:STORE=None)->list[Search]:
        print(f'Add searches :')
        new_searches = []               
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

        self.db.save()
        print('Embeddings searches')
        for search in new_searches:
            self.db.store_search_embeddings(search) #TODO manage list

        if up_to_store:
            self.chain_loader(new_searches, STORE.SEARCH, up_to_store)
        
        return new_searches

    # ---------------------------------------------------------------------------
    # Source
                
    def update_sources(self
                       , up_to_store:STORE=None)->list[Source]:
        return self.add_sources(self.db.select_searches(), up_to_store=up_to_store)

    def add_sources(self, searches:list[Search]
                    , up_to_store:STORE=None)->list[Source]:
        print(f'Add sources : ')
        new_sources = []
        with alive_bar(len(searches)) as bar:
            for search in searches:
                print(f'Sources for : "{search.query}"')
                results = google_search(search.query)                
                for rank in range(len(results)):
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

        if up_to_store:
            self.chain_loader(new_sources, STORE.SOURCE, up_to_store)

        return new_sources

    def extract_sources(self, sources:list[Source]
                        , up_to_store:STORE=None)->list[Source]:
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

        if up_to_store:
            self.chain_loader(update_sources, STORE.SRC_EXTRACT, up_to_store)

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