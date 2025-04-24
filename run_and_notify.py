import os
import subprocess
import requests
import time
import zipfile
import re

# 企业微信 webhook
WECHAT_WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c93abe73-669a-48ea-9499-bca101128f3f"

def run_pytest():
    """运行 pytest 测试用例并返回执行结果和统计信息"""
    print("✅ 开始运行测试用例...")
    result = subprocess.run(
        ["pytest", "testcases/", "--alluredir=allure-results", "-p", "allure_pytest"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output = result.stdout.decode()
    print("📤 pytest 输出：\n", output)
    print("📤 pytest 错误：\n", result.stderr.decode())

    # 提取统计信息
    summary_match = re.search(r"=+ ([0-9]+) (passed|failed|skipped|error)[^=]*=+", output)
    stats = summary_match.group(0) if summary_match else "未知"

    # 计算执行时间
    time_match = re.search(r"in ([0-9.]+)s", output)
    exec_time = time_match.group(1) + " 秒" if time_match else "未知"

    return result.returncode, stats, exec_time

def generate_allure_report(output_dir="allure-report"):
    """生成 Allure 报告到指定目录"""
    print(f"✅ 生成 Allure 报告到 {output_dir}...")
    result = subprocess.run(
        ["/usr/bin/allure", "generate", "allure-results", "-o", output_dir, "--clean"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    print("📤 Allure 输出：\n", result.stdout.decode())
    print("📤 Allure 错误输出：\n", result.stderr.decode())

    if result.returncode != 0:
        print("❌ 报告生成失败")
        exit(1)

def zip_report(report_dir="allure-report", zip_file="allure-report.zip"):
    """将 Allure 报告打包成 zip 文件"""
    print(f"📦 打包 {report_dir} 为 ZIP 文件...")
    with zipfile.ZipFile(zip_file, 'w') as zipf:
        for foldername, subfolders, filenames in os.walk(report_dir):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arc_path = os.path.relpath(file_path, report_dir)
                zipf.write(file_path, arc_path)

def send_wechat_notification(stats, exec_time):
    """发送企业微信通知"""
    print("📨 正在发送企业微信通知...")
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    report_url = "http://118.178.189.83:8000"  # 修改为你的公网地址

    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": f"""## 🧪 自动化测试完成
- 执行时间：{timestamp}
- 用例统计：{stats}
- 总耗时：{exec_time}
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
    # 运行 pytest 并获取结果
    returncode, stats, exec_time = run_pytest()

    # 生成 Allure 报告并指定输出目录
    output_dir = "/var/www/allure-report"  # 修改为你希望保存报告的目录
    generate_allure_report(output_dir)

    # 打包报告
    zip_report(output_dir)

    # 发送企业微信通知
    send_wechat_notification(stats, exec_time)

    print("🎉 所有步骤完成！")
