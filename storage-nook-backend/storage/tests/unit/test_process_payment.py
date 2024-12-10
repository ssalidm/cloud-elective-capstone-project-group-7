import json
from moto import mock_dynamodb
import boto3
from lambda_function import lambda_handler
from uuid import uuid4


@mock_dynamodb
def test_successful_payment():
    # Set up mock DynamoDB
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

    # Create tables
    bookings_table = dynamodb.create_table(
        TableName="BookingsTable",
        KeySchema=[{"AttributeName": "bookingId", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "bookingId", "AttributeType": "S"}],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    profiles_table = dynamodb.create_table(
        TableName="ProfilesTable",
        KeySchema=[{"AttributeName": "userId", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "userId", "AttributeType": "S"}],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    bookings_table.meta.client.get_waiter("table_exists").wait(TableName="BookingsTable")
    profiles_table.meta.client.get_waiter("table_exists").wait(TableName="ProfilesTable")

    # Add mock data
    booking_id = str(uuid4())
    user_id = str(uuid4())
    profiles_table.put_item(
        Item={
            "userId": user_id,
            "paymentMethods": [{"type": "CreditCard", "details": "Visa 1234"}],
        }
    )
    bookings_table.put_item(
        Item={"bookingId": booking_id, "paymentStatus": "Pending", "status": "Reserved"}
    )

    # Define test event
    event = {
        "pathParameters": {"bookingId": booking_id},
        "body": json.dumps({"paymentMethodType": "CreditCard"}),
        "requestContext": {"authorizer": {"claims": {"sub": user_id}}},
    }

    # Call the Lambda function
    response = lambda_handler(event, None)

    # Assert response
    assert response["statusCode"] == 200
    response_body = json.loads(response["body"])
    assert response_body["message"] == "Payment successful"
    assert response_body["paymentMethod"]["type"] == "CreditCard"


@mock_dynamodb
def test_missing_required_fields():
    # Define test event with missing fields
    event = {
        "pathParameters": {"bookingId": "booking-123"},
        "body": json.dumps({}),
        "requestContext": {"authorizer": {"claims": {"sub": "user-123"}}},
    }

    # Call the Lambda function
    response = lambda_handler(event, None)

    # Assert response
    assert response["statusCode"] == 400
    assert "Missing userId or paymentMethodType" in json.loads(response["body"])["error"]


@mock_dynamodb
def test_user_not_found():
    # Set up mock DynamoDB
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    profiles_table = dynamodb.create_table(
        TableName="ProfilesTable",
        KeySchema=[{"AttributeName": "userId", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "userId", "AttributeType": "S"}],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    profiles_table.meta.client.get_waiter("table_exists").wait(TableName="ProfilesTable")

    # Define test event
    event = {
        "pathParameters": {"bookingId": "booking-123"},
        "body": json.dumps({"paymentMethodType": "CreditCard"}),
        "requestContext": {"authorizer": {"claims": {"sub": "nonexistent-user"}}},
    }

    # Call the Lambda function
    response = lambda_handler(event, None)

    # Assert response
    assert response["statusCode"] == 404
    assert "User not found" in json.loads(response["body"])["error"]


@mock_dynamodb
def test_booking_already_paid():
    # Set up mock DynamoDB
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    bookings_table = dynamodb.create_table(
        TableName="BookingsTable",
        KeySchema=[{"AttributeName": "bookingId", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "bookingId", "AttributeType": "S"}],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    bookings_table.meta.client.get_waiter("table_exists").wait(TableName="BookingsTable")

    # Add a paid booking
    booking_id = "booking-123"
    bookings_table.put_item(
        Item={"bookingId": booking_id, "paymentStatus": "Paid", "status": "Reserved"}
    )

    # Define test event
    event = {
        "pathParameters": {"bookingId": booking_id},
        "body": json.dumps({"paymentMethodType": "CreditCard"}),
        "requestContext": {"authorizer": {"claims": {"sub": "user-123"}}},
    }

    # Call the Lambda function
    response = lambda_handler(event, None)

    # Assert response
    assert response["statusCode"] == 400
    assert "Booking is already paid" in json.loads(response["body"])["error"]
