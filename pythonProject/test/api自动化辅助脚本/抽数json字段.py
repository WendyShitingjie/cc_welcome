import json


def getExtract_exdata(response_json, key):
    try:
        json_object = json.loads(response_json)
        if 'data' in json_object:
            return json_object['data'].get(key)
        else:
            return None
    except Exception as e:
        return f'Invalid json string, {str(e)}'


if __name__ == "__main__":
    response_json = '''
        {
        "code": 0,
        "data": {"fileId": "7104914652278912"}
    }
    '''
    key = "fileId"
    result = getExtract_exdata(response_json, key)
    print(result)
