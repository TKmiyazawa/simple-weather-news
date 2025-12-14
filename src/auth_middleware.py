"""認証ミドルウェアモジュール"""

import functools
import logging
from typing import Callable

from exceptions import AuthenticationError
from auth_service import extract_claims_from_event, is_authenticated
from models import ApiResponse, ErrorResponse

logger = logging.getLogger(__name__)


def require_auth(func: Callable) -> Callable:
    """認証を要求するデコレータ

    使用例:
        @require_auth
        def handler(event, context):
            user = event['requestContext']['authorizer']['claims']
            # 認証済みユーザーの処理
    """

    @functools.wraps(func)
    def wrapper(event: dict, context) -> dict:
        try:
            if not is_authenticated(event):
                logger.warning("Unauthenticated access attempt")
                error = ErrorResponse(
                    code="AUTH_ERROR",
                    message="認証が必要です",
                    request_id=getattr(context, "aws_request_id", None),
                )
                return ApiResponse(status_code=401, body=error.to_dict()).to_lambda_response()

            # クレームを取得してイベントに追加
            claims = extract_claims_from_event(event)
            if not claims:
                logger.warning("No claims found in authenticated request")
                error = ErrorResponse(
                    code="AUTH_ERROR",
                    message="認証情報が不正です",
                    request_id=getattr(context, "aws_request_id", None),
                )
                return ApiResponse(status_code=401, body=error.to_dict()).to_lambda_response()

            # 認証済みの場合は元の関数を実行
            return func(event, context)

        except AuthenticationError as e:
            logger.error(f"Authentication error: {e}")
            error = ErrorResponse(
                code=e.code,
                message=e.message,
                request_id=getattr(context, "aws_request_id", None),
            )
            return ApiResponse(status_code=401, body=error.to_dict()).to_lambda_response()

        except Exception as e:
            logger.error(f"Unexpected error in auth middleware: {e}")
            error = ErrorResponse(
                code="INTERNAL_ERROR",
                message="認証処理中にエラーが発生しました",
                request_id=getattr(context, "aws_request_id", None),
            )
            return ApiResponse(status_code=500, body=error.to_dict()).to_lambda_response()

    return wrapper
