import json
import uuid
import dynamo_json
import boto3

dynamo_client = boto3.client("dynamodb")

def update_vehicle_model(model_id, vehicle_model, expression_names, expression):
    vehicle_model = dynamo_json.marshall(vehicle_model)
    dynamo_client.update_item(
        TableName="vehicle-demo-model-data",
        Key={
            "model_id": {
                "S": model_id,
            }
        },
        UpdateExpression=expression,
        ExpressionAttributeNames=expression_names,
        ExpressionAttributeValues=vehicle_model
    )

def create_expression(vehicle_model):
    expression_names = {}
    expression = "SET "
    vehicle_model_keys = list(vehicle_model.keys())
    for vehicle_model_key in vehicle_model_keys:
        expression_names[f"#{vehicle_model_key}"] = vehicle_model_key
        expression += f"#{vehicle_model_key} = :{vehicle_model_key}, "
        vehicle_model[f":{vehicle_model_key}"] = vehicle_model.pop(vehicle_model_key)
    expression = expression.rstrip(", ")
    return {"names": expression_names, "expression": expression, "vehicle_model": vehicle_model}


def lambda_handler(event, context):
    vehicle_model = event.get('arguments')
    model_id = vehicle_model.get('model_id')
    vehicle_model.pop('model_id')
    update_expressions = create_expression(vehicle_model)
    expression_names = update_expressions.get("names")
    expression = update_expressions.get("expression")
    vehicle_model = update_expressions.get("vehicle_model")
    update_vehicle_model(model_id, vehicle_model, expression_names, expression)
    return event.get('arguments')