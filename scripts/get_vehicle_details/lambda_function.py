import json
import boto3
import dynamo_json

dynamo_client = boto3.client("dynamodb")
lambda_client = boto3.client("lambda")
s3_client = boto3.client("s3")
#comment
def get_vehicle_data(email):
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
                'vehicles'
            ],
        )
        print(dynamo_response)
        items = dynamo_json.unmarshall(dynamo_response.get("Item"))
        return items.get('vehicles')
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

def generate_image_urls(vehicle_details):
    for vehicle_detail in vehicle_details:
        signed_url = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': 'vehicle-demo-vehicle-image-bucket',
                                                            'Key': f"{vehicle_detail.get('model_id')}.png"},
                                                    ExpiresIn=900)
        vehicle_detail['model_url'] = signed_url
    return vehicle_details

def lambda_handler(event, context):
    user_id = event.get('identity').get('username')
    email = get_user_email(user_id)
    vehicle_details = get_vehicle_data(email)
    vehicle_details = generate_image_urls(vehicle_details)
    return vehicle_details