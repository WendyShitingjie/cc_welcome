import schedule
import time
import requests
import json
import datetime


# 每次手动触发运行后发消息到群
# 记录access_token = "e518d1e41a25cbb95b18ca906cb605ee952b97da908e22f69d62cfea818b479c"
# 定义消息模板
messages = {
    0: "每日提醒：周一了，别忘了写计划哦！",
    1: "每日提醒：周二了，别忘了写用例哦！",
    2: "每日提醒：周三了，别忘了买奶茶哦！",
    3: "每日提醒：早上好！周四了，放假倒计时2天！",
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
    # 获取当前是星期几
    weekday = datetime.datetime.now().weekday()
    # 如果是周一、周二或周三，发送对应的提醒消息
    if weekday in messages:
        # 钉钉机器人的access_token，需要替换为你自己的
        access_token = "e518d1e41a25cbb95b18ca906cb605ee952b97da908e22f69d62cfea818b479c"
        send_dingtalk_message(access_token, messages[weekday])
'''
# 安排在每周四的08:00发送钉钉消息
schedule.every().day.at("17:10").do(send_dingtalk_message)

while True:
    schedule.run_pending()
    time.sleep(1)
'''
