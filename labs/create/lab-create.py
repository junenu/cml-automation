import requests
import urllib3
import yaml
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# CML2サーバーの情報
CML_URL = "https://"
CML_USERNAME = "admin"
CML_PASSWORD = "C1sco12345"

# テストベッドファイルを読み込む
with open(sys.argv[1], "r") as file:
    testbed = yaml.safe_load(file)

# 認証情報を取得する
response = requests.post(
    f"{CML_URL}/api/v0/authenticate",
    headers={"Content-Type": "application/json"},
    json={"username": CML_USERNAME, "password": CML_PASSWORD},
    verify=False,
)
response.raise_for_status()  # エラーレスポンスがあれば例外を投げる
auth_token = response.text.strip('"')

# ヘッダーに認証情報を含める
headers = {
    "Authorization": f"Bearer {auth_token}",
    "Content-Type": "application/json",
}

# ラボを作成する
response = requests.post(
    f"{CML_URL}/api/v0/labs",
    headers=headers,
    json={"title": "My Test Lab", "description": "This is a test lab"},
    verify=False,
)
response.raise_for_status()  # エラーレスポンスがあれば例外を投げる
lab_id = response.json()["id"]

# x, y 座標を設定する
x_var = 0

# テストベッドに記述された各デバイスを追加する
for device_name, device_info in testbed["devices"].items():
    if device_info["type"] != "router":
        continue
    response = requests.post(
        f"{CML_URL}/api/v0/labs/{lab_id}/nodes",
        headers=headers,
        json={
            "node_definition": device_info["platform"],  # node_definition を platform に基づいて設定
            "label": device_name,
            "x": x_var,  # ノードのx座標
            "y": 0,  # ノードのy座標
        },
        verify=False,
    )
    x_var += 200
    response.raise_for_status()  # エラーレスポンスがあれば例外を投げる
