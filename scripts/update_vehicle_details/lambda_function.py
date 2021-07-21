import json
import boto3
import dynamo_json
#comment
dynamo_client = boto3.client("dynamodb")
lambda_client = boto3.client("lambda")

def get_vehicles_data(user_id):
    lambda_response = lambda_client.invoke(
        FunctionName='get_vehicle_details',
        InvocationType='RequestResponse',
        Payload=json.dumps({'identity': {'username': user_id}})
    )
    vehicles = {"vehicles":json.loads(lambda_response['Payload'].read())}
    return vehicles


def update_vehicle_data(user_id, vehicle_data):
    vehicle_data = dynamo_json.marshall(vehicle_data)
    vehicle_data[":vehicles"] = vehicle_data.pop('vehicles')
    print(vehicle_data)
    dynamo_client.update_item(
        TableName = "vehicle-demo-user-data",
        Key = {
            "id": {
                "S": user_id,
            }
        },
        UpdateExpression = "Set #vehicles = :vehicles",
        ExpressionAttributeNames = {"#vehicles":"vehicles"},
        ExpressionAttributeValues = vehicle_data
    )

def get_user_email(user_id):
    lambda_response = lambda_client.invoke(
        FunctionName='get_user_email',
        InvocationType='RequestResponse',
        Payload=json.dumps({'identity': {'username': user_id}})
    )
    return json.loads(lambda_response['Payload'].read())


def lambda_handler(event, context):
    user_id = event.get("identity").get("username")
    email = get_user_email(user_id)
    vehicles = get_vehicles_data(email)
    print(vehicles)
    vehicle_data = event.get('arguments')
    regestration_number = event.get("arguments").get("regestrationNumber")
    add_as_new_value = True
    for index, vehicle in enumerate(vehicles.get("vehicles")):
        if vehicle.get("regestrationNumber") == regestration_number:
            vehicles["vehicles"][index] = vehicle_data
            add_as_new_value = False
    if add_as_new_value:
        vehicles["vehicles"].append(vehicle_data)

    update_vehicle_data(email, vehicles)
    return vehicle_data
