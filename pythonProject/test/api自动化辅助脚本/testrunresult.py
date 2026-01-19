import requests

# 定义URL和参数
url = 'http://dataops.apps01.ali-bj-sit03.shuheo.net/dataops/etlx/getTestTaskProcess'
params = {
    'taskId': 1283
}

try:
    # 发送GET请求
    response = requests.get(url, params=params, timeout=60)

    # 检查响应状态码
    if response.status_code == 200:
        # 解析JSON响应
        data = response.json()

        # 打印响应中的data字段
        print("Response data:")
        print(data['data']['nodeName'])
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(f"Response content: {response.content}")

except requests.exceptions.RequestException as e:
    # 处理请求异常
    print(f"An error occurred: {e}")
