"""CSV取り込みLambda関数"""

import os
import csv
import logging
from io import StringIO
from datetime import datetime, timedelta
from decimal import Decimal
from urllib.parse import unquote_plus

import boto3

# ロギング設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS クライアント
s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

# 環境変数
TABLE_NAME = os.environ.get("TABLE_NAME", "weather-data")

# TTL: 24時間
DEFAULT_TTL_HOURS = 24


def lambda_handler(event: dict, context) -> dict:
    """S3イベントトリガーのエントリーポイント"""
    logger.info(f"Received event: {event}")

    success_count = 0
    error_count = 0

    for record in event.get("Records", []):
        try:
            # S3情報を取得
            bucket = record["s3"]["bucket"]["name"]
            key = unquote_plus(record["s3"]["object"]["key"])

            logger.info(f"Processing file: s3://{bucket}/{key}")

            # CSVファイルを処理
            processed, errors = process_csv_file(bucket, key)
            success_count += processed
            error_count += errors

        except Exception as e:
            logger.error(f"Error processing record: {e}")
            error_count += 1

    result = {
        "statusCode": 200,
        "body": {
            "message": "CSV処理完了",
            "success_count": success_count,
            "error_count": error_count,
        },
    }

    logger.info(f"Processing result: {result}")
    return result


def process_csv_file(bucket: str, key: str) -> tuple[int, int]:
    """CSVファイルを処理してDynamoDBに保存"""
    success_count = 0
    error_count = 0

    try:
        # S3からファイルを読み込み
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response["Body"].read().decode("utf-8")

        logger.info(f"Read {len(content)} bytes from S3")

        # CSVを解析
        reader = csv.reader(StringIO(content))

        # DynamoDBテーブル
        table = dynamodb.Table(TABLE_NAME)

        # タイムスタンプとTTLを設定
        now = datetime.utcnow()
        timestamp = now.isoformat()
        ttl = int((now + timedelta(hours=DEFAULT_TTL_HOURS)).timestamp())

        for row_num, row in enumerate(reader, start=1):
            try:
                # 行を処理
                item = parse_csv_row(row, timestamp, ttl)
                if item:
                    # DynamoDBに保存
                    table.put_item(Item=item)
                    success_count += 1
                    logger.info(f"Row {row_num}: Saved city {item['CityId']}")
                else:
                    logger.warning(f"Row {row_num}: Invalid format, skipping")
                    error_count += 1

            except Exception as e:
                logger.error(f"Row {row_num}: Error processing - {e}")
                error_count += 1
                continue

    except Exception as e:
        logger.error(f"Error reading CSV file: {e}")
        raise

    return success_count, error_count


def parse_csv_row(row: list, timestamp: str, ttl: int) -> dict | None:
    """CSV行を解析してDynamoDB項目に変換

    フォーマット（ヘッダーなし）:
    CityId,CityName,WeatherId,WeatherName,RainfallProbability
    """
    if len(row) < 5:
        return None

    try:
        city_id = int(row[0].strip())
        city_name = row[1].strip()
        # WeatherId (row[2]) は使用しない
        weather_name = row[3].strip()
        rainfall_probability = int(row[4].strip())

        # バリデーション
        if not city_name or not weather_name:
            return None

        if rainfall_probability < 0 or rainfall_probability > 100:
            return None

        return {
            "CityId": city_id,
            "CityName": city_name,
            "WeatherName": weather_name,
            "RainfallProbability": Decimal(str(rainfall_probability)),
            "timestamp": timestamp,
            "ttl": Decimal(str(ttl)),
        }

    except (ValueError, IndexError) as e:
        logger.warning(f"Parse error: {e}")
        return None


# テスト用の関数
def _test_parse_row():
    """パース関数のテスト"""
    test_row = ["1", "札幌", "1", "晴れ", "10"]
    result = parse_csv_row(test_row, "2024-01-01T00:00:00", 1704067200)
    print(f"Test result: {result}")
    return result


if __name__ == "__main__":
    _test_parse_row()
