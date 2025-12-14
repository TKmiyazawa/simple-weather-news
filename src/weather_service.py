"""天気サービスモジュール - ビジネスロジック"""

import random
import logging
from datetime import datetime, timedelta
from typing import Optional

from models import WeatherData, CITIES, WEATHER_TYPES
from database import WeatherDatabase
from exceptions import WeatherDataError

logger = logging.getLogger(__name__)

# TTL: 24時間
DEFAULT_TTL_HOURS = 24


class WeatherService:
    """天気データのビジネスロジッククラス"""

    def __init__(self, database: Optional[WeatherDatabase] = None):
        self.database = database or WeatherDatabase()

    def generate_weather_data(self) -> list[WeatherData]:
        """全都市のランダム天気データを生成して保存"""
        now = datetime.utcnow()
        timestamp = now.isoformat()
        ttl = int((now + timedelta(hours=DEFAULT_TTL_HOURS)).timestamp())

        weather_data_list = []

        for city_id, city_name in CITIES.items():
            weather_id = random.choice(list(WEATHER_TYPES.keys()))
            weather_name = WEATHER_TYPES[weather_id]

            # 天気タイプに応じた降水確率を生成
            if weather_id == 1:  # 晴れ
                rainfall = random.randint(0, 20)
            elif weather_id == 2:  # くもり
                rainfall = random.randint(20, 50)
            else:  # 雨
                rainfall = random.randint(50, 100)

            weather_data = WeatherData(
                city_id=city_id,
                city_name=city_name,
                weather_id=weather_id,
                weather_name=weather_name,
                rainfall_probability=rainfall,
                timestamp=timestamp,
                ttl=ttl,
            )
            weather_data_list.append(weather_data)

        # データベースに保存
        success, errors = self.database.save_multiple_weather_data(weather_data_list)
        logger.info(f"Generated weather data: {success} success, {errors} errors")

        if success == 0:
            raise WeatherDataError("天気データの生成に失敗しました")

        return weather_data_list

    def get_current_weather(self) -> list[dict]:
        """全都市の最新天気データを取得"""
        try:
            weather_list = self.database.get_all_cities_latest_weather()
            return [w.to_dict() for w in weather_list]
        except Exception as e:
            logger.error(f"Failed to get current weather: {e}")
            raise WeatherDataError(f"天気データの取得に失敗しました: {str(e)}")

    def get_weather_by_city(self, city_id: int) -> Optional[dict]:
        """指定都市の最新天気データを取得"""
        if city_id not in CITIES:
            raise WeatherDataError(f"無効な都市ID: {city_id}")

        try:
            weather = self.database.get_latest_weather(city_id)
            return weather.to_dict() if weather else None
        except Exception as e:
            logger.error(f"Failed to get weather for city {city_id}: {e}")
            raise WeatherDataError(f"天気データの取得に失敗しました: {str(e)}")

    def get_forecast(self) -> list[dict]:
        """天気予報を取得（現在は最新データを返す）"""
        return self.get_current_weather()

    def get_statistics(self) -> dict:
        """天気統計情報を取得"""
        try:
            weather_list = self.database.get_all_cities_latest_weather()

            if not weather_list:
                return {
                    "total_cities": len(CITIES),
                    "data_available": 0,
                    "weather_distribution": {},
                    "average_rainfall": 0,
                }

            # 天気タイプ別の分布を計算
            weather_distribution = {}
            total_rainfall = 0

            for weather in weather_list:
                weather_name = weather.weather_name
                weather_distribution[weather_name] = (
                    weather_distribution.get(weather_name, 0) + 1
                )
                total_rainfall += weather.rainfall_probability

            avg_rainfall = total_rainfall / len(weather_list) if weather_list else 0

            return {
                "total_cities": len(CITIES),
                "data_available": len(weather_list),
                "weather_distribution": weather_distribution,
                "average_rainfall": round(avg_rainfall, 1),
            }
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            raise WeatherDataError(f"統計情報の取得に失敗しました: {str(e)}")

    @staticmethod
    def get_weather_types() -> list[dict]:
        """天気タイプ一覧を取得"""
        return [
            {"id": weather_id, "name": name}
            for weather_id, name in WEATHER_TYPES.items()
        ]

    @staticmethod
    def get_cities() -> list[dict]:
        """都市一覧を取得"""
        return [{"id": city_id, "name": name} for city_id, name in CITIES.items()]
