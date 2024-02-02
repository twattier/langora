
from langora import Langora
app = Langora(is_task_mode=True)

def add_searches(topic_ids:list[int], up_to_store_id:int):
    app.add_searches(topic_ids, up_to_store_id)

def add_sources(search_ids:list[int], up_to_store_id:int):
    app.add_sources(search_ids, up_to_store_id)

def extract_source(source_id:int, up_to_store_id:int):
    app.extract_source(source_id, up_to_store_id)
        
def summarize_source(source_id:int):
    app.summarize_source(source_id)
        