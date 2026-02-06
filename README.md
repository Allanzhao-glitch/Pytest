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

### 2.1、运行多个测试

pytest将在当前目录及其子目录中运行 ​`test_*.py`​ 或 ​`*_test.py`​ 形式的所有文件。  

### 2.2、断言引发了某个异常

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

### 2.3、将多个测试分组到一个类中

一旦您开发了多个测试，您可能希望将它们分组到一个类中。 pytest 可以很容易地创建一个包含多个测试的类：

```python
# content of test_class.py
class TestClass:
    def test_one(self):
        x = "this"
        assert "h" in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, "check")
```

pytest 按照其 Python 测试约定发现所有测试，因此它会找到两个以 ​`test_` ​为前缀的函数。 不需要对任何东西进行子类化，但请确保在您的类前面加上 ​`Test` ​，否则该类将被跳过。 我们可以通过传递文件名来简单地运行模块：

```
(base) PS D:\Code\Pytest> pytest -q test_class.py
.F                                                                                                                     [100%]
========================================================= FAILURES ========================================================== 
____________________________________________________ TestClass.test_two _____________________________________________________ 

self = <test_class.TestClass object at 0x000002522DBAC8C0>

    def test_two(self):
        x = "hello"
>       assert hasattr(x, "check") #使用assert断言语句检查字符串x是否有check属性
        ^^^^^^^^^^^^^^^^^^^^^^^^^^
E       AssertionError: assert False
E        +  where False = hasattr('hello', 'check')

test_class.py:8: AssertionError
================================================== short test summary info ==================================================
FAILED test_class.py::TestClass::test_two - AssertionError: assert False
1 failed, 1 passed in 0.07s
```

第一次测试通过，第二次失败。 您可以很容易地看到断言中的中间值，以帮助您了解失败的原因。

将测试分组在类中可能是有益的，原因如下：

- 测试配置
- 仅在该特定类中共享用于测试的固定装置
- 在类级别应用标记，并将它们隐式应用于所有测试  

在类中对测试进行分组时需要注意的是，每个测试都有一个唯一的类实例。 让每个测试共享相同的类实例对测试隔离非常不利，并且会促进不良的测试实践。 例如：

```python
# content of test_class_demo.py
class TestClassDemoInstance:
    value = 0

    def test_one(self):
        self.value = 1
        assert self.value == 1

    def test_two(self):
        assert self.value == 1
```

```
(base) PS D:\Code\Pytest> pytest.exe -k TestClassDemoInstance -q
.F                                                                                                                               [100%]
============================================================== FAILURES ===============================================================
___________________________________________________ TestClassDemoInstance.test_two ____________________________________________________

self = <test_class_demo.TestClassDemoInstance object at 0x0000026B9DF2CF80>

    def test_two(self):
>       assert self.value == 1
E       assert 0 == 1
E        +  where 0 = <test_class_demo.TestClassDemoInstance object at 0x0000026B9DF2CF80>.value

test_class_demo.py:8: AssertionError
======================================================= short test summary info =======================================================
FAILED test_class_demo.py::TestClassDemoInstance::test_two - assert 0 == 1
1 failed, 1 passed, 4 deselected in 0.10s
```

注意，在类级别添加的属性是类属性，因此它们将在测试之间共享。

### 2.4、为功能测试请求一个唯一的临时目录

pytest提供内置​`fixture /function`​参数来请求任意资源，比如一个唯一的临时目录:

```python
# content of test_tmp_path.py
def test_needsfiles(tmp_path):
    print(tmp_path)
    assert 0
```

在测试函数签名中列出名称​`tmp_path`​, pytest将在执行测试函数调用之前查找并调用一个​`fixture`​工厂来创建资源。在运行测试之前，pytest会创建一个每个测试调用唯一的临时目录:

```python
(base) PS D:\Code\Pytest> pytest -q test_tmp_path.py
F                                                                                                                                                             [100%]
============================================================================= FAILURES =============================================================================
_________________________________________________________________________ test_needsfiles __________________________________________________________________________

tmp_path = WindowsPath('C:/Users/Allan/AppData/Local/Temp/pytest-of-Allan/pytest-0/test_needsfiles0')

    def test_needsfiles(tmp_path):
        print(tmp_path)
>       assert 0
E       assert 0

test_tmp_path.py:3: AssertionError
----------------------------------------------------------------------- Captured stdout call ----------------------------------------------------------------------- 
C:\Users\Allan\AppData\Local\Temp\pytest-of-Allan\pytest-0\test_needsfiles0
===================================================================== short test summary info ====================================================================== 
FAILED test_tmp_path.py::test_needsfiles - assert 0
1 failed in 0.12s
```

