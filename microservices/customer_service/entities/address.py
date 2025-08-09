from pydantic import BaseModel

class Address(BaseModel):
    Street: str
    City: str
    State: str
    ZipCode: str
    Country: str