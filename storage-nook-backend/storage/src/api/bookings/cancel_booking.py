import json
import boto3
import os
from datetime import datetime, timedelta

# Initialize DynamoDB
dynamodb = boto3.resource("dynamodb")
bookings_table = dynamodb.Table(os.environ["TABLE_NAME"])
units_table = dynamodb.Table(os.environ["UNITS_TABLE"])


def get_booking(booking_id):
    """
    Retrieve a booking by ID.
    """
    response = bookings_table.get_item(Key={"bookingId": booking_id})
    return response.get("Item", {})


def lambda_handler(event, context):
    """
    Handle cancellation requests for a booking.
    """
    try:
        # Parse input
        booking_id = event["pathParameters"]["bookingId"]
        body = json.loads(event["body"])
        cancellation_date = datetime.strptime(body.get("cancellationDate"), "%Y-%m-%d")

        # Retrieve booking
        booking = get_booking(booking_id)
        if not booking:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Booking not found"}),
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "PUT",
                    "Access-Control-Allow-Headers": "Content-Type,Authorization",
                },
            }

        # Extract necessary details
        end_date = datetime.strptime(booking["endDate"], "%Y-%m-%d")
        notice_period = int(booking.get("noticePeriod", 0))
        unit_id = booking["unitId"]
        type_id = booking["typeId"]

        # Validate notice period
        latest_cancellation_date = end_date - timedelta(days=notice_period)
        if cancellation_date > latest_cancellation_date:
            return {
                "statusCode": 400,
                "body": json.dumps(
                    {
                        "error": f"Cancellation requires at least {notice_period} days' notice."
                    }
                ),
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "PUT",
                    "Access-Control-Allow-Headers": "Content-Type,Authorization",
                },
            }

        # Update booking status and unit availability
        bookings_table.update_item(
            Key={"bookingId": booking_id},
            UpdateExpression="SET #status = :status, cancellationRequested = :requested",
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={":status": "Cancelling", ":requested": True},
        )

        units_table.update_item(
            Key={"unitId": unit_id, "typeId": type_id},
            UpdateExpression="SET #status = :status",
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={":status": "Cancelling"},
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Cancellation successful"}),
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "PUT",
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
                "Access-Control-Allow-Methods": "PUT",
                "Access-Control-Allow-Headers": "Content-Type,Authorization",
            },
        }
