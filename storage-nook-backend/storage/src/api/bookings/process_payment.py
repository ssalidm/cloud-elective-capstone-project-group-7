import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
bookings_table = dynamodb.Table(os.environ["TABLE_NAME"])

def lambda_handler(event, context):
    """
    Simulate payment processing for a booking.
    """
    try:
        # Parse input
        body = json.loads(event["body"])
        booking_id = body.get("bookingId")
        payment_method = body.get("paymentMethod", "Card")

        if not booking_id:
            return {"statusCode": 400, "body": json.dumps({"error": "Missing bookingId"})}

        # Retrieve the booking
        response = bookings_table.get_item(Key={"bookingId": booking_id})
        booking = response.get("Item")

        if not booking:
            return {"statusCode": 404, "body": json.dumps({"error": "Booking not found"})}

        # Simulate payment logic
        if payment_method not in ["Card", "EFT"]:
            return {"statusCode": 400, "body": json.dumps({"error": "Unsupported payment method"})}

        # Simulate success or failure
        payment_status = "Paid" if payment_method == "Card" else "Pending"

        # Update booking with payment status
        bookings_table.update_item(
            Key={"bookingId": booking_id},
            UpdateExpression="SET paymentStatus = :status",
            ExpressionAttributeValues={":status": payment_status},
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Payment processed successfully", "paymentStatus": payment_status}),
        }

    except Exception as e:
        print(f"Error: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": "Internal server error"})}
