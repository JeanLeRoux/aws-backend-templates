import json
import dynamo_json
import boto3
#comment
dynamo_client = boto3.client("dynamodb")
lambda_client = boto3.client("lambda")

def get_user_data(email):
    try:
        dynamo_response = dynamo_client.get_item(
            TableName="vehicle-demo-user-data",
            Key={
                "id": {
                    "S": email,
                }
            },
            AttributesToGet=[
                'id',
                'address',
                'contact',
                'firstname',
                'lastname',
                'preferences',
            ],
        )
        return dynamo_json.unmarshall(dynamo_response.get("Item"))
    except Exception as err:
        print(err)
        return err

def get_user_email(user_id):
    lambda_response = lambda_client.invoke(
        FunctionName='get_user_email',
        InvocationType='RequestResponse',
        Payload=json.dumps({'identity': {'username': user_id}})
    )
    return json.loads(lambda_response['Payload'].read())


def lambda_handler(event, context):
    user_id = event.get('identity').get('username')
    email = get_user_email(user_id)
    user_data = get_user_data(email)
    return user_data