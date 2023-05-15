import requests
import json
import pytest
import datetime
import globals as gbl


@pytest.fixture(scope="session")
def session(request):
    base = request.config.getini('base_url')
    username = request.config.getini('username')
    password = request.config.getini('password')
    url = base + "api/login"
    
    s = requests.Session()
   
    payload = json.dumps({
     "username": username, "password": password
    })
    headers = {
    'Content-Type': 'application/json',
    }
    
    response = s.post(url=url,headers=headers, data=payload)    
    return s
    
    
def test_login(request):
    base = request.config.getini('base_url')
    url = base + "api/login"

    username = request.config.getini('username')
    password = request.config.getini('password')
    payload = json.dumps({
     "username": username, "password": password
    })
    
    headers = {
    'Content-Type': 'application/json',
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)
    assert response.status_code == 200
    assert len(response.json().get("login").get('token')) != 0 
    

def test_get_login(session, request):
    base = request.config.getini('base_url')
    url = base + "api/login"
    
    token = session.cookies.get('token')
    
    headers = {
        'Cookie': 'culture=zh-CN; token=' + token
    }
    
    response = requests.request("GET", url, headers=headers)

    assert response.status_code == 200
    assert response.json().get("login").get('token') == token
    #print(datetime.datetime.fromisoformat('2023-05-12T19:48:57Z'))
    #print(datetime.datetime.isoformat((response.json().get("login").get("expiry"))))

def test_enrollment_android(session, request):
    base = request.config.getini('base_url')
    url = base + "zs/enrollment/android"
    token = session.cookies.get('token')
    payload = json.dumps({
    "deviceId": "23948729879842",
    "family": "android",
    "password": request.config.getini('android_group_password'),
    })
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'culture=zh-CN; token=' + token
    } 
    response = requests.request("POST", url, headers=headers, data=payload)
    assert response.status_code == 200
    assert response.json().get("token") != None
    gbl.device_token = response.json().get("token")
    
 
def test_device_rename(session, request):
    base = request.config.getini('base_url')
    url = base + "api/device/" + gbl.device_token + "/rename"
    token = session.cookies.get('token')
    
    payload = json.dumps({
    "name": "test_updated",
    })
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'culture=zh-CN; token=' + token
    }
    response = requests.request("PUT", url, headers=headers, data=payload)

    assert response.status_code == 200

def test_search_device_by_name(session, request):
    base = request.config.getini('base_url')
    group_id = request.config.getini('group_id')
    keyword = "test_updated"
    url = base + "api/device/search?group=" + group_id + "&keyword=" + keyword + "&by=name"
    
    token = session.cookies.get('token')
    headers = {
    'Cookie': 'culture=zh-CN; token=' + token
    }
    response = requests.request("GET", url, headers=headers)
    
    assert response.status_code == 200
    assert keyword in response.json().get("devices")[0].get("name")

def test_delete_device(session,request):
    base = request.config.getini('base_url')
    group_id = request.config.getini('group_id')
    url = base + "api/device?group=" + group_id
    token = session.cookies.get('token')

    payload = json.dumps({
    "devices": {
        gbl.device_token: "test_updated"
    },
    "wipe": "False"
    })
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'culture=zh-CN; token=' + token
    }

    response = requests.request("DELETE", url, headers=headers, data=payload)
    assert response.status_code == 200
    assert "success" in response.json().get('result').get(gbl.device_token)
    

def test_block_single_device(session,request):
    base = request.config.getini('base_url')
    device_token = request.config.getini('device_token')
    url = base + "api/device/" + device_token + "/block"
    token = session.cookies.get('token')
    print(url)
    
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'culture=zh-CN; token=' + token
    }

    response = requests.request("PUT", url, headers=headers)
    assert "null" in response.text
    assert response.status_code == 200
    
    
def test_unblock_single_device(session,request):
    base = request.config.getini('base_url')
    device_token = request.config.getini('device_token')
    url = base + "api/device/" + device_token + "/block"
    token = session.cookies.get('token')
    
    headers = {
    'Cookie': 'culture=zh-CN; token=' + token
    }

    response = requests.request("DELETE", url, headers=headers)
    
    assert response.status_code == 405
    

def test_locate_device(session,request):
    base = request.config.getini('base_url')
    url = base + "api/device/locate" 
    device_token = request.config.getini('device_token')
    
    token = session.cookies.get('token')
    payload = json.dumps({
    "ids": [
     device_token
     ]
    })
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'culture=zh-CN; token=' + token
    }
    response = requests.request("PUT", url, headers=headers, data=payload)
    assert response.status_code == 200
    assert token in response.json().get("token")


def test_move_device(session,request):
    base = request.config.getini('base_url')
    url = base + "api/device/move" 
    device_token = request.config.getini('device_token')
    token = session.cookies.get('token')
    from_group_id = request.config.getini('group_id')
    to_group_id = request.config.getini('group_id2')
    
    payload = json.dumps({
    "ids": [
       device_token
    ],
     "to": to_group_id,
      "from": from_group_id
    })
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'culture=zh-CN; token=' + token
    }

    response = requests.request("PUT", url, headers=headers, data=payload)
    assert response.status_code == 200
    assert "null" in response.text
    

def test_send_message(session,request):
    base = request.config.getini('base_url')
    url = base + "api/device/message" 
    device_token = request.config.getini('device_token')
    token = session.cookies.get('token')
    payload = json.dumps({
    "ids": [
        device_token
      ],
    "param": "hello from api test"
    })
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'culture=zh-CN; token=' + token
    }
    response = requests.request("PUT", url, headers=headers, data=payload)
    assert response.status_code == 200
    assert "null" in response.text

def test_set_block_template(session,request):
    base = request.config.getini('base_url')
    url = base + "api/system/blockTemplate" 
    device_token = request.config.getini('device_token')
    template = request.config.getini('template')

    token = session.cookies.get('token')
    payload = json.dumps({ "setting": template})
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'culture=zh-CN; token=' + token
    }
    response = requests.request("PUT", url, headers=headers, data=payload)
    assert response.status_code == 200
    assert "null" in response.text
    
def test_get_block_template(session,request):
    base = request.config.getini('base_url')
    url = base + "api/system/blockTemplate" 
    device_token = request.config.getini('device_token')
    template = request.config.getini('template')

    token = session.cookies.get('token')
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'culture=zh-CN; token=' + token
    }
    response = requests.request("GET", url, headers=headers)
    assert response.status_code == 200
    assert template in response.text
    
def test_get_locations(session,request):
    base = request.config.getini('base_url')
    device_id = "0206830f-11fc-4060-a95b-064c72281d34"
    from_time = "2022-05-14T17:47:53-04:00"
    to_time = "2023-05-15T17:47:53-04:00"
    token = session.cookies.get('token')
    url = base + "api/data/" + device_id + "/locations?from=" + from_time + "&to=" + to_time + "&max=50"
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'culture=zh-CN; token=' + token
    }
    response = requests.request("GET", url, headers=headers)
    assert response.status_code == 200
    assert "longitude" in response.text


def test_file_upload(session,request):
    base = request.config.getini('base_url')
    url = base + "files/lockTemplate"
    token = session.cookies.get('token')
    image_path = request.config.getini('image_path')


    files= {
        "test": open(image_path, 'rb')
    }
    # body, headers = urllib3.encode_multipart_formdata(payload, files)s
    # headers['Cookie'] = 'culture=zh-CN; token=' + token
    headers = {
        'Cookie': 'culture=zh-CN; token=' + token
    }
    response = requests.post(url, files=files, headers=headers)
    print(response.text)
    assert response.status_code == 200