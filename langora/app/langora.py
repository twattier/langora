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
        loader = ServiceLoader(sdb, self.db.vector, self.model, self.tasks)
        if self.is_task_mode:
            loader.init_tasks()
        return loader

    # ---------------------------------------------------------------------------
    # Loader
    # ---------------------------------------------------------------------------

    def install_db_knowledge(self, agent:str, topics:list[str],
                            up_to_store:STORE=STORE.SOURCE):
        loader = self.create_loader()
        loader.init_knowledge(agent, topics, up_to_store)
        
    def update_db_knowledge(self, up_to_store:STORE=STORE.SOURCE):
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

    # ---------------------------------------------------------------------------
    # Task

    def add_topics(self, topics:list[str], up_to_store_id:int):
        loader = self.create_loader()        
        up_to_store = STORE(up_to_store_id)            
        loader.add_topics(topics, up_to_store=up_to_store)        

    def add_searches(self, topic_ids:list[int], up_to_store_id:int):
        sdb = self.create_session()
        loader = self.create_loader(sdb=sdb)

        topics = sdb.select_topics_by_ids(topic_ids)
        up_to_store = STORE(up_to_store_id)            
        loader.add_searches_recommended(topics, up_to_store=up_to_store)

    def add_sources(self, search_ids:list[int], up_to_store_id:int):
        sdb = self.create_session()
        loader = self.create_loader(sdb=sdb)

        up_to_store = STORE(up_to_store_id)  
        for list_ids in split_list(search_ids, 10): 
            searches = sdb.select_searches_by_ids(list_ids)
            loader.add_sources(searches, up_to_store=up_to_store)

    def extract_source(self, source_id:int, up_to_store_id:int):
        sdb = self.create_session()
        loader = self.create_loader(sdb=sdb)

        source = sdb.select_source_by_id(source_id)
        up_to_store = STORE(up_to_store_id)            
        loader.extract_sources([source], up_to_store=up_to_store)
            
    def summarize_source(self, source_id:int):
        sdb = self.create_session()
        loader = self.create_loader(sdb=sdb)

        source = sdb.select_source_by_id(source_id)
        loader.summarize_sources([source])
    
    # ---------------------------------------------------------------------------
    # API function
    # ---------------------------------------------------------------------------
        
    def stats(self):
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
        sources_extracted_nb = len(list(filter(lambda t: t.extract is not None, sources)))
        sources_extracted_pct = sources_extracted_nb / sources_nb
        sources_summarized_nb = len(list(filter(lambda t: t.summary is not None, sources)))
        sources_summarized_pct = sources_summarized_nb / sources_nb

        return {
            'topics' : {'nb':topics_nb, 'filled_nb' : topics_filled_nb, 'filled_pct' : topics_filled_pct},
            'searches' : {'nb':searches_nb, 'filled_nb' : searches_filled_nb, 'filled_pct' : searches_filled_pct},
            'sources' : {'nb':sources_nb, 
                            'extracted_nb' : sources_extracted_nb, 'extracted_pct' : sources_extracted_pct, 
                            'summarized_nb' : sources_summarized_nb, 'summarized_pct' : sources_summarized_pct
                        }
        }
    
    def genAI(self, sdb:SessionDB, query, nb_extract=3, nb_ref=5):        

        sim_docs, sim_sources = self.db.vector.similarity_sources_extract(sdb, query, nb=nb_extract)
        if len(sim_sources)>nb_ref:
            sim_sources = sim_sources[:nb_ref]
        sim_searches = self.db.vector.similarity_searches(sdb, query)
        docs = []
        for ss in sim_docs:
            docs.append(Document(page_content=ss.doc_text))
        response = self.model.rag(sdb, query, docs)
        
        return response, sim_docs, sim_sources, sim_searches


    
