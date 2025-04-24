import os
import subprocess
import requests
import time
import zipfile
import re

WECHAT_WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c93abe73-669a-48ea-9499-bca101128f3f"

def run_pytest():
    print("✅ 开始运行测试用例...")
    result = subprocess.run(
        "pytest testcases/ --alluredir=allure-results -p allure_pytest",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output = result.stdout.decode()
    error_output = result.stderr.decode()
    print("📤 pytest 输出：\n", output)
    print("📤 pytest 错误：\n", error_output)
    
    match = re.search(r"=+\\s*(\\d+) passed.*?in ([\\d.]+)s", output)
    total = passed = failed = duration = 0
    if match:
        passed = int(match.group(1))
        total = passed
        duration = float(match.group(2))
    else:
        match2 = re.search(r"(\\d+) failed, (\\d+) passed", output)
        if match2:
            failed, passed = int(match2.group(1)), int(match2.group(2))
            total = failed + passed

    return total, passed, failed, duration

def generate_allure_report():
    print("✅ 生成 Allure 报告...")
    result = subprocess.run(
        ["allure", "generate", "allure-results", "-o", "allure-report", "--clean"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    if result.returncode != 0:
        print("❌ 报告生成失败")
        print(result.stderr.decode())
        exit(1)

def zip_report(report_dir="allure-report", zip_file="allure-report.zip"):
    print("📦 打包 HTML 报告...")
    with zipfile.ZipFile(zip_file, 'w') as zipf:
        for foldername, subfolders, filenames in os.walk(report_dir):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arc_path = os.path.relpath(file_path, report_dir)
                zipf.write(file_path, arc_path)

def send_wechat_notification(total, passed, failed, duration):
    print("📨 正在发送企业微信通知...")
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    report_url = "http://118.178.189.83:8000"

    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": f"""## 🧪 自动化测试完成  
- 执行时间：{timestamp}  
- 报告类型：Allure 报告  
- 总用例数：{total}  
- ✅ 成功用例：{passed}  
- ❌ 失败用例：{failed}  
- ⏱️ 执行耗时：{duration}s  
- [👉 点击查看报告]({report_url})  
"""
        }
    }

    resp = requests.post(WECHAT_WEBHOOK, json=data)
    if resp.status_code == 200:
        print("✅ 企业微信通知已发送")
    else:
        print(f"❌ 企业微信发送失败: {resp.text}")

if __name__ == "__main__":
    total, passed, failed, duration = run_pytest()
    generate_allure_report()
    zip_report()
    send_wechat_notification(total, passed, failed, duration)
    print("🎉 所有步骤完成！你可以运行 `allure serve allure-results` 查看报告。")
