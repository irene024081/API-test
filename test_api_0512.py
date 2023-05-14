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