"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time:2023/6/21 9:43
# @Author:Szeto YiZe
# @File:python_mysql.py
# @Update:对MySQL数据库操作进行封装的 Python 代码实现，包括对数据库进行新建、插入、查询、修改等操作
"""

'''
# 1. 新建数据库：

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  passwd="yourpassword"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE mydatabase")

# 2. 插入数据：

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  passwd="yourpassword",
  database="mydatabase"
)

mycursor = mydb.cursor()

sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
val = ("John", "Highway 21")
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")

# 3. 查询数据：

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  passwd="yourpassword",
  database="mydatabase"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM customers")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)

# 4. 修改数据：

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  passwd="yourpassword",
  database="mydatabase"
)

mycursor = mydb.cursor()

# 修改数据
sql = "UPDATE customers SET address = %s WHERE address = %s"
val = ("New Address", "Old Address")
mycursor.execute(sql, val)

# 提交更改
mydb.commit()

# 输出更改后的行数
print(mycursor.rowcount, "record(s) affected")

'''

import mysql.connector

class MySQLDatabase:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        self.connect()
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.close()
        return result

    def execute_update(self, query, params=None):
        self.connect()
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.connection.commit()
        count = self.cursor.rowcount
        self.close()
        return count
