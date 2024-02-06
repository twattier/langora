from enum import Enum
from copy import deepcopy
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain.vectorstores.pgvector import PGVector

from config.env import Config
from db.session_db import SessionDB
from db.datamodel import Base, Topic, Knowledge, Search, Source, SearchSource

CONNECTION_STRING = PGVector.connection_string_from_db_params(
    driver="psycopg2",
    host=Config.POSTGRES_HOST,
    port=Config.POSTGRES_PORT,
    database=Config.POSTGRES_DB,
    user=Config.POSTGRES_USER,
    password=Config.POSTGRES_PASSWORD
)

# ---------------------------------------------------------------------------
# DATAMODEL EMBEDDINGS
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# VECTOR DB Service
# ---------------------------------------------------------------------------
class DbVector():
    
    def __init__(self)->None:        
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

    # ---------------------------------------------------------------------------
    # EMBEDDINGS
    # ---------------------------------------------------------------------------

    # ---------------------------------------------------------------------------
    # Topic
        
    def store_topic_embeddings(self, sdb:SessionDB, topic:Topic)->None:
        #clean_embeddings
        query = """
                DELETE
                FROM langchain_pg_embedding
                WHERE CAST(cmetadata->>'topic_id' as integer) = %s
                """ % (topic.id)
        sdb.raw_execute(query)
        
        doc = Document(
                page_content=topic.name, metadata={"topic_id": topic.id}
            )
        self.stores[STORE.TOPIC.name].add_documents([doc])
            
    # ---------------------------------------------------------------------------
    # Search
        
    def update_search_embeddings(self, sdb:SessionDB):
        for search in sdb.select_searches():
            self.store_search_embeddings(sdb, search)
        
    def store_search_embeddings(self, sdb:SessionDB, search:Search)->None:
        #clean_embeddings
        query = """
                DELETE
                FROM langchain_pg_embedding
                WHERE CAST(cmetadata->>'search_id' as integer) = %s
                """ % (search.id)
        sdb.raw_execute(query)
        
        doc = Document(
                page_content=search.query, metadata={"search_id": search.id}
            )
        self.stores[STORE.SEARCH.name].add_documents([doc])

    # ---------------------------------------------------------------------------
    # Sources
        
    def update_sources_embeddings(self, sdb:SessionDB):
        for source in sdb.select_sources():
            self.store_source_embeddings(sdb, source)
        
    def store_source_embeddings(self, sdb:SessionDB, source:Source, type:STORE,
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
        sdb.raw_execute(query)

        #Split
        metadata = {"source_id" : source.id}
        docs = self._split_text(text, chunk_size)
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

    def _split_text(self, text:str, chunk_size=1000)->list[Document]:
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size, 
            chunk_overlap=0,
            # length_function=len,
            # is_separator_regex=False,
        )
        doc = Document(page_content=text)
        return text_splitter.split_documents([doc])
    
    def _similarities(self, text:str, type:STORE, 
                     nb=5)->(Document, float):
        return self.stores[type.name].similarity_search_with_relevance_scores(text, k=nb)   

    def _similarities_ids(self, text:str, type:STORE, 
                                nb=5)->dict[int, float]:
        sims = self._similarities(text, type, nb)
        ids = {}
        for sim in sims:
            doc = sim[0]
            id = doc.metadata['search_id'] if type == STORE.SEARCH else doc.metadata['source_id']
            ids[id] = sim[1]
        return ids     
        
    def similarity_searches(self, sdb:SessionDB, text:str, nb=5)->list[SimilaritySearch]:
        sims = self._similarities(text, STORE.SEARCH, nb)
        list = []
        for sim in sims:            
            doc = sim[0]
            score_query = sim[1]
            id = doc.metadata['search_id']
            search = sdb.select_search_by_id(id)
            list.append(SimilaritySearch(search, score_query))
        return list

    def similarity_sources(self, sdb:SessionDB, text:str,
                           nb=5)->list[SimilaritySource]:
        dict = {}
        for store in [STORE.SOURCE, STORE.SRC_SUMMARY]:
            sims = self._similarities_ids(text, store, nb=nb*4)
            for id, score in sims.items():
                ss = dict.get(id)
                if not ss:
                    source = sdb.select_source_by_id(id)
                    ss = SimilaritySource(source)
                    dict[id] = ss
                ss.set_score_src(store, score)
        lss = list(dict.values())
        lss.sort(key=lambda ss: ss.score_src(), reverse=True)
        if len(lss)>nb:
            lss = lss[:nb]
        return lss
    
    def similarity_sources_extract(self, sdb:SessionDB, text:str,
                                   nb=5)->(list[SimilaritySource], list[SimilaritySource]):
        sims = self.similarity_sources(sdb, text, nb=nb*5)
        sims_extract = self._similarities(text, STORE.SRC_EXTRACT, nb=nb*10)
        list = []
        for sim in sims_extract:
            doc = sim[0]
            score = sim[1]
            id = doc.metadata['source_id']
            chunk = doc.metadata.get('chunk')
            sim_src = self._seek_similarity_sources(id, sims)
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

    def _seek_similarity_sources(self, source_id:int, list:list[SimilaritySource])->SimilaritySource:
        for ss in list:
            if ss.source.id == source_id:
                return ss
        return None
            
