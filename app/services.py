import uuid
import boto3
import logging
from botocore.exceptions import ClientError
from app.models import Ticket
from fastapi import UploadFile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
s3 = boto3.client("s3", region_name="us-east-1")
S3_BUCKET_NAME = "maki-support-ticket-attachments"
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

def upload_ticket_attachment_service(ticket_id: str, file: UploadFile):
    try:
        ticket = get_ticket_by_id_service(ticket_id)

        if ticket is None:
            return None

        file_key = f"tickets/{ticket_id}/{file.filename}"

        s3.upload_fileobj(
            file.file,
            S3_BUCKET_NAME,
            file_key
        )

        attachment_info = {
            "bucket": S3_BUCKET_NAME,
            "key": file_key,
            "filename": file.filename
        }

        table.update_item(
            Key={"id": ticket_id},
            UpdateExpression="SET attachment = :attachment",
            ExpressionAttributeValues={
                ":attachment": attachment_info
            }
        )

        logger.info(f"Uploaded attachment for ticket id={ticket_id}")

        return {
            "message": "Attachment uploaded",
            "ticket_id": ticket_id,
            "attachment": attachment_info
        }

    except ClientError as e:
        logger.error(f"S3/DynamoDB error while uploading attachment: {e}")
        raise

def get_attachment_url_service(ticket_id: str):
    try:
        ticket = get_ticket_by_id_service(ticket_id)

        if not ticket or "attachment" not in ticket:
            return None

        key = ticket["attachment"]["key"]

        url = s3.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": S3_BUCKET_NAME,
                "Key": key
            },
            ExpiresIn=3600  # 1 hour
        )

        logger.info(f"Generated signed URL for ticket id={ticket_id}")

        return {
            "ticket_id": ticket_id,
            "url": url
        }

    except ClientError as e:
        logger.error(f"Error generating signed URL: {e}")
        raise