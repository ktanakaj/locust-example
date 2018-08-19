#!/bin/bash

#
# @(#)ローカル環境のLocust起動スクリプト
#
# 引数 $1 : ターゲットURL
#
# 実行例）
# ./run_local.sh http://172.28.128.3
#

# 定数
SCRIPT_DIR=$(cd $(dirname $0); pwd)
LOCUSTFILE=${SCRIPT_DIR}/src/locustfile.py
LOG_DIR=/var/log/locust
MASTER_HOST=localhost
MAX_SLAVE=2

# 引数の解析
if [ $# -le 0 ]; then
	echo "引数には ターゲットURL を指定してください"
	exit 64
fi

TARGET_URL=$1

# 生きているプロセスがあれば最初に全てkillする
pkill -f "locust -f ${LOCUSTFILE}"

# マスタープロセス起動
if [ -e ${LOG_DIR}/master.log ]; then
	gzip -f ${LOG_DIR}/master.log
fi
echo "locust -f ${LOCUSTFILE} --master --host=${TARGET_URL} --logfile=${LOG_DIR}/master.log"
nohup locust -f ${LOCUSTFILE} --master --host=${TARGET_URL} --logfile=${LOG_DIR}/master.log > /dev/null 2>&1 &

# スレーブプロセス起動、環境変数で一意な番号を渡す
for i in `seq 1 ${MAX_SLAVE}`
do
	if [ -e ${LOG_DIR}/slave${i}.log ]; then
		gzip -f ${LOG_DIR}/slave${i}.log
	fi
	echo "locust -f ${LOCUSTFILE} --slave --host=${TARGET_URL} --logfile=${LOG_DIR}/slave${i}.log"
	env LOCUST_NO=${i} nohup locust -f ${LOCUSTFILE} --slave --host=${TARGET_URL} --logfile=${LOG_DIR}/slave${i}.log > /dev/null 2>&1 &
done
