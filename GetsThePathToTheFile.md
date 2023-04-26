##python实现生成文件或图片的路径

```python
import os
import time

from PIL import Image
from pandas.tests.dtypes.test_missing import now


# BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# 获取图片大小
def imgSize(img_path):
    """获取图片大小

    :param img_path:
    :return:
    """
    img = Image.open(img_path)
    # print(img.size)
    return img.size


# 生成存放图片路径
def imgURL(name):
    """生成存放图片路径

    :param name:
    :return:
    """
    # random_name = now.strftime("%Y/%m/%d/") + str(round(time.time() * 1000)) + str(random.randint(1000, 9999))
    random_name = str(round(int(time.time())))
    # 存放OSS路径
    file_name = name.format(random_name)
    # print(file_name)
    return file_name


# 生成存放文件路径
def fileURL(name):
    """生成存放文件路径

    :param name:
    :return:
    """
    random_name = now.strftime("%Y%m%d/") + str(round(int(time.time())))
    # 存放OSS路径
    file_name = name.format(random_name)
    # print(file_name)
    return file_name
```
上面的代码用于生成存放文件的路径，对上面代码进行解析说明：
1. 导入os和time模块，以及PIL库中的Image模块，以及pandas.tests.dtypes.test_mising中的now模块，用于获取图片大小，生成存放图片和文件路径。

2. 定义imgSize函数，用于获取图片大小，参数为图片路径，返回值为图片大小。

3. 定义imgURL函数，用于生成存放图片路径，参数为name，返回值为file_name。

4. 定义fileURL函数，用于生成存放文件路径，参数为name，返回值为file_name。

我们开始对以上代码进行优化封装：
```python 
import os
import time
import random

from PIL import Image
from pandas.tests.dtypes.test_mising import now


# BASE_DIR = os.path.dirname(os.path.abspath(_file_)


def get_img_size(img_path):
    """获取图片大小
    
    :param img_path:
    :return
    """
    img = Image.open(img_path)
    # print(img.size)
    return img.size
    

def generate_img_url(name):
    """生成存放图片路径
    
    :param name:
    :return:
    """
    random_name = str(round(int(time.time()
    # 存放OS路径
    file_name = name.format(random_name)
    # print(file_name)
    return file_name


def generate_file_url(name):
    """生成存放文件路径
    
    :param name:
    :return:
    """
    random_name = now.strftime("%Y%m%d/") + str(round(int(time.time()
    # 存放OS路径
    file_name = name.format(random_name)
    # print(file_name)
    return file_name
```

我们对以上这段封装代码进行解析：
1. 首先导入了time、random和PIL库，time库用于获取当前时间，random库用于生成随机数，PIL库用于处理图片；
2. 然后定义了三个函数，get_img_size()用于获取图片大小，generate_img_url()用于生成存放图片路径，generate_file_url()用于生成存放文件路径；
3. get_img_size()函数中，使用Image.open()方法打开图片，并使用img.size获取图片大小；
4. generate_img_url()函数中，使用time.time()获取当前时间，并使用str()方法将其转换为字符串，然后使用name.format()方法生成存放图片路径；
5. generate_file_url()函数中，使用now.strftime()方法获取当前日期，并使用time.time()获取当前时间，然后使用name.format()方法生成存放文件路径。

###你会发现上述代码在python3.8版本能够使用但是在python3.10版本上无法使用。
`pandas.tests.dtypes.test_missing.now` 是一个测试用例中的方法，不应该被用于实际的代码中。
所以在 Python 3.8 中，`pandas.tests.dtypes.test_missing.now` 方法被定义为一个函数，可以被导入并使用。但是在 Python 3.10 中，`pandas.tests.dtypes.test_missing.now` 方法已经被删除，导入会直接抛出 `AttributeError` 异常。
因此， 如果需要获取当前时间，应该使用 Python 标准库 `datetime` 模块中的 `datetime.now()` 方法来获取当前时间。例如：

```
from datetime import datetime

now = datetime.now()
```

如果需要使用 `now` 方法，可以直接将其替换为 `datetime.now()`。
修改代码如下：
```python
from datetime import datetime

now = datetime.now()
```
根据上述原因我们将代码中的 `from pandas.tests.dtypes.test_mising import now` 是一个错误的导入语句，正确的语句应该是 `from datetime import datetime`。
在 Python 3.10 中，由于 `pandas` 库的一些内部变化，这个错误的导入语句会导致 `AttributeError` 异常。因此，需要将其修改为正确的导入语句。
修改后的代码如下所示：
```python
import os
import time
import random

from PIL import Image
from datetime import datetime


# BASE_DIR = os.path.dirname(os.path.abspath(_file_)


def get_img_size(img_path):
    """获取图片大小

    :param img_path:
    :return
    """
    img = Image.open(img_path)
    # print(img.size)
    return img.size


def generate_img_url(name):
    """生成存放图片路径

    :param name:
    :return:
    """
    random_name = str(round(int(time.time())))
    # 存放OS路径
    file_name = name.format(random_name)
    # print(file_name)
    return file_name


def generate_file_url(name):
    """生成存放文件路径

    :param name:
    :return:
    """
    random_name = datetime.now().strftime("%Y%m%d/") + str(round(int(time.time())))
    # 存放OS路径
    file_name = name.format(random_name)
    # print(file_name)
    return file_name
```




