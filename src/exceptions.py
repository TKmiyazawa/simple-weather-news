"""カスタム例外クラス"""


class WeatherSystemError(Exception):
    """天気システムの基底例外クラス"""

    def __init__(self, message: str, code: str = "SYSTEM_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class AuthenticationError(WeatherSystemError):
    """認証エラー"""

    def __init__(self, message: str = "認証に失敗しました"):
        super().__init__(message, "AUTH_ERROR")


class WeatherDataError(WeatherSystemError):
    """天気データエラー"""

    def __init__(self, message: str = "天気データの取得に失敗しました"):
        super().__init__(message, "DATA_ERROR")


class DatabaseError(WeatherSystemError):
    """データベースエラー"""

    def __init__(self, message: str = "データベース操作に失敗しました"):
        super().__init__(message, "DB_ERROR")


class ValidationError(WeatherSystemError):
    """バリデーションエラー"""

    def __init__(self, message: str = "入力データが不正です"):
        super().__init__(message, "VALIDATION_ERROR")
