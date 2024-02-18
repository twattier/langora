# from langora import Langora
# from db.dbvector import STORE

# app = Langora(is_task_mode=True)
# try:
#     # agent = "an expert in artificial intelligence consulting for businesses"
#     # topics = ["Generative AI", "Large language model", "Generative AI business use cases", "Generative AI development methodology"]
#     # app.install_db_knowledge(agent, topics, up_to_store=STORE.SRC_EXTRACT)
    
#     # sims = app.db.similarity_search("Explain LLM", STORE.SEARCH)
#     # print(sims)
        
#     app.init_store_model()
#     app.db.open_session()   

#     #app.add_sources([21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60], 5)



    
# finally:
#     app.db.close_session()


from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import postgresql
from db.datamodel import Source, SourceText, SourceTextImage
print(CreateTable(Source.__table__).compile(dialect=postgresql.dialect()))
print(CreateTable(SourceText.__table__).compile(dialect=postgresql.dialect()))
print(CreateTable(SourceTextImage.__table__).compile(dialect=postgresql.dialect()))