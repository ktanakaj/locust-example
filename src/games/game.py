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

    def play(self):
        # 取得したステージからランダムに選択してゲーム開始、
        # 一定時間後ゲーム終了
        response = self.client.get("/api/stages")
        if not response.ok:
            return

        stages = response.json()
        stage = random.choice(stages)

        response = self.client.post(
            "/api/games/start", json={"stageId": stage["id"]})
        if not response.ok:
            return

        playlog = response.json()
        utils.wait(self.locust.config.GAME_PLAY_WAIT_MIN,
                   self.locust.config.GAME_PLAY_WAIT_MAX)

        playlog["score"] = random.randint(0, 10000)
        playlog["cleared"] = random.choice([True, False])
        self.client.post("/api/games/end", json={"id": playlog["id"], "score": playlog["score"], "cleared": playlog["cleared"], "hash": self.hash(playlog)})

        # 未クリアの場合、30%の確率（適当）で同じステージをリスタート

        # それ以外は60%の確率で別のステージをプレイ
        # self.client.get("/api/stages")

        # 10%の確率でゲーム終了

    def hash(self, playlog):
        h = hashlib.sha1()
        h.update(self.locust.config.GAME_VALIDATION_SECRET.encode())
        h.update(str(playlog["id"]).encode())
        h.update(str(playlog["stageId"]).encode())
        h.update(str(playlog["userId"]).encode() if playlog["userId"] is not None else b"0")
        h.update(str(playlog["score"]).encode())
        h.update(b"true" if playlog["cleared"] else b"false")
        h.update(str(playlog["createdAt"]).encode())
        h.update(str(playlog["updatedAt"]).encode())
        return h.hexdigest()

    def stop(self):
        self.interrupt()

    def on_start(self):
        # 初期情報読み込み
        self.client.get("/api/blocks")
        auth.check_auth(self)

    tasks = {play: 50, stop: 10}
