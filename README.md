"# Pytest" 

# 一、pytest 开始使用

## 1、安装pytest

pytest需要：Python 3.7+ 或 PyPy3。  

1、在命令行中运行以下命令：

`pip install -U pytest`

2、检查您是否安装了正确的版本：

`$ pytest --version pytest 7.1.0`

## 2、创建你的第一个测试

创建一个名为 的新文件​`test_sample.py`​，其中包含一个函数和一个测试：

```python
# content of test_sample.py
def func(x):
    return x + 1


def test_answer():
    assert func(3) == 5
```

测试结果

![](C:\Users\Allan\AppData\Roaming\marktext\images\2026-02-05-17-30-03-image.png)

[100%] 是指运行所有测试用例的整体进度。 完成后，pytest 会显示失败报告，因为 func(3) 不返回 5。

### 运行多个测试

pytest将在当前目录及其子目录中运行 ​`test_*.py`​ 或 ​`*_test.py`​ 形式的所有文件。  

### 断言引发了某个异常

使用 ​`raises` ​断言某些代码引发了异常：

```python
# content of test_sysexit.py
import pytest


def f():
    raise SystemExit(1)


def test_mytest():
    with pytest.raises(SystemExit):
        f()
```

以“安静”报告模式执行测试功能：

![](C:\Users\Allan\AppData\Roaming\marktext\images\2026-02-05-17-32-02-image.png)
