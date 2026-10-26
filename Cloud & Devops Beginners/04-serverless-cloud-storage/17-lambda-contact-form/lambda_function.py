"""
AWS Lambda Function for Contact Form Handler

This function receives form submissions from your website,
validates the input, and sends you an email notification.

Integration: API Gateway (HTTP API) -> Lambda -> SES (Simple Email Service)
"""
import json
import os
import boto3
from email.mime.text import MIMEText

# Initialize AWS clients
ses_client = boto3.client("ses", region_name="us-east-1")

SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "your_email@example.com")
RECIPIENT_EMAIL = os.environ.get("RECIPIENT_EMAIL", "your_email@example.com")


def lambda_handler(event, context):
    """Process incoming contact form submissions."""

    # Parse the body from the API Gateway event
    try:
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON payload"})
        }

    name = body.get("name", "Anonymous")
    email = body.get("email", "")
    message = body.get("message", "")

    # Basic validation
    if not email or not message:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Email and message are required"})
        }

    # Compose the email
    subject = f"New message from {name} on your website"
    email_body = f"""
    You have received a new contact form submission:

    Name:    {name}
    Email:   {email}
    Message: {message}

    ---
    This email was sent via AWS Lambda + SES.
    """

    # Send the email via SES
    try:
        ses_client.send_email(
            Source=SENDER_EMAIL,
            Destination={"ToAddresses": [RECIPIENT_EMAIL]},
            Message={
                "Subject": {"Data": subject},
                "Body": {"Text": {"Data": email_body}}
            }
        )
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Failed to send email: {str(e)}"})
        }

    # Return success response
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps({"message": "Email sent successfully!"})
    }
