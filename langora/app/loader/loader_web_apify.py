from langchain_community.utilities import ApifyWrapper

from loader.loader_web import LoaderWeb, Document

class LoaderApify(LoaderWeb):
    def load_document(self, url:str)->Document:
        apify = ApifyWrapper()
        loader = apify.call_actor(
            actor_id="apify/website-content-crawler",
            run_input={"startUrls": [{"url": url}]},
            dataset_mapping_function=lambda item: Document(
                page_content=item["text"] or "", metadata={"source": item["url"]}
            ),
        )        
        docs = loader.load()
        if not docs or len(docs) ==0:
            return None
        return docs[0]