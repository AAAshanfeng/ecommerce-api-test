import requests

base_url = "https://dummyjson.com/products"


def test_get_product():
    """用例1：查询单个商品"""
    response = requests.get(f"{base_url}/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_null_product():
    """用例2：查询不存在商品id"""
    response = requests.get(f"{base_url}/666")
    assert response.status_code == 404


def test_add_product():
    """用例3：新增一个商品"""
    response = requests.post(f"{base_url}/add", json={"title": "我的测试商品"})
    assert response.status_code == 201
    assert response.json()["title"] == "我的测试商品"


def test_update_product():
    """用例4：更新修改商品信息"""
    response = requests.put(f"{base_url}/1", json={"title": "修改后的标题"})
    assert response.status_code == 200
    assert response.json()["title"] == "修改后的标题"


def test_delete_product():
    """用例5：删除一个商品"""
    response = requests.delete(f"{base_url}/1")
    assert response.status_code == 200
    assert response.json()["isDeleted"] == True