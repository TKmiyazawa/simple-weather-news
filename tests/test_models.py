"""models のテスト"""

import pytest
from models import WeatherData, ApiResponse, ErrorResponse, CITIES, WEATHER_TYPES


class TestCities:
    """都市マスターデータのテスト"""

    @pytest.mark.unit
    def test_cities_contains_five_cities(self):
        """5都市が定義されていること"""
        assert len(CITIES) == 5

    @pytest.mark.unit
    def test_cities_contains_expected_cities(self):
        """期待される都市が含まれていること"""
        expected = ['札幌', '東京', '名古屋', '大阪', '博多']
        actual = list(CITIES.values())
        for city in expected:
            assert city in actual


class TestWeatherTypes:
    """天気タイプマスターデータのテスト"""

    @pytest.mark.unit
    def test_weather_types_contains_three_types(self):
        """3種類の天気が定義されていること"""
        assert len(WEATHER_TYPES) == 3

    @pytest.mark.unit
    def test_weather_types_are_japanese(self):
        """天気タイプが日本語であること"""
        expected = ['晴れ', 'くもり', '雨']
        actual = list(WEATHER_TYPES.values())
        assert sorted(actual) == sorted(expected)


class TestWeatherData:
    """WeatherDataモデルのテスト"""

    @pytest.mark.unit
    def test_to_dict_returns_correct_structure(self):
        """to_dictが正しい構造を返すこと"""
        weather = WeatherData(
            city_id=13,
            city_name='東京',
            weather_id=1,
            weather_name='晴れ',
            rainfall_probability=10,
            timestamp='2024-01-01T12:00:00',
        )
        result = weather.to_dict()

        assert result['CityId'] == 13
        assert result['CityName'] == '東京'
        assert result['WeatherId'] == 1
        assert result['WeatherName'] == '晴れ'
        assert result['RainfallProbability'] == 10
        assert result['timestamp'] == '2024-01-01T12:00:00'

    @pytest.mark.unit
    def test_from_dict_creates_instance(self, sample_weather_data):
        """from_dictがインスタンスを生成すること"""
        weather = WeatherData.from_dict(sample_weather_data)

        assert weather.city_id == 13
        assert weather.city_name == '東京'
        assert weather.weather_name == '晴れ'

    @pytest.mark.unit
    def test_to_dict_includes_ttl_when_set(self):
        """TTLが設定されている場合は含まれること"""
        weather = WeatherData(
            city_id=1,
            city_name='札幌',
            weather_id=1,
            weather_name='晴れ',
            rainfall_probability=5,
            timestamp='2024-01-01T12:00:00',
            ttl=1704153600,
        )
        result = weather.to_dict()

        assert 'ttl' in result
        assert result['ttl'] == 1704153600


class TestApiResponse:
    """ApiResponseモデルのテスト"""

    @pytest.mark.unit
    def test_to_lambda_response_structure(self):
        """to_lambda_responseが正しい構造を返すこと"""
        response = ApiResponse(
            status_code=200,
            body={'message': 'test'}
        )
        result = response.to_lambda_response()

        assert result['statusCode'] == 200
        assert 'body' in result
        assert 'headers' in result
        assert result['headers']['Content-Type'] == 'application/json; charset=utf-8'


class TestErrorResponse:
    """ErrorResponseモデルのテスト"""

    @pytest.mark.unit
    def test_to_dict_includes_error_structure(self):
        """to_dictがerror構造を含むこと"""
        error = ErrorResponse(
            code='TEST_ERROR',
            message='テストエラー',
            request_id='test-123'
        )
        result = error.to_dict()

        assert 'error' in result
        assert result['error']['code'] == 'TEST_ERROR'
        assert result['error']['message'] == 'テストエラー'
        assert result['error']['request_id'] == 'test-123'
        assert 'timestamp' in result['error']
