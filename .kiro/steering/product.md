---
inclusion: always
---

<!--
╔══════════════════════════════════════════════════════════════════════════════╗
║  📚 KIRO 学習ガイド: product.md                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  このファイルの役割:                                                         ║
║  - プロダクトのビジョンと目的を定義                                          ║
║  - ターゲットユーザーを明確化                                                ║
║  - AIがプロジェクトの「なぜ」を理解するための情報を提供                       ║
║                                                                              ║
║  学習ポイント:                                                               ║
║  1. `inclusion: always` - このファイルはAIに常時提供される                   ║
║  2. Product Name, Purpose, Target Users は必須セクション                     ║
║  3. 日本語と英語を混在させる場合のルールを定義                               ║
║                                                                              ║
║  AIへの効果:                                                                 ║
║  - プロジェクトの目的に沿った提案ができる                                    ║
║  - ターゲットユーザーを意識したコードを生成できる                            ║
║  - 適切な言語（日本語/英語）を選択できる                                     ║
║                                                                              ║
║  詳細: KIRO_LEARNING.md の「3. Steering Files」を参照                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
-->

# Product Overview

## Product Name
Serverless Weather News System (サーバーレス会員制天気ニュースシステム)

## Purpose
AWS サーバーレスアーキテクチャのパターンを実演する PoC（概念実証）アプリケーション。
認証されたユーザーに対して日本5都市の天気情報を提供します。
AWS Kiro IDE およびサーバーレス開発の学習教材として設計されています。

## Target Users

### 1. 学習者 (Learners)
サーバーレスアーキテクチャと AWS サービスを学ぶ開発者
- AWS SAM / CloudFormation による IaC
- Lambda, API Gateway, DynamoDB の統合
- Cognito 認証パターン
- S3 イベントトリガーによるイベント駆動アーキテクチャ

### 2. エンドユーザー (End Users)
認証済みメンバーとして天気情報を閲覧
- 5都市の天気を一覧表示
- 日本語インターフェース

### 3. 管理者 (Administrators)
CSV アップロードによる天気データの一括管理
- S3 バケットへの CSV アップロード
- 自動データ取り込み

## Key Features

1. **Cognito 認証**: JWT トークンによるセキュアなアクセス制御
2. **5都市天気表示**: 札幌、東京、名古屋、大阪、博多
3. **ランダム天気生成**: 晴れ、くもり、雨のデータ自動生成
4. **CSV 一括取り込み**: S3 トリガーによるデータインポート
5. **RESTful API**: ヘルスチェックエンドポイント付き
6. **React フロントエンド**: AWS Amplify UI 統合

## Business Objectives

- AWS サーバーレスベストプラクティスの実演
- Infrastructure as Code のハンズオン学習
- 認証・認可パターンの実装例
- イベント駆動アーキテクチャの理解促進

## Learning Objectives（学習目標）

### Kiro IDE 学習
| スキル | 学習内容 | 関連ファイル |
|--------|---------|-------------|
| Spec駆動開発 | requirements → design → tasks のフロー | `.kiro/specs/` |
| Steering | AI コンテキスト管理 | `.kiro/steering/` |
| Hooks | 自動品質チェック | `.kiro/hooks/` |

### サーバーレス学習
| スキル | 学習内容 | 関連ファイル |
|--------|---------|-------------|
| IaC | SAM/CloudFormation テンプレート作成 | `template.yaml` |
| Lambda | Python関数の実装パターン | `src/weather_handler.py` |
| API設計 | REST API とCORS設定 | `template.yaml` |
| 認証 | Cognito + JWT ミドルウェア | `src/auth_middleware.py` |
| NoSQL | DynamoDB スキーマ設計 | `src/database.py` |
| イベント駆動 | S3 トリガー Lambda | `csv_ingest/app.py` |

### 推奨学習パス
1. `LEARNING_GUIDE.md` で基礎概念を理解
2. `KIRO_LEARNING.md` で Kiro IDE 機能を習得
3. `.kiro/specs/` で仕様駆動開発を実践
4. 新機能を Spec から実装して応用

## Languages

| カテゴリ | 言語 |
|---------|------|
| ドキュメント | 日本語（主）、英語（技術用語） |
| コードコメント | 英語 |
| UI | 日本語 |
| API レスポンス | 日本語（天気名等） |
