"""DynamoDB操作モジュール"""

import os
import logging
from typing import Optional
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key

from exceptions import DatabaseError
from models import WeatherData, CITIES

logger = logging.getLogger(__name__)


class WeatherDatabase:
    """天気データのDynamoDB操作クラス"""

    def __init__(self, table_name: Optional[str] = None):
        self.table_name = table_name or os.environ.get("TABLE_NAME", "weather-data")
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(self.table_name)

    def save_weather_data(self, weather_data: WeatherData) -> bool:
        """天気データを保存"""
        try:
            item = weather_data.to_dict()
            # Decimal変換（DynamoDB用）
            item["RainfallProbability"] = Decimal(str(item["RainfallProbability"]))
            if item.get("ttl"):
                item["ttl"] = Decimal(str(item["ttl"]))

            self.table.put_item(Item=item)
            logger.info(f"Saved weather data for city {weather_data.city_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to save weather data: {e}")
            raise DatabaseError(f"データの保存に失敗しました: {str(e)}")

    def get_latest_weather(self, city_id: int) -> Optional[WeatherData]:
        """指定都市の最新天気データを取得"""
        try:
            response = self.table.query(
                KeyConditionExpression=Key("CityId").eq(city_id),
                ScanIndexForward=False,  # 降順（最新が先頭）
                Limit=1,
            )
            items = response.get("Items", [])
            if items:
                return WeatherData.from_dict(items[0])
            return None
        except Exception as e:
            logger.error(f"Failed to get weather data for city {city_id}: {e}")
            raise DatabaseError(f"データの取得に失敗しました: {str(e)}")

    def get_all_cities_latest_weather(self) -> list[WeatherData]:
        """全都市の最新天気データを取得"""
        results = []
        errors = []

        for city_id in CITIES.keys():
            try:
                weather = self.get_latest_weather(city_id)
                if weather:
                    results.append(weather)
            except DatabaseError as e:
                logger.warning(f"Failed to get weather for city {city_id}: {e}")
                errors.append(city_id)
                continue

        if errors and not results:
            raise DatabaseError(f"全てのデータ取得に失敗しました: {errors}")

        return results

    def save_multiple_weather_data(
        self, weather_data_list: list[WeatherData]
    ) -> tuple[int, int]:
        """複数の天気データを保存（部分的な失敗を許容）"""
        success_count = 0
        error_count = 0

        for weather_data in weather_data_list:
            try:
                self.save_weather_data(weather_data)
                success_count += 1
            except DatabaseError as e:
                logger.error(f"Failed to save weather for city {weather_data.city_id}: {e}")
                error_count += 1
                continue

        return success_count, error_count

    def health_check(self) -> bool:
        """データベース接続のヘルスチェック"""
        try:
            self.table.table_status
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
