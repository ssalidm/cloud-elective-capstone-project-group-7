import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def extract_type_id_from_unit_id(unit_id):
    """
    Extract the typeId from the unitId.
    """
    return unit_id.split("-")[0]


def lambda_handler(event, context):
    """
    Delete a specific storage unit.
    """
    try:
        # Extract unitId from path parameters
        unit_id = event["pathParameters"]["unitId"]

        # Extract typeId dynamically from unitId
        type_id = extract_type_id_from_unit_id(unit_id)

        # Delete the item from DynamoDB
        table.delete_item(Key={"unitId": unit_id, "typeId": type_id})

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Unit deleted successfully!"}),
            "headers": {"Content-Type": "application/json"},
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"}),
            "headers": {"Content-Type": "application/json"},
        }
