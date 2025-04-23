import requests

def test_get_sum_brand_stock():
    from apis.login_api import login  # 写的 login 函数
    session = login()

    url = "https://shop.dianplus.cn/rs/wms/new_stock/get_sum_brand_stock.do"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Origin": "https://shop.dianplus.cn",
        "Referer": "https://shop.dianplus.cn/?module=50&menu=5040",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Traceid": "demo-trace-id",  # 可选
    }

    data = {
        "showStoreSale": "false",
        "goodsType": "3",
        "excludeZeroStock": "true",
        "sumType": "goods_sku"
    }

    # 发 POST 请求
    resp = session.post(url, headers=headers, data=data)

    assert resp.status_code == 200

    try:
        print(resp.json())
    except Exception as e:
        print("返回不是 JSON 格式：", resp.text[:300])
        raise e
