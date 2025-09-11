from pydantic import BaseModel

class Client(BaseModel):
    id: int | None = None
    name: str
    address: str
    contact_person: str
    country: str
    phone_number: str
    onrc_no: str
    cui: str