"""Lambda メインハンドラー - APIルーティング"""

import json
import logging
from typing import Callable

from models import ApiResponse, ErrorResponse
from weather_service import WeatherService
from auth_middleware import require_auth
from exceptions import WeatherSystemError, WeatherDataError

# ロギング設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# サービスインスタンス
weather_service = WeatherService()


def lambda_handler(event: dict, context) -> dict:
    """Lambda エントリーポイント"""
    logger.info(f"Received event: {json.dumps(event)}")

    # パスとメソッドを取得
    http_method = event.get("httpMethod", "GET")
    path = event.get("path", "/")

    # ルーティング
    route_key = f"{http_method} {path}"

    routes = {
        "GET /health": handle_health,
        "GET /weather": handle_get_weather,
        "POST /weather/generate": handle_generate_weather,
        "GET /weather/forecast": handle_get_forecast,
        "GET /weather/statistics": handle_get_statistics,
        "GET /weather/types": handle_get_weather_types,
        "OPTIONS /health": handle_options,
        "OPTIONS /weather": handle_options,
        "OPTIONS /weather/generate": handle_options,
        "OPTIONS /weather/forecast": handle_options,
        "OPTIONS /weather/statistics": handle_options,
        "OPTIONS /weather/types": handle_options,
    }

    handler = routes.get(route_key, handle_not_found)

    try:
        return handler(event, context)
    except Exception as e:
        logger.error(f"Unhandled error: {e}")
        error = ErrorResponse(
            code="INTERNAL_ERROR",
            message="サーバー内部エラーが発生しました",
            request_id=getattr(context, "aws_request_id", None),
        )
        return ApiResponse(status_code=500, body=error.to_dict()).to_lambda_response()


def handle_options(event: dict, context) -> dict:
    """OPTIONS リクエスト（CORS preflight）"""
    return ApiResponse(status_code=200, body={}).to_lambda_response()


def handle_health(event: dict, context) -> dict:
    """ヘルスチェックエンドポイント"""
    try:
        db_healthy = weather_service.database.health_check()
        status = "healthy" if db_healthy else "degraded"

        return ApiResponse(
            status_code=200,
            body={
                "status": status,
                "service": "weather-api",
                "database": "connected" if db_healthy else "disconnected",
            },
        ).to_lambda_response()
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return ApiResponse(
            status_code=200,
            body={
                "status": "degraded",
                "service": "weather-api",
                "database": "error",
            },
        ).to_lambda_response()


@require_auth
def handle_get_weather(event: dict, context) -> dict:
    """天気データ取得エンドポイント"""
    try:
        weather_data = weather_service.get_current_weather()

        if not weather_data:
            # データがない場合は自動生成
            weather_service.generate_weather_data()
            weather_data = weather_service.get_current_weather()

        return ApiResponse(
            status_code=200,
            body={
                "success": True,
                "data": weather_data,
                "count": len(weather_data),
            },
        ).to_lambda_response()
    except WeatherDataError as e:
        logger.error(f"Weather data error: {e}")
        error = ErrorResponse(
            code=e.code,
            message=e.message,
            request_id=getattr(context, "aws_request_id", None),
        )
        return ApiResponse(status_code=500, body=error.to_dict()).to_lambda_response()


def handle_generate_weather(event: dict, context) -> dict:
    """天気データ生成エンドポイント"""
    try:
        weather_data = weather_service.generate_weather_data()

        return ApiResponse(
            status_code=201,
            body={
                "success": True,
                "message": "天気データを生成しました",
                "data": [w.to_dict() for w in weather_data],
                "count": len(weather_data),
            },
        ).to_lambda_response()
    except WeatherDataError as e:
        logger.error(f"Weather generation error: {e}")
        error = ErrorResponse(
            code=e.code,
            message=e.message,
            request_id=getattr(context, "aws_request_id", None),
        )
        return ApiResponse(status_code=500, body=error.to_dict()).to_lambda_response()


@require_auth
def handle_get_forecast(event: dict, context) -> dict:
    """天気予報取得エンドポイント"""
    try:
        forecast = weather_service.get_forecast()

        return ApiResponse(
            status_code=200,
            body={
                "success": True,
                "data": forecast,
                "count": len(forecast),
            },
        ).to_lambda_response()
    except WeatherDataError as e:
        logger.error(f"Forecast error: {e}")
        error = ErrorResponse(
            code=e.code,
            message=e.message,
            request_id=getattr(context, "aws_request_id", None),
        )
        return ApiResponse(status_code=500, body=error.to_dict()).to_lambda_response()


@require_auth
def handle_get_statistics(event: dict, context) -> dict:
    """統計情報取得エンドポイント"""
    try:
        statistics = weather_service.get_statistics()

        return ApiResponse(
            status_code=200,
            body={
                "success": True,
                "data": statistics,
            },
        ).to_lambda_response()
    except WeatherDataError as e:
        logger.error(f"Statistics error: {e}")
        error = ErrorResponse(
            code=e.code,
            message=e.message,
            request_id=getattr(context, "aws_request_id", None),
        )
        return ApiResponse(status_code=500, body=error.to_dict()).to_lambda_response()


def handle_get_weather_types(event: dict, context) -> dict:
    """天気タイプ一覧取得エンドポイント（認証不要）"""
    weather_types = weather_service.get_weather_types()

    return ApiResponse(
        status_code=200,
        body={
            "success": True,
            "data": weather_types,
        },
    ).to_lambda_response()


def handle_not_found(event: dict, context) -> dict:
    """404 Not Found"""
    error = ErrorResponse(
        code="NOT_FOUND",
        message="エンドポイントが見つかりません",
        request_id=getattr(context, "aws_request_id", None),
    )
    return ApiResponse(status_code=404, body=error.to_dict()).to_lambda_response()
