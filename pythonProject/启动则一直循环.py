import schedule
import time
import requests
import json
import datetime

def send_dingtalk_message():
    webhook_url = f"https://oapi.dingtalk.com/robot/send?access_token=e518d1e41a25cbb95b18ca906cb605ee952b97da908e22f69d62cfea818b479c"  # 请替换为你的钉钉Webhook URL

    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    post_data = {
        "msgtype": "text",
        "text": {
            "content": "提醒：今天是周四，别忘了发周报哦！"
        }
    }
    response = requests.post(webhook_url, headers=headers, data=json.dumps(post_data))

    if response.status_code == 200:
        print("钉钉消息发送成功")
    else:
        print("钉钉消息发送失败，错误码：", response.status_code)


# 安排在每周四的08:00发送钉钉消息
schedule.every().day.at("17:38").do(send_dingtalk_message)

while True:
    schedule.run_pending()
    time.sleep(1)

