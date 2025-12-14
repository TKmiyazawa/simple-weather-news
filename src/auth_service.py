"""認証サービスモジュール"""

import os
import logging
from typing import Optional

import boto3

from exceptions import AuthenticationError

logger = logging.getLogger(__name__)


class AuthService:
    """Cognito認証サービスクラス"""

    def __init__(self):
        self.user_pool_id = os.environ.get("COGNITO_USER_POOL_ID", "")
        self.client_id = os.environ.get("COGNITO_CLIENT_ID", "")
        self.cognito = boto3.client("cognito-idp")

    def verify_token(self, token: str) -> dict:
        """JWTトークンを検証"""
        # API Gatewayの Cognito Authorizer が検証するため、
        # Lambda内では claims を取得するのみ
        if not token:
            raise AuthenticationError("トークンが提供されていません")

        # トークンから Bearer を除去
        if token.startswith("Bearer "):
            token = token[7:]

        # 実際の検証は API Gateway が行う
        return {"valid": True}

    def get_user_from_claims(self, claims: dict) -> Optional[dict]:
        """クレームからユーザー情報を取得"""
        if not claims:
            return None

        return {
            "sub": claims.get("sub", ""),
            "email": claims.get("email", ""),
            "username": claims.get("cognito:username", ""),
        }


def extract_claims_from_event(event: dict) -> Optional[dict]:
    """Lambda イベントから Cognito クレームを抽出"""
    try:
        request_context = event.get("requestContext", {})
        authorizer = request_context.get("authorizer", {})

        # API Gateway REST API の場合
        claims = authorizer.get("claims", {})
        if claims:
            return claims

        # API Gateway HTTP API の場合
        jwt = authorizer.get("jwt", {})
        if jwt:
            return jwt.get("claims", {})

        return None
    except Exception as e:
        logger.error(f"Failed to extract claims: {e}")
        return None


def is_authenticated(event: dict) -> bool:
    """リクエストが認証済みかどうかを確認"""
    claims = extract_claims_from_event(event)
    return claims is not None and bool(claims)
