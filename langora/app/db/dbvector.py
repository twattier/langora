import numbers
from enum import Enum
from copy import deepcopy
from langchain.vectorstores.pgvector import PGVector
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from sqlalchemy import create_engine, select, text, func, and_
from sqlalchemy.orm import Session

from config.env import Config
from db.datamodel import Base, Topic, Knowledge, Search, Source, SearchSource

CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver="psycopg2",
    host=Config.POSTGRES_HOST,
    port=Config.POSTGRES_PORT,
    database=Config.POSTGRES_DB,
    user=Config.POSTGRES_USER,
    password=Config.POSTGRES_PASSWORD
)

STORE = Enum('Store', ['TOPIC', 'SEARCH', 'SOURCE', 'SRC_EXTRACT', 'SRC_SUMMARY'])

class SimilaritySearch():
    def __init__(self, search:Search, score_query:float) -> None:
        self.search = search
        self.score_query = score_query

class SimilaritySource():
    def __init__(self, source:Source) -> None:
        self.source = source
        self.scores:dict[STORE, float] = {}
        self.doc_score:float = None
        self.doc_type:str = None
        self.doc_chunk:int = None
        self.doc_text:str = None
    
    def set_score_src(self, store:STORE, value:float):
        prev = self.scores.get(store)
        if prev and prev>value:
            return
        self.scores[store] = value

    def score_title(self):
        return self.scores.get(STORE.SOURCE)
    def score_summary(self):
        return self.scores.get(STORE.SRC_SUMMARY)

    def score_src(self)->float:
        if len(self.scores)==0:
            return None
        return max(list(self.scores.values()))
    
    def score_total(self)->float:
        """ doc score + weighting on src score (1/3) """
        if not self.doc_score:
            return 0
        vsrc = self.score_src()
        weight = vsrc/3 if vsrc else 1
        return self.doc_score * (1 + weight)


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
        for store in [STORE.SEARCH, STORE.SOURCE, STORE.SRC_EXTRACT, STORE.SRC_SUMMARY]:            
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
    
    def select_top_searches(self, max=5)->list[Source]:
        stmt = select(Search, func.count(SearchSource.source_id).label('total')) \
                .join(Source.search_sources).group_by(Search).order_by(text('total DESC')).limit(max)
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
    
    def select_top_sources(self, max=5)->list[Source]:
        stmt = select(Source, func.count(SearchSource.search_id).label('total')) \
                .join(Source.search_sources).group_by(Source).order_by(text('total DESC')).limit(max)
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
        if type==STORE.SOURCE:
            text = source.title
        elif type==STORE.SRC_EXTRACT:
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
            if len(docs)>1:
                doc.metadata['chunk'] = idx        

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
    
    def similarities(self, text:str, type:STORE, 
                     nb=5)->(Document, float):
        return self.stores[type.name].similarity_search_with_relevance_scores(text, k=nb)   

    def similarities_ids(self, text:str, type:STORE, 
                                nb=5)->dict[int, float]:
        sims = self.similarities(text, type, nb)
        ids = {}
        for sim in sims:
            doc = sim[0]
            id = doc.metadata['search_id'] if type == STORE.SEARCH else doc.metadata['source_id']
            ids[id] = sim[1]
        return ids     
        
    def similarity_searches(self, text:str, nb=5)->list[SimilaritySearch]:
        sims = self.similarities(text, STORE.SEARCH, nb)
        list = []
        for sim in sims:            
            doc = sim[0]
            score_query = sim[1]
            id = doc.metadata['search_id']
            search = self.select_search_by_id(id)
            list.append(SimilaritySearch(search, score_query))
        return list

    def similarity_sources(self, text:str,
                           nb=5)->list[SimilaritySource]:
        dict = {}
        for store in [STORE.SOURCE, STORE.SRC_SUMMARY]:
            sims = self.similarities_ids(text, store, nb=nb*4)
            for id, score in sims.items():
                ss = dict.get(id)
                if not ss:
                    source = self.select_source_by_id(id)
                    ss = SimilaritySource(source)
                    dict[id] = ss
                ss.set_score_src(store, score)
        lss = list(dict.values())
        lss.sort(key=lambda ss: ss.score_src(), reverse=True)
        if len(lss)>nb:
            lss = lss[:nb]
        return lss
    
    def similarity_sources_extract(self, text:str,
                                   nb=5)->(list[SimilaritySource], list[SimilaritySource]):
        sims = self.similarity_sources(text, nb=nb*5)
        sims_extract = self.similarities(text, STORE.SRC_EXTRACT, nb=nb*10)
        list = []
        for sim in sims_extract:
            doc = sim[0]
            score = sim[1]
            id = doc.metadata['source_id']
            chunk = doc.metadata.get('chunk')
            sim_src = self.seek_similarity_sources(id, sims)
            if not sim_src:
                continue
            sim_doc = deepcopy(sim_src)
            sim_doc.doc_type = "Extract"
            sim_doc.doc_text = doc.page_content
            if chunk:
                sim_doc.doc_chunk = int(chunk)
            sim_doc.doc_score = score
            list.append(sim_doc)

        #TODO manage if len<nb or add all sims_extract
            
        list.sort(key=lambda ss: ss.score_total(), reverse=True)
        if len(list)>nb:
            list = list[:nb]
        return list, sims

    def seek_similarity_sources(self, source_id:int, list:list[SimilaritySource])->SimilaritySource:
        for ss in list:
            if ss.source.id == source_id:
                return ss
        return None
            
