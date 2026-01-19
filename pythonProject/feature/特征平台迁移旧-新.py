import requests
import json

file_path = 'uid.txt'
def read_uids_from_file(file_path):
    with open(file_path, 'r') as file:
        uids = [line.strip() for line in file]
    return uids


# 查询单个特征的函数
def query_feature(feature_key, identifier):
    url = 'http://moka.dmz.prod.caijj.net/featurehubmgr/featurehub/feature-values'
    # X-TOKEN会过期，需要定时更换
    headers = {
        "Content-Type": "application/json",
        "X-TOKEN": "b12b5a39-66cc-4b49-895d-a5d990ffccad"
    }
    payload = {
        "idType": "UID",
        "featureList": feature_key,
        "identifier": identifier
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching feature for {identifier}: {response.text}")
        return None


# 比对两个特征的结果是否一致
def compare_features(uids, feature_key1, feature_key2):
    consistent_count = 0
    inconsistent_count = 0
    for uid in uids:
        result1 = query_feature(feature_key1, uid)
        result2 = query_feature(feature_key2, uid)
        if result1 is None or result2 is None:
            print(f"Failed to fetch features for UID {uid}")
        else:
            # 两种获取key值的写法都可以
            value1_new = result1['data'][0][feature_key1]
            value2_new = result2['data'][0].get(feature_key2, None)
            if value1_new != value2_new:
                inconsistent_count += 1
                print(f"不一致条目: {uid}: {feature_key1}={value1_new}, {feature_key2}={value2_new}")
            else:
                consistent_count += 1
                # print(f"一致条目: {uid}: {feature_key1}={value1_new}, {feature_key2}={value2_new}")
    print(f"\n一致的数量: {consistent_count}")
    print(f"不一致的数量: {inconsistent_count}")


# 主程序
if __name__ == "__main__":
    uids = read_uids_from_file('uid.txt')
    compare_features(uids, 'rt_usr_is_rj_14', 'rt_usr_just_for_test_92')
