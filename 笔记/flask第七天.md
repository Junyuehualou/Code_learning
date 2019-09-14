# flask第七天   

## moment.js   

> https://momentjs.com/   专门用来格式化本地时间的 

 ### 安装  

```
pip install flask-moment 
```

### 使用

```
 from flask_moment import  Moment #导入类库
 moment = Moment(app) 实例化对象  
 
@app.route('/moments/')
def moments():
    public_time = datetime.utcnow()+timedelta(seconds=-360)
    return render_template('moment.html',public_time=public_time)


moment.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>moment</title>
</head>
<body>
<div>
{#    原样输出#}
    <div>{{ public_time }}</div>
{#    简单格式化显示  #}
    <div>{{ moment(public_time).format('LLLL') }}</div>
    <div>{{ moment(public_time).format('LLL') }}</div>
    <div>{{ moment(public_time).format('LL') }}</div>
    <div>{{ moment(public_time).format('L') }}</div>
{#    自定义格式  #}
    <div>{{ moment(public_time).format('YYYY/MM/DD hh:mm:ss') }}</div>
{#    自定义时间差值#}
    <div>{{ moment(public_time).fromNow() }}</div>
</div>


{# moment.js依赖于 jquery  所以先将其加载过来 #}
{{ moment.include_jquery() }}   # 如果你这个页面中 使用了bootstrap  这一步可以省略 

{# 加载moment.js#}
{{ moment.include_moment() }}

{{ moment.locale('zh-CN') }}
</body>
</html>

```



## 原生 文件上传 

### index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>文件上传</title>
</head>
<body>
<img src="{{ img_url }}" alt="">
{#文件上传  form表单 必须写上enctype="multipart/form-data"#}
<form action="" method="post" enctype="multipart/form-data">
    <input type="file" name="photo">
    <input type="submit" value="上传">
</form>
</body>
</html>
```



 ## 实例文件  

```
1.配置  
#设置允许的后缀
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])
#设置保存的位置
app.config['UPLOAD_FOLDER'] = os.getcwd()
#设置上传文件的大小
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024

2.公共函数  
#判断是否是允许的后缀
def allowed(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

#生成随机字符串
def random_string(length=20):
    import random
    base_str = '1234567890QRERTYUIOPASDFGHJKLZXCVBNM'
    return ''.join( random.choice(base_str) for i in range(length))
3.构建完整的图片 url  
#http://127.0.0.1:5001/uploaded/CISF2QG1LNC0PR04FRQU.png/  让图片能访问 才能渲染到页面上
@app.route('/uploaded/<filename>/')
def uploaded(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)


4.@app.route('/upload/',methods=['GET','POST'])
def upload():
    img_url = None
    if request.method == 'POST':#判断请求方式
        #获取表单提交的文件
        #保存上传文件
        file = request.files.get('photo') #接收表单提交的文件
        #print(file.filename) #输入文件的名字
        if file and allowed(file.filename):
            #获取文件后缀
            suffix = os.path.splitext(file.filename)[1]

            #生成随机的文件名
            filename = random_string()+suffix
            pathname = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            file.save(pathname)
            #生成缩略图

            #1.打开文件
            img = Image.open(pathname)
            #2.重设尺寸
            img.thumbnail((128,128))
            #3.保存
            img.save(pathname)

            img_url = url_for('uploaded',filename=filename)

    return render_template('index.html',img_url=img_url)
    
    
 5.图片压缩 
 		    #1.打开文件
            img = Image.open(pathname)
            #2.重设尺寸
            img.thumbnail((128,128))
            #3.保存
            img.save(pathname)
 	
```

ps: 

1. 文件上传  必须写上 enctype="multipart/form-data
2. 必须是post提交 
3. 字段必须有name属性 
4. 设置最大大小 及允许的后缀名   



## flask—upload  

> 文件类型 过滤   校验等  进行了封装  文件上传变得很方便   

```
pip instal flask-uploads
```



### 导入  

```
from flask_uploads import UploadSet,IMAGES,configure_uploads,patch_request_class
```

### 配置  

```
app.config['MAX_CONTENT_LENGTH'] = 8*1024*1024  #自己设定的文件大小  
#设置保存的位置
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(os.path.dirname(__file__),'uploads')

#创建文件上传对象 主要用来设置 允许的上传类型
photos = UploadSet('photos',IMAGES)

#将上传对象 跟 app实例完成绑定
configure_uploads(app,photos)

#配置上传文件大小 size默认64M 如果size为None
#那么就会按照我们自己设置的 app.config['MAX_CONTENT_LENGTH'] 大小
patch_request_class(app,size=None)
```

### 视图函数 

```

@app.route('/uploads/',methods=['GET','POST'])
def uploads():
    img_url = None
    if request.method == "POST":
        #保存文件
        filename = photos.save(request.files['photos'])
        #获取保存的url
        img_url = photos.url(filename)
    return render_template('index.html',img_url=img_url)
```

### index.html 

```html
 {% if img_url %}
        <img src="{{ img_url }}" alt="">
    {% endif %}
    <form action="" method="post" enctype="multipart/form-data">
        <input type="file" name="photos">
        <input type="submit" value="立即上传">
    </form>
```



## 既有普通表单 又有文件上传表单 整合在一起的写法  这个大家 参考 

1.enctype="multipart/form-data" 模板的form中一定带上这个 

2.后台获取文件 需要通过 avator = request.files.get('')

3.需要对上传的文件名进行安全过滤werkzeug.utils .secure_filename

4.保存上传文件只需要通过  avator.save(路径)保存即可 

5.访问上传的图片  定义一个视图函数  使用  send_from_directory(文件目录,文件名)



以上是 没有定义表单类的情况  接下来如果使用表单类  



1.定义表单类 我们需要单独引入一个FileFiled

2.导入验证器 from flask_wtf.file import FileRequired,FileAllowed

3.需要将 request.form  和 request.files 通过 from werkzeug.datastructures import CombinedMultiDict 进行整合再交给 form 进行验证 

```
from werkzeug.datastructures import CombinedMultiDict
form = UploadForm(CombinedMultiDict([request.form,request.files]))
        if form.validate():
```





## flask_mail  

> 邮件发送 
>
> 端口号 :邮件发送服务器  smtp 25  接收服务器  pop3 110    



### 安装 

```
pip install flask_mail 
```

### 导入

```
from flask_mail import Message,Mail
#Message用来创建 发送什么内容
#Mail 表示 怎么出去
```

### 配置    必须在实例化 Mail对象之前完成 配置 

```
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER','smtp.126.com')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME','gaohj66666@126.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD','zxasqw12')

