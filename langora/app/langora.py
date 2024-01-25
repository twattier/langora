from flask_marshmallow.sqla import SQLAlchemySchema

from loader.service_loader import ServiceLoader
from llm.service_model import ServiceModel
from db.dbvector import DbVector, STORE

class Langora():
    def __init__(self) -> None:                  
        self.db = DbVector()
        self.model = ServiceModel(self.db)           

    def init_services(self):
        self.db.init_db()
        self.model.init_model()        

    # ---------------------------------------------------------------------------
    # CLI function
    # ---------------------------------------------------------------------------

    def install_db_knowledge(self, agent:str, topics:list[str],
                            up_to_store:STORE=None):
        try:
            self.db.init_db()
            self.db.open_session()    

            loader = ServiceLoader(self.model, up_to_store=up_to_store)
            loader.init_knowledge(agent, topics)
        finally:
            self.db.close_session()
    
    # ---------------------------------------------------------------------------
    # API function
    # ---------------------------------------------------------------------------
        
    def get_knowledge(self, schema:SQLAlchemySchema):
        try:
            self.db.open_session()
            data = self.db.select_knowledge()
            return schema.dump(data)
        finally:
            self.db.close_session()
