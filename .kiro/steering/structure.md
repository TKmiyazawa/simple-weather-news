---
inclusion: always
---

<!--
╔══════════════════════════════════════════════════════════════════════════════╗
║  📚 KIRO 学習ガイド: structure.md                                            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  このファイルの役割:                                                         ║
║  - ディレクトリ構造と各ファイルの責任を定義                                  ║
║  - 命名規則（Python: snake_case, React: PascalCase 等）を定義                ║
║  - インポートパターンを標準化                                                ║
║                                                                              ║
║  学習ポイント:                                                               ║
║  1. Directory Layout - AIがファイル配置を理解するための情報                  ║
║  2. Naming Conventions - 規約に沿った命名を提案                              ║
║  3. Import Patterns - 一貫したインポート順序                                 ║
║  4. Key File Descriptions - 各ファイルの責任を明確化                         ║
║                                                                              ║
║  AIへの効果:                                                                 ║
║  - 新しいファイルを適切なディレクトリに配置                                  ║
║  - 命名規則に沿った変数名・関数名を提案                                      ║
║  - 既存パターンに沿ったコードを生成                                          ║
║                                                                              ║
║  詳細: KIRO_LEARNING.md の「3. Steering Files」を参照                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
-->

# Project Structure

## Directory Layout

```
simple-weather-news/
├── .kiro/                          # Kiro IDE configuration
│   ├── specs/                      # Feature specifications
│   │   ├── serverless-weather-system/
│   │   │   ├── requirements.md     # 要件定義
│   │   │   ├── design.md           # 設計書
│   │   │   └── tasks.md            # 実装タスク
│   │   └── csv-data-ingestion/
│   │       ├── requirements.md
│   │       ├── design.md
│   │       └── tasks.md
│   ├── steering/                   # Steering files (this directory)
│   │   ├── product.md              # 製品ビジョン
│   │   ├── structure.md            # プロジェクト構造
│   │   └── tech.md                 # 技術スタック
│   └── hooks/                      # Agent hooks
│       ├── python-lint-format.md   # Python コード品質
│       ├── frontend-lint.md        # フロントエンド lint
│       ├── test-trigger.md         # テスト実行トリガー
│       ├── specs-sync-check.md     # Specs-コード同期
│       └── readme-update.md        # README 更新提案
│
├── src/                            # Backend Lambda source code
│   ├── weather_handler.py          # Main API handler (routing)
│   ├── weather_service.py          # Weather business logic
│   ├── auth_service.py             # Cognito authentication
│   ├── auth_middleware.py          # @require_auth decorator
│   ├── database.py                 # DynamoDB operations
│   ├── models.py                   # Data models
│   ├── exceptions.py               # Custom exceptions
│   └── requirements.txt            # Lambda dependencies
│
├── tests/                          # Backend test suite
│   ├── conftest.py                 # pytest configuration
│   ├── test_weather_handler.py     # Handler unit tests
│   ├── test_auth_service.py        # Auth unit tests
│   └── test_property_*.py          # Property-based tests (Hypothesis)
│
├── csv_ingest/                     # CSV ingestion Lambda
│   ├── app.py                      # S3 trigger handler
│   ├── test_app.py                 # Unit tests
│   ├── integration_test.py         # Integration tests
│   └── README.md                   # CSV module docs
│
├── simple-weather-frontend/        # React frontend
│   ├── src/
│   │   ├── App.jsx                 # Main component
│   │   ├── config.js               # AWS configuration
│   │   ├── config.js.example       # Config template
│   │   ├── main.jsx                # Entry point
│   │   ├── index.css               # Styling
│   │   └── utils/                  # Utilities
│   ├── dist/                       # Build output
│   ├── package.json                # npm dependencies
│   ├── vite.config.js              # Vite configuration
│   └── .eslintrc.cjs               # ESLint config
│
├── template.yaml                   # SAM CloudFormation template
├── Makefile                        # Build/deploy automation
├── pytest.ini                      # pytest configuration
├── requirements.txt                # Python dependencies
│
└── Documentation
    ├── README.md                   # Project overview
    ├── CLAUDE.md                   # Claude Code guidance
    ├── LEARNING_GUIDE.md           # Learning material (詳細)
    ├── DEPLOYMENT.md               # Deployment procedures
    ├── IMPLEMENTATION_SUMMARY.md   # Implementation overview
    └── CONTRIBUTING.md             # Contribution guidelines
```

## Naming Conventions

### Python Files (src/, tests/, csv_ingest/)
- ファイル名: `snake_case` (`weather_handler.py`, `auth_service.py`)
- テストファイル: `test_<module_name>.py`
- プロパティテスト: `test_property_<feature>.py`
- クラス名: `PascalCase` (`WeatherService`, `AuthenticationError`)
- 関数・変数: `snake_case` (`get_weather`, `city_id`)
- 定数: `UPPER_SNAKE_CASE` (`WEATHER_TYPES`, `CITY_IDS`)

### React/JavaScript Files (simple-weather-frontend/)
- コンポーネント: `PascalCase` (`App.jsx`)
- ユーティリティ: `camelCase` (`config.js`)
- CSS: `kebab-case` (`index.css`)

### AWS Resources (template.yaml)
- リソース名: `PascalCase` (`WeatherFunction`, `WeatherTable`)
- 説明的なサフィックス: `Function`, `Table`, `Bucket`, `Pool`
- 環境依存: `${Stage}` パラメータ使用

## Import Patterns

### Python (src/)
```python
# Standard library
import json
import os
from datetime import datetime

# Third-party
import boto3
from pydantic import BaseModel

# Local modules
from weather_service import WeatherService
from auth_middleware import require_auth
from database import WeatherDatabase
from exceptions import AuthenticationError, WeatherDataError
from models import WeatherData, City
```

### React (simple-weather-frontend/src/)
```javascript
// React
import React, { useState, useEffect } from 'react';

// AWS Amplify
import { Amplify } from 'aws-amplify';
import { Authenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';

// Local
import { config } from './config';
import './index.css';
```

## Key File Descriptions

| ファイル | 責任 |
|---------|------|
| `src/weather_handler.py` | API ルーティング、リクエスト/レスポンス処理 |
| `src/weather_service.py` | 天気データ生成・取得のビジネスロジック |
| `src/auth_middleware.py` | `@require_auth` デコレータによる認証強制 |
| `src/database.py` | DynamoDB CRUD 操作 |
| `csv_ingest/app.py` | S3 イベントトリガー、CSV パース、DB 書き込み |
| `template.yaml` | 全 AWS リソース定義 (IaC) |
