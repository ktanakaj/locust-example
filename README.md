# Locustスクリプトサンプル
[Locust](http://locust.io/)スクリプトのサンプルです。

起動中のサーバーに対してリクエストを投げます。このサンプルでは、[breakout-mk](https://github.com/ktanakaj/breakout-mk)のAPIをターゲットとしています。

## 実行環境
* CentOS 7
* Python 3.6
* Locust 0.9.0

### 開発環境
* Vagrant 2.2.4 - 仮想環境管理
    * Hyper-V (Windows 10 Pro) - 仮想環境

※ [VirtualBox](https://www.virtualbox.org/) + [vagrant-vbguest](https://github.com/dotless-de/vagrant-vbguest)プラグイン等でも動作します。

## インストール方法
リポジトリ内のファイルを任意の場所に配置してください。

サンプルのVM環境は `vagrant up` で構築可能です。

※ 攻撃対象のサーバーは別途準備してください。

## 実行方法
サンプルのVM環境は `/vagrant` 移動後に `./run_local.sh` でLocust起動可能です。  
（例、`./run_local.sh http://172.28.128.3`）

起動後はブラウザで `http://[DHCPで振られたIP]:8089/` 等でWebインタフェースにアクセスしてください。

ログは `/var/log/locust/` に出力されます。

## ソース解説
テストシナリオの本体は `src` ディレクトリ以下に格納されています。  
スクリプトの起点は `locustfile.py` です。ここでスクリプト全体を統括しています。

`common` ディレクトリには、スクリプト全体で使う共通処理などが実装されています。  
それ以外のディレクトリには、主に `TaskSet` の形で個別の画面ごとのテストが実装されています。  

## ライセンス
[MIT](https://github.com/ktanakaj/locust-example/blob/master/LICENSE)
