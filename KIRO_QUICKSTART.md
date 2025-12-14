# Kiro IDE クイックスタート

5分でKiro IDEの基本を体験できるガイドです。

---

## 前提条件

- Kiro IDE がインストール済み（[kiro.dev](https://kiro.dev) からダウンロード）
- このプロジェクトがクローン済み

---

## Step 1: プロジェクトを開く（1分）

```bash
# プロジェクトをKiroで開く
cd weather-news-serverless
kiro .
```

または、Kiro IDE の「File > Open Folder」からプロジェクトを選択

---

## Step 2: Steering を確認（1分）

1. サイドバーから `.kiro/steering/` フォルダを展開
2. `tech.md` を開く
3. **確認ポイント**:
   - `inclusion: always` が設定されている
   - Development Commands セクションにコマンドが定義されている

```yaml
---
inclusion: always  ← これでAIに常時提供される
---
```

**試してみる**: Kiroのチャットで「テストを実行して」と入力
→ `python -m pytest tests/ -v` が提案される

---

## Step 3: Specs を確認（1分）

1. `.kiro/specs/serverless-weather-system/` を開く
2. 3つのファイルを確認:

| ファイル | 内容 |
|---------|------|
| `requirements.md` | 何を作るか（要件） |
| `design.md` | どう作るか（設計） |
| `tasks.md` | どう進めるか（タスク） |

**試してみる**: Kiroのチャットで「このプロジェクトの要件を教えて」と入力
→ requirements.md の内容が要約される

---

## Step 4: Hook を体験（2分）

1. `src/weather_service.py` を開く
2. ファイルの最後にコメントを追加:
   ```python
   # test comment
   ```
3. ファイルを保存（Ctrl+S / Cmd+S）
4. **確認ポイント**: `python-lint-format` Hook が発火し、コード品質チェックが実行される

5. 追加したコメントを削除して保存

---

## 完了！

これでKiroの3つの主要機能を体験しました：

| 機能 | 体験した内容 |
|------|------------|
| **Steering** | tech.md からAIがコマンドを把握 |
| **Specs** | 3ファイル構成で仕様を管理 |
| **Hooks** | ファイル保存時に自動チェック |

---

## 次のステップ

### もっと詳しく学ぶ
- **[KIRO_LEARNING.md](./KIRO_LEARNING.md)** - 詳細な学習ガイド（2時間）

### 実践する
- **[LEARNING_CHECKLIST.md](./LEARNING_CHECKLIST.md)** - 学習進捗チェックリスト

### 新機能を追加する
1. `.kiro/specs/` に新しい機能ディレクトリを作成
2. `requirements.md` → `design.md` → `tasks.md` を作成
3. Kiroに「〜を実装して」と依頼

---

## よくある質問

### Q: Steering が反映されない
A: ファイルの先頭に以下があるか確認:
```yaml
---
inclusion: always
---
```

### Q: Hook が発火しない
A: `.kiro/hooks/` 内のファイルの `Trigger > Patterns` を確認

### Q: Specs が認識されない
A: ディレクトリ構造を確認: `.kiro/specs/<feature-name>/`

---

## 参考リンク

- [Kiro 公式ドキュメント](https://kiro.dev/docs/)
- [Steering Files](https://kiro.dev/docs/concepts/steering/)
- [Spec-driven Development](https://kiro.dev/docs/concepts/specs/)
- [Agent Hooks](https://kiro.dev/docs/concepts/hooks/)
