# content of conftest.py
from test_foocompare import Foo  # 从测试模块导入自定义类 Foo

def pytest_assertrepr_compare(op, left, right):
    # 这是一个 pytest hook 函数，用于自定义断言失败时的错误信息
    if isinstance(left, Foo) and isinstance(right, Foo) and op == "==":
        # 只有当左右两边都是 Foo 实例且操作符是 "==" 时才生效
        return [
            "Comparing Foo instances:",  # 自定义错误信息的标题
            "   vals: {} != {}".format(left.val, right.val),  # 显示具体的差异
        ]