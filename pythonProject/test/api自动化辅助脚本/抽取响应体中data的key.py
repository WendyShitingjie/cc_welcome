import json


def getExtract_exdata(json_value, key):
    try:
        json_object = json.loads(json_value)
        if 'data' in json_object:
            return json_object['data'].get(key)
        else:
            return None
    except Exception as e:
        return f'Invalid json string, {str(e)}'


def get_file_id(data):
    if 'fileId' in data:
        file_id = data['fileId']
        return file_id
    else:
        return None


if __name__ == "__main__":
    json_value = '''
        {
  "code": 0,
  "data": {
    "fileId": "7104942057885824"
  },
  "fail": false,
  "message": "OK",
  "success": true
}
    '''
    key = "fileId"
    result = getExtract_exdata(json_value, key)
    print(result)

    data= {"fileId":"7104932403736064"}
    value= get_file_id(data)
    print(value)