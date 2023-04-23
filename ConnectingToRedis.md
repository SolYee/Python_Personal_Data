##链接redis，修改验证次数

在自动化测试过程中，我们在修改设备验证次数和收取手机号验证码次数以及密码错误次数，无法实现自动化，故此我们直接使用机器连接到Redis中去修改

首先要下载两个库

`redis  2.10.6

redis-py-cluster  1.3.5`

再对其进行封装方便以后的使用

```python
from rediscluster import StrictRedisCluster


def deviceOR(num, count):
    """修改设备验证次数

    :param num:键
    :param count:设备号device
    :return:
    """
    # nodes传入的redis的ip和port和db
    nodes = [{"host": "192.168.1.201", "port": "8001", "db": 0}]
    # 链接redis池
    r = StrictRedisCluster(startup_nodes=nodes, decode_responses=True)
    # 根据建get到相关键值
    res = r.get("sms:count:" + str(num) + ":" + count)
    if int(res) > 10:
        # 修改键值
        r.set("sms:count:" + str(num) + ":" + count, "1")


def phoneOR(num, area, count):
    """修改手机号验证次数

    :param num:键
    :param area:地区号
    :param count:手机号
    :return:
    """
    # nodes传入的redis的ip和port和db
    nodes = [{"host": "192.168.1.201", "port": "8001", "db": 0}]
    # 链接redis池
    r = StrictRedisCluster(startup_nodes=nodes, decode_responses=True)
    # 根据建get到相关键值
    res = r.get("sms:count:" + str(num) + ":" + area + count)
    if int(res) > 10:
        # 修改键值
        r.set("sms:count:" + str(num) + ":" + area + count, "1")

def phoneORpwd(count):
    """修改手机号密码错误次数


    :param count:手机号
    :return:
    """
    # nodes传入的redis的ip和port和db
    nodes = [{"host": "192.168.1.201", "port": "8001", "db": 0}]
    # 链接redis池
    r = StrictRedisCluster(startup_nodes=nodes, decode_responses=True)
    # 根据建get到相关键值
    res = r.get("ua:count:login_pwd_error:" + count)
    if int(res) >= 10:
        # 修改键值
        r.set("ua:count:login_pwd_error:" + count, "1")

# deviceORphone("d41b071ca83ece2")
# phoneOR(2,"15816262885")
# phoneORpwd("15810145901")

```
以上这段代码主要是使用 Redis 存储和修改设备验证次数、手机号验证次数和手机号密码错误次数的功能。以下是对代码的解析和优化：

1. 代码重复度高：三个函数的代码结构几乎一致，只是传入的参数不同，可以将相同的代码提取出来，封装成一个函数，用于连接 Redis，避免代码重复。
```python
def get_redis_conn():
    """连接 Redis

    :return: Redis 连接对象
    """
    nodes = [{"host": "192.168.1.201", "port": "8001", "db": 0}]
    return StrictRedisCluster(startup_nodes=nodes, decode_responses=True)
```

2. 函数命名不规范：函数命名中包含了 “OR”，不太符合函数的实际作用，建议改为更加明确的名称。

3. 冗余代码：在修改键值时，部分代码可以简化，如下所示：

```python
# 修改键值
if int(res) > 10:
    r.set("sms:count:%s:%s" % (num, count), "1")
```

4. 函数注释不够详细：函数的注释中只是简单说明了函数的作用，可以增加更多的注释，如参数的含义、返回值等。

5. 函数中的硬编码：函数中的 Redis 连接信息硬编码在函数中，如果需要修改连接信息，需要修改多处代码，不够灵活，可以将连接信息提取出来，作为参数传入函数中。

综上所述，以下是对代码进行优化后的版本：

```python
def get_redis_conn(host, port, db):
    """连接 Redis

    :param host: Redis 服务器地址
    :param port: Redis 端口号
    :param db: Redis 数据库号
    :return: Redis 连接对象
    """
    nodes = [{"host": host, "port": port, "db": db}]
    return StrictRedisCluster(startup_nodes=nodes, decode_responses=True)


def update_device_count(num, count, host, port, db):
    """修改设备验证次数

    :param num: 键
    :param count: 设备号
    :param host: Redis 服务器地址
    :param port: Redis 端口号
    :param db: Redis 数据库号
    """
    r = get_redis_conn(host, port, db)
    res = r.get("sms:count:%s:%s" % (num, count))
    if int(res) > 10:
        r.set("sms:count:%s:%s" % (num, count), "1")


def update_phone_count(num, area, count, host, port, db):
    """修改手机号验证次数

    :param num: 键
    :param area: 地区号
    :param count: 手机号
    :param host: Redis 服务器地址
    :param port: Redis 端口号
    :param db: Redis 数据库号
    """
    r = get_redis_conn(host, port, db)
    res = r.get("sms:count:%s:%s%s" % (num, area, count))
    if int(res) > 10:
        r.set("sms:count:%s:%s%s" % (num, area, count), "1")


def update_phone_pwd_error_count(count, host, port, db):
    """修改手机号密码错误次数

    :param count: 手机号
    :param host: Redis 服务器地址
    :param port: Redis 端口号
    :param db: Redis 数据库号
    """
    r = get_redis_conn(host, port, db)
    res = r.get("ua:count:login_pwd_error:%s" % count)
    if int(res) >= 10:
        r.set("ua:count:login_pwd_error:%s" % count, "1")
```

在使用时，可以根据实际情况传入 Redis 服务器的地址、端口号和数据库号，调用相应的函数即可。

`StrictRedisCluster`是`redis-py-cluster`库中的一个类，用于连接 Redis 集群。`redis-py-cluster`是一个基于`redis-py`的 Redis 集群客户端，可以方便地连接 Redis 集群，执行读写操作。

在上述代码中，`StrictRedisCluster`类的实例被用作 Redis 连接对象，它接受一个包含 Redis 节点信息的列表作为参数，这里只有一个节点信息。`decode_responses=True`参数用于将 Redis 返回的二进制数据解码成字符串，这样可以方便地处理 Redis 中存储的数据。

如果你想要使用`StrictRedisCluster`类，需要先安装`redis-py-cluster`库，可以使用`pip`命令来安装：

```
pip install redis-py-cluster
```

安装完成后，就可以在 Python 代码中使用`StrictRedisCluster`类了。需要注意的是，如果你连接的是 Redis 单机版，应该使用`StrictRedis`类来代替`StrictRedisCluster`类，例如：

```python
from redis import StrictRedis

def get_redis_conn():
    """连接 Redis

    :return: Redis 连接对象
    """
    return StrictRedis(host="localhost", port=6379, db=0)
```

这里使用`StrictRedis`类来连接 Redis 单机版，`host`参数表示 Redis 服务器地址，`port`参数表示 Redis 服务器端口号，`db`参数表示 Redis 数据库编号。