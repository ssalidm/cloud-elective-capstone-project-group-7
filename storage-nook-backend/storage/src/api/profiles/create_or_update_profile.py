import json
import boto3
import os
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    try:
        # Get user details from the token
        claims = event["requestContext"]["authorizer"]["claims"]
        user_id = claims["sub"]  # Cognito user ID
        email = claims["email"]  # User's email address

        # Parse the request body
        body = json.loads(event["body"])
        phone = body.get("phone")
        first_name = body.get("first_name")
        last_name = body.get("last_name")
        address = body.get("address")

        # Build the profile object
        profile = {
            "userId": user_id,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "address": address,
        }

        # Save to DynamoDB
        table.put_item(Item=profile)

        return {
            "statusCode": 200,
            "body": json.dumps(
                {"message": "Profile updated successfully", "profile": profile}
            ),
            "headers": {"Content-Type": "application/json"},
        }

    except ClientError as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"}),
            "headers": {"Content-Type": "application/json"},
        }
