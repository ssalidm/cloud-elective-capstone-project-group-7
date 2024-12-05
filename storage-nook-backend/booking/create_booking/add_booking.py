import json
import uuid
import boto3
from datetime import datetime

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
bookings_table = dynamodb.Table('BookingsTable')

def lambda_handler(event, context):
    try:
        # Extract the booking data from the event body
        body = json.loads(event['body'])
        customer_id = body['customerId']
        facility_id = body['facilityId']
        start_date = body['startDate']
        end_date = body['endDate']
        
        # Generate a unique bookingId
        booking_id = str(uuid.uuid4())
        
        # Add the booking to DynamoDB
        booking_item = {
            'bookingId': booking_id,
            'customerId': customer_id,
            'facilityId': facility_id,
            'startDate': start_date,
            'endDate': end_date,
            'status': 'booked',  # Initial status is booked
            'createdAt': datetime.utcnow().isoformat(),
        }

        bookings_table.put_item(Item=booking_item)

        # Return a successful response with booking details
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Booking created successfully!',
                'bookingId': booking_id,
                'status': 'booked'
            })
        }
    
    except Exception as e:
        # Handle any errors
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }
