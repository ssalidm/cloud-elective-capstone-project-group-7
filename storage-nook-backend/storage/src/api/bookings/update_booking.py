import json
import boto3
import os
from uuid import uuid4
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
bookings_table = dynamodb.Table(os.environ["TABLE_NAME"])
units_table = dynamodb.Table(os.environ["UNITS_TABLE"])


def lambda_handler(event, context):
    """
    Update booking details.
    """
    try:
        booking_id = event["pathParameters"]["bookingId"]
        body = json.loads(event["body"])
        updates = body.get("updates", {})

        if not updates:
            return {"statusCode": 400, "body": json.dumps({"error": "No updates provided"})}

        update_expression = "SET " + ", ".join(f"{key} = :{key}" for key in updates.keys())
        expression_attribute_values = {f":{key}": value for key, value in updates.items()}

        bookings_table.update_item(
            Key={"bookingId": booking_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
        )

        return {"statusCode": 200, "body": json.dumps({"message": "Booking updated successfully"})}

    except Exception as e:
        print(f"Error: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": "Internal server error"})}
