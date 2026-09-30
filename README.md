# TSO / Hercules Automation Scripts

Status: **Prototype**

Hercules（z/OSメインフレームエミュレータ）とTK4-（Turnkey MVS）の自動操作スクリプト群。

## Overview

このリポジトリは、Hercules上で動作するMVS/TSO環境への自動ログオンおよび操作を行うスクリプト集です。

主に以下の用途を想定しています：
- TK4- MVSへの自動ログオン
- s3270/wc3270エミュレータ経由の自動操作
- TSOコマンドのバッチ実行

## Contents

| ファイル | 説明 |
|---|---|
| `tso_*.scr` | s3270/wc3270用スクリプト（TSOログオン、操作） |
| `check_user.scr` | ユーザーチェックスクリプト |
| `s3270_*.txt` | セッションログ・ダンプ |
| `start_wc3270.bat` | wc3270起動バッチ |
| `Start-TK4*.ps1/bat` | TK4-起動スクリプト |
| `Stop-TK4*.ps1/bat` | TK4-停止スクリプト |
| `connect*.py` | SSH接続ユーティリティ（サニタイズ済み） |
| `TK4-Guide.txt` | TK4-操作ガイド |

## Requirements

- Hercules（TK4-推奨）
- s3270 または wc3270（3270ターミナルエミュレータ）
- PowerShell / Windows Command Prompt
- Python 3（SSH接続スクリプト用）

## Usage

### TK4-起動
```powershell
.\Start-TK4-Interactive.ps1
```

### TSO自動ログオン
```bash
s3270 -script tso_logon.scr hercules-host:3270
```

## Project Status

- 基本的なTSOログオン・操作スクリプト: 動作確認済み
- エラーハンドリング: 簡易的
- マルチユーザ対応: 未対応

## Known Limitations

- スクリプト内のIPアドレス・ポートは各環境に応じて変更が必要
- 3270エミュレータのバージョン依存あり
- タイムゾーン・ロケール設定の違いにより動作が変わる可能性あり

## License

All rights reserved.
