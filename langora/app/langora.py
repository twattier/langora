from flask_marshmallow.sqla import SQLAlchemySchema

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
            
    def summarize_source(self, source_id:int, up_to_store_id:int):
        try:            
            self.init_store_model()
            self.db.open_session()   

            source = self.db.select_source_by_id(source_id)
            up_to_store = STORE(up_to_store_id)            
            self.loader.summarize_sources([source], up_to_store=up_to_store)
        finally:
            self.db.close_session()
    
    # ---------------------------------------------------------------------------
    # API function
    # ---------------------------------------------------------------------------
        
    
