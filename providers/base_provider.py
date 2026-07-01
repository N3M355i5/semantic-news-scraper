from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def search(
        self,
        query: str,
        max_results: int = 50
    ):
        pass