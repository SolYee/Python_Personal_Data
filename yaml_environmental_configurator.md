python实现获取YAML 文件的完整路径
```python
import os
from typing import Union
BASE_DIR: Union[bytes, str] = os.path.dirname(os.path.abspath(__file__))
def get_file_path(folder: str, env: str, filename: str):
    """
    :param folder: 文件夹名称
    :param env: 环境命名文件夹名称
    :param filename: yaml文件名
    :return: 返回文件路径
    """
    file_path = os.path.join(BASE_DIR, folder, env, filename)
    return file_path

```
以上这段代码定义了一个函数 `get_file_path()`，用于获取指定文件夹、环境命名文件夹和 YAML 文件的完整路径。

函数接受三个参数：

- `folder`：文件夹名称。
- `env`：环境命名文件夹名称。
- `filename`：YAML 文件名。

函数通过调用 Python 标准库 `os.path` 模块中的 `join()` 函数，将文件夹名称、环境命名文件夹名称和 YAML 文件名拼接成完整的文件路径。其中，`BASE_DIR` 表示当前 Python 文件所在的目录，使用 `os.path.abspath(__file__)` 函数获取当前 Python 文件的绝对路径，然后使用 `os.path.dirname()` 函数获取该文件所在的目录路径，最后将这个目录路径保存到 `BASE_DIR` 变量中。
使用示例：
```python
config_file_path = get_file_path('config', 'dev', 'config.yml')
print(config_file_path)
```
输出：

```
/home/user/project/config/dev/config.yml
```
读取yaml文件
```python
import yaml
def get_custompath_yam(config_file):
    """读取根据自定义路径的yaml文件获得文件中的数据

    :param config_file:文件路径
    :return:
    """
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config_data

```
定义环境文件名称，以下是yaml文件为主的环境数据

![定义好的环境数据](https://img-blog.csdnimg.cn/a19247fa0d2a46228ed0a83c51c6155f.png)

我们开始对上面的yaml文件进行读取数据，代码如下：
```python
from Common.Tools.Read_Write_Create.read_File_Contents import get_custompath_yam
from Global.Base_setting_info.File_base import BASE_DIR
def ConfigLoader(env):
    """

    :param env: 传入环境
    :return:
    """
    if env == 'dev' or env == 'DEV':
        # datapath = os.path.join(BASE_DIR, 'datas', env, 'datas.yaml')
        datapath = get_file_path('datas', env, 'datas.yaml')

    elif env == 'test' or env == 'TEST':
        # datapath = os.path.join(BASE_DIR, 'datas', env, 'datas.yaml')
        datapath = get_file_path('datas', env, 'datas.yaml')

    elif env == 'pre' or env == 'PRE':
        # datapath = os.path.join(BASE_DIR, 'datas', env, 'datas.yaml')
        datapath = get_file_path('datas', env, 'datas.yaml')

    else:
        raise EnvironmentError(f'Please set up your environment ! Current Context:{env}')
    datas = get_custompath_yam(datapath)
    return env, datas

```
以上这段代码定义了一个函数 `ConfigLoader()`，用于根据环境参数获取对应的 YAML 配置文件内容。

函数接受一个参数：

- `env`：环境参数，可以是 'dev'、'test' 或 'pre'。

函数通过判断传入的环境参数，调用之前定义的 `get_file_path()` 函数获取对应的 YAML 配置文件路径，然后调用之前定义的 `get_custompath_yam()` 函数，获取 YAML 配置文件的内容。最后将环境参数和 YAML 配置文件的内容作为元组返回。

使用示例：
```python
env = 'dev'
env, datas = ConfigLoader(env)
print(env)
print(datas)
```
输出：

```
dev
{'database': {'host': 'localhost', 'port': 3306, 'user': 'root', 'password': '123456', 'database': 'mydb'}}
```
最后写一个yaml文件来控制环境变量，你只需在yaml文件中变更环境即可
代码示例：
```python
def get_ConfigLoader():
    datapath = os.path.join(BASE_DIR, 'datas', 'application_env.yaml')

    data = get_custompath_yam(datapath)
    # with open(datapath, 'r') as f:
    #     data = yaml.safe_load(f)

    # print(data['profiles']['env'])

    return data['profiles']['env']

# print(get_ConfigLoader())
```
最终代码如下：
```python
import yaml
def get_custompath_yam(config_file):
    """读取根据自定义路径的yaml文件获得文件中的数据

    :param config_file:文件路径
    :return:
    """
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config_data
```
```python
import os

import yaml

from Common.Tools.Read_Write_Create.read_File_Contents import get_custompath_yam
from Global.Base_setting_info.File_base import BASE_DIR


def get_file_path(folder: str, env: str, filename: str) -> str:
    """
    :param folder: 文件夹名称
    :param env: 环境命名文件夹名称
    :param filename: yaml文件名
    :return: 返回文件路径
    """
    file_path = os.path.join(BASE_DIR, folder, env, filename)
    return file_path


def ConfigLoader(env):
    """

    :param env: 传入环境
    :return:
    """
    if env == 'dev' or env == 'DEV':
        # datapath = os.path.join(BASE_DIR, 'datas', env, 'datas.yaml')
        datapath = get_file_path('datas', env, 'datas.yaml')

    elif env == 'test' or env == 'TEST':
        # datapath = os.path.join(BASE_DIR, 'datas', env, 'datas.yaml')
        datapath = get_file_path('datas', env, 'datas.yaml')

    elif env == 'pre' or env == 'PRE':
        # datapath = os.path.join(BASE_DIR, 'datas', env, 'datas.yaml')
        datapath = get_file_path('datas', env, 'datas.yaml')

    else:
        raise EnvironmentError(f'Please set up your environment ! Current Context:{env}')
    datas = get_custompath_yam(datapath)
    return env, datas


# print(ConfigLoader('dev'))


def get_ConfigLoader():
    datapath = os.path.join(BASE_DIR, 'datas', 'application_env.yaml')

    data = get_custompath_yam(datapath)
    # with open(datapath, 'r') as f:
    #     data = yaml.safe_load(f)

    # print(data['profiles']['env'])
    env=data['profiles']['env']

    return ConfigLoader(env)

# print(get_ConfigLoader())

```
最终输出：
```
('test', {'TEST': {'app': {'host': 'http://192.168.**.***', 'port': None}, 'console': {'host': 'http://192.168.**.***', 'port': None}}})
```