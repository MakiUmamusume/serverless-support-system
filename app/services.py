import uuid
import boto3
import logging
from botocore.exceptions import ClientError
from app.models import Ticket

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("tickets")

def create_ticket_service(ticket: Ticket):
    try:
        ticket_id = str(uuid.uuid4())

        new_ticket = {
            "id": ticket_id,
            "title": ticket.title,
            "description": ticket.description
        }

        table.put_item(Item=new_ticket)
        logger.info(f"Ticket created successfully with id={ticket_id}")

        return {
            "message": "Ticket created",
            "ticket": new_ticket
        }

    except ClientError as e:
        logger.error(f"DynamoDB error while creating ticket: {e}")
        raise

def get_all_tickets_service():
    try:
        response = table.scan()
        items = response.get("Items", [])
        logger.info(f"Retrieved {len(items)} ticket(s)")
        return items

    except ClientError as e:
        logger.error(f"DynamoDB error while retrieving all tickets: {e}")
        raise

def get_ticket_by_id_service(ticket_id: str):
    try:
        response = table.get_item(Key={"id": ticket_id})
        item = response.get("Item")

        if item:
            logger.info(f"Retrieved ticket with id={ticket_id}")
        else:
            logger.warning(f"Ticket not found with id={ticket_id}")

        return item

    except ClientError as e:
        logger.error(f"DynamoDB error while retrieving ticket id={ticket_id}: {e}")
        raise