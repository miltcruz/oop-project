import sqlite3
from microservices.data_acccess_service.base.db_provider import DbProvider

class SqliteProvider(DbProvider):
    def get_connection(self):
        conn = sqlite3.connect(self._db_url)
        conn.row_factory = sqlite3.Row
        return conn