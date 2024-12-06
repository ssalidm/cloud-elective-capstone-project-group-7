import boto3
import os

GROUP_NAME = os.environ["GROUP_NAME"]


def lambda_handler(event, context):
    """
    Post-Confirmation trigger to add users to the 'customer' group.
    """
    try:
        # Initialize Cognito client
        client = boto3.client("cognito-idp")

        # Add user to the 'customer' group
        client.admin_add_user_to_group(
            UserPoolId=event["userPoolId"],
            Username=event["userName"],
            GroupName=GROUP_NAME,
        )

        print(f"Added user {event['userName']} to group '{GROUP_NAME}'")
        return event

    except Exception as e:
        print(f"Error: {e}")
        raise
