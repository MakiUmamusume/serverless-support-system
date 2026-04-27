from fastapi import APIRouter, HTTPException, UploadFile, File
from botocore.exceptions import ClientError
from app.models import Ticket
from app.services import (
    create_ticket_service,
    get_all_tickets_service,
    get_ticket_by_id_service,
    upload_ticket_attachment_service
)
router = APIRouter()

@router.post("/tickets")
def create_ticket(ticket: Ticket):
    try:
        return create_ticket_service(ticket)
    except ClientError:
        raise HTTPException(status_code=500, detail="Failed to create ticket")

@router.get("/tickets")
def get_all_tickets():
    try:
        return get_all_tickets_service()
    except ClientError:
        raise HTTPException(status_code=500, detail="Failed to retrieve tickets")

@router.get("/tickets/{ticket_id}")
def get_ticket_by_id(ticket_id: str):
    try:
        ticket = get_ticket_by_id_service(ticket_id)

        if ticket is None:
            raise HTTPException(status_code=404, detail="Ticket not found")

        return ticket

    except ClientError:
        raise HTTPException(status_code=500, detail="Failed to retrieve ticket")
    
@router.post("/tickets/{ticket_id}/attachment")
def upload_ticket_attachment(ticket_id: str, file: UploadFile = File(...)):
    try:
        result = upload_ticket_attachment_service(ticket_id, file)

        if result is None:
            raise HTTPException(status_code=404, detail="Ticket not found")

        return result

    except ClientError:
        raise HTTPException(status_code=500, detail="Failed to upload attachment")