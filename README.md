Future improvement: replace broad AWS managed policies with least-privilege IAM permissions.

# Serverless Support Ticket API

A backend support ticket API built with Python and FastAPI. The project allows users to create and retrieve support tickets, stores ticket data in AWS DynamoDB, and includes automated testing, logging, and error handling.

## Features

- Create support tickets through a REST API
- Retrieve all tickets
- Retrieve a ticket by ID
- Store ticket data in AWS DynamoDB
- Automated tests with pytest
- Logging for observability and debugging
- Basic error handling for reliability

## Tech Stack

- Python
- FastAPI
- Uvicorn
- boto3
- AWS DynamoDB
- pytest

## Project Structure

```text
app/
  main.py
  models.py
  routes.py
  services.py

tests/
  test_tickets.py

  ## Deployed Architecture

FastAPI application deployed to AWS Lambda using Mangum and exposed through API Gateway.

Data flow:

Client → API Gateway → AWS Lambda → FastAPI → DynamoDB / S3

## Cloud Features

- DynamoDB persistent ticket storage
- S3 file attachment upload
- Secure attachment retrieval using pre-signed URLs
- AWS Lambda deployment
- API Gateway public endpoint

## Security Notes

- S3 bucket is private
- File access is handled through temporary pre-signed URLs
- AWS credentials are not stored in the repository
- IAM permissions should be scoped down for production use