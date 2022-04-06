from abc import ABC, abstractmethod

class DisplayResult(ABC):

    @abstractmethod
    def display_output(self, data: dict) -> None:
        pass