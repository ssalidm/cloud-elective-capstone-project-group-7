import json
import boto3
from datetime import datetime

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
bookings_table = dynamodb.Table('BookingsTable')

def lambda_handler(event, context):
    try:
        # Get the facilityId from the path parameters
        facility_id = event['pathParameters']['facilityId']
        # Get the desired start and end date for availability check
        query_params = event['queryStringParameters']
        start_date = query_params['startDate']
        end_date = query_params['endDate']
        
        # Query DynamoDB to find conflicting bookings
        response = bookings_table.scan(
            FilterExpression="facilityId = :facilityId AND startDate < :endDate AND endDate > :startDate",
            ExpressionAttributeValues={
                ':facilityId': facility_id,
                ':startDate': start_date,
                ':endDate': end_date
            }
        )
        
        # If there are conflicting bookings, the unit is not available
        if response['Items']:
            return {
                'statusCode': 200,
                'body': json.dumps({'available': False, 'message': 'Unit is not available for the selected dates'})
            }
        
        # If no conflicting bookings, the unit is available
        return {
            'statusCode': 200,
            'body': json.dumps({'available': True, 'message': 'Unit is available for the selected dates'})
        }
    
    except Exception as e:
        # Handle any errors
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }
