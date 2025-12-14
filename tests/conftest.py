"""pytest設定とフィクスチャ"""

import os
import sys
import pytest
import boto3
from moto import mock_aws

# srcディレクトリをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# 環境変数設定
os.environ['TABLE_NAME'] = 'test-weather-table'
os.environ['COGNITO_USER_POOL_ID'] = 'ap-northeast-1_TestPool'
os.environ['COGNITO_CLIENT_ID'] = 'test-client-id'
os.environ['AWS_DEFAULT_REGION'] = 'ap-northeast-1'
os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'


@pytest.fixture
def mock_dynamodb():
    """DynamoDBのモック"""
    with mock_aws():
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')

        # テスト用テーブルを作成
        table = dynamodb.create_table(
            TableName='test-weather-table',
            KeySchema=[
                {'AttributeName': 'CityId', 'KeyType': 'HASH'},
                {'AttributeName': 'timestamp', 'KeyType': 'RANGE'},
            ],
            AttributeDefinitions=[
                {'AttributeName': 'CityId', 'AttributeType': 'N'},
                {'AttributeName': 'timestamp', 'AttributeType': 'S'},
            ],
            BillingMode='PAY_PER_REQUEST',
        )
        table.wait_until_exists()

        yield dynamodb


@pytest.fixture
def sample_weather_data():
    """サンプル天気データ"""
    return {
        'CityId': 13,
        'CityName': '東京',
        'WeatherId': 1,
        'WeatherName': '晴れ',
        'RainfallProbability': 10,
        'timestamp': '2024-01-01T12:00:00',
    }


@pytest.fixture
def authenticated_event():
    """認証済みイベント"""
    return {
        'httpMethod': 'GET',
        'path': '/weather',
        'requestContext': {
            'authorizer': {
                'claims': {
                    'sub': 'test-user-id',
                    'email': 'test@example.com',
                    'cognito:username': 'testuser',
                }
            }
        }
    }


@pytest.fixture
def unauthenticated_event():
    """未認証イベント"""
    return {
        'httpMethod': 'GET',
        'path': '/weather',
        'requestContext': {}
    }


class MockContext:
    """Lambdaコンテキストのモック"""

    def __init__(self):
        self.aws_request_id = 'test-request-id'
        self.function_name = 'test-function'
        self.memory_limit_in_mb = 128
        self.invoked_function_arn = 'arn:aws:lambda:ap-northeast-1:123456789:function:test'


@pytest.fixture
def lambda_context():
    """Lambdaコンテキストフィクスチャ"""
    return MockContext()
