import os
import re
import json
from urllib.parse import unquote, urlparse, parse_qs

def translate_to_chinese(name):
    mapping = {
        "save": "保存",
        "create": "创建",
        "update": "更新",
        "delete": "删除",
        "get": "获取",
        "list": "列表",
        "do": "操作",
        "order": "订单",
        "apply": "申请",
        "bill": "单据",
        "stock": "库存",
        "scan": "扫码",
        "goods": "商品",
        "purchase": "采购",
        "out": "出库",
        "in": "入库",
        "channel": "渠道",
    }
    words = name.split("_")
    translated = [mapping.get(w.lower(), w) for w in words]
    return "方法用途：" + "".join(translated)


def parse_curl_file(curl_path):
    with open(curl_path, "r", encoding="utf-8") as f:
        content = f.read()

    curl_blocks = re.findall(r"(curl .+?)(?=\ncurl|\Z)", content, flags=re.S)
    return [parse_curl_to_python(block) for block in curl_blocks]


def parse_curl_to_python(curl_command):
    all_urls = re.findall(r"'(https?://[^']+)'", curl_command)
    full_url = all_urls[-1] if all_urls else ""
    parsed_url = urlparse(full_url)
    url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path

    headers_raw = re.findall(r"-H\s+'([^:]+):\s?(.+?)'", curl_command)
    headers = {k.strip(): v.strip() for k, v in headers_raw}
    headers_lc = {k.lower(): v for k, v in headers.items()}
    content_type = headers_lc.get("content-type", "")

    if "cookie" in headers_lc:
        headers.pop("Cookie", None)
        headers.pop("cookie", None)

    data_match = re.search(r"--data-raw\s+'(.+?)'", curl_command)
    raw_data = data_match.group(1) if data_match else ""
    data_items = [item.split("=", 1) for item in raw_data.split("&") if "=" in item]
    data_dict = {k: unquote(v) for k, v in data_items}

    query_dict = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(parsed_url.query).items()}

    path_parts = parsed_url.path.strip("/").split("/")
    if len(path_parts) >= 2:
        func_name = "_".join(re.sub(r"\W+", "_", p) for p in path_parts[-2:])
    elif path_parts:
        func_name = re.sub(r"\W+", "_", path_parts[-1])
    else:
        func_name = "api_request"

    method = "post" if "--data" in curl_command.lower() else "get"
    comment = translate_to_chinese(func_name)

    lines = [f"# {comment}",
             f"def {func_name}(session):",
             f"    url = \"{url}\"",
             f"    headers = {headers}"]

    if method == "post" and data_dict:
        if "application/json" in content_type:
            lines.append(f"    json_data = {data_dict}")
            lines.append(f"    return session.post(url, headers=headers, json=json_data)")
        else:
            lines.append(f"    data = {data_dict}")
            lines.append(f"    return session.post(url, headers=headers, data=data)")
    elif method == "get" and query_dict:
        lines.append(f"    params = {query_dict}")
        lines.append(f"    return session.get(url, headers=headers, params=params)")
    else:
        lines.append(f"    return session.{method}(url, headers=headers)")

    return "\n".join(lines)


def parse_har_to_functions(har_path):
    with open(har_path, "r", encoding="utf-8") as f:
        har_data = json.load(f)

    entries = har_data.get("log", {}).get("entries", [])
    functions = []

    for entry in entries:
        req = entry.get("request", {})
        method = req.get("method", "GET").lower()
        url = req.get("url")
        headers = {h["name"]: h["value"] for h in req.get("headers", [])}
        post_data = req.get("postData", {}).get("params", [])
        data_dict = {p["name"]: p.get("value", "") for p in post_data}

        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip("/").split("/")
        if len(path_parts) >= 2:
            func_name = "_".join(re.sub(r"\W+", "_", p) for p in path_parts[-2:])
        else:
            func_name = re.sub(r"\W+", "_", path_parts[-1])

        comment = translate_to_chinese(func_name)
        headers.pop("Cookie", None)
        lines = [f"# {comment}",
                 f"def {func_name}(session):",
                 f"    url = \"{url}\"",
                 f"    headers = {headers}"]

        if method == "post":
            lines.append(f"    data = {data_dict}")
            lines.append(f"    return session.post(url, headers=headers, data=data)")
        elif method == "get":
            lines.append(f"    return session.get(url, headers=headers)")
        else:
            lines.append(f"    return session.{method}(url, headers=headers)")

        functions.append("\n".join(lines))

    return functions


def convert_file(input_file, output_file="generated_api.py"):
    if input_file.endswith(".har"):
        functions = parse_har_to_functions(input_file)
    else:
        functions = parse_curl_file(input_file)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Auto-generated API functions\n\n")
        f.write("import requests\n\n")
        f.write("\n\n".join(functions))

    print(f"✅ 已生成 {len(functions)} 个接口方法，保存在: {output_file}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert curl or HAR to Python requests code")
    parser.add_argument("input", help="Path to a .txt (curl) or .har file")
    parser.add_argument("--output", default="generated_api.py", help="Output Python file name")
    args = parser.parse_args()
    convert_file(args.input, args.output)
