import os
import re

def extract_functions_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return re.findall(r"def\s+(\w+)\(session.*?\):", content)

def generate_test_case(functions, import_module="drp_api", output="testcases/test_drp_api.py"):
    lines = [
        "import pytest",
        "import requests",
        f"from apis import {import_module}",
        "",
        "@pytest.fixture(scope='module')",
        "def session():",
        "    return requests.Session()",
        "",
        "def test_drp_order_flow(session):",
        '    """测试：DRP订单流程"""',
        "",
    ]
    for i, func in enumerate(functions):
        if i == 0:
            lines.append(f"    res{i+1} = {import_module}.{func}(session)")
            lines.append(f"    assert res{i+1}.status_code == 200")
            lines.append(f"    bill_id = res{i+1}.json().get('resultObject', {{}}).get('billId')")
        elif "modify" in func:
            lines.append(f"    res{i+1} = {import_module}.{func}(session, bill_id=bill_id)")
            lines.append(f"    assert res{i+1}.status_code == 200")
        elif "submit" in func:
            lines.append(f"    res{i+1} = {import_module}.{func}(session, bill_id=bill_id)")
            lines.append(f"    assert res{i+1}.status_code == 200")
        else:
            lines.append(f"    res{i+1} = {import_module}.{func}(session)")
            lines.append(f"    assert res{i+1}.status_code == 200")
        lines.append("")

    with open(output, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    print(f"✅ 已生成测试文件：{output}")

if __name__ == "__main__":
    api_file = "apis/drp_api.py"
    functions = extract_functions_from_file(api_file)
    generate_test_case(functions)
