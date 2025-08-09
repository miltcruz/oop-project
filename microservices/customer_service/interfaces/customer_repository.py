from typing import Protocol, Iterable, Optional
from microservices.customer_service.entities.customer import Customer, Customers

class ICustomerRepository(Protocol):
    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        ...
    def list(self, limit: int = 100, offset: int = 0) -> Customers:
        ... 