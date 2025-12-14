# Kiro IDE 学習ガイド

このドキュメントでは、AWS Kiro IDE の機能を本プロジェクトを通じて段階的に学習する方法を解説します。

---

## 目次

1. [Kiro IDE とは](#1-kiro-ide-とは)
2. [学習ロードマップ](#2-学習ロードマップ)
3. [Steering Files（AIコンテキスト管理）](#3-steering-filesaiコンテキスト管理)
4. [Spec駆動開発](#4-spec駆動開発)
5. [Hooks（エージェント自動化）](#5-hooksエージェント自動化)
6. [ハンズオン演習](#6-ハンズオン演習)
7. [応用編：新機能を Spec から実装](#7-応用編新機能を-spec-から実装)
8. [トラブルシューティング](#8-トラブルシューティング)
9. [参考リンク](#9-参考リンク)

---

## 1. Kiro IDE とは

### 1.1 概要

**Kiro**（きろ）は、AWSが提供するエージェント型AI開発環境です。名前は日本語の「きろ」（岐路・交差点）に由来し、従来の開発とAI駆動開発の交差点を象徴しています。

> **公式サイト**: [https://kiro.dev](https://kiro.dev)

### 1.2 Kiroが解決する課題

| 従来のAIコーディング | Kiroのアプローチ |
|---------------------|-----------------|
| プロンプトの曖昧さ → 意図と異なるコード | **Spec駆動開発** で要件を明文化 |
| コンテキストの欠如 → 毎回説明が必要 | **Steering** でプロジェクト情報を常時提供 |
| 手動チェック → 品質のばらつき | **Hooks** で自動品質チェック |
| 場当たり的な開発 → 保守性の低下 | requirements → design → tasks の構造化フロー |

### 1.3 Kiroの3つの主要機能

| 機能 | 役割 | 本プロジェクトでの使用 |
|------|------|----------------------|
| **Steering** | AIに常時提供するプロジェクトコンテキスト | `.kiro/steering/` |
| **Specs** | 機能仕様を requirements → design → tasks で管理 | `.kiro/specs/` |
| **Hooks** | ファイル変更時に自動実行されるエージェントアクション | `.kiro/hooks/` |

### 1.4 学習前提条件

- [ ] Kiro IDE がインストールされていること（[kiro.dev](https://kiro.dev) からダウンロード）
- [ ] 基本的なGitの操作ができること
- [ ] Python / JavaScript の基礎知識があること

---

## 2. 学習ロードマップ

### 段階的学習パス

```
┌─────────────────────────────────────────────────────────┐
│  STEP 1: Steering を理解する (30分)                      │
│  └─ AIがプロジェクトを理解するための情報を提供する方法    │
├─────────────────────────────────────────────────────────┤
│  STEP 2: Specs を理解する (45分)                         │
│  └─ 要件 → 設計 → タスク の仕様駆動開発フローを学ぶ      │
├─────────────────────────────────────────────────────────┤
│  STEP 3: Hooks を理解する (30分)                         │
│  └─ ファイル保存時の自動アクションを設定する方法          │
├─────────────────────────────────────────────────────────┤
│  STEP 4: 実践 - 新機能をSpec駆動で実装 (60分)            │
│  └─ 学んだ知識を統合して新機能を追加する                  │
└─────────────────────────────────────────────────────────┘
```

### 学習時間の目安

| ステップ | 所要時間 | 難易度 |
|---------|---------|--------|
| STEP 1: Steering | 30分 | ★☆☆ |
| STEP 2: Specs | 45分 | ★★☆ |
| STEP 3: Hooks | 30分 | ★★☆ |
| STEP 4: 実践 | 60分 | ★★★ |

---

## 3. Steering Files（AIコンテキスト管理）

### 3.1 Steeringとは

**Steering files** は、Kiro AI に**常時**提供されるプロジェクトのコンテキスト情報です。
`inclusion: always` を指定することで、すべての対話で自動的に参照されます。

### 3.2 なぜSteeringが重要か

```
【Steeringなし】
ユーザー: "テストを実行して"
AI: "どのテストフレームワークを使っていますか？ディレクトリ構造は？"

【Steeringあり】
ユーザー: "テストを実行して"
AI: "python -m pytest tests/ -v を実行します"  ← tech.md から把握済み
```

### 3.3 本プロジェクトのSteering構成

```
.kiro/steering/
├── product.md    # 製品ビジョン、ターゲットユーザー、学習目標
├── structure.md  # ディレクトリ構造、命名規則、インポートパターン
└── tech.md       # 技術スタック、コマンド、DynamoDBスキーマ
```

### 3.4 各ファイルの役割

#### product.md - プロダクト概要
```markdown
---
inclusion: always  ← 重要！これでAIに常時提供される
---

# Product Overview

## Purpose
AWS サーバーレスアーキテクチャの学習教材

## Target Users
- サーバーレス学習者
- AWS初学者
```

**AIへの効果**: プロジェクトの目的と対象ユーザーを理解し、適切な提案ができる

#### tech.md - 技術スタック
```markdown
---
inclusion: always
---

# Technology Stack

## Development Commands
- テスト: `python -m pytest tests/ -v`
- ローカル開発: `sam local start-api`
```

**AIへの効果**: 正しいコマンドを提案できる、適切なライブラリを使用できる

#### structure.md - プロジェクト構造
```markdown
---
inclusion: always
---

# Project Structure

## Naming Conventions
- Python: snake_case
- React: PascalCase
```

**AIへの効果**: コーディング規約に従ったコードを生成できる

### 3.5 Steering記述のベストプラクティス

| Do ✓ | Don't ✗ |
|------|---------|
| 簡潔に必要最小限の情報 | 長文の説明 |
| テーブルやリストで構造化 | 散文的な記述 |
| 具体的なコード例を含める | 抽象的な説明のみ |
| 定期的に更新する | 古い情報を放置 |

### 3.6 演習: Steeringの効果を確認

1. `.kiro/steering/tech.md` を開く
2. `Development Commands` セクションを確認
3. Kiro に「テストを実行して」と依頼
4. **期待結果**: `python -m pytest tests/ -v` が提案される

---

## 4. Spec駆動開発

### 4.1 Spec駆動開発とは

**Spec駆動開発**（Specification-Driven Development）は、以下の流れで機能を実装するアプローチです：

```
requirements.md    →    design.md    →    tasks.md    →    実装
    (What)              (How)            (Steps)         (Code)
    何を作るか          どう作るか        どう進めるか     コード
```

### 4.2 なぜSpec駆動開発か

| 問題 | Spec駆動開発の解決策 |
|------|---------------------|
| 曖昧な要件 → 手戻り | requirements.md で受け入れ条件を明確化 |
| 設計の属人化 | design.md でアーキテクチャを文書化 |
| 進捗の不透明さ | tasks.md でタスクを可視化 |
| AIへの指示が曖昧 | 3つのファイルがコンテキストを提供 |

### 4.3 Specsの構造

```
.kiro/specs/<feature-name>/
├── requirements.md    # 要件定義（What）- EARS記法推奨
├── design.md          # 設計（How）- アーキテクチャ、データモデル
└── tasks.md           # 実装タスク（Steps）- チェックリスト形式
```

### 4.4 本プロジェクトのSpecs

#### serverless-weather-system（メインシステム）

**requirements.md の構成:**
```markdown
## Introduction
システムの概要説明

## Glossary
用語定義（AIが正確に理解できる）

## Requirements
### Requirement 1
**User Story:** 〜として、〜したい、なぜなら〜
**Acceptance Criteria:**
1. WHEN 〜 THEN THE システム SHALL 〜
```

**design.md の構成:**
```markdown
## アーキテクチャ
全体構成図

## コンポーネントとインターフェース
各コンポーネントの責任範囲

## データモデル
DynamoDBスキーマ定義

## 正確性プロパティ
テストで検証すべき性質
```

**tasks.md の構成:**
```markdown
- [x] 1. 完了したタスク
- [ ] 2. 未完了のタスク
  - サブタスクの説明
  - _要件: 1.1, 1.2_  ← 要件へのトレーサビリティ
```

### 4.5 EARS記法とは

**E**asy **A**pproach to **R**equirements **S**yntax - 要件を明確に記述するための構文

| パターン | 構文 | 例 |
|---------|------|-----|
| Ubiquitous | THE システム SHALL 〜 | THE システム SHALL UTF-8でデータを保存する |
| Event-driven | WHEN 〜 THEN THE システム SHALL 〜 | WHEN ユーザーがログインする THEN THE システム SHALL トークンを発行する |
| State-driven | WHILE 〜 THE システム SHALL 〜 | WHILE オフライン状態 THE システム SHALL キャッシュデータを表示する |

### 4.6 演習: Specsを読んでみる

1. `.kiro/specs/serverless-weather-system/requirements.md` を開く
2. **Requirement 1** のUser StoryとAcceptance Criteriaを確認
3. 対応する `design.md` の「正確性プロパティ」を確認
4. `tasks.md` で実装タスクの進捗を確認

---

## 5. Hooks（エージェント自動化）

### 5.1 Hooksとは

**Hooks** は、特定のイベント（ファイル保存など）が発生したときに自動実行されるエージェントアクションです。

```
ファイル保存 → Hook発火 → エージェントが自動でチェック/アクション実行
```

### 5.2 Hookのユースケース

| Hook | トリガー | アクション |
|------|---------|-----------|
| コード品質 | ソースファイル保存 | リント、フォーマット確認 |
| テスト提案 | ソースファイル変更 | 対応テスト実行を提案 |
| ドキュメント | API変更 | READMEの更新を提案 |
| 仕様同期 | Specs変更 | コードとの整合性確認 |

### 5.3 本プロジェクトのHooks

```
.kiro/hooks/
├── python-lint-format.md   # Python PEP8チェック
├── frontend-lint.md        # ESLint実行
├── test-trigger.md         # テスト実行提案
├── specs-sync-check.md     # Specs-コード同期確認
└── readme-update.md        # README更新提案
```

### 5.4 Hookファイルの構造

```markdown
# Hook タイトル

## Description
このHookの説明

## Trigger
- **Event**: File saved
- **Patterns**: `src/**/*.py`  ← glob パターン
- **Exclude**: `**/__pycache__/**`

## Agent Instructions
エージェントへの具体的な指示

## Reference Files
参照すべきファイルリスト
```

### 5.5 Hookの例: python-lint-format.md

```markdown
# Python Code Quality Check

## Trigger
- **Event**: File saved
- **Patterns**:
  - `src/**/*.py`
  - `tests/**/*.py`

## Agent Instructions

Python ファイルが保存されました。以下をチェックしてください：

1. **PEP 8 スタイル準拠**
   - インデント（4スペース）
   - 行の長さ（79-99文字推奨）

2. **型ヒント**
   - 関数の引数と戻り値に型ヒントがあるか

3. **問題が見つかった場合**
   - 具体的な修正案を提示
```

### 5.6 演習: Hookの動作確認

1. `src/weather_service.py` を開く
2. 任意の場所にコメントを追加（例: `# test`）
3. ファイルを保存
4. **期待結果**: python-lint-format Hook が発火し、コード品質チェックが実行される
5. 変更を元に戻す

---

## 6. ハンズオン演習

### 演習1: Steering の効果を体験（10分）

**目標**: Steeringがなぜ重要かを体験する

1. `.kiro/steering/tech.md` の `Development Commands` セクションを確認
2. Kiroに以下を依頼:
   - 「このプロジェクトのテストを実行するコマンドを教えて」
3. **確認ポイント**: `python -m pytest tests/ -v` が正しく提案されるか

### 演習2: Specs の構造を理解（15分）

**目標**: 仕様駆動開発の3ファイル構成を理解する

1. `.kiro/specs/serverless-weather-system/` ディレクトリを開く
2. 以下の関係を確認:
   - `requirements.md` の Requirement 1 → `design.md` のプロパティ1, 2 → `tasks.md` のタスク5
3. **確認ポイント**: 要件からタスクまでのトレーサビリティがあるか

### 演習3: Hook を追加（20分）

**目標**: 新しいHookを作成する方法を学ぶ

1. `.kiro/hooks/` に `template-validate.md` を作成:
   ```markdown
   # SAM Template Validation

   ## Description
   SAMテンプレート変更時に検証を実行します。

   ## Trigger
   - **Event**: File saved
   - **Patterns**: `template.yaml`

   ## Agent Instructions
   template.yaml が変更されました。以下を確認してください：

   1. `sam validate` コマンドで構文検証
   2. リソース名の命名規則（PascalCase）
   3. 環境変数の設定漏れがないか

   ## Reference Files
   - `.kiro/steering/tech.md` - デプロイコマンド
   ```
2. `template.yaml` を開いて保存
3. **確認ポイント**: 新しいHookが発火するか

---

## 7. 応用編：新機能を Spec から実装

### 7.1 演習: 天気アラート機能を追加（60分）

**シナリオ**: 降水確率が80%以上の場合にアラートを表示する機能を追加

#### Step 1: requirements.md を作成

```bash
mkdir -p .kiro/specs/weather-alerts
```

`.kiro/specs/weather-alerts/requirements.md`:
```markdown
# 天気アラート機能 要件定義

## Introduction
降水確率が高い場合にユーザーに警告を表示する機能

## Glossary
- **Weather_Alert**: 降水確率80%以上の場合に表示される警告
- **Alert_Threshold**: アラート表示の閾値（80%）

## Requirements

### Requirement 1
**User Story:** ユーザーとして、降水確率が高い場合に警告を見たいので、傘の準備ができる

#### Acceptance Criteria
1. WHEN 降水確率が80%以上 THEN THE システム SHALL アラートを表示する
2. WHEN アラートが表示される THEN THE システム SHALL 赤色で目立つように表示する
3. WHEN 降水確率が80%未満 THEN THE システム SHALL アラートを表示しない
```

#### Step 2: design.md を作成

`.kiro/specs/weather-alerts/design.md`:
```markdown
# 天気アラート機能 設計書

## 概要
降水確率が閾値を超えた場合にUIでアラートを表示する

## コンポーネント

### AlertBanner
- **責任範囲**: アラートメッセージの表示
- **配置**: WeatherDisplayコンポーネント内
- **スタイル**: 赤背景、白文字

## 正確性プロパティ

**プロパティ 1: アラート表示条件**
*すべての* 天気データにおいて、降水確率 >= 80 の場合のみアラートが表示される
```

#### Step 3: tasks.md を作成

`.kiro/specs/weather-alerts/tasks.md`:
```markdown
# 天気アラート機能 実装タスク

- [ ] 1. AlertBanner コンポーネント作成
  - React コンポーネントの作成
  - _要件: 1.1, 1.2_

- [ ] 2. App.jsx に組み込み
  - 降水確率のチェックロジック追加
  - _要件: 1.1, 1.3_

- [ ] 3. スタイリング
  - 赤色背景のCSS追加
  - _要件: 1.2_

- [ ] 4. テスト作成
  - プロパティベーステスト追加
  - _プロパティ: 1_
```

#### Step 4: Kiro に実装を依頼

```
天気アラート機能を実装してください。
仕様は .kiro/specs/weather-alerts/ を参照してください。
```

---

## 8. トラブルシューティング

### Hooks が実行されない

| 確認項目 | 対処法 |
|---------|-------|
| triggerパターンが正しいか | glob パターンを確認 (`src/**/*.py`) |
| ファイルパスがマッチするか | Exclude パターンに含まれていないか確認 |
| Kiro IDE が最新か | 最新バージョンに更新 |

### Steering が反映されない

| 確認項目 | 対処法 |
|---------|-------|
| `inclusion: always` があるか | YAML フロントマターを確認 |
| YAML形式が正しいか | `---` で囲まれているか確認 |
| ファイルパスが正しいか | `.kiro/steering/` 直下にあるか |

### Specs が認識されない

| 確認項目 | 対処法 |
|---------|-------|
| ディレクトリ構造 | `.kiro/specs/<feature>/` 形式か |
| ファイル名 | `requirements.md`, `design.md`, `tasks.md` か |

---

## 9. 参考リンク

### 公式ドキュメント
- [Kiro 公式サイト](https://kiro.dev)
- [Kiro ドキュメント](https://kiro.dev/docs/)
- [Kiro GitHub](https://github.com/aws/kiro)

### AWS サーバーレス
- [AWS Serverless](https://aws.amazon.com/serverless/)
- [AWS SAM](https://aws.amazon.com/serverless/sam/)
- [AWS Lambda](https://aws.amazon.com/lambda/)

### 関連記事
- [Spec-driven development with Kiro](https://kiro.dev/docs/concepts/specs/)
- [Agent Hooks](https://kiro.dev/docs/concepts/hooks/)
- [Steering Files](https://kiro.dev/docs/concepts/steering/)

---

## 次のステップ

1. **[KIRO_QUICKSTART.md](./KIRO_QUICKSTART.md)** - 5分で始めるクイックスタート
2. **[LEARNING_CHECKLIST.md](./LEARNING_CHECKLIST.md)** - 学習進捗チェックリスト
3. **[LEARNING_GUIDE.md](./LEARNING_GUIDE.md)** - サーバーレスアーキテクチャの詳細学習
