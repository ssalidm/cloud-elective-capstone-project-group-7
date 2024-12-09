import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    """
    Delete a specific storage unit.
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
                    "Access-Control-Allow-Methods": "DELETE",
                    "Access-Control-Allow-Headers": "Content-Type,Authorization",
                },
            }

        # Extract unitId from path parameters
        unit_id = event["pathParameters"]["unitId"]

        # Delete the item from DynamoDB
        response = table.delete_item(
            Key={"unitId": unit_id},
            ConditionExpression="attribute_exists(unitId)",
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Unit deleted successfully!"}),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "DELETE",
                "Access-Control-Allow-Headers": "Content-Type,Authorization",
            },
        }

    except dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Unit not found"}),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "DELETE",
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
                "Access-Control-Allow-Methods": "DELETE",
                "Access-Control-Allow-Headers": "Content-Type,Authorization",
            },
        }
