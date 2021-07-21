import json
import dynamo_json
import boto3

cognito_client = boto3.client("cognito-idp")
ssm_client = boto3.client("ssm")

def get_user_pool_id():
    ssm_response = ssm_client.get_parameter(
        Name='Vehicle_Demo_Cognito_User_Pool_Id',
        WithDecryption=False
    )
    return ssm_response.get('Parameter').get('Value')


def get_user_email(user_pool, user_id):
    email = None
    cognito_response = cognito_client.admin_get_user(
        UserPoolId=user_pool,
        Username=user_id
    )
    user_attributes = cognito_response.get('UserAttributes')
    for user_attribute in user_attributes:
        if user_attribute.get('Name') == 'email':
            email = user_attribute.get('Value')
            break
    return email

def lambda_handler(event, context):
    user_id = event.get('identity').get('username')
    user_pool = get_user_pool_id()
    email = get_user_email(user_pool, user_id)
    return email