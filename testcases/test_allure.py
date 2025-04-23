import allure

@allure.title("测试 1 + 1")
def test_sum():
    a = 1
    b = 1
    result = a + b
    allure.attach(str(result), "实际计算结果")
    assert result == 2
