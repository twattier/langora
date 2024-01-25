from langchain_community.utilities import ApifyWrapper

from .loader_web import LoaderWeb, Document

class LoaderApify(LoaderWeb):
    def load_web(self, url:str)->Document:
        apify = ApifyWrapper()
        loader = apify.call_actor(
            actor_id="apify/website-content-crawler",
            run_input={"startUrls": [{"url": url}]},
            dataset_mapping_function=lambda item: Document(
                page_content=item["text"] or "", metadata={"source": item["url"]}
            ),
        )        
        docs = loader.load()
        return docs[0]