import os
import subprocess
import requests
import time
import zipfile
import re

# 企业微信 Webhook 地址
WECHAT_WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c93abe73-669a-48ea-9499-bca101128f3f"

# 公网报告访问地址（替换为你自己的 IP 或域名）
REPORT_URL = "http://118.178.189.83:8000"

def run_pytest():
    print("✅ 开始运行测试用例...")
    result = subprocess.run(
        ["pytest", "testcases/", "--alluredir=allure-results", "-p", "allure_pytest"],
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout = result.stdout.decode()
    stderr = result.stderr.decode()
    print("📤 pytest 输出：\n", stdout)
    print("📤 pytest 错误：\n", stderr)
    if result.returncode != 0:
        print("❌ 测试运行失败")

    return stdout

def parse_summary_from_output(output):
    """
    从 pytest 输出中提取用例执行统计信息
    """
    passed = failed = skipped = duration = "0"
    summary_line = re.search(r"=+.+?(\d+)\s+passed.*?in\s+([\d\.]+)s", output)
    if summary_line:
        passed = summary_line.group(1)
        duration = summary_line.group(2)

    failed_match = re.search(r"(\d+)\s+failed", output)
    skipped_match = re.search(r"(\d+)\s+skipped", output)

    if failed_match:
        failed = failed_match.group(1)
    if skipped_match:
        skipped = skipped_match.group(1)

    return passed, failed, skipped, duration

def generate_allure_report():
    print("✅ 生成 Allure 报告...")
    result = subprocess.run(
        ["allure", "generate", "allure-results", "-o", "allure-report", "--clean"],
        shell=True
    )
    if result.returncode != 0:
        print("❌ 报告生成失败")
        exit(1)

def zip_report(report_dir="allure-report", zip_file="allure-report.zip"):
    print("📦 打包 HTML 报告...")
    with zipfile.ZipFile(zip_file, 'w') as zipf:
        for foldername, subfolders, filenames in os.walk(report_dir):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arc_path = os.path.relpath(file_path, report_dir)
                zipf.write(file_path, arc_path)

def send_wechat_notification(passed, failed, skipped, duration):
    print("📨 正在发送企业微信通知...")
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    content = f"""## 🧪 自动化测试完成  
- 执行时间：{timestamp}  
- 报告类型：Allure 报告  
- ⏱️ 耗时：{duration} 秒  
- ✅ 成功：{passed}  
- ❌ 失败：{failed}  
- 🔁 跳过：{skipped}  
- [👉 点击查看报告]({REPORT_URL})  
"""

    data = {
        "msgtype": "markdown",
        "markdown": {"content": content}
    }

    resp = requests.post(WECHAT_WEBHOOK, json=data)
    if resp.status_code == 200:
        print("✅ 企业微信通知已发送")
    else:
        print(f"❌ 企业微信发送失败: {resp.text}")

if __name__ == "__main__":
    pytest_output = run_pytest()
    passed, failed, skipped, duration = parse_summary_from_output(pytest_output)
    generate_allure_report()
    zip_report()
    send_wechat_notification(passed, failed, skipped, duration)
    print("🎉 所有步骤完成！")
