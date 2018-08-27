"""
ゲーム画面周りのタスクや処理のモジュール
"""
from locust import TaskSet, task
import random
import hashlib
import common.utils as utils
import common.auth as auth


class GamePage(TaskSet):
    """
    ゲーム画面のタスクセット。
    """

    @task(5)
    def play(self):
        # 取得したステージからランダムに選択してゲームプレイ
        response = self.client.get("/api/stages")
        if not response.ok:
            return

        stages = response.json()
        stage = random.choice(stages)

        self.play_stage(stage["id"])

    @task(3)
    def retry(self):
        # クリアできなかったステージに再挑戦する
        if self.last_stage_id is None:
            return

        self.play_stage(self.last_stage_id)

    def play_stage(self, stage_id):
        # ゲーム開始後、一定時間でゲーム終了
        response = self.client.post("/api/games/start", json={
            "stageId": stage_id
        })
        if not response.ok:
            return

        playlog = response.json()
        utils.wait(self.locust.config.GAME_PLAY_WAIT_MIN,
                   self.locust.config.GAME_PLAY_WAIT_MAX)

        playlog["score"] = random.randint(0, 10000)
        playlog["cleared"] = random.choice([True, False])
        self.client.post("/api/games/end", json={
            "id": playlog["id"],
            "score": playlog["score"],
            "cleared": playlog["cleared"],
            "hash": self.hash(playlog)
        })

        # 未クリアの場合、リスタート用に最後にプレイしたステージを記録
        self.last_stage_id = stage_id if not playlog["cleared"] else None

    def hash(self, playlog):
        h = hashlib.sha1()
        h.update(self.locust.config.GAME_VALIDATION_SECRET.encode())
        h.update(str(playlog["id"]).encode())
        h.update(str(playlog["stageId"]).encode())
        h.update(str(playlog["userId"]).encode()
                 if playlog["userId"] is not None else b"0")
        h.update(str(playlog["score"]).encode())
        h.update(b"true" if playlog["cleared"] else b"false")
        h.update(str(playlog["createdAt"]).encode())
        h.update(str(playlog["updatedAt"]).encode())
        return h.hexdigest()

    @task(1)
    def stop(self):
        self.interrupt()

    def on_start(self):
        # 初期情報読み込み
        self.client.get("/api/blocks")
        auth.check_auth(self)
        # プロパティ初期化
        self.last_stage_id = None
