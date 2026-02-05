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

```python
(base) PS D:\Code\Pytest> pytest.exe 
================================================================= test session starts ==================================================================
platform win32 -- Python 3.12.1, pytest-9.0.2, pluggy-1.6.0
rootdir: D:\Code\Pytest
collected 1 item                                                                                                                                        

test_sample.py F                                                                                                                                  [100%]

======================================================================= FAILURES =======================================================================
_____________________________________________________________________ test_answer ______________________________________________________________________

    def test_answer():
>       assert func(3) == 5
E       assert 4 == 5
E        +  where 4 = func(3)

test_sample.py:7: AssertionError
=============================================================== short test summary info ================================================================ 
FAILED test_sample.py::test_answer - assert 4 == 5
================================================================== 1 failed in 0.08s =================================================================== 
```

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

```python
(base) PS D:\Code\Pytest>  pytest -q test_sysexit.py
.                                                                                                                                                 [100%]
1 passed in 0.01s
```
