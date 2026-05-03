---
title: "スキルを「育てる」仕組みをGitHubで作った"
date: 2026-05-03 11:15:00 +0900
categories: [ADS受講メモ, アイデア設計]
tags: [ADS, Cursor, GitHub, Claude, 学習記録, 個人利用]
---

Claudeには「スキル」と呼ばれる、自分専用の動作指示ファイル（SKILL.md）を登録できる仕組みがあります。

自分でいくつか作ってみたものの、ある問題に気づきました。

**「どのバージョンがどう動くか、まったく記録していない」**

スキルをブラッシュアップするたびに、前の状態に戻せない。何を変えたか思い出せない。そんな状態でした。

今回はそれを解決するために、GitHubを使ったスキル管理の仕組みを整えました。

---

## 構成

リポジトリ名は `claude-skills`（Private）。構成はシンプルです。

```
claude-skills/
├── README.md
├── daily-task-routine/
│   ├── SKILL.md
│   └── CHANGELOG.md
├── trio-ohom-article-writer/
│   ├── SKILL.md
│   └── CHANGELOG.md
└── self-inquiry-deepener/
    ├── SKILL.md
    └── CHANGELOG.md
```

各スキルに `SKILL.md`（本体）と `CHANGELOG.md`（変更履歴）を置くだけ。シンプルですが、「いつでも戻れる安全網」としては十分です。

---

## スキル更新ワークフロー

更新のたびに以下の流れで動かします。

```
① Claudeで改善内容を対話しながら詰める
        ↓
② ClaudeがSKILL.mdを出力（ダウンロード）
        ↓
③ VS Codeで既存ファイルとdiff（差分）確認
        ↓
④ VS CodeのAIでさらにブラッシュアップ（任意）
        ↓
⑤ 「SKILL.mdの差分からCHANGELOG.mdのエントリを生成して」
        ↓
⑥ Git commit & push
        ↓
⑦ Claude設定画面でSKILL.mdをアップロード
```

> 「考える」はClaude、「編集・管理」はVS Code。この分担が決まってから、作業がスムーズになりました。
{: .prompt-tip }

---

## ハマったこと

Claude設定画面からアップロードしたSKILL.mdをGitHubに置いたところ、**バイナリ扱いになってテキストとして表示されない**問題が発生しました。

原因は、アップロード時の形式がClaudeの内部フォーマットで保存されていたためです。

解決策は単純で、**Claudeに `/mnt/skills/user/` の中身を読み込んでテキストファイルとして出力してもらい、それをGitHubに上書き**するだけでした。

> 設定画面からアップロードしたファイルをそのままGitHubに置いても、テキストとして扱われないことがあります。Claudeに出力してもらったファイルを使うのが確実です。
{: .prompt-warning }

---

## まとめ

| やったこと | ツール |
|-----------|--------|
| リポジトリ・CHANGELOG作成 | GitHub |
| SKILL.mdのテキスト出力 | Claude |
| clone・diff確認・commit | VS Code |

スキルが増えるほど、この仕組みが活きてきます。「ちゃんと育てられるスキル」になった感覚がありました。

💡 **OHOポイント:** Claudeのスキルは「登録して終わり」ではなく、バージョン管理することで初めて「育てられる資産」になります。
