##python连接数据库的操作
python's operation of connecting to a database

首先我们先写一个使用Python连接数据库并获取数据的示例代码如下：

```python
import pymysql

# 连接数据库
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='password',
    db='mydatabase'
)

# 获取游标
cursor = connection.cursor()

# 查询数据
sql = "SELECT * FROM mytable"
cursor.execute(sql)

# 获取数据
result = cursor.fetchall()
for row in result:
    print(row)

# 关闭游标和连接
cursor.close()
connection.close()
```
在这个示例中，我们使用了Python的pymysql模块来连接MySQL数据库。首先，我们使用`pymysql.connect`函数连接到了本地的MySQL数据库。然后，我们使用`connection.cursor()`方法获取游标对象。接着，我们使用`cursor.execute`方法执行了一条查询语句，并使用`cursor.fetchall`方法获取了所有的查询结果。最后，我们使用`cursor.close`和`connection.close`方法关闭游标和连接。

那么，我们开始对代码进行封装。
# python连接数据库的操作封装
```python
# 操作数据库
import pymysql

from Common.tools.write_xlsx import write_xlsx


class OperationSql:
    _conn = None
    _cursor = None

    def __init__(self, address, user, password, database):
        """

        :param address: IP地址
        :param user: 用户名
        :param password: 密码
        :param database: 数据库名
        """
        self.address = address
        self.user = user
        self.password = password
        self.database = database

    # 获取连接数据库
    def get_connect_sql(self):
        if self._conn is None:
            self._conn = pymysql.connect(self.address, self.user, self.password, self.database)
        return self._conn

    # 获取创建游标
    def get_newCursor(self):
        if self._cursor is None:
            self._cursor = self.get_connect_sql().cursor()
        return self._cursor

    # 关闭数据库连接
    def close_sql_connect(self):
        if self._conn is not None:
            self.get_connect_sql().close()
            self._conn = None

    # 关闭游标
    def close_cursor(self):
        if self._cursor is not None:
            self.get_newCursor().close()
            self._cursor = None

    # 操作数据库
    def show_sql(self, sql):
        try:
            # 创建游标
            cursor = self.get_newCursor()
            cursor.execute(sql)
            data = cursor.fetchall()
        except Exception as e:
            raise e
        finally:
            self.close_cursor()
            self.close_sql_connect()
        # print(data)
        return data





# 使用pymongo模块连接mongoDB数据库
# coding=utf-8
from pymongo import MongoClient


def MongoDB(address, port, database, surface, key, price):
    """

    :param address:ip地址
    :param port: 端口号
    :param database: 数据名
    :param surface: 表名
    :param key: 键
    :param price:值
    :return:返回查询的MongoDB数据库里面的符合条件的所有数据
    """
    # 建立MongoDB数据库连接
    client = MongoClient(address, port)

    # 连接所需数据库,database为数据库名
    db = client[database]

    # 连接所用集合，也就是我们通常所说的表，surface为表名
    collection = db[surface]

    # 接下里就可以用collection来完成对数据库表的一些操作

    # 查找集合中所有数据
    # for item in collection.find():
    #     print(item)

    # 查找集合中单条数据
    mydoc = collection.find({key: price})
    list1 = list()
    for x in mydoc:
        # print(x)
        list1.append(x)
    return list1
```


以上代码定义了`OperationSql`和`MongoDB`两个类，分别用于连接MySQL和MongoDB数据库，并执行查询操作。下面对每个类的方法进行解释：

`OperationSql`类：

- `__init__`方法：初始化连接MySQL数据库所需的IP地址、用户名、密码和数据库名。
- `get_connect_sql`方法：获取MySQL数据库连接对象。
- `get_newCursor`方法：获取MySQL数据库游标对象。
- `close_sql_connect`方法：关闭MySQL数据库连接。
- `close_cursor`方法：关闭MySQL数据库游标。
- `show_sql`方法：执行MySQL数据库查询语句，并返回查询结果。

`MongoDB`类：

- `MongoDB`方法：连接MongoDB数据库，并执行查询操作。需要传入MongoDB数据库的IP地址、端口号、数据库名、表名、查询所需的键和值。
- 在该方法中，首先使用`MongoClient`类连接MongoDB数据库，然后使用`db[surface]`获取表对象，使用`collection.find({key: price})`查询符合条件的所有数据，并将查询结果存储在列表中返回。

