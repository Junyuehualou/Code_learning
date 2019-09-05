# 类视图

之前我们接触的视图都是函数，所以一般简称视图函数。其实视图也可以基于类来实现，类视图的好处是支持继承，但是类视图不能跟函数视图一样，写完类视图还需要通过`app.add_url_rule(url_rule,view_func)`来进行注册。以下将对两种类视图进行讲解：

## 标准类视图：

标准类视图是继承自`flask.views.View`，并且在子类中必须实现`dispatch_request`方法，这个方法类似于视图函数，也要返回一个基于`Response`或者其子类的对象。以下将用一个例子进行讲解：

```python
from flask.views import View
class PersonalView(View):
    def dispatch_request(self):
        return "kangbazi"
# 类视图通过add_url_rule方法和url做映射
app.add_url_rule('/users/',view_func=PersonalView.as_view('personalview'))
```

### 基于调度方法的视图：

`Flask`还为我们提供了另外一种类视图`flask.views.MethodView`，对每个HTTP方法执行不同的函数（映射到对应方法的小写的同名方法上），以下将用一个例子来进行讲解：

```python
    class LoginView(views.MethodView):
        # 当客户端通过get方法进行访问的时候执行的函数
        def get(self):
            return render_template("login.html")

        # 当客户端通过post方法进行访问的时候执行的函数
        def post(self):
            email = request.form.get("email")
            password = request.form.get("password")
            if email == 'xx@qq.com' and password == '111111':
                return "登录成功！"
            else:
                return "用户名或密码错误！"

    # 通过add_url_rule添加类视图和url的映射，并且在as_view方法中指定该url的名称，方便url_for函数调用

    app.add_url_rule('/myuser/',view_func=LoginView.as_view('loginview'))
```

用类视图的一个缺陷就是比较难用装饰器来装饰，比如有时候需要做权限验证的时候，比如看以下例子：

```python
from flask import session
def login_required(func):
    def wrapper(*args,**kwargs):
        if not session.get("user_id"):
            return 'auth failure'
        return func(*args,**kwargs)
    return wrapper
```

装饰器写完后，可以在类视图中定义一个属性叫做`decorators`，然后存储装饰器。以后每次调用这个类视图的时候，就会执行这个装饰器。示例代码如下：

```python
class UserView(views.MethodView):
    decorators = [user_required]
    ...
```