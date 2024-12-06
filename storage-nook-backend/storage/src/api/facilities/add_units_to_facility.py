import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.environ["TABLE_NAME"]


def lambda_handler(event, context):
    """
    Add units to a specific facility by facilityId, specifying locations.
    """
    try:
        facility_id = event["pathParameters"]["facilityId"]
        body = json.loads(event["body"])
        new_units = body.get("units", [])

        if not new_units:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No units provided"}),
                "headers": {"Content-Type": "application/json"},
            }

        table = dynamodb.Table(TABLE_NAME)

        for unit in new_units:
            unit["facilityId"] = facility_id
            table.put_item(Item=unit)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Units added successfully!"}),
            "headers": {"Content-Type": "application/json"},
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"}),
            "headers": {"Content-Type": "application/json"},
        }