```



## 视图函数  

```python
@app.route('/')
def index():
    # #创建邮件对象
    # msg = Message(subject="账户激活",recipients=['2592668397@qq.com'],sender=app.config['MAIL_USERNAME'])
    # #如果你是用浏览器访问 邮件
    # msg.html = '<h1>你好,请点击以下链接完成激活</h1>'
    #
    # # 如果你是用客户端 来查看邮件
    # msg.body = '你好,请点击以下链接完成激活'
    #
    # mail.send(message=msg)
    return '发送成功'
    
    
 函数封装  
 
 def send_mail(to,sub,template,**kwargs):
    #根据current_app 我们获取到  当前app
    app = current_app._get_current_object()
    #创建邮件对象
    msg = Message(subject=sub, recipients=[to], sender=app.config['MAIL_USERNAME'])
    # 如果你是用浏览器访问 邮件
    msg.html =render_template(template+'.html',**kwargs)

    # 如果你是用客户端 来查看邮件
    msg.body = render_template(template+'.txt',**kwargs)

  	mail.send(message=msg)
    return 'ok'
    
  
  
  异步发送: 
  1.创建一个线程   耗时任务交给 线程  
  2.需要告诉线程  做什么  以及传参  
  3.先创建的线程没有上下文 需要手动创建   
  
  
  def async_send_mail(app,msg):
    #发送邮件需要程序上下文,新的线程没有上下文  需要手动创建
    with app.app_context():
        mail.send(message=msg)


def send_mail(to,sub,template,**kwargs):
    #根据current_app 我们获取到  当前app
    app = current_app._get_current_object()
    #创建邮件对象
    msg = Message(subject=sub, recipients=[to], sender=app.config['MAIL_USERNAME'])
    # 如果你是用浏览器访问 邮件
    msg.html =render_template(template+'.html',**kwargs)

    # 如果你是用客户端 来查看邮件
    msg.body = render_template(template+'.txt',**kwargs)

    #创建一个线程
    thread = Thread(target=async_send_mail,args=[app,msg])

    #启动线程
    thread.start()
    return thread
  
```



