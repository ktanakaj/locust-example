"""
汎用的なユーティリティのモジュール
"""
import os
import string
import random
import calendar
import gevent
from datetime import datetime


def random_alphanumeric_string(n):
    """
    任意の文字数のランダムな英数文字列を生成する。
    """
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(n)])


def random_numeric_string(n):
    """
    任意の文字数のランダムな数値文字列を生成する。
    """
    return ''.join([random.choice(string.digits) for _ in range(n)])


def unixtime():
    """
    現在日時のUNIXTIMEを取得する。
    """
    return calendar.timegm(datetime.utcnow().utctimetuple())


def weekday_at_local():
    """
    現在のタイムゾーンでの現在日時の曜日を取得する。
    """
    return datetime.now().weekday()


def search_dict(list, key, value):
    """
    dictの配列から指定された値を持つdictを取得する。
    """
    for d in list:
        if key in d and d[key] == value:
            return d
    return None


def wait(min_wait, max_wait=None):
    """
    一定時間処理を待機する。
    """
    # Locust.wait() とは別にウェイトを入れたい場合用
    millis = min_wait
    if max_wait is not None:
        millis = random.randint(min_wait, max_wait)
    seconds = millis / 1000.0
    gevent.sleep(seconds)


def env_no():
    """
    環境変数からこのスレッドの通し番号を取得する。
    ※ Locust起動時にシェルスクリプトなどで環境変数 LOCUST_NO が指定されている必要あり。
    """
    no = os.environ.get("LOCUST_NO")
    if no is None:
        print("Warning: env LOCUST_NO is not found")
        return 1
    return int(no)
