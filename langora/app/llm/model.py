from abc import ABC, abstractmethod

class Model(ABC):
    def __init__(self) -> None:           
        self.llm = None
        self.agent = ""
        self.topics:list[str] = []

    @abstractmethod
    def init_model(self):
        pass