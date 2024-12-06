import boto3
import os

def lambda_handler(event, context):
    """
    Automatically add confirmed users to the 'customer' group.
    """
    try:
        client = boto3.client("cognito-idp")
        user_pool_id = event["userPoolId"]
        username = event["userName"]
        group_name = os.environ["GROUP_NAME"]

        client.admin_add_user_to_group(
            UserPoolId=user_pool_id,
            Username=username,
            GroupName=group_name
        )

        print(f"User {username} added to group {group_name}")
        return event

    except Exception as e:
        print(f"Error: {e}")
        raise
