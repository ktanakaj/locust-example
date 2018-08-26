"""
自分のユーザー画面周りのタスクや処理のモジュール
"""
from locust import TaskSet, task
import common.utils as utils


class MyPage(TaskSet):
    """
    自分のユーザー画面周りのタスクセット。
    """

    @task(10)
    def stages(self):
        self.client.get("/api/users/" + str(self.locust.user["id"]), name="/api/users/:id")
        self.client.get("/api/users/" + str(self.locust.user["id"]) + "/stages", name="/api/users/:id/stages")
        # TODO: 本当は取得したステージに対して StagePage のような画面遷移があるが、現状そこまでは未実装

    @task(10)
    def playlogs(self):
        self.client.get("/api/users/me/playlogs")
        # TODO: プレイログからステージへの遷移もあるが、現状そこまでは未実装

    @task(1)
    def edit(self):
        self.client.get("/api/users/" + str(self.locust.user["id"]), name="/api/users/:id")

        # TODO: 現状は、画面を開いた人は全員編集を実施する動作になっている
        utils.wait(self.locust.config.USER_EDIT_WAIT_MIN, self.locust.config.USER_EDIT_WAIT_MAX)

        # ユーザー名&パスワードを変えるとCSVのユーザーが再利用できなくなるので変えない
        self.client.put("/api/users/" + str(self.locust.user["id"]), name="/api/users/:id", json={
            "name": self.locust.user["name"],
            "password": ""
        })

    @task(10)
    def stop(self):
        self.interrupt()

    def on_start(self):
        if self.locust.user is None:
            self.interrupt()

        self.client.get("/api/users/" + str(self.locust.user["id"]) + "?fields=all", name="/api/users/:id?fields=all")
