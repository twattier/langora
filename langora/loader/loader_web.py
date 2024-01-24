from abc import ABC, abstractmethod

from langchain_community.document_loaders.base import Document

class LoaderWeb(ABC):
    
    @abstractmethod
    def load_web(self, url:str)->Document:
        pass 