"""
ステージ画面周りのタスクや処理のモジュール
"""
from locust import TaskSet, task
import random
import common.utils as utils


class StagePage(TaskSet):
    """
    ステージ画面のタスクセット。
    """

    @task(2)
    def latest_stages(self):
        response = self.client.get("/api/stages/latest")
        if response.ok:
            self.stages = response.json()

    @task(1)
    def play_rankings(self):
        self.client.get("/api/rankings/play/keys")
        response = self.client.get("/api/rankings/play/?offset=0&limit=50", name="/api/rankings/play/")
        if response.ok:
            self.stages = [r["stage"] for r in response.json()]
        # TODO: 期間を指定してのランキング表示には未対応
        # TODO: ページングの2ページ目以降には未対応

    @task(1)
    def rating_rankings(self):
        response = self.client.get("/api/rankings/rating/?offset=0&limit=50", name="/api/rankings/rating/")
        if response.ok:
            self.stages = [r["stage"] for r in response.json()]
        # TODO: ページングの2ページ目以降には未対応

    @task(1)
    def favorite_rankings(self):
        response = self.client.get("/api/rankings/favorite/?offset=0&limit=50", name="/api/rankings/favorite/")
        if response.ok:
            self.stages = [r["stage"] for r in response.json()]
        # TODO: ページングの2ページ目以降には未対応

    @task(4)
    def stage(self):
        # 選択中のステージからランダムに表示
        if self.stages is None or not self.stages:
            return
        stage = random.choice(self.stages)

        self.client.get("/api/stages/" + str(stage["id"]) + "?fields=all", name="/api/stages/:id?fields=all")
        self.client.get("/api/stages/" + str(stage["id"]) + "/rankings/score/keys", name="/api/stages/:id/rankings/score/keys")
        self.client.get("/api/stages/" + str(stage["id"]) + "/rankings/score/?offset=0&limit=50", name="/api/stages/:id/rankings/score/")
        # TODO: ページングの2ページ目以降には未対応
        # TODO: 期間を指定してのランキング表示には未対応
        # TODO: コメントの投稿や、選択中のステージのプレイ、作者やユーザーの表示は未対応

    @task(1)
    def player_rankings(self):
        self.client.get("/api/rankings/player/keys")
        self.client.get("/api/rankings/player/?offset=0&limit=50", name="/api/rankings/player/")
        # TODO: 期間を指定してのランキング表示には未対応
        # TODO: ページングの2ページ目以降には未対応
        # TODO: 検索したユーザーの表示には未対応

    @task(1)
    def creator_rankings(self):
        self.client.get("/api/rankings/creator/?offset=0&limit=50", name="/api/rankings/creator/")
        # TODO: ページングの2ページ目以降には未対応
        # TODO: 検索したユーザーの表示には未対応

    @task(1)
    def create(self):
        if self.locust.user is None:
            return

        self.client.get("/api/blocks")

        # TODO: 現状は、画面を開いた人は全員編集を実施する動作になっている
        utils.wait(self.locust.config.STAGE_EDIT_WAIT_MIN,
                   self.locust.config.STAGE_EDIT_WAIT_MAX)

        # TODO: 現状、ステージのマップは固定値
        self.client.post("/api/stages", json={
            "name": "teststage_" + utils.random_alphanumeric_string(6),
            "header": {
                "status": random.choice(["public", "private"]),
            },
            "map": "[B][B][B][B][B][B][B][B][B][B][B][B][B][B][B][B][B][B][B][B]\n\n[R][R][R][R][R][R][R][R][R][R][R][R][R][R][R][R][R][R][R][R]\n\n[G][G][G][G][G][G][G][G][G][G][G][G][G][G][G][G][G][G][G][G]\n\n[SILVER][SILVER][SILVER][SILVER][SILVER][SILVER][SILVER][SILVER][SILVER][SILVER][SILVER][SILVER][SILVER][SILVER][SILVER][SILVER][SILVER][SILVER][SILVER][SILVER]\n\n[GOLD][GOLD][GOLD][GOLD][GOLD][GOLD][GOLD][GOLD][GOLD][GOLD][GOLD][GOLD][GOLD][GOLD][GOLD][GOLD][GOLD][GOLD][GOLD][GOLD]",
            "comment": "testcomment_" + utils.random_alphanumeric_string(20),
        })

        self.latest_stages()

    # TODO: ステージの編集には未対応

    @task(2)
    def stop(self):
        self.interrupt()

    def on_start(self):
        self.stages = None
        self.latest_stages()