通过下面的命令来了解内置pytest fixture的类型:

```
pytest --fixtures   # shows builtin and custom fixtures
```

注意，除非添加了​`-v`​选项，否则该命令会省略带有​`_`​前导的fixture。

# 二、 pytest 核心功能

## 1、 pytest 核心功能-调用pytest

通常，pytest 使用命令 ​`pytest` ​调用。这将执行当前目录及其子目录中名称遵循 ​`test_*.py`​ 或 ​`\*_test.py`​ 形式的所有文件中的所有测试。 更一般地说，pytest 遵循标准的测试发现规则。

指定要运行的测试

Pytest 支持多种从命令行运行和选择测试的方法。

### 1.1、在模块中运行测试

```
pytest test_mod.py
```

### 1.2、在目录中运行测试

```
pytest testing/
```

### 1.3、通过关键字表达式运行测试

```
pytest -k "MyClass and not method"
```

这将运行包含与给定字符串表达式匹配的名称（不区分大小写）的测试，其中可以包括使用文件名、类名和函数名作为变量的 Python 运算符。 上面的示例将运行 ​`TestMyClass.test_something`​ 但不是 ​`TestMyClass.test_method_simple`​

### 1.4、按节点ID运行测试

每个收集到的测试都分配有一个唯一的 ​`nodeid`​，它由模块文件名和后面的说明符组成，如类名、函数名和来自参数化的参数，用​`::`​字符分隔。

要在模块中运行特定测试：

```
pytest test_mod.py::test_func
```

在命令行中指定测试方法的另一个示例：

```
pytest test_mod.py::TestClass::test_method
```

### 1.5、通过标记表达式运行测试

```
pytest -m slow
```

将运行所有使用 ​`@pytest.mark.slow`​ 装饰器装饰的测试。

### 1.6、从包运行测试

```
pytest --pyargs pkg.testing
```

### 1.7、获取有关版本、选项名称、环境变量的帮助

```
pytest --version   # shows where pytest was imported from
pytest --fixtures  # show available builtin function arguments
pytest -h | --help # show help on command line and config file options
```

分析测试执行时间

要获得超过1.0秒的最慢10个测试持续时间的列表

```
pytest --durations=10 --durations-min=1.0
```

默认情况下，除非在命令行上传递了​ `-vv`​，否则 pytest 不会显示太小（<0.005s）的测试持续时间。

### 1.8、管理插件的加载

提前加载插件
您可以使用 ​-p​ 选项在命令行中显式地提前加载插件（内部和外部）：

```
pytest -p mypluginmodule
```

该选项接收一个​`name`​参数，可以是：

- 完整的模块名称，例如 ​`myproject.plugins`​。 这个带点的名称必须是可导入的。
- 插件的入口点名称。 这是注册插件时传递给 ​`setuptools` ​的名称。 例如，要提前加载 ​`pytest-cov`​ 插件，您可以使用：

```
pytest -p pytest_cov
```

禁用插件
要在调用时禁用加载特定插件，请使用 ​-p​ 选项和前缀 ​no:​

示例：要禁用加载插件 ​doctest​，该插件负责从文本文件执行 ​doctest ​测试，请像这样调用 ​pytest​：

```
pytest -p no:doctest
```

### 1.9、调用pytest的其他方式

通过 python -m pytest 调用 pytest 您可以从命令行通过 Python 解释器调用测试：

```
python -m pytest [...]
```

这几乎等同于直接调用命令行脚本 ​pytest [...]​，只是通过 python 调用还会将当前目录添加到 ​sys.path​ 中。

从 Python 代码调用 pytest
您可以直接从 Python 代码调用 ​pytest​：

```
retcode = pytest.main()
```

这就像您从命令行调用​`pytest`​一样。 它不会引发 ​`SystemExit` ​而是返回退出代码。 您可以传入选项和参数：

```
retcode = pytest.main(["-x", "mytestdir"])
```

您可以为​ `pytest.main`​ 指定其他插件：

```
# content of myinvoke.py
import pytest
import sys


class MyPlugin:
    def pytest_sessionfinish(self):
        print("*** test run reporting finishing")


if __name__ == "__main__":
    sys.exit(pytest.main(["-qq"], plugins=[MyPlugin()]))
```

运行它将显示 ​`MyPlugin` ​已添加并且它的钩子已被调用：

```
$ python myinvoke.py
*** test run reporting finishing
```

注解

