from langora import Langora
from db.dbvector import STORE

app = Langora(is_task_mode=True)
try:
    # agent = "an expert in artificial intelligence consulting for businesses"
    # topics = ["Generative AI", "Large language model", "Generative AI business use cases", "Generative AI development methodology"]
    # app.install_db_knowledge(agent, topics, up_to_store=STORE.SRC_EXTRACT)
    
    # sims = app.db.similarity_search("Explain LLM", STORE.SEARCH)
    # print(sims)
        
    app.init_store_model()
    app.db.open_session()   

    # app.loader.update_extract_sources()



    
finally:
    app.db.close_session()

