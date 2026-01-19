import requests
import time


def poll_api(instanceId=None, interval=5):
    url = 'http://cdmops.apps01.ali-bj-sit03.shuheo.net/cdmops/pdm/testRun/getResult/v2'
    params = {
        "instanceId": instanceId,
        "projectName": "cdmx_sit"
    }
    while True:
        response = requests.get(url, params=params)
        data = response.json()
        if 'data' in data:
            break
        else:
            interval = int(interval)
            time.sleep(interval)


if __name__ == "__main__":
    instanceId = "7085393992021184"  # 替换为实际的instanceId

    poll_api(instanceId, interval=5)  # 每5秒轮询一次
