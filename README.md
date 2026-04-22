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