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



from loader.loader_tree_b4 import LoaderTreeB4

loader = LoaderTreeB4()
tree = loader.load_tree("https://www.techtarget.com/searchenterpriseai/definition/generative-AI")
# tree = loader.load_tree("https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/the-economic-potential-of-generative-ai-the-next-productivity-frontier")
# tree = loader.load_tree("https://www.sciencedirect.com/science/article/pii/S0268401223000233")
# tree = loader.load_tree("https://www.whitehouse.gov/briefing-room/presidential-actions/2023/10/30/executive-order-on-the-safe-secure-and-trustworthy-development-and-use-of-artificial-intelligence/")
# tree = loader.load_tree("https://www.gartner.com/en/topics/generative-ai")
