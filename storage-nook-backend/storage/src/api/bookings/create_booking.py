import json
import boto3
import os
from uuid import uuid4
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
bookings_table = dynamodb.Table(os.environ["TABLE_NAME"])
units_table = dynamodb.Table(os.environ["UNITS_TABLE"])


def get_pricing_for_unit(unit_id):
    """
    Retrieve pricing details for a specific unit.
    """
    response = units_table.get_item(Key={"unitId": unit_id})
    item = response.get("Item", {})
    pricing = item.get("pricing", {})

    # Ensure pricing values are properly parsed
    pricing = {key: float(value) for key, value in pricing.items() if value}
    return pricing, item.get("status", "Unavailable")


def calculate_price(pricing, duration_in_days):
    """
    Calculate total price based on duration.
    """
    per_day = float(pricing.get("perDay", 0))
    per_week = float(pricing.get("perWeek", 0))
    per_month = float(pricing.get("perMonth", 0))

    if duration_in_days <= 7:
        return per_day * duration_in_days
    elif duration_in_days <= 30:
        weeks = duration_in_days // 7
        remaining_days = duration_in_days % 7
        return (per_week * weeks) + (per_day * remaining_days)
    elif duration_in_days <= 365:
        months = duration_in_days // 30
        remaining_days = duration_in_days % 30
        return (per_month * months) + (per_day * remaining_days)


def calculate_notice_period(duration_in_days):
    """
    Calculate the notice period based on rental duration.
    """
    if duration_in_days <= 7:
        return 1
    elif duration_in_days <= 30:
        return 7
    elif duration_in_days <= 365:
        return 30


def lambda_handler(event, context):
    """
    Handle booking creation.
    """
    try:
        body = json.loads(event["body"])
        customer_id = body.get("customerId")
        unit_id = body.get("unitId")
        start_date = body.get("startDate")
        end_date = body.get("endDate")

        if not (customer_id and unit_id and start_date and end_date):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing required fields"}),
            }

        # Convert dates to datetime objects
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        duration_in_days = (end_date - start_date).days

        if duration_in_days < 1:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid booking duration"}),
            }

        # Retrieve pricing and unit status
        pricing, status = get_pricing_for_unit(unit_id)
        if not pricing or status != "Available":
            return {
                "statusCode": 400,
                "body": json.dumps({"error": f"Unit {unit_id} is not available"}),
            }

        # Calculate total price and notice period
        total_price = calculate_price(pricing, duration_in_days)
        notice_period = calculate_notice_period(duration_in_days)

        # Generate booking ID and create booking
        booking_id = str(uuid4())
        booking_item = {
            "bookingId": booking_id,
            "customerId": customer_id,
            "unitId": unit_id,
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
            "totalPrice": str(total_price),
            "status": "Confirmed",
            "noticePeriod": notice_period,
            "paymentStatus": "Awaiting Payment",
            "cancellationRequested": False,
        }

        bookings_table.put_item(Item=booking_item)

        # Update unit status
        units_table.update_item(
            Key={"unitId": unit_id},
            UpdateExpression="SET #status = :status",
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={":status": "Reserved"},
        )

        return {
            "statusCode": 201,
            "body": json.dumps(
                {"message": "Booking created successfully", "bookingId": booking_item}
            ),
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"}),
        }