在这两个类中，都使用了连接数据库后必须关闭连接和游标的方式，以免长时间占用数据库资源。

最后我发现上面代码还能再进行优化。故此，我开始对其进行再次优化。
先说下思路，具体如下：

1. 对`OperationSql`类的`get_connect_sql`和`get_newCursor`方法进行优化，让它们在首次调用时才获取连接和游标对象，避免重复获取。

2. 对`OperationSql`类的`show_sql`方法进行优化，使用`with`语句管理连接和游标对象的生命周期，避免忘记关闭连接和游标。

3. 对`MongoDB`类的`MongoDB`方法进行优化，使用`with`语句管理MongoDB连接的生命周期，避免忘记关闭连接。

```python
# 操作数据库
import pymysql

from Common.tools.write_xlsx import write_xlsx


class OperationSql:
    def __init__(self, address, user, password, database):
        """
        :param address: IP地址
        :param user: 用户名
        :param password: 密码
        :param database: 数据库名
        """
        self.address = address
        self.user = user
        self.password = password
        self.database = database
        self._conn = None
        self._cursor = None

    # 获取连接数据库
    def get_connect_sql(self):
        if not self._conn:
            self._conn = pymysql.connect(self.address, self.user, self.password, self.database)
        return self._conn

    # 获取创建游标
    def get_newCursor(self):
        if not self._cursor:
            self._cursor = self.get_connect_sql().cursor()
        return self._cursor

    # 操作数据库
    def show_sql(self, sql):
        with self.get_connect_sql() as conn, conn.cursor() as cursor:
            cursor.execute(sql)
            data = cursor.fetchall()
        return data


# 使用pymongo模块连接mongoDB数据库
# coding=utf-8
from pymongo import MongoClient


def MongoDB(address, port, database, surface, key, price):
    """
    :param address:ip地址
    :param port: 端口号
    :param database: 数据名
    :param surface: 表名
    :param key: 键
    :param price:值
    :return:返回查询的MongoDB数据库里面的符合条件的所有数据
    """
    # 建立MongoDB数据库连接
    with MongoClient(address, port) as client:
        # 连接所需数据库,database为数据库名
        db = client[database]

        # 连接所用集合，也就是我们通常所说的表，surface为表名
        collection = db[surface]

        # 接下里就可以用collection来完成对数据库表的一些操作

        # 查找集合中所有数据
        # for item in collection.find():
        #     print(item)

        # 查找集合中单条数据
        mydoc = collection.find({key: price})
        list1 = list()
        for x in mydoc:
            # print(x)
            list1.append(x)
        return list1
        
```
以上这段代码实现了对 MySQL 数据库和 MongoDB 数据库的连接和操作。

### MySQL 数据库连接和操作

1. `OperationSql`类的构造函数中接受四个参数：`address`、`user`、`password`、`database`，分别表示 MySQL 服务器的 IP 地址、用户名、密码和要操作的数据库名。
2. `get_connect_sql`方法用于获取数据库连接对象。如果连接对象不存在，则创建一个新的连接对象。
3. `get_newCursor`方法用于获取游标对象。如果游标对象不存在，则创建一个新的游标对象。
4. `show_sql`方法用于执行 SQL 语句并返回查询结果。这里使用`with`语句来自动关闭数据库连接和游标对象，避免资源泄漏。

### MongoDB 数据库连接和操作

1. `MongoDB`方法接受六个参数：`address`、`port`、`database`、`surface`、`key`、`price`，分别表示 MongoDB 服务器的 IP 地址、端口号、数据库名、表名、查询的键和值。
2. 使用`MongoClient`类来创建 MongoDB 数据库连接对象。
3. 使用连接对象访问数据库和集合，执行查询操作，最终将符合查询条件的数据返回。

另外，在这段代码中，还调用了一个`write_xlsx`函数，这个函数可能是用来将查询结果写入 Excel 文件的自定义函数，但是在这段代码中并没有给出函数的实现，所以无法对其进行进一步的解析。优化后的代码更加简洁、易读，并且避免了一些潜在的错误。

