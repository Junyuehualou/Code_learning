# WTForms笔记：
这个库一般有两个作用。第一个就是做表单验证，把用户提交上来的数据进行验证是否合法。第二个就是做模版渲染。



### 做表单验证：
1. 自定义一个表单类，继承自wtforms.Form类。
2. 定义好需要验证的字段，字段的名字必须和模版中那些需要验证的input标签的name属性值保持一致。
3. 在需要验证的字段上，需要指定好具体的数据类型。
4. 在相关的字段上，指定验证器。
5. 以后在视图中，就只需要使用这个表单类的对象，并且把需要验证的数据，也就是request.form传给这个表单类，以后调用form.validate()方法，如果返回True，那么代表用户输入的数据都是合法的，否则代表用户输入的数据是有问题的。如果验证失败了，那么可以通过form.errors来获取具体的错误信息。
示例代码如下：
ReistForm类的代码：
```python
class RegistForm(Form):
    username = StringField(validators=[Length(min=3,max=10,message='用户名长度必须在3到10位之间')])
    password = StringField(validators=[Length(min=6,max=10)])
    password_repeat = StringField(validators=[Length(min=6,max=10),EqualTo("password")])
```
视图函数中的代码：
```python
form = RegistForm(request.form)
if form.validate():
    return "success"
else:
    print(form.errors)
    return "fail"
```


### 常用的验证器：
数据发送过来，经过表单验证，因此需要验证器来进行验证，以下对一些常用的内置验证器进行讲解：
1. Email：验证上传的数据是否为邮箱。
2. EqualTo：验证上传的数据是否和另外一个字段相等，常用的就是密码和确认密码两个字段是否相等。
3. InputRequir：原始数据的需要验证。如果不是特殊情况，应该使用InputRequired。
3. Length：长度限制，有min和max两个值进行限制。
4. NumberRange：数字的区间，有min和max两个值限制，如果处在这两个数字之间则满足。
5. Regexp：自定义正则表达式。
6. URL：必须要是URL的形式。
7. UUID：验证UUID。

```python
from wtforms import Form,StringField,PasswordField,SubmitField,IntegerField,BooleanField,SelectField,DateField
from wtforms.validators import Length,EqualTo,Email,InputRequired,NumberRange,Regexp,URL,UUID
from flask_wtf import FlaskForm
class RegisterForm(Form):
    username = StringField("用户名",validators=[Length(min=6,max=20,message="用户名长度在6-20位")])
    password = PasswordField("密码",validators=[Length(min=6,max=20,message="密码长度在6-20位")])
    password_repeat =  PasswordField("确认密码",validators=[Length(min=6,max=20,message="密码长度在6-20位"),EqualTo("password",message="两次密码必须一致")])
    submit = SubmitField("立即注册")

#FlaskForm 继承于 Form
#如果你想用 flask_bootstrap渲染 那么必须继承于 FlaskForm
#如果使用 {{form.email.label}}{{form.email()}} 那么继承于 Form即可
class LoginForm(FlaskForm):
    email = StringField("邮箱",validators=[Email(message="必须是邮箱类型")])
    username = StringField("用户名", validators=[Length(min=6, max=20, message="用户名长度在6-20位"),InputRequired("请填写用户名")])
    age = IntegerField(validators=[NumberRange(18,90)])
    phone = StringField(validators=[Regexp(r'1[3-9]\d{9}')])
    homepage = StringField(validators=[URL()])
    uuid = StringField(validators=[UUID()])
    captcha = StringField(validators=[Length(4,4)])
    creat_time = DateField("注册时间",validators=[])
    remember = BooleanField("记住我:")
    tags = SelectField("标签",choices=[('1','python'),('2','java')])
    submit = SubmitField("立即登录")
    #http://www.jiabin.com
```



### 自定义验证器：
如果想要对表单中的某个字段进行更细化的验证，那么可以针对这个字段进行单独的验证。步骤如下：
1. 定义一个方法，方法的名字规则是：`validate_字段名(self,filed)`。
2. 在方法中，使用`field.data`   或者  `self.字段名.data`   可以获取到这个字段的具体的值。
3. 如果数据满足条件，那么可以什么都不做。如果验证失败，那么应该抛出一个`wtforms.validators.ValidationError`的异常，并且把验证失败的信息传到这个异常类中。
示例代码：
```python
captcha = StringField(validators=[Length(4,4)])
    # 1234
    def validate_captcha(self,field):  #不要忘了filed参数   
        self.captcha.data
        if field.data != '1234':
            raise ValidationError('验证码错误！')
```



### flask_wtf

安装 

```
pip install  flask_wtf
```



##  form.py 

```
from flask_wtf import FlaskForm  
from wtfforms import StringField,SubmitField
from wtfforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField("邮箱",validators=[Email(message="必须是邮箱类型")])
    username = StringField("用户名", validators=[Length(min=6, max=20, message="用户名长度在6-20位"),InputRequired("请填写用户名")])
    age = IntegerField(validators=[NumberRange(18,90)])
    phone = StringField(validators=[Regexp(r'1[3-9]\d{9}')])
    homepage = StringField(validators=[URL()])
    uuid = StringField(validators=[UUID()])
    captcha = StringField(validators=[Length(4,4)])
    creat_time = DateField("注册时间",validators=[])
    remember = BooleanField("记住我:")
    tags = SelectField("标签",choices=[('1','python'),('2','java')])
    submit = SubmitField("立即登录")
    
  
	
	
```

