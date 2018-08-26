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
        self.USER_AGENT = "LocustSample"
        self.MAX_RETRY = 3
        self.MAX_SLAVES = 4
        self.USER_CSV_PATH = os.path.join(
            os.path.dirname(__file__), "../../users.csv")

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

# ステージ情報編集想定のウェイト
STAGE_EDIT_WAIT_MIN = 60000
STAGE_EDIT_WAIT_MAX = 600000

# ユーザー情報編集想定のウェイト
USER_EDIT_WAIT_MIN = 30000
USER_EDIT_WAIT_MAX = 60000

# ゲームPlaylogバリデーション用の秘密鍵
GAME_VALIDATION_SECRET = "yt7u9rtv095wo6w9;hit6yw9"
