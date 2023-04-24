##Python中'Callable'的使用变化
关于这个问题“ Using or importing the ABCs from 'collections' instead of from 'collections. abc' is deprecated since Python 3.3, and in 3.10 it will stop workin”
提示你在代码中使用了即将被弃用的函数或配置项。具体来说，python中的`collections.Callable`将在Python 3.10中停止工作，应该使用`collections.abc.Callable`代替。

你可以使用`sys.version_info`来获取当前Python解释器的版本信息，并判断是否需要进行兼容处理。下面是一个示例代码：

```python
import sys
import collections
from collections.abc import Callable

if sys.version_info >= (3, 3):
    # Python 3.3及以上版本，使用collections.abc模块中的Callable
    return isinstance(x, Callable)
else:
    # Python 3.3以下版本，使用collections模块中的Callable
    return isinstance(x, collections.Callable)

```

这样，就可以根据Python解释器的版本来选择使用哪个版本的`Callable`了。
我们可以将以上这段代码封装成一个函数，以便在其他地方使用：

```python
import sys
import collections
from collections.abc import Callable


def is_callable(x):
    """
    检查x是否可调用
    """
    if sys.version_info >= (3, 3):
        # Python 3.3及以上版本，使用collections.abc模块中的Callable
        return isinstance(x, Callable)
    else:
        # Python 3.3以下版本，使用collections模块中的Callable
        return isinstance(x, collections.Callable)

```

这样，在其他地方就可以直接调用`is_callable`函数来检查一个对象是否可调用了，而不必每次都写一遍判断Python版本、导入`collections.abc.Callable`和调用`isinstance`函数。