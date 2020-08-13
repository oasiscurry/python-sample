#!/usr/bin/env python
# * ****************************************************************************
# * Conohaメールサーバの容量を取得するファイル
# *
# * @package   Python\Conoha
# * @author    shingo.yoshioka / https://www.sighon-system.jp
# * @copyright 2020 shingo.yoshioka
# * @license   http://opensource.org/licenses/mit-license.php MIT License
# * ****************************************************************************
from requests.exceptions import *
import datetime
import json
import requests
import sys

# Conohaのパラメータ
AS_URL=''	# Account Service
CS_URL=''	# Compute Service
VS_URL='' # Volume Service
DBS_URL=''	# Database Service
IMGS_URL=''	# Image Service
DS_URL=''	# DNS Service
OSS_URL=''	# Object Storage Service
MS_URL=''	# Mail Service
IS_URL=''	# Identity Service
NS_URL=''	# Network Service
TENANT_ID=''
APP_SERVER_UUID=''
MAIL_SERVER_UUID=''
API_USER=''
API_PASSWORD=''

# Conohaメールサーバの情報出力先
OUTPUT_FILENAME=''

# * *************************************************************************
# * Conohaのトークンを取得
# *
# * @param str user ConohaのAPIユーザー
# *        str password ConohaのAPIユーザーのパスワード
# *        str tenantid ConohaのテナントID
# *        str url ConohaのIdentity Service URL
# *
# * @return string
# * @author shingo.yoshioka / https://www.sighon-system.jp
# * *************************************************************************
def getConohaToken(user, password, tenantid, url):
	request_token = {
		"auth": {
			"passwordCredentials": {
				"username": user,
				"password": password
			},
			"tenantId": tenantid
		}}
	request_header = {'Accept': 'application/json'}
	try:
		request_result = requests.post(url + '/tokens', data = json.dumps(request_token), headers = request_header)
		return (json.loads(request_result.text))['access']['token']['id']
	except (ValueError, NameError, ConnectionError, RequestException, HTTPError) as e:
		print('エラー：Conohaのトークン取得に失敗しました。', e)
		sys.exit()

# * *************************************************************************
# * Conohaメールサーバの使用容量上限値を取得（単位GB）
# *
# * @param str tenantid ConohaのテナントID
# *        str token Conohaのトークン
# *        str uuid ConohaのUUID
# *        str url ConohaのMail Service URL
# *
# * @return number
# * @author shingo.yoshioka / https://www.sighon-system.jp
# * *************************************************************************
def getConohaMailQuota(tenantid, token, uuid, url):
	request_header = {'Accept': 'application/json', 'X-Auth-Token': token}
	try:
		request_result = requests.get(url + '/services/' + uuid + '/quotas', headers = request_header)
		return (json.loads(request_result.text))['quota']['quota']
	except (ValueError, NameError, ConnectionError, RequestException, HTTPError) as e:
		print('エラー：Conohaの使用容量上限値取得に失敗しました。', e)
		sys.exit()

# * *************************************************************************
# * Conohaメールサーバの使用容量合算値を取得（単位GB）
# *
# * @param str tenantid ConohaのテナントID
# *        str token Conohaのトークン
# *        str uuid ConohaのUUID
# *        str url ConohaのMail Service URL
# *
# * @return number
# * @author shingo.yoshioka / https://www.sighon-system.jp
# * *************************************************************************
def getConohaMailUsage(tenantid, token, uuid, url):
	request_header = {'Accept': 'application/json', 'X-Auth-Token': token}
	try:
		request_result = requests.get(url + '/services/' + uuid + '/quotas', headers = request_header)
		return (json.loads(request_result.text))['quota']['total_usage']
	except (ValueError, NameError, ConnectionError, RequestException, HTTPError) as e:
		print('エラー：Conohaの使用容量合算値取得に失敗しました。', e)
		sys.exit()

# * *************************************************************************
# * メイン処理
# *
# * @return void
# * @author shingo.yoshioka / https://www.sighon-system.jp
# * *************************************************************************
def main():
	conoha_token = getConohaToken(API_USER, API_PASSWORD, TENANT_ID, IS_URL)
	conoha_quota = getConohaMailQuota(TENANT_ID,conoha_token,MAIL_SERVER_UUID, MS_URL)
	conoha_usage = getConohaMailUsage(TENANT_ID,conoha_token,MAIL_SERVER_UUID, MS_URL)

	now_date = datetime.datetime.now()
	str_date = now_date.strftime('%Y/%m/%d %H:%M:%S')
	conoha_mail_info = '"' + str_date + '",' + str(conoha_quota) + ',' + str(conoha_usage) + '\n'

	with open(OUTPUT_FILENAME,mode='w') as fp:
		fp.write(conoha_mail_info)

if __name__ == "__main__":
	main()
