import requests

base_url = "https://dummyjson.com/carts"


def test_get_all_carts():
    """用例1 查询全部购物车 → 成功 200"""
    response = requests.get(base_url)
    assert response.status_code == 200


def test_get_single_carts():
    """用例2 查询单个购物车 → 成功200"""
    response = requests.get(f"{base_url}/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_add_cart():
    """用例3 新增一个购物车 → 成功201"""
    response = requests.post(
        f"{base_url}/add",
        json={
            "userId": 1,
            "products": [
                {
                    "id": 1,
                    "quantity": 4,
                }
            ]
        })
    assert response.status_code == 201
    assert response.json()["products"][0]["id"] == 1
    assert response.json()["products"][0]["quantity"] == 4


def test_add_cart_with_nonexistent_product():
    """用例4 购物车中添加不存在的商品ID

    观察结果：接口返回201（成功），但products列表为空、所有统计字段为0

    潜在问题：状态码表示"创建成功"，但实际未创建任何有效数据，
    存在语义不一致的风险，建议后续与开发确认此行为是否符合预期设计
    """
    response = requests.post(
        f"{base_url}/add",
        json={
            "userId": 1,
            "products": [
                {
                    "id": 99999,
                    "quantity": 4,
                }
            ]
        })
    assert response.status_code == 201
    assert response.json()["products"] == []


def test_add_cart_with_zero_quantity():
    """用例5 购物车中商品数量传0

    观察结果：接口返回201，但quantity被静默修改为1，而不是保留0或返回错误提示

    潜在问题：输入校验缺失，用户传入的无效值被接口
    "自作主张"修改，且没有任何提示，可能造成数据与用户预期不符
    """
    response = requests.post(
        f"{base_url}/add",
        json={
            "userId": 1,
            "products": [
                {
                    "id": 1,
                    "quantity": 0,
                }
            ]
        })
    assert response.status_code == 201
    # 记录实际观察到的异常行为（不代表这是"正确"的，只是记录现状）
    assert response.json()["products"][0]["quantity"] == 1


def test_add_cart_with_negative_quantity():
    """用例6 购物车中商品数量传负数（边界值测试）

    观察结果：接口返回201，quantity和total均按负数正常计算，
    total字段出现负值（-49.95）

    严重程度：高
    影响分析：如果该数据流转到结算环节，可能导致金额计算错误，
    存在资损风险。建议后端在数量字段增加非负校验（quantity > 0）
    """
    response = requests.post(
        f"{base_url}/add",
        json={
            "userId": 1,
            "products": [
                {
                    "id": 1,
                    "quantity": -5,
                }
            ]
        })
    result = response.json()
    print(f"传入quantity=-5，实际total={result['products'][0]['total']}")
    # 这里刻意不写assert断言成功，因为这本身就是一个发现的问题，而是记录用于后续输出缺陷报告


def test_update_cart():
    """用例7 更新购物车 → 成功200 购物车原本有4个商品,更新为5个"""
    response = requests.put(
        f"{base_url}/1",
        json={
            "merge": True,
            "products": [
                {
                    "id": 1,
                    "quantity": 1,
                },
            ]
        })
    assert response.status_code == 200
    assert response.json()["totalProducts"] == 5
    products_ids = []
    for p in response.json()["products"]:
        products_ids.append(p["id"])
    assert 1 in products_ids


def test_delete_cart():
    """用例8 更新购物车 → 成功200，返回isDeleted明确购物车已经删除，返回删除时间deletedOn"""
    response = requests.delete(f"{base_url}/1")
    assert response.status_code == 200
    assert response.json()["isDeleted"] == True
    assert "deletedOn" in response.json()
    assert response.json()["id"] == 1
