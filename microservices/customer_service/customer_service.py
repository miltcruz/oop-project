from typing import Iterable, Optional
from microservices.customer_service.entities.customer import Customer, Customers
from microservices.customer_service.interfaces.customer_repository import ICustomerRepository

class CustomerService:
    def __init__(self, repo: ICustomerRepository):
        self._repo = repo

    def get_customer(self, customer_id: int) -> Optional[Customer]:
        return self._repo.get_by_id(customer_id)

    def list_customers(self, limit: int = 100, offset: int = 0) -> Customers:
        items = list(self._repo.list(limit=limit, offset=offset))
        return Customers(customers=items)