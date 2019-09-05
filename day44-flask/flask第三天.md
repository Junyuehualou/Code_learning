# flask第三天  

## 控制语句  

所有的控制语句都是放在`{% ... %}`中，并且有一个语句`{% endxxx %}`来进行结束，`Jinja`中常用的控制语句有`if/for..in..`，现对他们进行讲解：

1. `if`：if语句和`python`中的类似，可以使用`>，<，<=，>=，==，!=`来进行判断，也可以通过`and，or，not，()`来进行逻辑合并操作，以下看例子：

   ```
   {% if kenny.sick %}
      Kenny is sick.
   {% elif kenny.dead %}
    You killed Kenny!  You bastard!!!
   {% else %}
    Kenny looks okay --- so far
   {% endif %}
   ```

2. `for...in...`：`for`循环可以遍历任何一个序列包括列表、字典、元组。并且可以进行反向遍历，以下将用几个例子进行解释：

   - 普通的遍历：

     ```html
        <ul>
        {% for user in users %}
        <li>{{ user.username|e }}</li>
        {% endfor %}
        </ul>
     ```

   - a遍历字典：

     ```html
        <dl>
        {% for key, value in my_dict.iteritems() %}
        <dt>{{ key|e }}</dt>
        <dd>{{ value|e }}</dd>
        {% endfor %}
        </dl>
     ```

   - 如果序列中没有值的时候，进入`else`：

     ```html
        <ul>
        {% for user in users %}
        <li>{{ user.username|e }}</li>
        {% else %}
        <li><em>no users found</em></li>
        {% endfor %}
        </ul>
     ```

   并且`Jinja`中的`for`循环还包含以下变量，可以用来获取当前的遍历状态：

   | 变量 | 描述 | | --- | --- | | loop.index | 当前迭代的索引（从1开始） | | loop.index0 | 当前迭代的索引（从0开始） | | loop.first | 是否是第一次迭代，返回True或False | | loop.last | 是否是最后一次迭代，返回True或False | | loop.length | 序列的长度 |

   另外，不可以使用`continue`和`break`表达式来控制循环的执行。

   ```python
       <table border="1">
           <tbody>
               {% for x in range(1,10) %}
               <tr>
                  {% for y in range(1,10) if y<=x %}
                       <td>{{ y }} * {{ x }} = {{ x*y }}</td>
                  {% endfor %}
   
               </tr>
               {% endfor %}
   
           </tbody>
       </table>
   
   ```

   

# 转义

转义的概念是，在模板渲染字符串的时候，字符串有可能包括一些非常危险的字符比如`<`、`>`等，这些字符会破坏掉原来`HTML`标签的结构，更严重的可能会发生`XSS`跨域脚本攻击，因此如果碰到`<`、`>`这些字符的时候，应该转义成`HTML`能正确表示这些字符的写法，比如`>`在`HTML`中应该用`&lt;`来表示等。

但是`Flask`中默认没有开启全局自动转义，针对那些以`.html`、`.htm`、`.xml`和`.xhtml`结尾的文件，如果采用`render_template`函数进行渲染的，则会开启自动转义。并且当用`render_template_string`函数的时候，会将所有的字符串进行转义后再渲染。而对于`Jinja2`默认没有开启全局自动转义，作者有自己的原因：

1. 渲染到模板中的字符串并不是所有都是危险的，大部分还是没有问题的，如果开启自动转义，那么将会带来大量的不必要的开销。
2. `Jinja2`很难获取当前的字符串是否已经被转义过了，因此如果开启自动转义，将对一些已经被转义过的字符串发生二次转义，在渲染后会破坏原来的字符串。

在没有开启自动转义的模式下（比如以`.conf`结尾的文件），对于一些不信任的字符串，可以通过`{{ content_html|e }}`或者是`{{ content_html|escape }}`的方式进行转义。在开启了自动转义的模式下，如果想关闭自动转义，可以通过`{{ content_html|safe }}`的方式关闭自动转义。而`{%autoescape true/false%}...{%endautoescape%}`可以将一段代码块放在中间，来关闭或开启自动转义，例如以下代码关闭了自动转义：

```
{% autoescape false %}   false
  <p>autoescaping is disabled here
  <p>{{ will_not_be_escaped }}
{% endautoescape %}
```



# 宏和import语句

### 宏：

模板中的宏跟python中的函数类似，可以传递参数，但是不能有返回值，可以将一些经常用到的代码片段放到宏中，然后把一些不固定的值抽取出来当成一个变量，以下将用一个例子来进行解释：

```
    {% macro input(name, value='', type='text') %}
        <input type="{{ type }}" name="{{ name }}" value="{{ value|e }}">
    {% endmacro %}
```

以上例子可以抽取出了一个input标签，指定了一些默认参数。那么我们以后创建`input`标签的时候，可以通过他快速的创建：

