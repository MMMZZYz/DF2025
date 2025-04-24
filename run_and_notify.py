import os
import subprocess
import requests
import time
import zipfile

# 企业微信 webhook 
WECHAT_WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c93abe73-669a-48ea-9499-bca101128f3f"

def run_pytest():
    print("✅ 开始运行测试用例...")
    start_time = time.time()
    
    result = subprocess.run(
        ["pytest", "testcases/", "--alluredir=allure-results", "-p", "allure_pytest"],
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    duration = time.time() - start_time
    stdout = result.stdout.decode()
    stderr = result.stderr.decode()

    print("⏱️ 执行耗时：{:.2f} 秒".format(duration))
    print("✅ 控制台输出（部分）：")
    print("\n".join(stdout.splitlines()[-10:]))

    passed, failed = 0, 0
    for line in stdout.splitlines():
        if "passed" in line and "failed" in line:
            # 如：== 2 passed, 1 failed in 3.42s ==
            parts = line.split(',')
            for p in parts:
                if "passed" in p:
                    passed = int(p.strip().split()[0])
                elif "failed" in p:
                    failed = int(p.strip().split()[0])
            break

    if result.returncode != 0:
        print("❌ 有用例失败")
    else:
        print("✅ 所有用例执行成功")

    return passed, failed, duration

def generate_allure_report():
    print("✅ 生成 Allure 报告...")
    result = subprocess.run(
        [r"C:\Tools\allure-2.33.0\bin\allure.bat", "generate", "allure-results", "-o", "allure-report", "--clean"],
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

def send_wechat_notification(passed, failed, duration):
    print("📨 正在发送企业微信通知...")
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    report_url = "http://118.178.189.83:8000"

    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": f"""## 🧪 自动化测试完成  
- 执行时间：{timestamp}  
- 用例统计：✅ 成功 {passed}，❌ 失败 {failed}  
- 耗时：{duration:.2f} 秒  
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
    passed, failed, duration = run_pytest()
    generate_allure_report()
    zip_report()
    send_wechat_notification(passed, failed, duration)
    print("🎉 所有步骤完成！你可以运行 `allure serve allure-results` 查看报告。")
