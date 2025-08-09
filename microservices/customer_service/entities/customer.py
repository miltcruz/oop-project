from typing import Optional
from pydantic import BaseModel
from .address import Address

class Customer(BaseModel):
    CustomerID: int
    Gender: str
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    IsActiveMember: int
    EstimatedSalary: float
    Exited: bool
    MailingAddress: Optional[Address] = None
    BillingAddress: Optional[Address] = None

class Customers(BaseModel):
    customers: list[Customer]