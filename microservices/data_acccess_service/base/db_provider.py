from abc import ABC, abstractmethod

"""
Abstract base class for database providers.
"""
class DbProvider(ABC):
    def __init__(self, db_url: str):
        self._db_url = db_url
        self._connection = None   

    @abstractmethod
    def get_connection(self):
        pass