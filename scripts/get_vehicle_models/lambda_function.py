import json
import dynamo_json
import boto3
#comment
dynamo_client = boto3.client("dynamodb")
lambda_client = boto3.client("lambda")

def get_vehicle_models():
    try:
        dynamo_response = dynamo_client.scan(
            TableName="vehicle-demo-model-data",
            AttributesToGet=[
                'model_id',
                'model',
                'year'
            ],
        )
        return dynamo_response.get("Items")
    except Exception as err:
        print(err)
        return err

def convert_response_to_json(vehicle_models):
    new_vehicle_model_list = [] 
    for vehicle_model in vehicle_models:
        new_vehicle_model_list.append(dynamo_json.unmarshall(vehicle_model))
    return new_vehicle_model_list

def lambda_handler(event, context):
    vehicle_modals_dynamo_json = get_vehicle_models()
    vehicle_models = convert_response_to_json(vehicle_modals_dynamo_json)
    print(vehicle_models)
    return None