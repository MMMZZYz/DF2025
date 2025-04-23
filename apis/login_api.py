import requests

def login():
    session = requests.Session()

    url = "https://auth.dianplus.cn/login?service=https://shop.dianplus.cn/oauth"

    headers = {
        "Origin": "https://auth.dianplus.cn",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://auth.dianplus.cn/login?service=https%3A%2F%2Fshop.dianplus.cn%2Foauth",
    }

    data = {
        "appid": "",
        "scope": "",
        "state": "",
        "redirectUrl": "https://shop.dianplus.cn/oauth",
        "cipherCode": "",
        "qwScanAuthCode": "",
        "Traceid": "69917abd-7189-4f47-9178-3ec09020f883",
        "Rpcid": "0",
        "LTkey": "",
        "entType": "true",
        "qrcodekey": "",
        "entId": "10010",
        "username": "15900110011",
        "password": "88888888",
    }

    # 1. 提交登录，不自动跳转
    resp = session.post(url, headers=headers, data=data, allow_redirects=False)

    # 2. 获取带 ticket 的跳转地址
    ticket_url = resp.headers.get("Location")
    if not ticket_url:
        raise Exception("登录失败，未返回 ticket 跳转链接")

    # 3. 手动访问 ticket 链接，完成登录
    print(ticket_url)
    session.get(ticket_url)

    return session
