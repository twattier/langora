from langchain_core.documents import Document

from loader.service_loader import ServiceLoader
from llm.service_model import ServiceModel
from db.dbvector import DbVector, STORE
from task.service_task import ServiceTask

class Langora():
    def __init__(self,
                 is_task_mode = False) -> None:                  
        self.db = DbVector()
        self.model = ServiceModel(self.db)
        self.tasks = ServiceTask()
        self.loader = ServiceLoader(self.model, tasks=self.tasks)
        if is_task_mode:
            self.loader.init_tasks()

    def init_store_model(self):
        self.db.init_stores()
        self.model.init_model()    

    # ---------------------------------------------------------------------------
    # Loader
    # ---------------------------------------------------------------------------

    def install_db_knowledge(self, agent:str, topics:list[str],
                            up_to_store:STORE=STORE.SOURCE):
        try:            
            self.init_store_model()
            self.db.open_session()               
            self.loader.init_knowledge(agent, topics, up_to_store)
        finally:
            self.db.close_session()

    def update_db_knowledge(self, up_to_store:STORE=STORE.SOURCE):
        try:            
            self.init_store_model()
            self.db.open_session()    
            #Sources without summary
            self.loader.update_summarize_sources()            
            #Sources without extract or summary
            self.loader.update_extract_sources(up_to_store=up_to_store)
            #Empty topics
            topics = self.db.select_topics()
            empties = filter(lambda t: len(t.searches)==0, topics)
            self.loader.update_topics(empties, up_to_store=up_to_store)
        finally:
            self.db.close_session()

    # ---------------------------------------------------------------------------
    # Task

    def add_searches(self, topic_ids:list[int], up_to_store_id:int):
        try:            
            self.init_store_model()
            self.db.open_session()   

            topics = self.db.select_topics_by_ids(topic_ids)
            up_to_store = STORE(up_to_store_id)            
            self.loader.add_searches_recommended(topics, up_to_store=up_to_store)
        finally:
            self.db.close_session()

    def add_sources(self, search_ids:list[int], up_to_store_id:int):
        try:            
            self.init_store_model()
            self.db.open_session()   

            searches = self.db.select_searches_by_ids(search_ids)
            up_to_store = STORE(up_to_store_id)            
            self.loader.add_sources(searches, up_to_store=up_to_store)
        finally:
            self.db.close_session()

    def extract_source(self, source_id:int, up_to_store_id:int):
        try:            
            self.init_store_model()
            self.db.open_session()   

            source = self.db.select_source_by_id(source_id)
            up_to_store = STORE(up_to_store_id)            
            self.loader.extract_sources([source], up_to_store=up_to_store)
        finally:
            self.db.close_session()
            
    def summarize_source(self, source_id:int):
        try:            
            self.init_store_model()
            self.db.open_session()   

            source = self.db.select_source_by_id(source_id)
            self.loader.summarize_sources([source])
        finally:
            self.db.close_session()
    
    # ---------------------------------------------------------------------------
    # API function
    # ---------------------------------------------------------------------------
        
    def genAI(self, query, nb_extract=3, nb_ref=5):

        sim_docs, sim_sources = self.db.similarity_sources_extract(query, nb=nb_extract)
        if len(sim_sources)>nb_ref:
            sim_sources = sim_sources[:nb_ref]
        sim_searches = self.db.similarity_searches(query)
        docs = []
        for ss in sim_docs:
            docs.append(Document(page_content=ss.doc_text))
        response = self.model.rag(query, docs)
        
        return response, sim_docs, sim_sources, sim_searches


    
