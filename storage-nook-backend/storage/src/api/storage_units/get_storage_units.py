import json
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def lambda_handler(event, context):
    """
    Retrieve all units for a specific storage type, with optional filtering.
    """
    try:
        # Extract typeId from path parameters
        type_id = event["pathParameters"]["typeId"]

        # Extract query parameters (optional filters)
        query_params = event.get("queryStringParameters") or {}
        location = query_params.get("location")
        status = query_params.get("status")

        # Perform a scan and filter by typeId
        response = table.scan(
            FilterExpression="typeId = :typeId",
            ExpressionAttributeValues={":typeId": type_id},
        )

        # Apply filtering if query parameters are provided
        units = response.get("Items", [])
        
        if location:
            units = [unit for unit in units if unit.get("location") == location]
        if status:
            units = [unit for unit in units if unit.get("status") == status]

        # Return the filtered or unfiltered units
        return {
            "statusCode": 200,
            "body": json.dumps(units),
            "headers": {"Content-Type": "application/json"},
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"}),
            "headers": {"Content-Type": "application/json"},
        }
