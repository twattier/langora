from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from sqlalchemy.pool import NullPool

from config.env import Config
from langchain_community.embeddings import HuggingFaceEmbeddings
from db.dbvector import DbVector, CONNECTION_STRING
from db.session_db import SessionDB
from db.datamodel import Base

class ServiceDB():
    def __init__(self)->None:
        self.engine = create_engine(CONNECTION_STRING, echo=False)    
        self.embeddings = None  
        self.init_embeddings()          

    def create_session(self)->SessionDB:
        connexion = self.engine.connect()
        return SessionDB(connexion, self.embeddings)
    
    def init_embeddings(self):
        if self.embeddings:
            return
        print("Load model embeddings : " + Config.MODEL_EMBEDDINGS)
        self.embeddings = HuggingFaceEmbeddings(model_name = Config.MODEL_EMBEDDINGS, cache_folder=Config.HUGGINGFACE_CACHE)
    
    # ---------------------------------------------------------------------------
    # Create Database
    # ---------------------------------------------------------------------------

    def recreate_database(self):
        self.clean_database()        
        self.create_schema()

    def clean_database(self):
        connection = self.engine.connect()
        print('Clean Database if needed')       
        try:
            for dm in ["knowledge", 
                    "search_topic", 
                    "topic", 
                    "search_source", 
                    "source_text_images", 
                    "source_text", 
                    "source", 
                    "search"
                    ]:
                query = "DROP TABLE IF EXISTS " + dm
                connection.execute(text(query))
            for em in ["langchain_pg_embedding"]:
                query = "TRUNCATE " + em
                connection.execute(text(query))
        except:
            print('Clean Database error')
        finally:
            connection.close()

    def create_schema(self):
        print('Create schema')
        Base.metadata.create_all(self.engine)