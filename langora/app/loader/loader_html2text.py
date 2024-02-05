from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import Html2TextTransformer

from loader.loader_web import LoaderWeb, Document

class LoaderHtml2Text(LoaderWeb):
    def load_web(self, url:str)->Document:

        loader = AsyncChromiumLoader([url])
        html = loader.load()

        html2text = Html2TextTransformer()
        docs_transformed = html2text.transform_documents(html)
        return docs_transformed[0]