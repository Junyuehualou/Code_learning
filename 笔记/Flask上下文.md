# Flask上下文

`Flask`项目中有两个上下文，一个是应用上下文（app），另外一个是请求上下文（request）。请求上下文`request`和应用上下文`current_app`都是一个全局变量。所有请求都共享的。`Flask`有特殊的机制可以保证每次请求的数据都是隔离的，即A请求所产生的数据不会影响到B请求。所以可以直接导入`request`对象，也不会被一些脏数据影响了，并且不需要在每个函数中使用request的时候传入`request`对象。这两个上下文具体的实现方式和原理可以没必要详细了解。只要了解这两个上下文的四个属性就可以了：

- request：请求上下文上的对象。这个对象一般用来保存一些请求的变量。比如`method`、`args`、`form`等。
- session：请求上下文上的对象。这个对象一般用来保存一些会话信息。
- current_app：返回当前的app。
- g：应用上下文上的对象。处理请求时用作临时存储的对象。

# 常用的钩子函数

- before_first_request：处理第一次请求之前执行。例如以下代码：

  ```python
    @app.before_first_request
    def first_request():
        print 'first time request'
  ```

- before_request：在每次请求之前执行。通常可以用这个装饰器来给视图函数增加一些变量。例如以下代码：

  ```python
    @app.before_request
    def before_request():
        if not hasattr(g,'user'):
            setattr(g,'user','xxxx')
  ```

- teardown_appcontext：不管是否有异常，注册的函数都会在每次请求之后执行。

  ```python
    @app.teardown_appcontext
    def teardown(exc=None):
        if exc is None:
            db.session.commit()
        else:
            db.session.rollback()
        db.session.remove()
  ```

- template_filter：在使用

  ```
  Jinja2
  ```

  模板的时候自定义过滤器。比如可以增加一个

  ```
  upper
  ```

  的过滤器（当然Jinja2已经存在这个过滤器，本示例只是为了演示作用）：

  ```python
    @app.template_filter
    def upper_filter(s):
        return s.upper()
  ```

- context_processor：上下文处理器。返回的字典中的键可以在模板上下文中使用。例如：

  ```python
    @app.context_processor
    return {'current_user':'xxx'}
  
  
  index.html 
  
  {{current_user }}
  ```

- errorhandler：errorhandler接收状态码，可以自定义返回这种状态码的响应的处理方法。例如：

  ```python
    @app.errorhandler(404)
    def page_not_found(error):
        return 'This page does not exist',404
  ```