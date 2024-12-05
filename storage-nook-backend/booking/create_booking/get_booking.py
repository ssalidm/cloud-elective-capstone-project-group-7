import json
import boto3

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
bookings_table = dynamodb.Table('BookingsTable')

def lambda_handler(event, context):
    try:
        # Get the bookingId from the path parameters
        booking_id = event['pathParameters']['bookingId']
        
        # Retrieve the booking from DynamoDB
        response = bookings_table.get_item(Key={'bookingId': booking_id})
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Booking not found'})
            }
        
        # Return the booking details
        return {
            'statusCode': 200,
            'body': json.dumps(response['Item'])
        }
    
    except Exception as e:
        # Handle any errors
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }
