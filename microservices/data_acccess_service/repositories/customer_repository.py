import sqlite3   
from typing import Iterable, Optional
from microservices.customer_service.entities.customer import Customer
from microservices.customer_service.interfaces.customer_repository import ICustomerRepository
from microservices.data_acccess_service.base.db_provider import DbProvider

class CustomerRepository(ICustomerRepository):
    """Works with any DbProvider (SQLite or SQL Server) via DB-API/pyodbc rows."""
    def __init__(self, db_provider: DbProvider):
        self._provider = db_provider

    def _row_to_customer(self, row) -> Customer:

        # For sqlite3.Row: dict-like. For pyodbc.Row: attribute or index.
        get = (lambda k: row[k]) if hasattr(row, "__getitem__") else (lambda k: getattr(row, k))

        return Customer(
            CustomerID=get("CustomerID"),
            Gender=get("Gender"),
            Age=get("Age"),
            Tenure=get("Tenure"),
            Balance=get("Balance"),
            NumOfProducts=get("NumOfProducts"),
            IsActiveMember=get("IsActiveMember"),
            EstimatedSalary=get("EstimatedSalary"),
            Exited=get("Exited")
        )

    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        sql = """
                SELECT CustomerID,
                    Gender,
                    Age,
                    Tenure,
                    Balance,
                    NumOfProducts,
                    IsActiveMember,
                    EstimatedSalary,
                    Exited
                FROM Customer
                WHERE CustomerID = ?
                """
        with self._provider.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, (customer_id,))
            row = cur.fetchone()
            return self._row_to_customer(row) if row else None
        
    def list(self, limit: int = 100, offset: int = 0) -> list[Customer]:
        query =  """
                SELECT CustomerID,
                    Gender,
                    Age,
                    Tenure,
                    Balance,
                    NumOfProducts,
                    IsActiveMember,
                    EstimatedSalary,
                    Exited
                FROM Customer
                ORDER BY CustomerID
                """
        with self._provider.get_connection() as conn:
            cur = conn.cursor()
            is_sqlite = conn.__class__.__module__.startswith("sqlite3")

            if is_sqlite:
                sql = f"{query} LIMIT ? OFFSET ?"
                params = (limit, offset)
            else:
                # SQL Server paging syntax requires ORDER BY
                sql = f"{query} OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
                params = (offset, limit)

            cur.execute(sql, params)
            rows = cur.fetchall()
            return [self._row_to_customer(r) for r in rows]