import os
import subprocess
import requests
import time
import zipfile

WECHAT_WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c93abe73-669a-48ea-9499-bca101128f3f"
REPORT_URL = "http://118.178.189.83:8000"

def run_pytest():
    print("✅ 开始运行测试用例...")
    result = subprocess.run(
        "pytest testcases/ --alluredir=allure-results -p allure_pytest",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print("📤 pytest 输出：\n", result.stdout.decode())
    print("📤 pytest 错误：\n", result.stderr.decode())

    # 解析执行结果
    output = result.stdout.decode()
    total = int(output.split("collected ")[1].split(" item")[0]) if "collected " in output else 0
    passed = output.count("PASSED") + output.count(".")  # 简易统计
    failed = output.count("FAILED") + output.count("F")

    print(f"✅ 共执行用例: {total}，通过: {passed}，失败: {failed}")
    return total, passed, failed

def generate_allure_report():
    print("✅ 生成 Allure 报告...")
    result = subprocess.run(
        "allure generate allure-results -o allure-report --clean",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print(result.stdout.decode())
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

def send_wechat_notification(total, passed, failed):
    print("📨 正在发送企业微信通知...")
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": f"""## 🧪 自动化测试完成  
- 执行时间：{timestamp}  
- 总用例数：{total}  
- ✅ 通过：{passed}  
- ❌ 失败：{failed}  
- [👉 点击查看报告]({REPORT_URL})  
"""
        }
    }

    resp = requests.post(WECHAT_WEBHOOK, json=data)
    if resp.status_code == 200:
        print("✅ 企业微信通知已发送")
    else:
        print(f"❌ 企业微信发送失败: {resp.text}")

if __name__ == "__main__":
    total, passed, failed = run_pytest()
    generate_allure_report()
    zip_report()
    send_wechat_notification(total, passed, failed)
    print("🎉 所有步骤完成！")
