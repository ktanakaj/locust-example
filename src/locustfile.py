"""
Locustスクリプトのエントリーポイント
"""
from locust import TaskSet, TaskSequence, seq_task
from common import config, auth, AppLocust
from games import GamePage
from stages import StagePage
from blocks import BlockPage
from users import MyPage


class GuestUserBehavior(TaskSet):
    """
    ゲストユーザーの振る舞い。
    """

    def create_user(self):
        if auth.create_user(self.locust):
            self.interrupt()

    def login(self):
        if auth.login_by_csv(self.locust):
            self.interrupt()

    tasks = {GamePage: 10, StagePage: 4, create_user: 1, login: 1}


class AuthenticatedUserBehavior(TaskSet):
    """
    ログインユーザーの振る舞い。
    """

    def logout(self):
        if auth.logout(self.locust):
            self.interrupt()

    tasks = {GamePage: 10, StagePage: 4, BlockPage: 1, MyPage: 2, logout: 1}


class UserBehavior(TaskSequence):
    """
    ユーザー全体の振る舞い。
    """
    @seq_task(1)
    def switch(self):
        # 認証済と未認証で想定される操作が異なるため、ここで大きく振り分ける。
        # 認証状態が変わった場合は、タスクセットを終了して再実行させる。
        # （認証状態には管理者もあるが、管理者の大量アクセスは想定しないのでテスト省略）
        if auth.check_auth(self.locust):
            self.schedule_task(AuthenticatedUserBehavior, first=True)
        else:
            self.schedule_task(GuestUserBehavior, first=True)


class AppUser(AppLocust):
    """
    アプリケーションのユーザー。
    """
    task_set = UserBehavior

    def __init__(self, *args, **kwargs):
        super(AppUser, self).__init__(*args, **kwargs)

        # ログイン情報をプロパティとして保持
        self.user = None
