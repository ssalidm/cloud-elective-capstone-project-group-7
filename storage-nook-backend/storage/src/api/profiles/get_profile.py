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
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET",
                    "Access-Control-Allow-Headers": "Content-Type,Authorization",
                },
            }

        return {
            "statusCode": 200,
            "body": json.dumps({"profile": profile}),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
                "Access-Control-Allow-Headers": "Content-Type,Authorization",
            },
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"}),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
                "Access-Control-Allow-Headers": "Content-Type,Authorization",
            },
        }
