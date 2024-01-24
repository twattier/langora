from loader.service_loader import ServiceLoader
from llm.service_model import ServiceModel
from db.dbvector import DbVector

class Langora():
    def __init__(self) -> None:                  
        self.db = DbVector()
        self.svc_model = ServiceModel(self.db)   
        self.svc_loader = ServiceLoader(self.svc_model)

    def init_services(self):
        self.db.init_embeddings()
        self.db.init_stores()        
        self.svc_model.init_model()
        self.svc_loader.init_loader()
