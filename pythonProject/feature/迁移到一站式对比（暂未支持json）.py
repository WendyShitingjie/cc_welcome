import requests
import json

file_path = 'uid.txt'


def read_uids_from_file(file_path):
    with open(file_path, 'r') as file:
        uids = [line.strip() for line in file]
        print("测试样本量:", len(uids))
    return uids


# 查询2个特征值
def query_old_feature(old_key, uid):
    url = 'http://moka.dmz.prod.caijj.net/featurehubmgr/featurehub/feature-values'
    token_prod = 'dd08a1fd-f9c2-4926-959a-5445ca067138'
    headers = {
        "Content-Type": "application/json",
        "X-TOKEN": token_prod
    }
    payload = {
        "idType": "UID",
        "featureList": old_key,
        "identifier": uid
    }
    response_old = requests.post(url, headers=headers, data=json.dumps(payload))
    if response_old.status_code == 200:
        return response_old.json()
    else:
        print(f"Error fetching feature for {uid}: {response_old.text} ")
        return None


def query_new_feature(new_key, uid, columnName):
    url = 'http://moka.dmz.prod.caijj.net/featurestoreopr/featurestorejob/feature/test'
    token_prod = 'dd08a1fd-f9c2-4926-959a-5445ca067138'
    # X-TOKEN会过期，需要定时更换
    headers = {
        "Content-Type": "application/json",
        "X-TOKEN": token_prod
    }
    payload = {
        "registerType": "SQL_COMPUTE",
        "groupCode": new_key,
        "logicVersion": 1,
        "paramInfoList": "identifier",
        "inputList": [uid]
    }
    response_new = requests.post(url, headers=headers, data=json.dumps(payload))
    if response_new.status_code == 200:
        data_dict = response_new.json()
        featureValue = next(
            (item['featureValue'] for item in data_dict['data']['featureList'] if item['columnName'] == columnName),
            None)
        return response_new.json(), featureValue
    else:
        print(f"Error fetching feature for {uid}: {response_new.text}")
        return None


def compare_features(uids, old_key, new_key, columnName):
    consistent_count = 0
    inconsistent_count = 0
    for uid in uids:
        result1 = query_old_feature(old_key, uid)
        result2, featureValue = query_new_feature(new_key, uid, columnName)  # 接收featureValue
        if result1 is None or result2 is None:
            print(f"Failed to fetch features for UID {uid}")
        else:
            value1_new = result1['data'][0][old_key]
            value2_new = featureValue  # 获取新特征值
            if value1_new != value2_new:
                inconsistent_count += 1
                print(f"不一致条目: {uid}: {old_key}={value1_new}, {new_key}.{columnName}={value2_new}")
            else:
                consistent_count += 1
                # print(f"same: {uid}")
                # print(f"same: {uid}: {old_key}={value1_new}, {new_key}.{columnName}={value2_new}")
    print(f"\n一致的数量: {consistent_count}")
    print(f"不一致的数量: {inconsistent_count}")


if __name__ == "__main__":
    uids = read_uids_from_file('uid.txt')
    # 执行时注意缩进
    # 注意生产token替换
    # compare_features(uids, 'rt_usr_t_if_meet_app', 'fg.rt.usr.is_install_meet_app','is_installed')
    compare_features(uids, 'rt_usr_ip_typ', 'fg.rt.usr.ip_type', 'ip_typ')
