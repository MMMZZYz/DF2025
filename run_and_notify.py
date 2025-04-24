import os
import subprocess
import requests
import time
import zipfile
import re
import shutil
import sys
print("Python 环境:", sys.executable)
os.environ["PATH"] += ":/usr/bin"  # 添加 allure 所在的路径

# 企业微信 Webhook 地址
WECHAT_WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c93abe73-669a-48ea-9499-bca101128f3f"

# 报告公网地址（你的公网 IP 或绑定的域名）
REPORT_URL = "http://118.178.189.83"

# allure 命令的绝对路径（修改为你的实际路径）
allure_path = "/usr/bin/allure"  # 修改为实际的路径

# 确保脚本在正确的工作目录下执行
os.chdir("/root/DF2025")  # 修改为你的项目根目录

def run_pytest():
    print("✅ 开始运行测试用例...")
    result = subprocess.run(
        ["pytest", "testcases/", "--alluredir=allure-results", "-p", "allure_pytest"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout = result.stdout.decode()
    stderr = result.stderr.decode()
    print("📤 pytest 输出：\n", stdout)
    print("📤 pytest 错误：\n", stderr)
    if result.returncode != 0:
        print("❌ 测试运行失败")
    return stdout

def parse_summary_from_output(output):
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
        ["sh", "-c", "allure generate allure-results/ -o allure-report --clean"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout = result.stdout.decode()
    stderr = result.stderr.decode()
    print("📤 allure 输出：\n", stdout)
    print("📤 allure 错误：\n", stderr)
    if result.returncode != 0:
        print("❌ 报告生成失败")
        exit(1)
def deploy_report_to_nginx():
    print("🚀 部署报告到 Nginx ...")
    nginx_html_dir = "/usr/share/nginx/html"
    if os.path.exists(nginx_html_dir):
        shutil.rmtree(nginx_html_dir)
    shutil.copytree("allure-report", nginx_html_dir)
    print("✅ 部署成功，可通过公网访问查看报告")

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
    deploy_report_to_nginx()
    send_wechat_notification(passed, failed, skipped, duration)
    print("🎉 所有步骤完成！")
