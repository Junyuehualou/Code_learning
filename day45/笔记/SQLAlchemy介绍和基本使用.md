## ORM 对象 关系 映射模型    object relationship mapping

> 一个类就是一个model 然后可以将model映射到数据库中    对象模型 与数据表的映射 

```
#
# class Person(object):
#     name = 'xx'
#     age = 18
#     country = 'xx'
#
# p = Person('xx','xx')
# Person -> 数据表  名字
#Person 的属性  -> 一张表的字段
#Person类的对象  -> 一张表的数据行
```





# SQLAlchemy介绍和基本使用

数据库是一个网站的基础。`Flask`可以使用很多种数据库。比如`MySQL`，`MongoDB`,`SQLite`,`PostgreSQL`等。这里我们以`MySQL`为例进行讲解。而在`Flask`中，如果想要操作数据库，我们可以使用`ORM`来操作数据库，使用`ORM`操作数据库将变得非常简单。

在讲解`Flask`中的数据库操作之前，先确保你已经安装了以下软件：

- `mysql`：如果是在`windows`上，到[官网](http://dev.mysql.com/downloads/windows/)下载。如果是`ubuntu`，通过命令`sudo apt-get install mysql-server libmysqlclient-dev -yq`进行下载安装。
- `MySQLdb`：`MySQLdb`是用`Python`来操作`mysql`的包，因此通过`pip`来安装，命令如下：`pip install mysql-python`。
- `pymysql`：`pymysql`是用`Python`来操作`mysql`的包，因此通过`pip`来安装，命令如下：`pip3 install pymysql`。如果您用的是`Python 3`，请安装`pymysql`。
- `SQLAlchemy`：`SQLAlchemy`是一个数据库的`ORM`框架，我们在后面会用到。安装命令为：`pip3 install SQLAlchemy`。

### 通过`SQLAlchemy`连接数据库：

首先来看一段代码：

```python
from sqlalchemy import create_engine

# 数据库的配置变量
HOSTNAME = '127.0.0.1'
PORT     = '3306'
DATABASE = 'xt_flask'
USERNAME = 'root'
PASSWORD = 'root'
DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)

# 创建数据库引擎
engine = create_engine(DB_URI)

#创建连接
with engine.connect() as con:
    rs = con.execute('SELECT 1')
    print rs.fetchone()
```

首先从`sqlalchemy`中导入`create_engine`，用这个函数来创建引擎，然后用`engine.connect()`来连接数据库。其中一个比较重要的一点是，通过`create_engine`函数的时候，需要传递一个满足某种格式的字符串，对这个字符串的格式来进行解释：

```
dialect+driver://username:password@host:port/database?charset=utf8
```

`dialect`是数据库的实现，比如`MySQL`、`PostgreSQL`、`SQLite`，并且转换成小写。`driver`是`Python`对应的驱动，如果不指定，会选择默认的驱动，比如MySQL的默认驱动是`MySQLdb`。`username`是连接数据库的用户名，`password`是连接数据库的密码，`host`是连接数据库的域名，`port`是数据库监听的端口号，`database`是连接哪个数据库的名字。

如果以上输出了`1`，说明`SQLAlchemy`能成功连接到数据库。

### 用SQLAlchemy执行原生SQL：

我们将上一个例子中的数据库配置选项单独放在一个`constants.py`的文件中，看以下例子：

```python
from sqlalchemy import create_engine
from constants import DB_URI

#连接数据库
engine = create_engine(DB_URI,echo=True)

# 使用with语句连接数据库，如果发生异常会被捕获
with engine.connect() as con:
    # 先删除users表
    con.execute('drop table if exists authors')
    # 创建一个users表，有自增长的id和name
    con.execute('create table authors(id int primary key auto_increment,'name varchar(25))')
    # 插入两条数据到表中
    con.execute('insert into persons(name) values("abc")')
    con.execute('insert into persons(name) values("xiaotuo")')
    # 执行查询操作
    results = con.execute('select * from persons')
    # 从查找的结果中遍历
    for result in results:
        print(result)
```