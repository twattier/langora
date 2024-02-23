from langchain_core.documents import Document

from loader.service_loader import ServiceLoader
from llm.service_model import ServiceModel
from db.service_db import ServiceDB, SessionDB
from db.dbvector import STORE
from task.service_task import ServiceTask
from utils.functions import split_list

class Langora():
    def __init__(self,
                 is_task_mode = False) -> None:
        self.is_task_mode = is_task_mode

        self.db = ServiceDB()        
        self.model = ServiceModel()
        self.model.init_model()
        self.tasks = ServiceTask() if self.is_task_mode else None

    def create_session(self):
        return self.db.create_session()
    
    def create_loader(self, sdb:SessionDB=None)->ServiceLoader:
        if not sdb:
            sdb = self.create_session()
        loader = ServiceLoader(sdb, self.model, self.tasks)
        if self.is_task_mode:
            loader.init_tasks()
        return loader

    # ---------------------------------------------------------------------------
    # Loader
    # ---------------------------------------------------------------------------

    def install_db_knowledge(self, agent:str, topics:list[str],
                            up_to_store=STORE.SOURCE):
        try:
            self.db.recreate_database()
            
            loader = self.create_loader()
            loader.init_knowledge(agent, topics, up_to_store)
        finally:
            loader.sdb.close()
        
    def update_db_knowledge(self, up_to_store=STORE.SOURCE):
        try:
            sdb = self.create_session()
            loader = self.create_loader(sdb=sdb)

            if up_to_store.value >= STORE.SRC_SUMMARY.value:
                #Sources without summary
                loader.update_summarize_sources()

            if up_to_store.value >= STORE.SRC_EXTRACT.value:
                #Sources without extract or summary
                loader.update_extract_sources(up_to_store=up_to_store)

            if up_to_store.value >= STORE.SOURCE.value:
                #Empty searches
                searches = sdb.select_searches()
                empties = [t for t in searches if len(t.search_sources)==0]
                if len(empties)>0:
                    loader.update_searches(empties, up_to_store=up_to_store)

            #Empty topics
            topics = sdb.select_topics()            
            empties = [t for t in topics if len(t.searches)==0]
            if len(empties)>0:
                loader.update_topics(empties, up_to_store=up_to_store)
        finally:
            sdb.close()

    # ---------------------------------------------------------------------------
    # Task

    def add_topics(self, topics:list[str], up_to_store_id:int):
        try:
            loader = self.create_loader()        
            up_to_store = STORE(up_to_store_id)            
            loader.add_topics(topics, up_to_store=up_to_store)        
        finally:
            loader.sdb.close()

    def add_searches(self, topic_ids:list[int], up_to_store_id:int):
        try:
            sdb = self.create_session()
            loader = self.create_loader(sdb=sdb)

            topics = sdb.select_topics_by_ids(topic_ids)
            up_to_store = STORE(up_to_store_id)            
            loader.add_searches_recommended(topics, up_to_store=up_to_store)
        finally:
            sdb.close()

    def add_sources(self, search_ids:list[int], up_to_store_id:int):
        try:
            sdb = self.create_session()
            loader = self.create_loader(sdb=sdb)

            up_to_store = STORE(up_to_store_id)  
            for list_ids in split_list(search_ids, 10): 
                searches = sdb.select_searches_by_ids(list_ids)
                loader.add_sources(searches, up_to_store=up_to_store)
        finally:
            sdb.close()

    def extract_source(self, source_id:int, up_to_store_id:int):
        try:
            sdb = self.create_session()
            loader = self.create_loader(sdb=sdb)

            source = sdb.select_source_by_id(source_id)
            up_to_store = STORE(up_to_store_id)            
            loader.extract_sources([source], up_to_store=up_to_store)
        finally:
            sdb.close()
            
    def summarize_source(self, source_id:int):
        try:
            sdb = self.create_session()
            loader = self.create_loader(sdb=sdb)

            source = sdb.select_source_by_id(source_id)
            loader.summarize_sources([source])
        finally:
            sdb.close()
    
    # ---------------------------------------------------------------------------
    # API function
    # ---------------------------------------------------------------------------
        
    def stats(self):
        try:
            sdb = self.create_session()

            topics = sdb.select_topics()
            topics_nb = len(topics)
            topics_filled_nb = len(list(filter(lambda t: len(t.searches)>0, topics)))
            topics_filled_pct = topics_filled_nb / topics_nb
            
            searches = sdb.select_searches()
            searches_nb = len(searches)
            searches_filled_nb = len(list(filter(lambda t: len(t.search_sources)>0, searches)))
            searches_filled_pct = searches_filled_nb / searches_nb

            sources = sdb.select_sources()
            sources_nb = len(sources)            
            sources_texts_nb = len(list(filter(lambda t: len(t.source_texts)>0, sources)))
            sources_texts_pct = sources_texts_nb / sources_nb
            sources_summarized_nb = len(list(filter(lambda t: t.summary is not None, sources)))
            sources_summarized_pct = sources_summarized_nb / sources_nb

            return {
                'topics' : {'nb':topics_nb, 'filled_nb' : topics_filled_nb, 'filled_pct' : topics_filled_pct},
                'searches' : {'nb':searches_nb, 'filled_nb' : searches_filled_nb, 'filled_pct' : searches_filled_pct},
                'sources' : {'nb':sources_nb,                                 
                                'texts_nb' : sources_texts_nb, 'texts_pct' : sources_texts_pct, 
                                'summarized_nb' : sources_summarized_nb, 'summarized_pct' : sources_summarized_pct
                            }
            }
        finally:
            sdb.close()
    
    def genAI(self, sdb:SessionDB, query, nb_extract=10, nb_ref=10):

        sim_docs, sim_sources = sdb.vector.similarity_sources_extract(query, nb=nb_extract)
        if len(sim_sources)>nb_ref:
            sim_sources = sim_sources[:nb_ref]
        sim_searches = sdb.vector.similarity_searches(query)
        docs = []
        for ss in sim_docs:
            docs.append(Document(page_content=ss.doc_text))
        response = self.model.rag(sdb, query, docs)
        
        return response, sim_docs, sim_sources, sim_searches


    
