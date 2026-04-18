---
title: Drafts × Gemini × Linear 連携プロジェクト 開発レポート
date: 2026-04-17 15:10:00 +0900
categories: [タスク管理]
tags: [Drafts,Gemini,Linear]
description: めっちゃ大変だった・・・
---

# Drafts × Gemini × Linear 連携プロジェクト 開発レポート

## 1. プロジェクト概要

iPhone/Macのメモアプリ「Drafts」から送信された雑多なメモを、Google Gemini AIで解析して「RPG風タスク」に構造化し、タスク管理ツール「Linear」へ自動登録するシステムの構築。

## 2. 開発の軌跡（時系列）

- **環境構築:** VSCodeでの開発環境セットアップ。Linear APIキーおよびGoogle Workspace（Google Cloud）のAPIキー取得。
- **インフラ構築:** ngrok の導入により、ローカルのMacを外部（Drafts）からアクセス可能な状態に公開。express（Node.js）によるWebhook受付サーバーの構築。
- **Gemini API 404エラーとの格闘:** 当初 `gemini-1.5-flash` 等の一般的名称でエラーが発生。SDKのデフォルトURL（`v1beta`）とWorkspaceキーの仕様不一致が判明。
- **モデルの特定（ターニングポイント）:** 診断用スクリプトを実行し、現在のAPIキーで使用可能なモデル名 `gemini-3.1-flash-image-preview` を特定。
- **最終実装:** SDKを介さず、axios を用いた直接的なREST APIコールに切り替えることで、URLとモデル名のミスマッチを解消。LinearのチームID自動取得機能を搭載。
- **疎通確認成功:** Draftsからの送信 → Geminiの解析 → Linearへの登録という全工程の自動化を確認。

## 3. 現時点でのシステム構成

```
[Drafts (Webhook)] -> [ngrok (Tunnel)] -> [Node.js (Local Server)] -> [Gemini API (AI)] -> [Linear API (Task)]
```

## 4. 設定ファイル定義 (.env)

プロジェクトのルートディレクトリに配置。

```
LINEAR_API_KEY=lin_api_xxxxxxxxxxxxxxxx
GOOGLE_GENERATIVE_AI_API_KEY=AIzaSyxxxxxxxxxxxxxxxx
PORT=3000
```
