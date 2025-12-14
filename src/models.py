"""データモデル定義"""

import json
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


class DecimalEncoder(json.JSONEncoder):
    """DynamoDBのDecimal型をJSONシリアライズ可能にするエンコーダー"""

    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super().default(obj)


# 都市マスターデータ
CITIES = {
    1: "札幌",
    13: "東京",
    23: "名古屋",
    27: "大阪",
    40: "博多",
}

# 天気タイプマスターデータ
WEATHER_TYPES = {
    1: "晴れ",
    2: "くもり",
    3: "雨",
}


@dataclass
class WeatherData:
    """天気データモデル"""

    city_id: int
    city_name: str
    weather_id: int
    weather_name: str
    rainfall_probability: int
    timestamp: str
    ttl: Optional[int] = None

    def to_dict(self) -> dict:
        """辞書形式に変換"""
        result = {
            "CityId": self.city_id,
            "CityName": self.city_name,
            "WeatherId": self.weather_id,
            "WeatherName": self.weather_name,
            "RainfallProbability": self.rainfall_probability,
            "timestamp": self.timestamp,
        }
        if self.ttl:
            result["ttl"] = self.ttl
        return result

    @classmethod
    def from_dict(cls, data: dict) -> "WeatherData":
        """辞書からインスタンスを生成"""
        ttl_value = data.get("ttl")
        return cls(
            city_id=int(data.get("CityId", 0)),
            city_name=data.get("CityName", ""),
            weather_id=int(data.get("WeatherId", 0)),
            weather_name=data.get("WeatherName", ""),
            rainfall_probability=int(data.get("RainfallProbability", 0)),
            timestamp=data.get("timestamp", ""),
            ttl=int(ttl_value) if ttl_value is not None else None,
        )


@dataclass
class ApiResponse:
    """APIレスポンスモデル"""

    status_code: int
    body: dict
    headers: Optional[dict] = None

    def to_lambda_response(self) -> dict:
        """Lambda形式のレスポンスに変換"""
        response = {
            "statusCode": self.status_code,
            "body": json.dumps(self.body, ensure_ascii=False, cls=DecimalEncoder),
            "headers": self.headers
            or {
                "Content-Type": "application/json; charset=utf-8",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,Authorization",
                "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
            },
        }
        return response


@dataclass
class ErrorResponse:
    """エラーレスポンスモデル"""

    code: str
    message: str
    request_id: Optional[str] = None

    def to_dict(self) -> dict:
        """辞書形式に変換"""
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "timestamp": datetime.utcnow().isoformat(),
                "request_id": self.request_id or "",
            }
        }
