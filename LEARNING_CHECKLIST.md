# Kiro IDE 学習進捗チェックリスト

このチェックリストを使って、Kiro IDE の学習進捗を確認しましょう。

---

## 学習の進め方

1. 各セクションのチェック項目を順番に確認
2. 理解できたら `[ ]` を `[x]` に変更
3. すべてのチェックが完了したら次のセクションへ

---

## Level 1: 基礎理解（所要時間: 30分）

### 1.1 Kiro IDE の概要
- [ ] Kiro IDE が何かを説明できる
- [ ] Kiroの名前の由来（日本語の「岐路」）を知っている
- [ ] Kiroの3つの主要機能（Steering, Specs, Hooks）を列挙できる

### 1.2 環境セットアップ
- [ ] Kiro IDE をインストールした
- [ ] このプロジェクトを Kiro で開いた
- [ ] `.kiro/` ディレクトリの構造を確認した

---

## Level 2: Steering（所要時間: 30分）

### 2.1 Steering の基本
- [ ] Steering files の役割を説明できる
- [ ] `inclusion: always` の意味を理解している
- [ ] Steering がない場合の問題点を説明できる

### 2.2 本プロジェクトの Steering
- [ ] `.kiro/steering/product.md` の内容を確認した
- [ ] `.kiro/steering/tech.md` の内容を確認した
- [ ] `.kiro/steering/structure.md` の内容を確認した

### 2.3 Steering の実践
- [ ] Kiro に「テストを実行して」と依頼し、正しいコマンドが提案されることを確認した
- [ ] Steering がどのように AI の応答に影響するか理解した

---

## Level 3: Specs（所要時間: 45分）

### 3.1 Spec駆動開発の基本
- [ ] requirements.md の役割を説明できる
- [ ] design.md の役割を説明できる
- [ ] tasks.md の役割を説明できる
- [ ] 「requirements → design → tasks → 実装」のフローを理解している

### 3.2 EARS記法
- [ ] EARS記法が何かを説明できる
- [ ] `WHEN 〜 THEN THE システム SHALL 〜` の形式を理解している
- [ ] requirements.md でEARS記法が使われている箇所を特定した

### 3.3 本プロジェクトの Specs
- [ ] `.kiro/specs/serverless-weather-system/` の3ファイルを確認した
- [ ] `.kiro/specs/csv-data-ingestion/` の3ファイルを確認した
- [ ] 要件 → 設計 → タスク のトレーサビリティを確認した

### 3.4 正確性プロパティ
- [ ] design.md の「正確性プロパティ」セクションを確認した
- [ ] プロパティがどのようにテストに反映されるか理解した

---

## Level 4: Hooks（所要時間: 30分）

### 4.1 Hooks の基本
- [ ] Hooks の役割を説明できる
- [ ] Hook がいつ発火するか理解している
- [ ] Hook ファイルの構造を理解している

### 4.2 本プロジェクトの Hooks
- [ ] `python-lint-format.md` の内容を確認した
- [ ] `test-trigger.md` の内容を確認した
- [ ] `specs-sync-check.md` の内容を確認した
- [ ] `frontend-lint.md` の内容を確認した
- [ ] `readme-update.md` の内容を確認した

### 4.3 Hooks の実践
- [ ] Python ファイルを編集・保存して Hook の発火を確認した
- [ ] Hook によるコード品質チェックの結果を確認した

---

## Level 5: 実践（所要時間: 60分）

### 5.1 新機能の Specs 作成
- [ ] `.kiro/specs/` に新しい機能ディレクトリを作成した
- [ ] requirements.md を作成した
- [ ] design.md を作成した
- [ ] tasks.md を作成した

### 5.2 Kiro を使った実装
- [ ] Kiro に機能実装を依頼した
- [ ] Specs がコンテキストとして使用されることを確認した
- [ ] tasks.md のチェックリストを更新した

### 5.3 新しい Hook の作成
- [ ] `.kiro/hooks/` に新しい Hook ファイルを作成した
- [ ] Trigger パターンを設定した
- [ ] Agent Instructions を記述した
- [ ] Hook が正しく発火することを確認した

---

## Level 6: 応用（所要時間: 任意）

### 6.1 Steering のカスタマイズ
- [ ] プロジェクト固有の情報を Steering に追加した
- [ ] 追加した情報が AI の応答に反映されることを確認した

### 6.2 Specs テンプレートの作成
- [ ] 自分のプロジェクト用の Specs テンプレートを作成した
- [ ] EARS記法を使った要件定義を記述した

### 6.3 チームでの活用
- [ ] Steering / Specs / Hooks を Git で管理する方法を理解した
- [ ] チームメンバーと Kiro 設定を共有する方法を理解した

---

## 進捗サマリー

| Level | 項目数 | 完了 | 進捗 |
|-------|-------|------|-----|
| Level 1: 基礎理解 | 6 | _/6 | _% |
| Level 2: Steering | 7 | _/7 | _% |
| Level 3: Specs | 10 | _/10 | _% |
| Level 4: Hooks | 9 | _/9 | _% |
| Level 5: 実践 | 9 | _/9 | _% |
| Level 6: 応用 | 5 | _/5 | _% |
| **合計** | **46** | _/46 | _% |

---

## 学習完了後のアクション

### 自分のプロジェクトに適用する

1. **Steering を作成**
   ```
   .kiro/steering/
   ├── product.md    # プロダクト概要
   ├── tech.md       # 技術スタック
   └── structure.md  # プロジェクト構造
   ```

2. **Specs を作成**
   ```
   .kiro/specs/<feature>/
   ├── requirements.md
   ├── design.md
   └── tasks.md
   ```

3. **Hooks を作成**
   ```
   .kiro/hooks/
   ├── lint-check.md
   └── test-trigger.md
   ```

### 参考資料

- [KIRO_LEARNING.md](./KIRO_LEARNING.md) - 詳細な学習ガイド
- [KIRO_QUICKSTART.md](./KIRO_QUICKSTART.md) - クイックスタート
- [Kiro 公式ドキュメント](https://kiro.dev/docs/)

---

## フィードバック

学習中に困ったことや改善提案があれば、Issue を作成してください。
