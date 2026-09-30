#!/usr/bin/env python3
"""
SSH 接続スクリプト - reality_dashboard 環境へのアクセス
【注意】IPアドレス・パスワードは環境変数または設定ファイルで管理してください
"""

import paramiko
from datetime import datetime


def connect_ssh(host="10.x.x.x", port=22, username="root", password="YOUR_PASSWORD_HERE"):
    """SSH 接続を確立し、環境情報を取得する。"""
    
    print("=" * 60)
    print("SSH 接続：reality_dashboard")
    print(f"ホスト: {host}:{port}")
    print(f"ユーザー名：{username}")
    print(f"時刻：{datetime.now()}")
    print("=" * 60)
    
    # SSH クライアント設定
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # 接続
        print("\n[1/3] SSH 接続中...")
        client.connect(
            hostname=host,
            port=port,
            username=username,
            password=password,
            timeout=10
        )
        print("✓ 接続成功！\n")
        
        # シェルセッション作成
        stdin, stdout, stderr = client.exec_command('echo "環境情報取得中..."')
        output = stdout.read().decode('utf-8').strip()
        error = stderr.read().decode('utf-8').strip()
        
        if error:
            print(f"[警告] エラーメッセージ：{error}")
        
        # 環境情報を表示するコマンド実行
        commands_to_run = [
            "echo '=== システム情報 ==='",
            "uname -a",
            "echo '=== Python バージョン ==='",
            "python3 --version 2>/dev/null || python --version 2>/dev/null || echo 'Python not found'",
            "echo '=== Node.js バージョン ==='",
            "node --version 2>/dev/null || echo 'Node.js not found'",
            "echo '=== Rust バージョン ==='",
            "rustc --version 2>/dev/null || cargo --version 2>/dev/null || echo 'Rust not found'",
            "echo '=== Go バージョン ==='",
            "go version 2>/dev/null || echo 'Go not found'",
            "echo '=== Java バージョン ==='",
            "java -version 2>&1 | head -3",
            "echo '=== Web サーバー ==='",
            "ps aux | grep -E '(nginx|apache|python|node|go|ruby)' | grep -v grep",
            "echo '=== プロセス数 ==='",
            "wc -l < /proc/loadavg 2>/dev/null || uptime",
            "echo '=== ディスク使用量 ==='",
            "df -h 2>/dev/null | head -10",
            "echo '=== Web サーバーポート ==='",
            "netstat -tlnp 2>/dev/null | grep LISTEN || ss -tlnp 2>/dev/null | grep LISTEN",
            "echo '=== プロジェクト構造 ==='",
            "find /var/www/reality_dashboard -type f -name '*.py' -o -name '*.html' -o -name '*.js' -o -name '*.json' 2>/dev/null | head -30",
            "echo '=== Docker コンテナ ==='",
            "docker ps 2>/dev/null || echo 'Docker not found or no containers running'",
        ]
        
        print("\n[2/3] 環境情報を取得中...")
        for cmd in commands_to_run:
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read().decode('utf-8').strip()
            error = stderr.read().decode('utf-8').strip()
            
            if output and 'error' not in output.lower():
                print(f"\n{cmd}")
                print("-" * 40)
                print(output)
                
        # 追加情報：プロジェクトファイル一覧
        print("\n[3/3] プロジェクト詳細...")
        
        # ディレクトリ構造を取得
        stdin, stdout, stderr = client.exec_command("tree -L 2 /var/www/reality_dashboard 2>/dev/null || find /var/www/reality_dashboard -type f | head -50")
        project_structure = stdout.read().decode('utf-8').strip()
        
        if project_structure:
            print(f"\n📁 プロジェクト構造:")
            print("-" * 40)
            for line in project_structure.split('\n')[:30]:
                print(line)
        
        # データベース情報（もしあれば）
        stdin, stdout, stderr = client.exec_command("grep -r 'DATABASE_URL\\|DB_\\|MYSQL\\|POSTGRES' /var/www/reality_dashboard 2>/dev/null | head -10")
        db_info = stdout.read().decode('utf-8').strip()
        
        if db_info:
            print(f"\n🗄️  データベース関連:")
            print("-" * 40)
            for line in db_info.split('\n')[:5]:
                print(line)
        
        # API エンドポイント一覧（もしあれば）
        stdin, stdout, stderr = client.exec_command("grep -rE 'api|endpoint|route' /var/www/reality_dashboard 2>/dev/null | grep -v '.git' | head -10")
        api_info = stdout.read().decode('utf-8').strip()
        
        if api_info:
            print(f"\n🔌 API エンドポイント:")
            print("-" * 40)
            for line in api_info.split('\n')[:5]:
                print(line)
        
        # 環境変数
        stdin, stdout, stderr = client.exec_command("printenv | grep -E '(PORT|HOST|DEBUG|SECRET|KEY)'")
        env_vars = stdout.read().decode('utf-8').strip()
        
        if env_vars:
            print(f"\n⚙️  環境変数:")
            print("-" * 40)
            for line in env_vars.split('\n')[:5]:
                print(line)
        
        # ファイルサイズ確認
        stdin, stdout, stderr = client.exec_command("du -sh /var/www/reality_dashboard/* 2>/dev/null | sort -hr")
        sizes = stdout.read().decode('utf-8').strip()
        
        if sizes:
            print(f"\n📊 ディレクトリサイズ:")
            print("-" * 40)
            for line in sizes.split('\n'):
                print(line)
        
        # ログ情報（最近の）
        stdin, stdout, stderr = client.exec_command("ls -la /var/log/reality_dashboard* 2>/dev/null || ls -la /var/www/reality_dashboard/logs/ 2>/dev/null | tail -10")
        logs = stdout.read().decode('utf-8').strip()
        
        if logs:
            print(f"\n📋 ログファイル:")
            print("-" * 40)
            for line in logs.split('\n'):
                print(line)
        
        # Web サーバーの構成
        stdin, stdout, stderr = client.exec_command("cat /etc/nginx/conf.d/*.conf 2>/dev/null | head -30 || cat /etc/apache2/sites-enabled/*.conf 2>/dev/null | head -30")
        web_config = stdout.read().decode('utf-8').strip()
        
        if web_config:
            print(f"\n🌐 Web サーバー構成:")
            print("-" * 40)
            for line in web_config.split('\n')[:20]:
                print(line)
        
        # シェルを閉じる
        client.close()
        print("\n[完了] SSH セッション終了")
        
    except paramiko.AuthenticationException:
        print("✗ 認証に失敗しました。ユーザー名またはパスワードを確認してください。")
    except paramiko.SSHException as e:
        print(f"✗ SSH エラー：{e}")
    except Exception as e:
        print(f"✗ 接続エラー：{type(e).__name__}: {e}")
    
    return True


if __name__ == "__main__":
    connect_ssh()
