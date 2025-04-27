import requests
import allure

def request_with_allure(method, url, session=None, **kwargs):
    """
    封装 requests 请求，并自动在 Allure 中附加请求和响应信息
    :param method: 请求方法 (GET, POST, PUT, DELETE)
    :param url: 请求地址
    :param session: 使用的 requests session 对象
    :param kwargs: 其他 requests 支持的参数（如 json, data, headers 等）
    :return: Response 对象
    """
    # 使用 session 进行请求
    if session is None:
        session = requests.Session()

    with allure.step(f"接口请求: {method} {url}"):
        if 'json' in kwargs:
            allure.attach(str(kwargs['json']), "请求 JSON 参数", allure.attachment_type.JSON)
        if 'data' in kwargs:
            allure.attach(str(kwargs['data']), "请求表单参数", allure.attachment_type.TEXT)
        if 'params' in kwargs:
            allure.attach(str(kwargs['params']), "请求 URL 参数", allure.attachment_type.TEXT)
        if 'headers' in kwargs:
            allure.attach(str(kwargs['headers']), "请求头", allure.attachment_type.JSON)

        # 发送请求
        response = session.request(method, url, **kwargs)

        allure.attach(str(response.status_code), "响应状态码", allure.attachment_type.TEXT)
        try:
            # 如果返回是 json，就格式化展示
            allure.attach(response.text, "响应内容", allure.attachment_type.JSON)
        except Exception:
            allure.attach(response.text, "响应内容", allure.attachment_type.TEXT)

        return response
