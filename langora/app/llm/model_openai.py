from langchain_openai import OpenAI

from .model import Model

class ModelOpenAI(Model):
    def __init__(self) -> None:   
        Model.__init__(self)

    def init_model(self):
        self.llm = OpenAI()