调用 ​`pytest.main()`​ 将导致导入您的测试以及它们导入的任何模块。 由于 python 导入系统的缓存机制，从同一进程对 ​`pytest.main()`​ 的后续调用将不会反映调用之间对这些文件的更改。 因此，不建议从同一进程多次调用 ​`pytest.main()`​（例如，为了重新运行测试）。

## 2、 pytest 核心功能-在测试中编写和报告断言

### 2.1、使用assert语句进行断言

pytest 允许您使用标准 Python 断言来验证 Python 测试中的期望和值。 例如，您可以编写以下内容：

```
# content of test_assert1.py
def f():
    return 3


def test_function():
    assert f() == 4
```

断言您的函数返回某个值。 如果此断言失败，您将看到函数调用的返回值：

```
(base) PS D:\Code\Pytest> pytest.exe .\test_assert1.py
======================================================================= test session starts ========================================================================
platform win32 -- Python 3.12.1, pytest-9.0.2, pluggy-1.6.0
rootdir: D:\Code\Pytest
collected 1 item                                                                                                                                                    

test_assert1.py F                                                                                                                                             [100%]

============================================================================= FAILURES ============================================================================= 
__________________________________________________________________________ test_function ___________________________________________________________________________ 

    def test_function():
>       assert f() == 4
E       assert 3 == 4
E        +  where 3 = f()

test_assert1.py:5: AssertionError
===================================================================== short test summary info ====================================================================== 
FAILED test_assert1.py::test_function - assert 3 == 4
======================================================================== 1 failed in 0.12s ========================================================================= 
```

Pytest支持显示最常用的子表达式的值，包括调用、属性、比较以及二进制和一元操作符。这允许您在不使用样板代码的情况下使用惯用的python构造，同时不丢失内省信息。

但是，如果您使用这样的断言指定消息：

```
assert a % 2 == 0, "value was odd, should be even"
```

然后，根本不会发生任何断言内省，消息将简单地显示在回溯中。

### 2.2、关于预期异常的断言

为了编写有关引发异常的断言，您可以使用 ​`pytest.raises()`​ 作为上下文管理器，如下所示：

```
import pytest


def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        1 / 0
```

如果你需要访问实际的异常信息，你可以使用:

```
def test_recursion_depth():
    with pytest.raises(RuntimeError) as excinfo:

        def f():
            f()

        f()
    assert "maximum recursion" in str(excinfo.value)
```

`excinfo`​是一个​`ExceptionInfo`​实例，它包装了实际引发的异常。interest的主要属性是​`.type`​、​`.value`​和​`.traceback`​

