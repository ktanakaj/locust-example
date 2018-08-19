"""
各種設定定義モジュール
"""
import os


class DefaultConfig():
    """
    環境別の設定デフォルト。
    """

    def __init__(self, host=None):
        super(DefaultConfig, self).__init__()
        self.API_HOST = host
        self.USER_AGENT = "LocustSample"
        self.RESPONSE_ENCODING = "UTF-8"
        self.SSL_VERIFY = False
        self.MAX_RETRY = 3
        self.MAX_SLAVES = 4
        self.USER_CSV_PATH = os.path.join(
            os.path.dirname(__file__), "../../users.csv")
        self.NEW_USER_RATE = 0.7

    def __getattr__(self, name):
        # 一応普通の定数もここから取れるようにしておく
        return eval(name)


def get(host):
    """
    環境別の設定を取得する。
    """
    for config in []:
        if config.API_HOST == host:
            return config
    return DefaultConfig(host)


# ゲームプレイ時間想定のウェイト
GAME_PLAY_WAIT_MIN = 60000
GAME_PLAY_WAIT_MAX = 600000
