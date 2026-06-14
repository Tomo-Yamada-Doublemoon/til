# TIL Post Editor（別リポジトリ）

投稿ツールは **`til-post-editor`** として独立管理しています。

## セットアップ

```bash
git clone https://github.com/Tomo-Yamada-Doublemoon/til-post-editor.git
cd til-post-editor
npm install

# この til repo を対象に指定
bash scripts/setup-repo.sh /Users/tomoyamada/Developer/til

# 起動
bash start.sh
```

UI: http://127.0.0.1:5173

SSH で clone する場合:

```bash
git clone git@github.com:Tomo-Yamada-Doublemoon/til-post-editor.git
```

## ローカル開発用

ワークスペースの正本: `~/Developer/til-post-editor`

詳細は [til-post-editor README](https://github.com/Tomo-Yamada-Doublemoon/til-post-editor) を参照してください。
