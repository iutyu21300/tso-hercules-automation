#!/usr/bin/env python3
"""SSH 接続スクリプト - reality_dashboard の環境に SSH 接続"""

import paramiko
from datetime import datetime


def connect_ssh(host: str = "10.x.x.x", username: str = "root", password: str = "YOUR_PASSWORD_HERE") -> None:
    """SSH 接続を実行する関数"""

    print("=" * 60)
    print(f"SSH 接続先：{host}")
    print(f"ユーザー名：{username}")
    print(f"時刻：{datetime.now()}")
    print("=" * 60)

    try:
        # SSH クライアントの作成
        transport = paramiko.Transport((host, 22))
        transport.connect(username=username, password=password)

        # SSH コネクションの作成
        sftp_client = None
        stdin, stdout, stderr = transport.open_session()
        channel = stdout.channel
        print(f"\n[SUCCESS] SSH 接続に成功しました!")
        print(f"ホスト：{host}")
        print(f"ユーザー：{username}")

        # サーバー情報の取得
        remote_version = stdout.read().decode("utf-8").strip()
        if remote_version:
            print(f"サーバーバージョン情報:\n{remote_version}")

        # ディレクトリ構造の確認
        print("\n--- 現在のディレクトリ ---")
        files_list = channel.execute("ls -la")
        for line in files_list.splitlines():
            print(line)

        print("\n--- SSH 接続完了 ---")

    except paramiko.AuthenticationException:
        print("[ERROR] 認証に失敗しました。ユーザー名またはパスワードを確認してください。")
    except Exception as e:
        print(f"[ERROR] 接続中にエラーが発生しました：{e}")


if __name__ == "__main__":
    connect_ssh()
