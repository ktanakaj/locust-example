"""
ブロックくずしメーカー認証処理モジュール
"""
import threading
import os
import random
import csv
from . import utils


def check_auth(l):
    """
    認証状態を確認する
    """
    l.user = None
    with l.client.get("/api/users/me", catch_response=True) as response:
        if response.ok:
            response.success()
            l.user = response.json()
            return True
        if response.status_code == 401:
            response.success()
            return False
        response.failure(response.text)
        return False


def create_user(l):
    """
    ユーザーを作成する。
    """
    l.user = None
    name = "testuser_" + utils.random_alphanumeric_string(6)
    response = l.client.post(
        "/api/users", json={"name": name, "password": "testpassword"})
    if response.ok:
        l.user = response.json()
        return True
    return False


def login_by_csv(l):
    """
    CSVのユーザーでログインする。
    """
    l.user = None
    user_csv_loader = UserCsvLoader(l.config)
    user = user_csv_loader.next()
    if user is None:
        return False

    response = l.client.post(
        "/api/authenticate", json={"name": user['name'], "password": user['password']})
    if response.ok:
        l.user = response.json()
        return True
    return False


def logout(l):
    """
    ログアウトする
    """
    response = l.client.post("/api/authenticate/logout")
    if response.ok:
        l.user = None
        return True
    return False


class UserCsvLoader:
    """
    ユーザー定義CSVファイルのローダー。
    ユーザー名,パスワード形式のCSVファイルから、
    複数のスレーブプロセス間で一意になるようにユーザーを読み込む。
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, config):
        # 一意に読み込むためシングルトンにする
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.init(config)

        return cls._instance

    def __del__(self):
        self.finish()

    def init(self, config):
        # コンストラクタ。__init__ にするとシングルトンのつもりでも呼ばれてしまうので別名で定義
        self._lock = threading.Lock()
        self.max_no = config.MAX_SLAVES
        self.no = utils.env_no()
        self.csvfile = None
        self.csvreader = None

        if config.USER_CSV_PATH is None:
            return

        self.csvpath = config.USER_CSV_PATH
        if not os.path.isfile(self.csvpath):
            print("Warning: " + self.csvpath + " is not found")
            return

        self.csvfile = open(self.csvpath, "r", newline='')
        self.csvreader = csv.DictReader(
            self.csvfile, delimiter=",", fieldnames=["name", "password"])

        # 他のスレッドと被らないようにnoだけ開始位置をずらす
        self.skip(self.no - 1)
        print(self.csvpath + " is opened")

    def finish(self):
        self.csvreader = None
        if self.csvfile is not None and not self.csvfile.closed:
            self.csvfile.close()
            print(self.csvpath + " is closed")
        self.csvfile = None

    def next(self):
        """
        次のユーザーを取得する。
        ※ 存在しない場合は None
        """
        with self._lock:
            if self.csvreader is None:
                return None
            try:
                user = next(self.csvreader)
            except StopIteration:
                self.finish()
                return None

            # 他のスレッドと被らないようにスレッド数分後ろに移動
            self.skip(self.max_no - 1)
            return user

    def skip(self, count):
        """
        指定回数だけユーザーをスキップする。
        """
        if self.csvreader is not None:
            for _ in range(0, count):
                try:
                    next(self.csvreader)
                except StopIteration:
                    self.finish()
                    break
