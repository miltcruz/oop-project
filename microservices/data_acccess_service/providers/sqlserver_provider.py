import pyodbc
from microservices.data_acccess_service.base.db_provider import DbProvider

class SqlServerProvider(DbProvider):
    def get_connection(self):
        return pyodbc.connect(self._db_url)