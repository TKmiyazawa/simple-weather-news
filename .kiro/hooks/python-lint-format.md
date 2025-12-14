<!--
╔══════════════════════════════════════════════════════════════════════════════╗
║  📚 KIRO 学習ガイド: Hooks の基本パターン                                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  このファイルは Hook の基本構造を学ぶのに最適なサンプルです。                ║
║                                                                              ║
║  Hook ファイルの構造:                                                        ║
║  1. Description - Hook の目的を説明                                          ║
║  2. Trigger - いつ発火するかを定義（Event + Patterns）                       ║
║  3. Agent Instructions - エージェントへの具体的な指示                        ║
║  4. Reference Files - 参照すべきファイルリスト                               ║
║                                                                              ║
║  Trigger パターン:                                                           ║
║  - `src/**/*.py` → src 配下の全 .py ファイル                                 ║
║  - `**/__pycache__/**` → 除外パターン                                        ║
║                                                                              ║
║  学習ポイント:                                                               ║
║  - Patterns は glob 形式で指定                                               ║
║  - Agent Instructions は具体的かつ構造化して記述                             ║
║  - Reference Files で関連ファイルを明示                                      ║
║                                                                              ║
║  詳細: KIRO_LEARNING.md の「5. Hooks（エージェント自動化）」を参照           ║
╚══════════════════════════════════════════════════════════════════════════════╝
-->

# Python Code Quality Check

## Description
Python ファイル保存時に PEP 8 スタイル準拠とコード品質をチェックします。

## Trigger
- **Event**: File saved
- **Patterns**:
  - `src/**/*.py`
  - `tests/**/*.py`
  - `csv_ingest/**/*.py`
- **Exclude**: `**/__pycache__/**`

## Agent Instructions

Python ファイルが保存されました。以下をチェックしてください：

1. **PEP 8 スタイル準拠**
   - インデント（4スペース）
   - 行の長さ（79-99文字推奨）
   - import の順序（標準ライブラリ → サードパーティ → ローカル）
   - 空行の使い方

2. **型ヒント**
   - 関数の引数と戻り値に型ヒントがあるか
   - 複雑な型には `typing` モジュールを使用しているか

3. **エラーハンドリングパターン**
   - 適切な例外クラスを使用しているか (`exceptions.py` 参照)
   - ログ記録が適切か

4. **問題が見つかった場合**
   - 具体的な修正案を提示
   - 該当行番号を明示

## Reference Files
- `.kiro/steering/tech.md` - コード標準
- `src/exceptions.py` - カスタム例外クラス
