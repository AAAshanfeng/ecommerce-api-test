import requests

"""
登录 → 拿到token和userId
  ↓
查看商品详情 → 拿到商品id
  ↓
把这个商品id，和登录拿到的userId，一起传给购物车接口 → 加购物车
  ↓
验证购物车里的内容，是否跟前面两步的数据一致
"""

def test_shopping():
    """完整购物流程：登录 → 查看商品 → 加入购物车 → 验证购物车内容"""

    # ===== 第1步：登录，拿到token和userId =====
    login_response = requests.post("https://dummyjson.com/auth/login", json={
        "username": "emilys",
        "password": "emilyspass"
    })
    token = login_response.json()["accessToken"]
    user_id = login_response.json()["id"]

    assert login_response.status_code == 200

    # ===== 第2步：查看商品详情，拿到商品id和标题 =====
    product_response = requests.get("https://dummyjson.com/products/1")
    product_id = product_response.json()["id"]
    product_title = product_response.json()["title"]

    assert product_response.status_code == 200

    # ===== 第3步：用第1步的userId + 第2步的product_id，加入购物车 == == =
    cart_response = requests.post( "https://dummyjson.com/carts/add",
        json={
            "userId": user_id,
            "products": [
                {
                    "id": product_id,
                    "quantity": 2,
                }
            ]
        })

    assert cart_response.status_code == 201

    # ===== 第4步：验证购物车内容，跟前面两步的数据是否一致 =====
    cart_data = cart_response.json()

    assert cart_data["userId"] == user_id
    assert cart_data["products"][0]["id"] == product_id
    assert cart_data["products"][0]["title"] == product_title
    assert cart_data["products"][0]["quantity"] == 2

    print("完整购物流程测试通过！")
    print(f"用户{user_id} 购买了商品《{product_title}》x2")