app.py

```
from forms imort LoginForm

@app.route('/login/',methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == "GET":
        return render_template('login.html',form=form)
    else:
        form = LoginForm(request.form) # 表单提交多来的内容作为 参数
        if form.validate(): #如果用户的输入 满足要求
            return 'success'
        else:
            print(form.errors)  #打印表单错误消息
            return 'fail'
```



login.html

```
{% extends 'bootstrap/base.html' %}


{% import 'bootstrap/wtf.html' as wtf %}


{% block content %}
    {{ wtf.quick_form(form,action="",method="post") }}
{% endblock %}


或者  

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <table>
        <tbody>
            <tr>
                <td>{{ form.username.label }}</td>
{#                如果你想给表单添加样式  直接传参即可#}
                <td>{{ form.username(class="username") }}</td>
            </tr>
            <tr>
                <td>{{ form.password.label }}</td>
                <td>{{ form.password() }}</td>
            </tr>
            <tr>
                <td>{{ form.password_repeat.label }}</td>
                <td>{{ form.password_repeat() }}</td>
            </tr>
             <tr>
                <td>{{ form.submit.label }}</td>
                <td>{{ form.submit() }}</td>
            </tr>
        </tbody>
    </table>
</form>
</body>
</html>
```





## flask_bootstrap 

### 安装 

```
pip install flask_bootstrap  
```

### app.py 

```
from flask import Flask,render_template
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap #导入 
app = Flask(__name__)
#在实例化 bootstrap 之前  设置  使用本地文件 不用 官网css.js
#提高打开速度
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SECRET_KEY'] = 'ADADSSDA12211ASDD'

bootstrap = Bootstrap(app)  #实例化  跟app 进行绑定 



class  LoginForm(FlaskForm): #写一个 表单类 
    username = StringField("用户名",validators=[DataRequired()])
    password = PasswordField("密码",validators=[DataRequired()])
    submit = SubmitField("立即登录")


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/login/')   #写个方法 
def login():
    form = LoginForm()  #实例化一个表单对象  
    return render_template("login.html",form=form)  #将表单渲染到  页面上


if __name__ == '__main__':
    app.run(debug=True,port=5001)

```



### login.html 

```
{#因为我们已经安装好了 flask_bootstrap #}
{#你的虚拟环境位置\Lib\site-packages\flask_bootstrap\templates\bootstrap#}
{% extends 'bootstrap/base.html' %}  #这是父页面 页面继承于它 


{#导入渲染工具 也就是导入宏  #}

{% import 'bootstrap/wtf.html' as wtf %} #这是所有的宏  


{% block content %}  #父页面规定好的区块
    {{ wtf.quick_form(form,action="",method="post") }}  #宏    参数 1要渲染的表单 2.提交到哪里
    3.提交方式  

{%endblock%}


```

## flash 消息显示  

> 上面的操作  是在 服务器端  print(form.errors) 前台页面看不到 具体的错误信息  如果想要看到错误信息  
>
> 我们可以通过flash 这个方法   
>
> 比如如果需要输出错误信息  服务器端 调用flash方法  
>
> 前端页面 查询错误消息  

app.py 

```  python
from flask import Flask,render_template,request,flash,redirect,url_for
from flask_script import  Manager
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,Length,ValidationError
from flask_bootstrap import Bootstrap
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ad12ADFA12'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
manager = Manager(app)
bootstrap = Bootstrap(app)


class NameForm(FlaskForm):
    name = StringField('用户名',validators=[DataRequired()])
    submit = SubmitField("立即提交")

    def validate_name(self,field):
        if len(field.data) < 6:
            raise ValidationError("用户名不能少于6个字符")



@app.route('/',methods=['GET','POST'])
def hello_world():
    form = NameForm()
    if form.validate():
        lastname = "十年前的流行是火星文"
        if lastname != form.name.data:
            flash("常换签名两种情况，要么你是性情中人，要么你是不专一")
            return redirect(url_for('hello_world'))
    name = form.name.data
    return render_template('form.html',form=form,name=name)


if __name__ == '__main__':
    manager.run()

```



## form.html

```
{% extends 'bootstrap/base.html' %}

{% import 'bootstrap/wtf.html' as wtf %}


{% block content %}
    {% for message in get_flashed_messages() %} #如果服务器 输送了flash信息  那么遍历
          <div class="alert alert-warning alert-dismissible" role="alert">
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">	        <span aria-hidden="true">&times;</span></button>
                <strong>Warning!</strong> {{ message }}.
                {# bootstrap  组件 警告框#}
         </div>
    {% endfor %}

    {% if name %}
        {{ name }}
        {% else %}
        <p>hello world</p>
    {% endif %}
    {{ wtf.quick_form(form,action="",method="post") }}
{% endblock %}
```

