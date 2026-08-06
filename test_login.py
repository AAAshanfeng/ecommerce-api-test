import requests

login_url = "https://dummyjson.com/auth/login"

def test_login_success():
    """ 用例1：正确账号密码 → 应该登录成功 """
    response = requests.post(login_url, json={"username": "emilys", "password": "emilyspass"})
    assert response.status_code == 200
    assert "accessToken" in response.json()


def test_login_wrong_password():
    """ 用例2：密码错误 → 应该返回400 """
    response = requests.post(login_url, json={"username": "emilys", "password": "1111"})
    assert response.status_code == 400


def test_login_null_username():
    """ 用例3：用户名为空 → 应该返回400 """
    response = requests.post(login_url, json={"username": "", "password": "emilyspass"})
    assert response.status_code == 400


def test_login_null_password():
    """ 用例4：密码为空 → 应该返回400 """
    response = requests.post(login_url, json={"username": "emilys", "password": ""})
    assert response.status_code == 400


def test_login_username_password_dontexist():
    """ 用例5：账号密码都不存在 → 应该返回400 """
    response = requests.post(login_url, json={"username": "aaa", "password": "1111"})
    assert response.status_code == 400


def test_login_password_null():
    """ 用例6：密码字段不存在 → 应该返回400 """
    response = requests.post(login_url, json={"username": "emilys"})
    assert response.status_code == 400