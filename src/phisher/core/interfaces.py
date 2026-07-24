from abc import ABC, abstractmethod
from typing import List, Dict, Any


class SearchEngine(ABC):
    """Абстракция для поиска доменов по запросам"""
    @abstractmethod
    def count(self, datatype: str, query: str) -> int:
        pass

    @abstractmethod
    def download(self, datatype: str, query: str, fields: str, size: int) -> List[Dict[str, Any]]:
        pass


class WhoisProvider(ABC):
    @abstractmethod
    def get_whois(self, domain: str) -> List[Dict[str, Any]]:
        pass


class MutationGenerator(ABC):
    @abstractmethod
    def generate(self, domain: str) -> List[str]:
        pass
