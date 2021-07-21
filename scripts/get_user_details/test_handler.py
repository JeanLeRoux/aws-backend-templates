import boto3
from moto import mock_cognitoidp
from moto import mock_dynamodb2
from moto import mock_ssm
import pytest
import lambda_function

def test_ssm():
    user_pool = lambda_function.get_user_pool_id()
    region = user_pool.split('_')[0]
    assert region == 'eu-west-1'



