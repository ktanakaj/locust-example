"""
Locustスクリプトのエントリーポイント
"""

import random
from locust import HttpLocust, TaskSet
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from common import config, auth
from games import GamePage
from stages import StagePage
from blocks import BlockPage
from users import MyPage


class GuestUserBehavior(TaskSet):
    def create_user(self):
        if auth.create_user(self.locust):
            self.interrupt()

    def login(self):
        if auth.login_by_csv(self.locust):
            self.interrupt()

    tasks = {GamePage: 10, StagePage: 4, create_user: 1, login: 1}


class AuthenticatedUserBehavior(TaskSet):
    def logout(self):
        if auth.logout(self.locust):
            self.interrupt()

    tasks = {GamePage: 10, StagePage: 4, BlockPage: 1, MyPage: 2, logout: 1}


class UserBehavior(TaskSet):
    def stop(self):
        self.interrupt()

    def on_start(self):
        # 認証済と未認証で想定される操作が異なるため、ここで大きく振り分ける。
        # 認証状態が変わった場合は、タスクセットを終了して再実行させる。
        # （認証状態には管理者もあるが、管理者の大量アクセスは想定しないのでテスト省略）
        if auth.check_auth(self.locust):
            self.schedule_task(AuthenticatedUserBehavior, first=True)
        else:
            self.schedule_task(GuestUserBehavior, first=True)

    tasks = {stop: 1}


class UserBehaviorContainer(TaskSet):
    # UserBehaviorの中でinterrupt()を呼ぶための親タスク
    tasks = {UserBehavior: 1}


class AppUser(HttpLocust):
    task_set = UserBehaviorContainer

    def __init__(self, *args, **kwargs):
        super(AppUser, self).__init__(*args, **kwargs)

        # 環境別の設定ファイルを取得
        self.config = config.get(self.host)

        # クライアントにデフォルトの設定を追加、リトライも指定
        self.client.headers['User-Agent'] = self.config.USER_AGENT
        self.client.headers['Accept'] = "application/json, text/html, text/plain"
        retries = Retry(total=self.config.MAX_RETRY,
                        backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        self.client.mount('https://', HTTPAdapter(max_retries=retries))
        self.client.mount('http://', HTTPAdapter(max_retries=retries))

        # ログイン情報をプロパティとして保持
        self.user = None
