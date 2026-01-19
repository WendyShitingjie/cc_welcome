import schedule
import time
import requests
import json
import datetime

# 每次手动触发运行后发消息到群
# 记录access_token = "e518d1e41a25cbb95b18ca906cb605ee952b97da908e22f69d62cfea818b479c"
# 定义消息模板
messages = {

"每日提醒"

}


def send_dingtalk_message(access_token, messages):
    webhook_url = f"https://oapi.dingtalk.com/robot/send?access_token={access_token}"  # 请替换为你的钉钉Webhook URL

    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    post_data = {
        "msgtype": "text",
        "text": {
            "content": messages
        }
    }
    response = requests.post(webhook_url, headers=headers, data=json.dumps(post_data))

    if response.status_code == 200:
        print("钉钉消息发送成功")
    else:
        print("钉钉消息发送失败，错误码：", response.status_code)


if __name__ == "__main__":
    access_token = "e518d1e41a25cbb95b18ca906cb605ee952b97da908e22f69d62cfea818b479c"
    send_dingtalk_message(access_token, messages)
