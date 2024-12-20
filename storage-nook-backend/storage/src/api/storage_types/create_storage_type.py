import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    """
    Create a new storage type.
    """
    try:
        claims = event["requestContext"]["authorizer"]["claims"]
        groups = claims.get("cognito:groups", [])
        if "admin" not in groups:
            return {
                "statusCode": 403,
                "body": json.dumps({"error": "Forbidden"}),
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST",
                    "Access-Control-Allow-Headers": "Content-Type,Authorization",
                },
            }

        # Parse the request body
        body = json.loads(event["body"])

        # Validate required fields
        if not all(key in body for key in ("typeId", "name", "description")):
            return {
                "statusCode": 400,
                "body": json.dumps(
                    {
                        "error": "Missing some or all required fields: typeId, name, description"
                    }
                ),
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST",
                    "Access-Control-Allow-Headers": "Content-Type,Authorization",
                },
            }

        # Construct the item
        storage_type = {
            "typeId": body["typeId"],
            "name": body["name"],
            "size": body["size"],
            "description": body["description"],
        }

        # Save to DynamoDB
        table.put_item(Item=storage_type)

        # Success response
        return {
            "statusCode": 201,
            "body": json.dumps({"message": "Storage type created successfully!"}),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST",
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
                "Access-Control-Allow-Methods": "POST",
                "Access-Control-Allow-Headers": "Content-Type,Authorization",
            },
        }
