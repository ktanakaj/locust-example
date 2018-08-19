"""
Locustスクリプトのエントリーポイント
"""

import random
from locust import HttpLocust, TaskSet
from common import config, auth
from games import GamePage


class UserBehavior(TaskSet):
    def reset(self):
        # セッションを消して終了
        if auth.check_auth(self):
            auth.logout(self)
        self.interrupt()

    def stop(self):
        # セッションを保ったまま終了
        self.interrupt()

    def on_start(self):
        # 必ず最初に /api/users/me にアクセスして認証状態を確認する
        if auth.check_auth(self):
            # TODO: 認証中のタスクを実行
            pass
        else:
            # TODO: 未認証のタスクを実行
            pass

        self.client.get("/index.html")

    tasks = {GamePage: 10, stop: 2, reset: 1}


class UserBehaviorContainer(TaskSet):
    # UserBehaviorの中でinterrupt()を呼ぶための親タスク
    tasks = {UserBehavior: 1}


class AppUser(HttpLocust):
    task_set = UserBehaviorContainer

    def __init__(self, *args, **kwargs):
        super(AppUser, self).__init__(*args, **kwargs)
        # 環境別の設定ファイルを取得
        self.config = config.get(self.host)
        # クライアントを独自拡張したものに差し替え。またデフォルトの設定を追加
        self.client.headers['User-Agent'] = self.config.USER_AGENT
        self.client.headers['Accept'] = "application/json, text/html, text/plain"
