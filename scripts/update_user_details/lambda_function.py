import json
import boto3
import dynamo_json

dynamo_client = boto3.client("dynamodb")
lambda_client = boto3.client("lambda")


main_keys = ['firstname', 'lastname', 'contact', 'address', 'preferences']
sub_key_dictionary = {
    'address': ['postcode', 'province', 'streetAddress', 'streetNumber', 'suburb'],
    'contact': ['phoneNumber', 'telephoneNumber', 'email'],
    'preferences': ['mfa', 'sendAppNotification', 'sendEmail', 'sendSms']
}

def get_user_data(user_id):
    lambda_response = lambda_client.invoke(
        FunctionName='get_user_details',
        InvocationType='RequestResponse',
        Payload=json.dumps({'identity': {'username': user_id}})
    )
    return json.loads(lambda_response['Payload'].read())


def update_user_data(id, user_data, expression_names, expression):
    user_data = dynamo_json.marshall(user_data)
    print(user_data)
    print(expression)
    print(expression_names)
    dynamo_client.update_item(
        TableName="vehicle-demo-user-data",
        Key={
            "id": {
                "S": id,
            }
        },
        UpdateExpression=expression,
        ExpressionAttributeNames=expression_names,
        ExpressionAttributeValues=user_data
    )

def build_expression_values(arguments, user_data):
    has_sub_keys = list(sub_key_dictionary.keys())
    for main_key in main_keys:
        if arguments.get(main_key) != None:
            if main_key in has_sub_keys:
                for sub_key in sub_key_dictionary.get(main_key):
                    if arguments.get(main_key).get(sub_key) != None:
                        user_data[main_key][sub_key] = arguments.get(main_key).get(sub_key)
            else:
                user_data[main_key] = arguments.get(main_key)
        else:
            user_data.pop(main_key)
    return user_data

def create_expression(user_data):
    expression_names = {}
    expression = "SET "
    user_data_keys = list(user_data.keys())
    for user_data_key in user_data_keys:
        expression_names[f"#{user_data_key}"] = user_data_key
        expression += f"#{user_data_key} = :{user_data_key}, "
        user_data[f":{user_data_key}"] = user_data.pop(user_data_key)
    expression = expression.rstrip(", ")
    return {"names": expression_names, "expression": expression, "user_data": user_data}


def lambda_handler(event, context):
    user_id = event.get("identity").get("username")
    user_data = get_user_data(user_id)
    user_email = user_data.get('id')
    user_data.pop('id')
    arguments = event.get("arguments")
    user_data = build_expression_values(arguments, user_data)
    update_expressions = create_expression(user_data)
    expression_names = update_expressions.get("names")
    expression = update_expressions.get("expression")
    user_data = update_expressions.get("user_data")
    update_user_data(user_email, user_data, expression_names, expression)
    return arguments
