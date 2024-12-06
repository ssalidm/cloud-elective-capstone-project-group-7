import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    try:
        # Get user ID from the token
        claims = event["requestContext"]["authorizer"]["claims"]
        user_id = claims["sub"]  # Cognito user ID

        # Fetch profile from DynamoDB
        response = table.get_item(Key={"userId": user_id})
        profile = response.get("Item")

        if not profile:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Profile not found"}),
                "headers": {"Content-Type": "application/json"},
            }

        return {
            "statusCode": 200,
            "body": json.dumps({"profile": profile}),
            "headers": {"Content-Type": "application/json"},
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"}),
            "headers": {"Content-Type": "application/json"},
        }
