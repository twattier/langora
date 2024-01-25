from flask_marshmallow.sqla import SQLAlchemySchema

from loader.service_loader import ServiceLoader
from llm.service_model import ServiceModel
from db.dbvector import DbVector

class Langora():
    def __init__(self) -> None:                  
        self.db = DbVector()
        self.svc_model = ServiceModel(self.db)   
        self.svc_loader = ServiceLoader(self.svc_model)

    def init_services(self):
        self.db.init_db()
        self.svc_model.init_model()
        self.svc_loader.init_loader()

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