```html
    <p>{{ input('username') }}</p>
    <p>{{ input('password', type='password') }}</p>
```

### import语句：

在真实的开发中，会将一些常用的宏单独放在一个文件中，在需要使用的时候，再从这个文件中进行导入。`import`语句的用法跟`python`中的`import`类似，可以直接`import...as...`，也可以`from...import...`或者`from...import...as...`，假设现在有一个文件，叫做`forms.html`，里面有两个宏分别为`input`和`textarea`，如下：

```html
    forms.html：
    {% macro input(name, value='', type='text') %}
        <input type="{{ type }}" value="{{ value|e }}" name="{{ name }}">
    {% endmacro %}

    {% macro textarea(name, value='', rows=10, cols=40) %}
        <textarea name="{{ name }}" rows="{{ rows }}" cols="{{ cols
        }}">{{ value|e }}</textarea>
    {% endmacro %}
```

#### 导入宏的例子：

1. `import...as...`形式：

   ```html
   {% import 'forms.html' as forms %}
   <dl>
     <dt>Username</dt>
     <dd>{{ forms.input('username') }}</dd>
   ```



## include 

> 头部文件和底部文件单独写  主页面 引入即可 

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>首页</title>
</head>
<body>
    {% include 'common/header.html' %}
    <div class="content">
        我是中间内容
    </div>
   
    {% include 'common/footer.html' %}
</body>
</html>
```



## 页面设置 变量  

```
 {% set classroom='python1901' %}
    <p>教室名: {{ classroom }}</p>这个页面都有效

    {% with   %}  username只能with范围内才有效 否则无效  
        {% set username='wuhankangbazi' %}
         <p>who are you? {{ username }}</p>
    {% endwith %}

    <p>who are you? {{ username }}</p>
```





## 导入静态资源 

> url_for('static',filename=“”)

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>首页</title>
    <link rel="stylesheet" href="{{ url_for('static',filename='css/index.css') }}">
    <script src="{{ url_for("static",filename="js/index.js") }}"></script>
</head>
<body>
<img src="{{ url_for("static",filename="images/1.jpg") }}" alt="">
</body>
</html>
```



## 模板继承   

### 继承语法  

```
{% extends 'common/base.html' %}
```

### block 语法  

```
父模板中:
{% block block名字 %}

{% endblock %}

子模板中  
{% block block名字 %}
	子模板的代码 
{% endblock %}

```



### 调用父模板中  block的代码 

```
父模板  
    {% block content %}
        <p style="background: green">我来自父模板</p>
    {% endblock %}
    
子模板  
     {% block content %}
     	{{super()}}  即显示父模板 也显示子模板 
    	<p style="background: red">欢迎来到红浪漫</p>
	{% endblock %}
```



### 调用其它 block 代码  

```
{% block title %} 这里是title
首页
{% endblock %}


{% block content %}  想调用 title 内容 
	{{self.title()}}  这里显示 上面 block 标题的内容    这里就是 title()
    {{ super() }}
    <p style="background: red">欢迎来到红浪漫</p>
{% endblock %}
```



## 蓝图  也有人叫蓝本       blueprint  flask特有的   

> 目的是 相关的视图函数  放到一起  实现 结构清晰    达到解耦的目的  

```
movie.py   

#encoding:utf-8
from flask import Blueprint,render_template,url_for

# movie_bp = Blueprint('movie',__name__,url_prefix='/movie',static_folder="movie_static",template_folder="movie")
movie_bp = Blueprint('movies',__name__,url_prefix='/movie',static_folder="movie_static")

#http://127.0.0.1:5001/user/profile/
@movie_bp.route("/list/")
def list():
    return render_template("movie_list.html")

@movie_bp.route("/detail/")
def detail():
    return '电影详情页面'
    
    

app.py flask实例文件  

from apps.movie import movie_bp

app.register_blueprint(movie_bp)


蓝本中如果指定了 static_folder  其它页面如果想引用这个目录下面的 文件  

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>电影列表</title>
{#    这个到 默认的static 目录下面查找   #}
{#    <link rel="stylesheet" href="{{ url_for("static",filename="movie_css.css") }}">#}
{#    就到 movie 蓝本制定的  static_folder 下面查找   #}
{#    这个movies 值得是 蓝本  Blueprint的第一个参数  #}
    <link rel="stylesheet" href="{{ url_for("movies.static",filename="movie_css.css") }}">
    <style>
        body{
            background: rebeccapurple;
        }
    </style>

</head>
<body>
    电影列表
</body>
</html>
```



## 子域名   

```
app.py  你的 实例文件 

app.config['SERVER_NAME'] = 'jd.com:5001'  
app.run(port=5001)


C:\Windows\System32\drivers\etc\hosts文件   

添加 
127.0.0.1 jd.com  
重启项目  即可  

jd.com:5001/movie/list来访问了  
```



