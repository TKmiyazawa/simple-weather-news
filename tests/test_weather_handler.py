"""weather_handler のテスト"""

import json
import pytest
from moto import mock_aws

from weather_handler import lambda_handler, handle_health, handle_get_weather_types


class TestHealthEndpoint:
    """ヘルスチェックエンドポイントのテスト"""

    @pytest.mark.unit
    def test_health_check_returns_200(self, lambda_context):
        """ヘルスチェックが200を返すこと"""
        event = {'httpMethod': 'GET', 'path': '/health'}
        response = lambda_handler(event, lambda_context)

        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['status'] in ['healthy', 'degraded']
        assert body['service'] == 'weather-api'


class TestWeatherTypesEndpoint:
    """天気タイプエンドポイントのテスト"""

    @pytest.mark.unit
    def test_get_weather_types_returns_all_types(self, lambda_context):
        """全ての天気タイプが返されること"""
        event = {'httpMethod': 'GET', 'path': '/weather/types'}
        response = lambda_handler(event, lambda_context)

        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['success'] is True
        assert len(body['data']) == 3  # 晴れ、くもり、雨

        weather_names = [w['name'] for w in body['data']]
        assert '晴れ' in weather_names
        assert 'くもり' in weather_names
        assert '雨' in weather_names


class TestAuthenticationRequired:
    """認証が必要なエンドポイントのテスト"""

    @pytest.mark.unit
    def test_unauthenticated_request_returns_401(
        self, unauthenticated_event, lambda_context
    ):
        """未認証リクエストは401を返すこと"""
        response = lambda_handler(unauthenticated_event, lambda_context)

        assert response['statusCode'] == 401
        body = json.loads(response['body'])
        assert 'error' in body


class TestNotFoundEndpoint:
    """存在しないエンドポイントのテスト"""

    @pytest.mark.unit
    def test_unknown_path_returns_404(self, lambda_context):
        """存在しないパスは404を返すこと"""
        event = {'httpMethod': 'GET', 'path': '/unknown'}
        response = lambda_handler(event, lambda_context)

        assert response['statusCode'] == 404
        body = json.loads(response['body'])
        assert body['error']['code'] == 'NOT_FOUND'


class TestCORSHeaders:
    """CORSヘッダーのテスト"""

    @pytest.mark.unit
    def test_response_includes_cors_headers(self, lambda_context):
        """レスポンスにCORSヘッダーが含まれること"""
        event = {'httpMethod': 'GET', 'path': '/health'}
        response = lambda_handler(event, lambda_context)

        assert 'Access-Control-Allow-Origin' in response['headers']
        assert response['headers']['Access-Control-Allow-Origin'] == '*'


class TestOptionsRequest:
    """OPTIONSリクエストのテスト"""

    @pytest.mark.unit
    def test_options_request_returns_200(self, lambda_context):
        """OPTIONSリクエストは200を返すこと"""
        event = {'httpMethod': 'OPTIONS', 'path': '/weather'}
        response = lambda_handler(event, lambda_context)

        assert response['statusCode'] == 200
