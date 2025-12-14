---
inclusion: always
---

<!--
╔══════════════════════════════════════════════════════════════════════════════╗
║  📚 KIRO 学習ガイド: tech.md                                                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  このファイルの役割:                                                         ║
║  - 使用技術スタック（言語、フレームワーク、AWSサービス）を定義               ║
║  - 開発・テスト・デプロイコマンドを一覧化                                    ║
║  - コーディング規約とパターンを定義                                          ║
║  - データベーススキーマを記載                                                ║
║                                                                              ║
║  学習ポイント:                                                               ║
║  1. Development Commands - AIが正しいコマンドを提案するための情報            ║
║  2. Code Standards - コーディング規約に沿ったコード生成                      ║
║  3. DynamoDB Schema - データモデルを理解した提案                             ║
║                                                                              ║
║  AIへの効果:                                                                 ║
║  - 「テストを実行して」→ 正しいコマンドを提案                                ║
║  - 「Pythonでエラーハンドリング」→ exceptions.py のパターンを使用            ║
║  - 「データを保存」→ DynamoDBスキーマに沿った実装                            ║
║                                                                              ║
║  詳細: KIRO_LEARNING.md の「3. Steering Files」を参照                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
-->

# Technology Stack

## Backend

### Runtime & Language
| 技術 | バージョン | 用途 |
|------|-----------|------|
| Python | 3.12 | Lambda runtime |
| boto3 | 1.34.0+ | AWS SDK for Python |
| pydantic | 2.5.0+ | Data validation |

### AWS Services
| サービス | 用途 |
|---------|------|
| Lambda | サーバーレス関数実行 |
| API Gateway | REST API エンドポイント |
| DynamoDB | NoSQL データベース |
| Cognito | ユーザー認証 (JWT) |
| S3 | 静的ホスティング & CSV ストレージ |
| CloudFront | CDN |
| CloudWatch | ログ & メトリクス |

### Infrastructure
| 技術 | 用途 |
|------|------|
| AWS SAM | Serverless Application Model |
| CloudFormation | Infrastructure as Code |
| Region | ap-northeast-1 (Tokyo) |

## Frontend

### Framework & Build
| 技術 | バージョン | 用途 |
|------|-----------|------|
| React | 18.2.0 | UI ライブラリ |
| Vite | 5.0.8 | ビルドツール & 開発サーバー |
| AWS Amplify UI | 6.0.0 | 認証コンポーネント |

### Linting
- **ESLint** - JavaScript linting
- Plugins: `react`, `react-hooks`, `react-refresh`

## Testing

### Backend Testing
| ツール | 用途 |
|-------|------|
| pytest | テストフレームワーク |
| Hypothesis | プロパティベーステスト |
| moto | AWS サービスモック |

**Test Markers** (pytest.ini):
- `unit` - 単体テスト
- `integration` - 統合テスト
- `property` - プロパティベーステスト

### Frontend Testing
- **Vitest** - Vite ネイティブテストランナー

---

## Development Commands

### Installation
```bash
# All dependencies
make install

# Backend only
pip install -r requirements.txt

# Frontend only
cd simple-weather-frontend && npm ci
```

### Testing
```bash
# All tests
make test

# Backend tests
python -m pytest tests/ -v

# Unit tests only
python -m pytest tests/ -v -m unit

# Property-based tests only
python -m pytest tests/ -v -m property

# Single test file
python -m pytest tests/test_weather_handler.py -v

# Frontend tests
cd simple-weather-frontend && npm test -- --run

# CSV ingest tests
cd csv_ingest && python3 test_app.py
```

### Linting
```bash
# Frontend ESLint
cd simple-weather-frontend && npm run lint
```

### Local Development
```bash
# Backend API (SAM Local)
sam local start-api --port 3001

# Frontend dev server
cd simple-weather-frontend && npm run dev
```

### Deployment
```bash
# Development environment
make deploy STAGE=dev REGION=ap-northeast-1

# Production
make prod-deploy

# Template validation
make validate
sam validate

# Check deployment status
make status
make outputs

# View Lambda logs
make logs
```

### Build & Clean
```bash
# Build
make build
sam build

# Clean build artifacts
make clean
```

---

## Code Standards

### Python

**Style**:
- PEP 8 準拠
- 型ヒント使用を推奨
- `logging` モジュールによる構造化ログ

**Error Handling**:
```python
from exceptions import AuthenticationError, WeatherDataError

try:
    result = weather_service.get_weather(city_id)
except WeatherDataError as e:
    logger.error(f"Weather data error: {e}")
    return error_response(500, str(e))
```

**Authentication Pattern**:
```python
from auth_middleware import require_auth

@require_auth
def handler(event, context):
    user = event['requestContext']['authorizer']['claims']
    # Protected logic here
```

### JavaScript/React

**Style**:
- Functional components with hooks
- async/await for API calls
- ESLint configuration in `.eslintrc.cjs`

**Component Pattern**:
```javascript
import React, { useState, useEffect } from 'react';

function WeatherDisplay() {
    const [weather, setWeather] = useState(null);

    useEffect(() => {
        fetchWeather();
    }, []);

    return (/* JSX */);
}
```

---

## DynamoDB Schema

### WeatherTable
| 属性 | 型 | 説明 |
|------|-----|------|
| CityId | Number (HASH) | 都市ID (1, 13, 23, 27, 40) |
| timestamp | String (RANGE) | ISO 8601 タイムスタンプ |
| CityName | String | 都市名 (札幌, 東京, 名古屋, 大阪, 博多) |
| WeatherName | String | 天気 (晴れ, くもり, 雨) |
| RainfallProbability | Number | 降水確率 (0-100) |
| ttl | Number | TTL (Unix timestamp) |

**Indexes**:
- GSI: `timestamp-index` - 時間順クエリ用

**City ID Mapping**:
| CityId | CityName |
|--------|----------|
| 1 | 札幌 |
| 13 | 東京 |
| 23 | 名古屋 |
| 27 | 大阪 |
| 40 | 博多 |
