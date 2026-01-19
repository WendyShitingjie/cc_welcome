import json
import requests
import pandas as pd


def get_input_uid_by_chunk_size(input_list, chunk_size, num):
    start_index = num * chunk_size
    end_index = start_index + chunk_size
    end_index = min(end_index, len(input_list))
    return input_list[start_index:end_index]


if __name__ == '__main__':
    df = pd.read_csv('input.csv').sort_values(by='uid')
    column_names = df.columns[1:].tolist()
    uid_list = df['uid'].tolist()
    url = 'http://moka.dmz.prod.caijj.net/featurestoreopr/featurestorejob/feature/test'
    groupCode = 'fg.rt.usr.device_rta_model_feature_record'
    logicVersion = '1'
    x_token = '9a0b2067-870d-4800-a86a-47d96f0bb6e3'
    chunk_size = 200
    num_chunks = len(uid_list) // chunk_size + (1 if len(uid_list) % chunk_size != 0 else 0)
    output = {key: [] for key in column_names}
    for i in range(num_chunks):
        now_process_uid_list = get_input_uid_by_chunk_size(uid_list, chunk_size, i)
        headers = {'X-TOKEN': x_token}
        data = {'registerType': 'SQL_COMPUTE', 'groupCode': groupCode, 'logicVersion': logicVersion,
                'paramInfoList': 'identifier', 'inputList': now_process_uid_list}
        rsp = requests.post(url, json=data, headers=headers)
        if rsp.status_code == 200:
            for key in column_names:
                feature_values = []
                sorted_featureList = sorted(
                    [d for d in json.loads(rsp.text)['data']['featureList'] if d.get("columnName") == key],
                    key=lambda x: x["resultKey"])
                for featureValue in sorted_featureList:
                    feature_values.append(featureValue["featureValue"])
                output[key].extend(feature_values)

    for key in column_names:
        col_index = df.columns.get_loc(key)
        comparison = ['same' if str(x) == str(y).replace(r'\N', '') else 'diff' for x, y in
                      zip(output[key], df[key].tolist())]
        df.insert(col_index + 1, f'{key}_featureValue', output[key])
        df.insert(col_index + 2, f'{key}_Comparison', comparison)

    df.to_csv(f'{groupCode.replace(".", "_")}_TestResult.csv', index=False)