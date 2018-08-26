"""
ブロック画面周りのタスクや処理のモジュール
"""
import json
from locust import TaskSet, task


class BlockPage(TaskSet):
    """
    ブロック画面のタスクセット。
    """

    @task(1)
    def stop(self):
        self.interrupt()

    def on_start(self):
        # 管理者以外の場合、一覧表示しかできない
        self.client.get("/api/blocks")
