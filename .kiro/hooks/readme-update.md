<!--
╔══════════════════════════════════════════════════════════════════════════════╗
║  📚 KIRO 学習ガイド: ドキュメント同期 Hook                                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  このHookはコードとドキュメントの同期を保つためのパターンです。              ║
║  コアファイル変更時に関連ドキュメントの更新を提案します。                    ║
║                                                                              ║
║  学習ポイント:                                                               ║
║  1. 特定ファイル（weather_handler.py, template.yaml 等）のみを対象           ║
║  2. 変更ファイル別のチェック項目マッピング                                   ║
║  3. 複数ドキュメントへの影響分析                                             ║
║  4. 更新提案のフォーマット定義                                               ║
║                                                                              ║
║  ドキュメント as Code:                                                       ║
║  - コード変更 → ドキュメント更新 の連携を自動化                              ║
║  - 「ドキュメントが古い」問題を防止                                          ║
║                                                                              ║
║  詳細: KIRO_LEARNING.md の「5. Hooks（エージェント自動化）」を参照           ║
╚══════════════════════════════════════════════════════════════════════════════╝
-->

# README Synchronization Reminder

## Description
コアファイル変更時に README.md の更新が必要かチェックします。

## Trigger
- **Event**: File saved
- **Patterns**:
  - `src/weather_handler.py`
  - `template.yaml`
  - `Makefile`

## Agent Instructions

コアプロジェクトファイルが変更されました。ドキュメントの更新が必要かチェックしてください：

### 1. 変更ファイル別チェック項目

**weather_handler.py が変更された場合**:
- API エンドポイントの追加/削除/変更があるか
- README.md の「API Endpoints」セクション更新が必要か
- CLAUDE.md の「API Endpoints」セクション更新が必要か

**template.yaml が変更された場合**:
- 新しい AWS リソースが追加されたか
- README.md の「Architecture」図の更新が必要か
- DEPLOYMENT.md の手順更新が必要か
- 環境変数や出力値が変更されたか

**Makefile が変更された場合**:
- 新しいコマンドが追加されたか
- README.md の「Common Commands」セクション更新が必要か
- CLAUDE.md の「Common Commands」セクション更新が必要か

### 2. 更新が必要な場合

以下のドキュメントを確認・更新してください：

| ドキュメント | 更新セクション |
|-------------|---------------|
| `README.md` | Architecture, API Endpoints, Deploy Commands |
| `CLAUDE.md` | API Endpoints, Common Commands |
| `LEARNING_GUIDE.md` | 学習コンテンツへの影響 |
| `DEPLOYMENT.md` | デプロイ手順の変更 |

### 3. 更新提案フォーマット

```markdown
## 推奨更新

### README.md
- セクション: [セクション名]
- 変更内容: [具体的な変更]
- 理由: [変更が必要な理由]

### CLAUDE.md
- セクション: [セクション名]
- 変更内容: [具体的な変更]
```

## Reference Files
- `README.md` - メインドキュメント
- `CLAUDE.md` - Claude Code ガイダンス
- `LEARNING_GUIDE.md` - 学習ガイド
- `DEPLOYMENT.md` - デプロイ手順
