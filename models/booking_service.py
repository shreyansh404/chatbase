#Third party imports
from pydantic import BaseModel
from typing import Optional

class BookServiceRequest(BaseModel):
    service_type: str
    date: Optional[str]
    time: Optional[str]
    apartment_unit: Optional[str]
    contact_name: Optional[str]
    phone: Optional[str]
    problem_summary: Optional[str]

class BookServiceResponse(BaseModel):
    booking_id: str
    confirmation: str