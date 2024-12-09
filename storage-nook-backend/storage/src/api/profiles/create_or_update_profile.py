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
        user_id = claims["sub"]
        email = claims["email"]

        # Parse the request body
        body = json.loads(event["body"])
        phone = body.get("phone")
        first_name = body.get("firstName")
        last_name = body.get("lastName")
        address = body.get("address")
        payment_methods = body.get("paymentMethods", [])

        # Build the profile object
        profile = {
            "userId": user_id,
            "userDetails": {
                "email": email,
                "firstName": first_name,
                "lastName": last_name,
                "phone": phone,
                "address": address,
            },
            "paymentMethods": payment_methods,
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