您可以向上下文管理器传递一个​`match`​关键字参数，以测试正则表达式是否匹配异常的字符串表示(类似于 ​`unittest` ​中的 ​`TestCase.assertRaisesRegex`​ 方法）：

```
import pytest


def myfunc():
    raise ValueError("Exception 123 raised")


def test_match():
    with pytest.raises(ValueError, match=r".* 123 .*"):
        myfunc()
```

`match` ​方法的 ​`regexp` ​参数与 ​`re.search`​ 函数匹配，因此在上面的示例中 ​`match='123'`​ 也可以正常工作。

​`pytest.raises()`​ 函数还有另一种形式，您可以在其中传递一个函数，该函数将使用给定的 ​`*args`​ 和 ​`**kwargs`​ 执行，并断言引发了给定的异常：

```
pytest.raises(ExpectedException, func, *args, **kwargs)
```

如果出现无异常或错误异常等故障，​`reporter` ​将为您提供有用的输出。

请注意，也可以为 ​`pytest.mark.xfail`​ 指定一个​`raises`​参数，它以更具体的方式检查测试是否失败，而不仅仅是引发任何异常：

```
@pytest.mark.xfail(raises=IndexError)
def test_f():
    f()
```

使用 ​`pytest.raises()`​ 对于您正在测试自己的代码故意引发的异常的情况可能会更好，而使用带有检查功能的​`@pytest.mark.xfail`​ 可能更适合记录未修复的错误（其中测试描述了应该发生什么）或依赖项中的错误。

### 2.2、 关于预期警告的断言

您可以使用 ​`pytest.warns`​ 检查代码是否引发了特定警告。

### 2.3、利用上下文相关的比较

Pytest具有丰富的支持，可以在遇到比较时提供上下文敏感的信息。例如:

```
# content of test_assert2.py
def test_set_comparison():
    set1 = set("1308")
    set2 = set("8035")
    assert set1 == set2
```

如果你运行这个模块：

```
(base) PS D:\Code\Pytest> pytest.exe .\test_assert2.py
======================================================================= test session starts ========================================================================
platform win32 -- Python 3.12.1, pytest-9.0.2, pluggy-1.6.0
rootdir: D:\Code\Pytest
collected 1 item                                                                                                                                                     

test_assert2.py F                                                                                                                                             [100%]

============================================================================= FAILURES ============================================================================= 
_______________________________________________________________________ test_set_comparison ________________________________________________________________________ 

    def test_set_comparison():
        set1 = set("1308")
        set2 = set("8035")
>       assert set1 == set2
E       AssertionError: assert {'0', '1', '3', '8'} == {'0', '3', '5', '8'}
E
E         Extra items in the left set:
E         '1'
E         Extra items in the right set:
E         '5'
E         Use -v to get more diff

test_assert2.py:4: AssertionError
===================================================================== short test summary info ====================================================================== 
FAILED test_assert2.py::test_set_comparison - AssertionError: assert {'0', '1', '3', '8'} == {'0', '3', '5', '8'}
======================================================================== 1 failed in 0.12s ========================================================================= 
```

对一些情况进行了特殊比较：

- 比较长字符串：显示上下文差异
- 比较长序列：第一个失败的索引
- 比较字典：不同的条目

### 2.4、为失败的断言定义你自己的解释

可以通过实现​`pytest_assertrepr_compare`​钩子来添加您自己的详细解释。

pytest_assertrepr_compare(config, op, left, right)

返回失败的断言表达式中比较的解释。

如果没有自定义解释，则返回​`None`​，否则返回一个字符串列表。字符串将由换行符连接，但字符串中的任何换行符将被转义。请注意，除第一行外的所有内容都稍微缩进，目的是将第一行作为摘要。

参数：

- ​`config (pytest.Config)`​ -- pytest 配置对象
- ​`op (str)`​ –
- ​`left (object)`​ –
- ​`right (object)`​ –

返回类型：

Optional[List[str]]

例如，可以考虑在​`conftest.py`​文件中添加以下钩子，它提供了对​`Foo`​对象的另一种解释:

```
# content of conftest.py
from test_foocompare import Foo


def pytest_assertrepr_compare(op, left, right):
    if isinstance(left, Foo) and isinstance(right, Foo) and op == "==":
        return [
            "Comparing Foo instances:",
            "   vals: {} != {}".format(left.val, right.val),
        ]
```

现在，给定这个测试模块：现在，给定这个测试模块：

现在，给定这个测试模块：

```
# content of test_foocompare.py
class Foo:
    def __init__(self, val):
        self.val = val

    def __eq__(self, other):
        return self.val == other.val


def test_compare():
    f1 = Foo(1)
    f2 = Foo(2)
    assert f1 == f2
```

你可以运行​`test`​模块，并获得在​`conftest`​文件中定义的自定义输出:

```
(base) PS D:\Code\Pytest> pytest -q test_foocompare.py
F                                                                                                                                                  [100%]
======================================================================= FAILURES ========================================================================
______________________________________________________________________ test_mytest ______________________________________________________________________

    def test_mytest():
        f1 = Foo(1)
        f2 = Foo(2)
>       assert f1 == f2
E       assert Comparing Foo instances:
E            vals: 1 != 2

test_foocompare.py:12: AssertionError
================================================================ short test summary info ================================================================
FAILED test_foocompare.py::test_mytest - assert Comparing Foo instances:
1 failed in 0.10s
```

### 2.5、断言内省细节

通过在​`assert`​语句运行之前重写它们，可以报告关于失败断言的详细信息。重写的断言语句将自省信息放入断言失败消息中。pytest只重写由其测试收集过程直接发现的测试模块，因此在不属于测试模块的支持模块中的断言不会被重写。

您可以在导入模块之前通过调用 ​`register_assert_rewrite` ​手动为导入的模块启用断言重写（这样做的好地方是在您的根目录 ​`conftest.py`​ 中）。

### 2.6、 断言重写将文件缓存到硬盘上

pytest 会将重写的模块写回磁盘进行缓存。 您可以通过将其添加到 ​`conftest.py`​ 文件的顶部来禁用此行为（例如，避免在经常移动文件的项目中留下陈旧的​ `.pyc`​ 文件）：

```
import sys

sys.dont_write_bytecode = True
```

请注意，您仍然可以获得断言自省的好处，唯一的变化是 ​`.pyc`​ 文件不会缓存在磁盘上。

此外，如果无法写入新的 ​`.pyc`​ 文件，即在只读文件系统或 zip 文件中，重写将静默跳过缓存。

### 2.7、禁用断言重写

pytest 在导入时重写测试模块，方法是使用导入钩子编写新的 ​`pyc`​ 文件。大多数情况下，这是透明的。如果您自己使用导入，导入钩子可能会干扰。

如果是这种情况，你有两个选择:

- 通过将字符串​`PYTEST_DONT_REWRITE`​添加到其文档字符串中，禁用特定模块的重写。
- 使用​`assert=plain`​禁用所有模块的重写。

## 3、pytest 核心功能-使用fixtures

### 3.1、pytest fixture-请求fixture

#### 3.1.1、什么是fixture

在测试中，​`fixture`​为测试 提供了一个定义好的、可靠的和一致的上下文。这可能包括环境（例如配置有已知参数的数据库）或内容（例如数据集）。  
​`Fixtures` ​定义了构成测试排列阶段的步骤和数据。在 pytest 中，它们是您定义的用于此目的的函数。它们也可以用来定义测试的行为阶段；这是设计更复杂测试的强大技术。  
由​`fixture`​设置的服务、状态或其他操作环境由测试函数通过参数访问。对于测试函数使用的每个​`fixture`​，在测试函数的定义中通常都有一个参数（以​`fixture`​命名）  

在基本级别上，测试函数通过将​​`fixture`​​声明为参数来请求它们所需要的​​`fixture`​​。

当pytest运行一个测试时，它会查看该测试函数签名中的参数，然后搜索与这些参数具有相同名称的​​`fixture`​​。一旦pytest找到它们，它就运行这些​​`fixture`​​，捕获它们返回的内容(如果有的话)，并将这些对象作为参数传递给测试函数。

#### 3.1.2、快速示例

```
import pytest


class Fruit:
    def __init__(self, name):
        self.name = name
        self.cubed = False

    def cube(self):
        self.cubed = True


class FruitSalad:
    def __init__(self, *fruit_bowl):
        self.fruit = fruit_bowl
        self._cube_fruit()

    def _cube_fruit(self):
        for fruit in self.fruit:
            fruit.cube()


# Arrange
@pytest.fixture
def fruit_bowl():
    return [Fruit("apple"), Fruit("banana")]


def test_fruit_salad(fruit_bowl):
    # Act
    fruit_salad = FruitSalad(*fruit_bowl)

    # Assert
    assert all(fruit.cubed for fruit in fruit_salad.fruit)
```

在这个例子中，​​`test_fruit_salad`​​请求​​`fruit_bowl`​​(即​​`def test_fruit_salad(fruit_bowl):​`​)，当pytest看到这个时，它将执行​​`fruit_bowl fixture`​​函数，并将它返回的对象作为​​`fruit_bowl`​​参数传递给​​`test_fruit_salad`​​

如果我们手动进行，大致会发生以下情况：

```
def fruit_bowl():
    return [Fruit("apple"), Fruit("banana")]


def test_fruit_salad(fruit_bowl):
    # Act
    fruit_salad = FruitSalad(*fruit_bowl)

    # Assert
    assert all(fruit.cubed for fruit in fruit_salad.fruit)


# Arrange
bowl = fruit_bowl()
test_fruit_salad(fruit_bowl=bowl)
```

#### 3.1.3、Fixtures可以请求其他fixtures

pytest最大的优势之一是它极其灵活的​​`fixture`​​系统。它允许我们将测试的复杂需求归结为更简单和更有组织的功能，我们只需要让每个功能描述它们所依赖的东西。我们将进一步深入讨论这个问题，但现在，这里有一个快速的例子来演示​​`fixtures`​​如何使用其他​​`fixtures`​​:

```
# contents of test_append.py
import pytest


# Arrange
@pytest.fixture
def first_entry():
    return "a"


# Arrange
@pytest.fixture
def order(first_entry):
    return [first_entry]


def test_string(order):
    # Act
    order.append("b")

    # Assert
    assert order == ["a", "b"]
```

请注意，这与上面的示例相同，但变化很小。 pytest 中的​​`fixture`​请求​​`fixture` ​就像测试一样。 所有相同的请求规则都适用于用于测试的​​`fixture`​​。 如果我们手动完成，这个例子的工作方式如下：

```
def first_entry():
    return "a"


def order(first_entry):
    return [first_entry]


def test_string(order):
    # Act
    order.append("b")

    # Assert
    assert order == ["a", "b"]


entry = first_entry()
the_list = order(first_entry=entry)
test_string(order=the_list)
```
