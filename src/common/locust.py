"""
LOCUST共通処理モジュール
"""
from locust import HttpLocust
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.util.retry import Retry
import warnings
from . import config, auth

# 開発環境などSSL証明書が自己署名の事もあるので無視
warnings.simplefilter('ignore', InsecureRequestWarning)


class AppLocust(HttpLocust):
    """
    アプリ共通の設定を加えたLocustクラス。
    """
    abstract = True

    def __init__(self, *args, **kwargs):
        super(AppLocust, self).__init__(*args, **kwargs)

        # 環境別の設定ファイルを取得
        self.config = config.get(self.host)

        # クライアントにデフォルトの設定を追加、リトライも指定
        self.client.headers['User-Agent'] = self.config.USER_AGENT
        self.client.headers['Accept'] = "application/json, text/html, text/plain"
        retries = Retry(total=self.config.MAX_RETRY,
                        backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        self.client.mount('https://', HTTPAdapter(max_retries=retries))
        self.client.mount('http://', HTTPAdapter(max_retries=retries))
        self.client.verify = False
