from langora import Langora

from db.dbvector import STORE

app = Langora()
app.db.open_session()
try:
    app.init_services()

    # agent = "an expert in artificial intelligence consulting for businesses"
    # topics = ["Generative AI", "Large language model", "Generative AI business use cases", "Generative AI development methodology"]
    # app.svc_loader.init_knowledge(agent, topics)
    # app.svc_loader.add_knowledge_recommendations()
    # app.svc_loader.import_knowledge_recommendations()

    #app.svc_loader.summarize_sources()
    #app.db.update_sources_embeddings()

    sims = app.db.similarity_search("Explain LLM", STORE.SEARCH)
    print(sims)
    
finally:
    app.db.close_session()
                       