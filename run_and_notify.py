import os
import subprocess
import requests
import time
import zipfile
import re
import sys
import shutil

# 企业微信 webhook
WECHAT_WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c93abe73-669a-48ea-9499-bca101128f3f"

# 定义固定路径
ALLURE_RESULTS_DIR = "allure-results"
ALLURE_REPORT_DIR = "/var/www/allure-report"
ALLURE_ZIP_FILE = "allure-report.zip"

def clean_allure_results():
    """清空 allure-results 目录"""
    if os.path.exists(ALLURE_RESULTS_DIR):
        for filename in os.listdir(ALLURE_RESULTS_DIR):
            file_path = os.path.join(ALLURE_RESULTS_DIR, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"⚠️ 删除 {file_path} 失败：{e}")
    print("🧹 已清空 allure-results 目录")

def run_pytest():
    """运行 pytest 测试用例并返回执行结果和统计信息"""
    clean_allure_results()

    print("✅ 开始运行测试用例...")
    result = subprocess.run(
        ["pytest", "testcases/", "--alluredir", ALLURE_RESULTS_DIR, "-p", "allure_pytest"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output = result.stdout.decode()
    error = result.stderr.decode()
    print("📤 pytest 输出：\n", output)
    print("📤 pytest 错误：\n", error)

    # 提取统计信息
    pass_count = fail_count = skip_count = 0

    match = re.search(r"=+.*?(\d+)\s+passed.*?(\d+)?\s+failed.*?(\d+)?\s+skipped.*?=+", output, re.DOTALL)
    if match:
        groups = match.groups()
        pass_count = int(groups[0]) if groups[0] else 0
        fail_count = int(groups[1]) if groups[1] else 0
        skip_count = int(groups[2]) if groups[2] else 0

    # 提取执行时间
    time_match = re.search(r"in ([0-9.]+)s", output)
    exec_time_sec = float(time_match.group(1)) if time_match else 0
    exec_time = format_exec_time(exec_time_sec)

    return result.returncode, pass_count, fail_count, skip_count, exec_time

def format_exec_time(seconds):
    """秒数转分钟秒"""
    if seconds < 60:
        return f"{seconds:.1f} 秒"
    else:
        minutes = int(seconds // 60)
        remain_sec = seconds % 60
        return f"{minutes} 分 {remain_sec:.1f} 秒"

def generate_allure_report():
    """生成 Allure 报告"""
    print("✅ 生成 Allure 报告...")
    result = subprocess.run(
        ["/usr/bin/allure", "generate", ALLURE_RESULTS_DIR, "-o", ALLURE_REPORT_DIR, "--clean"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print("📤 Allure 输出：\n", result.stdout.decode())
    print("📤 Allure 错误输出：\n", result.stderr.decode())

    if result.returncode != 0:
        print("❌ 报告生成失败！")
        sys.exit(1)

def zip_report():
    """将 Allure 报告打包成 zip 文件"""
    print(f"📦 打包 {ALLURE_REPORT_DIR} 为 ZIP 文件...")
    with zipfile.ZipFile(ALLURE_ZIP_FILE, 'w') as zipf:
        for foldername, _, filenames in os.walk(ALLURE_REPORT_DIR):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arc_path = os.path.relpath(file_path, ALLURE_REPORT_DIR)
                zipf.write(file_path, arc_path)
    print(f"✅ ZIP 文件已生成：{ALLURE_ZIP_FILE}")

def send_wechat_notification(pass_count, fail_count, skip_count, exec_time):
    """发送企业微信通知"""
    print("📨 正在发送企业微信通知...")
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    report_url = f"http://118.178.189.83/allure/?t={int(time.time())}"

    status_emoji = "✅" if fail_count == 0 else "❌"
    fail_text = f"**<font color=\"warning\">{fail_count}</font>**" if fail_count > 0 else f"{fail_count}"

    mentioned_mobile_list = []
    if fail_count > 0:
        mentioned_mobile_list.append("15938796756")  # 填丹枫的手机号

    content = f"""## {status_emoji} 自动化测试完成
- 执行时间：{timestamp}
- 执行用例：{pass_count + fail_count + skip_count} 个
- ✅ 通过：{pass_count}
- ❌ 失败：{fail_text}
- ⚡ 跳过：{skip_count}
- 总耗时：{exec_time}
- [👉 点击查看报告]({report_url})
"""

    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": content,
            "mentioned_mobile_list": mentioned_mobile_list  # 通过手机号@人
        }
    }

    resp = requests.post(WECHAT_WEBHOOK, json=data)
    if resp.status_code == 200:
        print("✅ 企业微信通知已发送")
    else:
        print(f"❌ 企业微信发送失败: {resp.text}")



if __name__ == "__main__":
    # 运行 pytest 并获取结果
    returncode, pass_count, fail_count, skip_count, exec_time = run_pytest()

    if returncode != 0:
        print("⚠️ 测试存在失败，继续生成报告...")

    # 生成 Allure 报告
    generate_allure_report()

    # 打包报告
    zip_report()

    # 发送企业微信通知
    send_wechat_notification(pass_count, fail_count, skip_count, exec_time)

    print("🎉 所有步骤完成！")
