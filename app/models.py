from pydantic import BaseModel

class Ticket(BaseModel):
    title: str
    description: str

class TicketResponse(Ticket):
    id: int