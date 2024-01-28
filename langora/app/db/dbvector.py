import numbers
from enum import Enum
from langchain.vectorstores.pgvector import PGVector
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from sqlalchemy import create_engine, select, text, func, and_
from sqlalchemy.orm import Session

from config.env import Config
from db.datamodel import Base, Topic, Knowledge, Search, Source

CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver="psycopg2",
    host=Config.POSTGRES_HOST,
    port=Config.POSTGRES_PORT,
    database=Config.POSTGRES_DB,
    user=Config.POSTGRES_USER,
    password=Config.POSTGRES_PASSWORD
)

STORE = Enum('Store', ['TOPIC', 'SEARCH', 'SOURCE', 'SRC_EXTRACT', 'SRC_SUMMARY'])

class DbVector():
    
    def __init__(self)->None:        
        self.engine = create_engine(CONNECTION_STRING, echo=False)
        self.session = None
        self.embeddings = None
        self.stores = None

    def init_embeddings(self):
        if self.embeddings:
            return
        print("Load model embeddings : " + Config.MODEL_EMBEDDINGS)
        self.embeddings = HuggingFaceEmbeddings(model_name = Config.MODEL_EMBEDDINGS, cache_folder=Config.HUGGINGFACE_CACHE)

    def init_stores(self)->None:
        if self.stores:
            return        
        self.init_embeddings()
        self.stores = {}
        for store in [STORE.TOPIC, STORE.SEARCH, STORE.SRC_EXTRACT, STORE.SRC_SUMMARY]:            
            self.stores[store.name] = PGVector(
                            collection_name=store.name,
                            connection_string=CONNECTION_STRING,
                            embedding_function=self.embeddings,
                            )
        
    def open_session(self)->None:
        if self.session:
            return
        self.session = Session(self.engine, expire_on_commit=False)

    def close_session(self)->None:
        if not self.session:
            return
        self.session.close()
        self.session = None
    
    def add(self, obj:Base)->None:
        self.session.add(obj)

    # ---------------------------------------------------------------------------
    # SELECT DATABASE
    # ---------------------------------------------------------------------------

    # ---------------------------------------------------------------------------
    # Knowledge
    
    def select_knowledge(self)->Knowledge:
        stmt = select(Knowledge)
        return self.select_one(stmt)
    
    # ---------------------------------------------------------------------------
    # Topic
    
    def select_topics_by_ids(self, ids:list[int])->list[Topic]:
        stmt = select(Topic).where(Topic.id.in_(ids))
        return self.select_many(stmt)

    # ---------------------------------------------------------------------------
    # Search 
        
    def select_search_by_id(self, id:int)->Search:
        stmt = select(Search).where(Search.id==id)
        return self.select_one(stmt)
    
    def select_searches_by_ids(self, ids:list[int])->list[Topic]:
        stmt = select(Search).where(Search.id.in_(ids))
        return self.select_many(stmt)
        
    def select_search_by_query(self, query)->Search:
        stmt = select(Search).where(func.lower(Search.query)==func.lower(query))
        return self.select_one(stmt)
    
    def select_searches(self)->list[Search]:
        stmt = select(Search)
        return self.select_many(stmt)
    
    # ---------------------------------------------------------------------------
    # Sources

    def select_source_by_id(self, id:int)->Source:
        stmt = select(Source).where(Source.id==id)
        return self.select_one(stmt)
    
    def select_source_by_url(self, url)->Source:
        stmt = select(Source).where(func.lower(Source.url)==func.lower(url))
        return self.select_one(stmt)
    
    def select_sources(self)->list[Source]:
        stmt = select(Source)
        return self.select_many(stmt)
    
    def select_not_extracted_sources(self)->list[Source]:
        stmt = select(Source).where(Source.extract == None)
        return self.select_many(stmt)
    
    def select_not_summarized_sources(self)->list[Source]:
        stmt = select(Source).where(
            and_(Source.extract != None, Source.summary == None)
            )
        return self.select_many(stmt)

    # ---------------------------------------------------------------------------
    # Utils SqlAlchemy
    # ---------------------------------------------------------------------------

    def recreate_database(self):
        self.clean_database()        
        self.create_schema()

    def clean_database(self):
        print('Clean Database if needed')       
        for dm in ["knowledge", "search_topic", "topic", "search_source", "source", "search"]:
            query = "DROP TABLE IF EXISTS " + dm
            self.raw_execute(query)
        for em in ["langchain_pg_embedding"]: #, "langchain_pg_collection"]:
            query = "TRUNCATE " + em
            self.raw_execute(query)        

    def create_schema(self):
        print('Create schema')
        Base.metadata.create_all(self.engine)

    def exists(self, table, **kargs):
        criteria = ""
        for key, value in kargs:
            if criteria != "": criteria += " AND "
            criteria += f"{key} = "
            criteria = str(value) if isinstance(value, numbers.Number) else f"'{value}'"
        stmt = text(f"SELECT 1 from {table} WHERE {criteria}")
        return self.session.execute(stmt).first() != None

    def select_one(self, stmt):        
        return self.session.execute(stmt).scalar_one_or_none()
    
    def select_many(self, stmt):
        return self.session.execute(stmt).scalars().all()
    
    def save(self)->None:        

        nb_new = len(self.session.new)
        nb_update = len(self.session.dirty)
        nb_delete = len(self.session.deleted)
        nb_change = nb_new + nb_update + nb_delete

        if nb_change == 0:
            print("Commit : No change")
            return 
          
        print("Commit : new objects  : {} , updated objects : {}, deleted objects : {}"
              .format(nb_new, nb_update, nb_delete))        
        self.session.commit()

    def raw_execute(self, query:str)->None:
        try:
            connection = self.engine.raw_connection()
            cursor = connection.cursor()
            command = query
            cursor.execute(command)
            connection.commit()            
        except:
            print("SQL Execute Error : " + query)
        finally:
            cursor.close()

    # ---------------------------------------------------------------------------
    # EMBEDDINGS
    # ---------------------------------------------------------------------------

    # ---------------------------------------------------------------------------
    # Topic
        
    def store_topic_embeddings(self, topic:Topic)->None:
        #clean_embeddings
        query = """
                DELETE
                FROM langchain_pg_embedding
                WHERE CAST(cmetadata->>'topic_id' as integer) = %s
                """ % (topic.id)
        self.raw_execute(query)
        
        doc = Document(
                page_content=topic.name, metadata={"topic_id": topic.id}
            )
        self.stores[STORE.TOPIC.name].add_documents([doc])
            
    # ---------------------------------------------------------------------------
    # Search
        
    def update_search_embeddings(self):
        for search in self.select_searches():
            self.store_search_embeddings(search)
        
    def store_search_embeddings(self, search:Search)->None:
        #clean_embeddings
        query = """
                DELETE
                FROM langchain_pg_embedding
                WHERE CAST(cmetadata->>'search_id' as integer) = %s
                """ % (search.id)
        self.raw_execute(query)
        
        doc = Document(
                page_content=search.query, metadata={"search_id": search.id}
            )
        self.stores[STORE.SEARCH.name].add_documents([doc])

    # ---------------------------------------------------------------------------
    # Sources
        
    def update_sources_embeddings(self):
        for source in self.select_sources():
            self.store_source_embeddings(source)
        
    def store_source_embeddings(self, source:Source, type:STORE,
                                chunk_size=1000)->None:
        text = None
        if type==STORE.SRC_EXTRACT:
            text = source.extract
        elif type==STORE.SRC_SUMMARY:
            text = source.summary
        if not text:
            return        
        
        #clean_embeddings
        query = """
                DELETE
                FROM langchain_pg_embedding
                WHERE CAST(cmetadata->>'source_id' as integer) = %s
                and collection_id in
                    (select uuid from langchain_pg_collection where name = '%s')
                """ % (source.id, type.name)
        self.raw_execute(query)

        #Split
        metadata = {"source_id" : source.id}
        docs = self.split_text(text, chunk_size)
        idx = 0
        for doc in docs:            
            idx += 1
            doc.metadata = metadata.copy()
            doc.metadata['chunk'] = idx
        self.stores[type.name].add_documents(docs)

        #Store
        self.stores[type.name].add_documents(docs)

    # ---------------------------------------------------------------------------
    # Utils

    def split_text(self, text:str, chunk_size=1000)->list[Document]:
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size, 
            chunk_overlap=0,
            # length_function=len,
            # is_separator_regex=False,
        )
        doc = Document(page_content=text)
        return text_splitter.split_documents([doc])
    
    def similarity_search(self, text:str, type:STORE, 
                          nb=5):
        return self.stores[type.name].similarity_search_with_relevance_scores(text, k=nb)        
        
    