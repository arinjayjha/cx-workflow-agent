
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name, docs=None, memory=None):
        self.name = name
        self.docs = docs
        self.memory = memory

    @abstractmethod
    def act(self, ticket_text):
        pass
