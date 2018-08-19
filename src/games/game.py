"""
ゲーム画面周りのタスクや処理のモジュール
"""
from locust import TaskSet, task
import random
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

        # TODO: ハッシュを計算する
        self.client.post("/api/games/end", json={"id": playlog["id"], "score": random.randint(
            0, 10000), "cleared": random.choice([True, False]), "hash": "INVALID_HASH"})

        # 未クリアの場合、30%の確率（適当）で同じステージをリスタート

        # それ以外は60%の確率で別のステージをプレイ
        # self.client.get("/api/stages")

        # 10%の確率でゲーム終了

    def stop(self):
        self.interrupt()

    def on_start(self):
        # 初期情報読み込み
        self.client.get("/api/blocks")
        auth.check_auth(self)

    tasks = {play: 50, stop: 10}
