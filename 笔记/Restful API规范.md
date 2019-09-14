# Restful API规范

`restful api`是用于在前端与后台进行通信的一套规范。使用这个规范可以让前后端开发变得更加轻松。以下将讨论这套规范的一些设计细节。

### 协议：

采用`http`或者`https`协议。

### 数据传输格式：

数据之间传输的格式应该都使用`json`，而不使用`xml`。

### url链接：

url链接中，不能有动词，只能有名词。并且对于一些名词，如果出现复数，那么应该在后面加`s`。

比如：获取文章列表，应该使用`/articles/`，而不应该使用/get_article/

### HTTP请求的方法：

1. `GET`：从服务器上获取资源。 request.method == 'GET'  查  

2. `POST`：在服务器上新创建一个资源。      增  

3. `PUT`：在服务器上更新资源。（客户端提供所有改变后的数据）   改  全量更新  10个字段只改一个  但是所有字段必须全部传过来

4. `PATCH`：在服务器上更新资源。（客户端只提供需要改变的属性）  改  增量 更新  10

   10个字段  改一个  只传这一个就好了

5. `DELETE`：从服务器上删除资源。 删  

**示例如下：**

- GET /users/：获取所有用户。 http://api.jd.com/users/
- POST /user/：新建一个用户。http://api.jd.com/user/    
- GET /user/id/：根据id获取一个用户。
- PUT /user/id/：更新某个id的用户的信息（需要提供用户的所有信息）。
- PATCH /user/id/：更新某个id的用户信息（只需要提供需要改变的信息）。
- DELETE /user/id/：删除一个用户。

### 状态码：

| 状态码 | 原生描述              | 描述                                                         |
| ------ | --------------------- | ------------------------------------------------------------ |
| 200    | OK                    | 服务器成功响应客户端的请求。                                 |
| 400    | INVALID REQUEST       | 用户发出的请求有错误，服务器没有进行新建或修改数据的操作     |
| 401    | Unauthorized          | 用户没有权限访问这个请求                                     |
| 403    | Forbidden             | 因为某些原因禁止访问这个请求                                 |
| 404    | NOT FOUND             | 用户发送的请求的url不存在                                    |
| 406    | NOT Acceptable        | 用户请求不被服务器接收（比如服务器期望客户端发送某个字段，但是没有发送）。 |
| 500    | Internal server error | 服务器内部错误，比如出现了bug                                |
| 405    | method not allowed    | 请求方法不被允许                                             |



## flask-restful  

### 安装   

```
pip install flask_restful 
```

### 导入 

```
from flask_restful import Api,Resource,reqparse
```

1.根据Api 创建一个api对象  

2.写一个视图函数 让它继承于  Resource  然后使用你想要的请求方式 定义对应的方法   比如 只想要post请求  那么就定义一个 post方法即可    

3.通过 api.add_resource 将视图函数 暴漏出去   

```
from flask_restful import Api,Resource
app = Flask(__name__)
manager = Manager(app)
api = Api(app)

class LoginView(Resource):
    def post(self,username=None):
        return {"username":"chaoge"}

api.add_resource(LoginView,'/login/<username>/','/signup/')

#注意事项
#如果你想要返回json数据 那么就使用flask_restful  还有就是类视图
#class JsonView(View): def dispath_request(self): jsonify(self.get_data)
#如果想返回给前端是个页面  那么  app.route 就可以了
```

## 参数验证  

> 使用vue 写的app   需要通过接口 提交数据   各个参数需要验证   
>
> flask_restful提供了一个 类似于 wtfforms的 验证参数是否合法  叫 reqparse 
>
> 1.实例化parser对象   parser = reqparse.RequestParser() 
>
> 2. args = parser.parse_args()  对参数进行过滤  

```
class LoginView(Resource):
    def post(self):
        from datetime import date
        #这是python自带的date
        #我们的flask_restfule验证日期类型 需要 inputs.date
        #区别: 原生的  date  date(2019,9,11)
        #inputs.date   2019-9-11  所以这里不用  自带的date
        parser = reqparse.RequestParser() 
        parser.add_argument('username',type=int,help="用户名验证错误",required=True)
        parser.add_argument('homepage',type=inputs.url,help="必须是url类型",required=True)
        parser.add_argument('telephone',type=inputs.regex(r'1[3-9]\d{9}'),help="手机号类型有错误",required=True)
        parser.add_argument('birth',type=inputs.date,help="生日字段验证错误",required=True)
        parser.add_argument('gender',type=str,choices=['male','female','secret'])
        args = parser.parse_args()
        print(args)
        return {"username": "chaoge"}
# api.add_resource(LoginView,'/login/<username>/','/signup/')
api.add_resource(LoginView,'/login/')
```

1. default  设置默认值  
2. required 这个参数是否是必填项 True 或者False  
3. choices 选项  输入的参数 必须在    选项范围内  才可以    
4. help 表示 如果不符合要求 那么提示信息  
5. trim  是否去除前后左右的空格  
6. type 输入的类型  可以是python自带的数据类型  也可以使用flask_restrful.inputs 特定的数据类型来强制转化 
   1. inputs.url  是否是 http://www.baidu.com  之类的url   否则抛异常 
   2. inputs.regex 是否是正则表达式  
   3. inputs.date 将字符串转成  datetime.date 类型 如果不成功  抛异常   



## flask_restful之输出字段   

> 定义一个视图函数  指定好一些字段用于返回  后期使用ORM  模型 可以自动获取模型的相应字段  生成json数据  然后再返回 客户端   这时候我们需要导入一个装饰器   flask_restful marshal_with 装饰器   并且需要写一个字典 用来指定   返回的字段  以及字段的类型  

### 导入  

```
from flask_restful import Api,Resource,fields,marshal_with 
#fields为字段类型   
#marshal_with 自动获取 对应的字段  生成json数据 返回给 客户端  
```

```

class ArticleView(Resource):
    resource_fields = {
        'name':fields.String(attribute="username"),
        'age':fields.Integer,
        'school':fields.String
    }

    @marshal_with(resource_fields)  #使用装饰器   
    def get(self):
        #即使你不写 age、school 也会给你返回 age  school
        #调用了装饰器  返回内容的时候 自动的  调取 上面的useranme age  school
        #拼接json 返回
        # return {"username":"kangbazi"}
        return article

api.add_resource(ArticleView,'/article/',endpoint='article')
```



### 重命名  

```
面向公众的 名称  可以不是  内部字段名称   可以使用attribute配置这种映射  也就是说  对外是一个名字  
对内 是一个名字  需要通过  attribute 将这两个名字进行映射   

 resource_fields = {
        'name':fields.String(attribute="username"),
        'age':fields.Integer,
        'school':fields.String
    }
    
    对内 字段是 username  但是 我们 想以  name 的名字 暴漏给 公众  
```



### 字段 默认值  

```
resource_fields = {
        'name':fields.String,
        'age':fields.Integer(default=18),
        'school':fields.String
    }
```



