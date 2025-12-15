# サーバーレス会員制天気ニュースシステム

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![React 18](https://img.shields.io/badge/react-18-61DAFB.svg)](https://reactjs.org/)
[![AWS SAM](https://img.shields.io/badge/AWS-SAM-FF9900.svg)](https://aws.amazon.com/serverless/sam/)
[![Kiro IDE](https://img.shields.io/badge/Kiro-IDE-00D4AA.svg)](https://kiro.dev/)

AWS サーバーレスアーキテクチャを使用した認証機能付き天気情報表示システムのPoC（概念実証）です。
日本の5都市（札幌、東京、名古屋、大阪、博多）の天気情報を表示します。

## スクリーンショット

### 天気情報表示画面
ログイン後、5都市の天気情報をカード形式で表示します。

![天気情報表示画面](./docs/images/weather-display.png?v=5)

## このプロジェクトで学べること

このリポジトリは **サーバーレスアーキテクチャの学習教材** として設計されています。

### 学習トピック

| カテゴリ | 学べる技術 |
|---------|-----------|
| **インフラ** | AWS SAM, CloudFormation, Infrastructure as Code |
| **コンピューティング** | AWS Lambda, Python 3.12, イベント駆動アーキテクチャ |
| **API** | API Gateway, REST API設計, CORS設定 |
| **認証** | AWS Cognito, JWT, 認証ミドルウェア |
| **データベース** | DynamoDB, NoSQLデータモデリング, GSI, TTL |
| **フロントエンド** | React 18, Vite, AWS Amplify UI |
| **CDN/ホスティング** | CloudFront, S3静的ホスティング |
| **テスト** | pytest, Vitest, プロパティベーステスト |
| **CI/CD** | Makefile, デプロイ自動化 |

詳細は [KIRO_LEARNING.md](./KIRO_LEARNING.md) を参照してください。

## アーキテクチャ

```
┌─────────────────────────────────────────────────────────────────┐
│                         CloudFront                               │
│                     (CDN / HTTPS終端)                            │
└───────────────┬─────────────────────────────────────────────────┘
                │
        ┌───────┴───────┐
        │               │
        ▼               ▼
┌───────────────┐ ┌─────────────────┐
│  S3 Bucket    │ │  API Gateway    │
│ (静的サイト)   │ │   (REST API)    │
│               │ │                 │
│ React SPA     │ │ /health         │
│               │ │ /weather        │
│               │ │ /weather/*      │
└───────────────┘ └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ AWS Lambda      │
                  │ (Python 3.12)   │◄───── Cognito認証
                  │                 │
                  │ weather_handler │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │   DynamoDB      │
                  │                 │
                  │ WeatherTable    │
                  │ (CityId, ts)    │
                  └─────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     CSV取り込み機能                               │
│                                                                  │
│  S3 (CSV) ──trigger──► Lambda (csv_ingest) ──► DynamoDB         │
└─────────────────────────────────────────────────────────────────┘
```

### 技術スタック

| レイヤー | 技術 |
|---------|------|
| フロントエンド | React 18, Vite, AWS Amplify UI |
| バックエンド | AWS Lambda (Python 3.12), API Gateway |
| データベース | DynamoDB |
| 認証 | AWS Cognito |
| CDN | CloudFront + S3 |
| インフラ | AWS SAM / CloudFormation |
| リージョン | ap-northeast-1 (東京) |

## クイックスタート

### 前提条件

- Python 3.12
- Node.js 18+
- AWS CLI (設定済み)
- AWS SAM CLI

### 1. リポジトリをクローン

```bash
git clone https://github.com/YOUR_USERNAME/simple-weather-news.git
cd simple-weather-news
```

### 2. 依存関係インストール

```bash
make install
```

### 3. AWSにデプロイ

```bash
# 開発環境
make deploy STAGE=dev REGION=ap-northeast-1

# または本番環境
make prod-deploy
```

### 4. フロントエンド設定

デプロイ完了後、SAMスタックの出力値を確認:

```bash
make outputs
```

出力値を使って設定ファイルを作成:

```bash
cd simple-weather-frontend/src
cp config.js.example config.js
# config.js を編集して実際の値を設定
```

### 5. フロントエンドをビルド・デプロイ

```bash
cd simple-weather-frontend
npm run build
# S3にアップロード（Makefileのdeployターゲットを使用）
```

## 🎓 Kiro IDE 学習教材

このプロジェクトは **[AWS Kiro IDE](https://kiro.dev/) の学習教材**として最適化されています。
Kiro IDE のSpec駆動開発、Steering、Hooksの実践的な使い方を学べます。

### Kiro 設定ファイル構成

```
.kiro/
├── specs/                          # 📋 機能仕様（Spec駆動開発）
│   ├── serverless-weather-system/  # メインシステム仕様
│   │   ├── requirements.md         #   要件定義
│   │   ├── design.md               #   設計ドキュメント
│   │   └── tasks.md                #   実装タスク
│   └── csv-data-ingestion/         # CSV取り込み機能仕様
│       ├── requirements.md
│       ├── design.md
│       └── tasks.md
│
├── steering/                       # 🧭 AIガイダンス（常時読み込み）
│   ├── product.md                  #   製品ビジョン・目標
│   ├── structure.md                #   プロジェクト構造・命名規則
│   └── tech.md                     #   技術スタック・コマンド
│
└── hooks/                          # ⚡ 自動化トリガー
    ├── python-lint-format.md       #   Python保存時: PEP8チェック
    ├── frontend-lint.md            #   JSX/JS保存時: ESLint
    ├── test-trigger.md             #   ソース変更時: テスト提案
    ├── specs-sync-check.md         #   Specs変更時: コード同期確認
    └── readme-update.md            #   コア変更時: README更新提案
```

### Kiro IDE での学習ステップ

| ステップ | 操作 | 学べること |
|---------|------|-----------|
| 1 | プロジェクトを開く | Steering filesの自動読み込み |
| 2 | `.kiro/specs/` を確認 | Spec駆動開発のドキュメント構造 |
| 3 | Pythonファイルを編集・保存 | Hooksによる自動品質チェック |
| 4 | 新機能をSpecから実装 | 要件→設計→タスクのフロー |

### Kiro IDE の主要機能を体験

1. **Spec駆動開発**: `specs/serverless-weather-system/` の requirements → design → tasks の流れを確認
2. **Steering**: `steering/tech.md` でコマンド一覧、コード規約を AI に自動提供
3. **Hooks**: `src/*.py` を保存して自動 lint チェックを体験

詳細は [Kiro documentation](https://kiro.dev/docs/) を参照してください。

## プロジェクト構造

```
├── .kiro/                        # Kiro IDE設定
│   ├── specs/                   # 機能仕様
│   ├── steering/                # AIガイダンス
│   └── hooks/                   # 自動化フック
├── src/                          # Lambda関数ソースコード
│   ├── weather_handler.py       # メインハンドラー（APIルーティング）
│   ├── weather_service.py       # 天気データのビジネスロジック
│   ├── auth_service.py          # Cognito認証サービス
│   ├── auth_middleware.py       # @require_auth デコレータ
│   ├── database.py              # DynamoDB操作
│   ├── models.py                # データモデル
│   └── exceptions.py            # カスタム例外クラス
├── tests/                        # テストスイート
│   ├── test_weather_handler.py  # ハンドラーテスト
│   ├── test_auth_service.py     # 認証テスト
│   ├── test_property_*.py       # プロパティベーステスト
│   └── conftest.py              # pytest設定
├── csv_ingest/                   # CSV取り込みLambda
│   ├── app.py                   # S3トリガーLambda
│   ├── test_app.py              # ユニットテスト
│   └── integration_test.py      # 統合テスト
├── simple-weather-frontend/      # Reactフロントエンド
│   ├── src/
│   │   ├── config.js.example    # 設定テンプレート
│   │   ├── App.jsx              # メインコンポーネント
│   │   └── components/          # UIコンポーネント
│   └── dist/                    # ビルド成果物
├── template.yaml                 # SAMテンプレート（全インフラ定義）
├── Makefile                      # ビルド・デプロイタスク
├── pytest.ini                    # pytest設定
├── requirements.txt              # Python依存関係
├── LEARNING_CHECKLIST.md        # 学習進捗チェックリスト
├── KIRO_LEARNING.md             # Kiro IDE 学習ガイド
└── KIRO_QUICKSTART.md           # 5分クイックスタート
```

## ローカル開発

```bash
# バックエンドAPI（SAM Local）
sam local start-api --port 3001

# フロントエンド開発サーバー
cd simple-weather-frontend && npm run dev
```

## テスト実行

```bash
# 全テスト
make test

# バックエンドのみ
python -m pytest tests/ -v

# フロントエンドのみ
cd simple-weather-frontend && npm test -- --run

# マーカー指定（unit, integration, property）
python -m pytest tests/ -v -m unit

# カバレッジ付き
python -m pytest tests/ -v --cov=src --cov-report=html
```

## API エンドポイント

| メソッド | パス | 認証 | 説明 |
|---------|------|------|------|
| GET | `/health` | 不要 | ヘルスチェック |
| GET | `/weather` | 必要 | 5都市の天気データ取得 |
| POST | `/weather/generate` | 必要 | ランダム天気データ生成 |
| GET | `/weather/forecast` | 必要 | 天気予報取得 |
| GET | `/weather/statistics` | 必要 | 統計情報取得 |
| GET | `/weather/types` | 不要 | 天気タイプ一覧取得 |

## DynamoDB スキーマ

```
WeatherTable
├── パーティションキー: CityId (Number)
├── ソートキー: timestamp (String)
├── GSI: timestamp-index
└── TTL: ttl属性

都市コード:
├── 1  = 札幌
├── 13 = 東京
├── 23 = 名古屋
├── 27 = 大阪
└── 40 = 博多
```

## CSV取り込み機能

S3バケットにCSVファイルをアップロードすると、自動的にDynamoDBに取り込まれます。

```csv
# フォーマット（ヘッダーなし）
CityId,CityName,WeatherId,WeatherName,RainfallProbability

# 例
1,札幌,1,晴れ,10
13,東京,2,くもり,30
23,名古屋,3,雨,80
```

## デプロイコマンド一覧

```bash
make install      # 依存関係インストール
make validate     # SAMテンプレート検証
make deploy       # 開発環境デプロイ
make prod-deploy  # 本番環境デプロイ
make status       # デプロイ状態確認
make outputs      # スタック出力値確認
make logs         # Lambdaログ確認
make clean        # ビルドキャッシュ削除
make test         # テスト実行
```

## ドキュメント

| ドキュメント | 内容 |
|-------------|------|
| [LEARNING_CHECKLIST.md](./LEARNING_CHECKLIST.md) | 学習進捗チェックリスト |
| [KIRO_LEARNING.md](./KIRO_LEARNING.md) | Kiro IDE 学習ガイド（ハンズオン演習付き） |
| [KIRO_QUICKSTART.md](./KIRO_QUICKSTART.md) | 5分クイックスタート |

## ライセンス

[MIT License](./LICENSE)

## 謝辞

このプロジェクトはサーバーレスアーキテクチャの学習を目的として作成されました。
AWSのベストプラクティスに基づいて設計されていますが、本番環境での使用前に
セキュリティレビューを行うことを推奨します。
