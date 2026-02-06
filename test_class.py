class TestClass:
    def test_one(self):
        x = "this"
        assert "h" in x #使用assert断言语句检查字符"h"是否存在于字符串x中

    def test_two(self):
        x = "hello"
        assert hasattr(x, "check") #使用assert断言语句检查字符串x是否有check属性