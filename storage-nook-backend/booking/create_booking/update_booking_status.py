import json
import boto3

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
bookings_table = dynamodb.Table('BookingsTable')

def lambda_handler(event, context):
    try:
        # Get the bookingId from the path parameters and the new status from the body
        booking_id = event['pathParameters']['bookingId']
        body = json.loads(event['body'])
        new_status = body['status']
        
        # Update the booking status in DynamoDB
        response = bookings_table.update_item(
            Key={'bookingId': booking_id},
            UpdateExpression="set #status = :status",
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={':status': new_status},
            ReturnValues="UPDATED_NEW"
        )
        
        # Return the updated booking details
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Booking status updated successfully',
                'updatedAttributes': response['Attributes']
            })
        }
    
    except Exception as e:
        # Handle any errors
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }
