from langchain_openai import OpenAI

from llm.model import Model

class ModelOpenAI(Model):
    def __init__(self) -> None:   
        Model.__init__(self)

    def init_model(self):
        self.llm = OpenAI(max_tokens=-1)
        # model='gpt-3.5-turbo-16k', 