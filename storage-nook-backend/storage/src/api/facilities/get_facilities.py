import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.environ["TABLE_NAME"]


def lambda_handler(event, context):
    """
    Retrieve all facilities from DynamoDB.
    """
    try:
        table = dynamodb.Table(TABLE_NAME)

        # Scan the table to get all items
        response = table.scan()
        facilities = response.get("Items", [])

        # Return a successful response with the data
        return {
            "statusCode": 200,
            "body": json.dumps({"facilities": facilities}),
            "headers": {"Content-Type": "application/json"},
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"}),
            "headers": {"Content-Type": "application/json"},
        }
