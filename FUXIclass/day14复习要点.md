复习要点：第十四天	快速学习使用新框架和WEB后端开发异常处理常规流程

---

#### 01-快速了解和学习使用异步任务框架Celery

```
官方文档：http://docs.celeryproject.org/en/latest/index.html
Celery作用：
	分布式任务队列Celery，它可以让任务的执行同主程序完全脱离，甚至不在同一台主机内。它通过队列来调度任务，不用担心并发量高时系统负载过大。它可以用来处理复杂系统性能问题，却又相当灵活易用。

Celery架构组成：
	消息中间人 Broker
    消息中间人，就是任务调度队列，通常以独立服务形式出现。它是一个生产者消费者模式，即主程序将任务放入队列中，而后台职程则会从队列中取出任务并执行。任务可以按顺序调度，也可以按计划时间调度。Celery组件本身并不提供队列服务，你需要集成第三方消息中间件。Celery推荐的有RabbitMQ和Redis，另外也支持MongoDB、SQLAlchemy、Memcached等，但不推荐。

    任务执行单元 Worker，也叫职程
    即执行任务的程序，可以有多个并发。它实时监控消息队列，获取队列中调度的任务，并执行它。

    执行结果存储 Backend
    由于任务的执行同主程序分开，如果主程序想获取任务执行的结果，就必须通过中间件存储。同消息中间人一样，存储也可以使用RabbitMQ、Redis、MongoDB、SQLAlchemy、Memcached等，建议使用带持久化功能的存储中间件。另外，并非所有的任务执行都需要保存结果，这个模块可以不配置。	

安装和选择中间人：
	安装：pip install celery
	中间人：中间人推荐使用RabbitMQ或Redis
	RabbitMQ安装教程：https://blog.csdn.net/u010889616/article/details/80643892
	⚠️：按上面的教程安装完成后，服务已经自动启动。想开启网页管理，需要再在终端中执行命令：
		开启WEB管理平台：sudo rabbitmq-plugins enable rabbitmq_management
        停止服务：sudo rabbitmqctl stop /或者  sudo service rabbitmq-server stop
        开启服务：sudo service rabbitmq-server start
	
	Redis安装：sudo apt install redis

安装Celery包：pip install celery
```

```Python
# 单独使用Celery的简单示例：
from celery import Celery

app = Celery('tasks',
             broker='amqp://admin:admin@localhost/FUXI',
             backend='redis://localhost:6379/0')
@app.task
def add(x, y):
    return x + y

"""
这里我们创建了一个Celery实例app，名称为’tasks’；
中间人用：RabbitMQ，URL为’amqp://admin:admin@localhost/FUXI’；
⚠️：FUXI是我后面通过RabbitMQ的web控制面板创建的虚拟空间，并且通过命令给admin用户添加了该空间的使用权限

存储人用：Redis，URL为’redis://localhost:6379/0’。
同时我们定义了一个Celery任务”add”，可以返回两个参数的和。当函数使用”@app.task”修饰后，即为可被Celery调度的任务。

接下来，让我们启动后台职程
职程会监听消息中间人队列并等待任务调度，启动命令为：
终端命令：celery worker -A tasks --loglevel=info

参数”-A”指定了Celery实例的位置，本例是在”tasks.py”中，celery命令会自动在该文件中寻找Celery对象实例。不过我更建议你指定Celery对象名称，如”-A tasks.app”。
参数”loglevel”指定了日志等级，也可以不加，默认为warning。

现在，让我们发些任务出来吧
打开python控制台，输入下面的指令：
>>> from tasks import add
>>> add.delay(2, 5)
<AsyncResult: 4c079d93-fd5f-47f0-8b93-c77a0112eb4e>

这个”delay()”方法会将任务发送到消息中间人队列，并由之前启动的后台职程来执行。所以这时Python控制台上只会返回”AsyncResult”信息。如果你看下之前职程的启动窗口，你会看到多了条日志”Task tasks.add[4c079d93-fd5f-47f0-8b93-c77a0112eb4e] succeeded in 0.0211374238133s: 7″。说明”add”任务已经被调度并执行成功，并且返回7。

因为我们的程序配置了后台结果存储（backend），我们可以通过如下方法获取任务执行后的返回值：
>>> result=add.delay(2, 5)
>>> result.ready()
True
>>> result.get(timeout=1)
7
此时我们就可以获取到返回值7了，由于有些任务执行时间会很长，我们可以使用”result.ready()”方法来检查任务是否执行完成。如果之前我们没有配置backend存储，那么刚才的调用会抛异常。

关于后台
上例中我们配置了Redis存储，那让我们去Redis里看看Celery任务执行的结果是怎么存储的吧。通过”keys celery*”，可以查到所有属于celery的键值。celery是一个任务一条记录啊，而且键值上带着任务的UUID。让我们查看刚才执行的那条记录的值吧，结果如下：
"{\"status\": \"SUCCESS\", \"traceback\": null, \"result\": 7, \"task_id\": \"4c079d93-fd5f-47f0-8b93-c77a0112eb4e\", \"children\": []}"
状态，异常，返回值等都是通过JSon序列化存在Redis里的，很好理解吧。
"""
```

##### delay()和apply_async()

我们之前调用任务使用了”delay()”方法，它其实是对”apply_async()”方法的封装，使得你只要传入任务所需的参数即可。对于特殊的任务调度需求，你需要使用”apply_async()”，其常用的参数有：

- countdown: 指定多少秒后任务才被执行

- eta: 指定任务被调度的时间，参数类型是datetime
- expires: 任务过期时间，参数类型可以是int（秒），也可以是datetime
- retry: 任务发送失败的重试次数
- priority: 任务优先级，范围是0-9
- serializer: 参数和返回值的序列化方式

##### Celery定时任务：

```python
# 单独使用Celery的简单示例：
from celery import Celery
from celery.schedules import crontab

app = Celery("workertest",
             broker='amqp://admin:admin@localhost/FUXI',  # broker使用rabbitmq链接地址
             backend='redis://localhost:6379/0')

app.conf.timezone = "Asia/Shanghai"  # 指定时区

app.conf.beat_schedule = {
    'task_name': {  # 定时任务名称
        'task': 'test.add',  # 任务导包路径
        # 'schedule': 2,       # 任务执行间隔时间,单位秒
        'schedule': crontab(hour=15, minute=29, day_of_week=6),  # 指定特定的时间执行
        'args': (3, 3)  # 任务要接收的参数,如果任务没有参数可以省略
    },
}

@app.task
def add(x, y):
    return x + y

# 启动worker时需要添加额外的参数： --beat
```

⚠️：更多使用方式请参考就业复习班课件资料11Celery异步框架

和Django项目的配合使用参考课件

和Flask项目的配合使用参考：http://www.bjhee.com/celery.html

---

02-快速了解和学习使用异步WEB框架sanic

```
学习文档：https://segmentfault.com/a/1190000014619175#articleHeader3
了解sanic：
	Sanic是一个支持 async/await 语法的异步无阻塞框架，这意味着我们可以依靠其处理异步请求的新特性来提升服务性能，如果你有Flask框架的使用经验，那么你可以迅速地使用Sanic来构建出心中想要的应用，并且性能会提升不少，同一服务分别用Flask和Sanic编写，再将压测的结果进行对比，发现Sanic编写的服务大概是Falsk的1.5倍。Sanic使用了uvloop作为asyncio的事件循环，uvloop由Cython编写，它的出现让asyncio更快
	说明：由于Windows下暂不支持安装uvloop，故在此建议使用Mac或Linux

了解async：https://blog.csdn.net/soonfly/article/details/78361819/
作用：python3.5-加入新的关键字 async ，可以将任何一个普通函数变成协程
	但是async对生成器是无效的。async无法将一个生成器转换成协程。 
	开启协程的任务的方式是固定的。

```

- 学习总结

  ```python
  # 第一步：创建application对象，从helloword开始
  from sanic import Sanic
  from sanic.response import text
  
  app = Sanic()
  
  @app.route("/")
  async def index(request):
      return text('Hello World!')
  ```

  ```python
  # 第二步：函数视图与类视图
  # 函数视图， 在普通函数的定义前添加关键字 asnyc，并可以使用app.route装饰注册路由
  @app.route("/viewFunc")
  async def viewFunc(request):
      return text("this is a view function")
  
  # 类视图，继承于HTTPMethodView。支持在类中定义5中与http请求方式同名的方法,也支持async语法
  from sanic.views import HTTPMethodView
  class SimpleView(HTTPMethodView):
  
    async def get(self, request):
        return text('I am get method')
  
    async def post(self, request):
        return text('I am post method')
  
    async def put(self, request):
        return text('I am put method')
  
    async def patch(self, request):
        return text('I am patch method')
  
    async def delete(self, request):
        return text('I am delete method')
  
  # 给类视图注册路由时可以通过app对象的add_router方法实现。
  app.add_route(SimpleView.as_view(), '/')
  ```

  ```python
  # 第三步：路由注册与路由参数
  
  # 对于函数视图：
  # 第一种方式：使用app.route()装饰,常用参数包括：path、methods，示例如下
  @app.route("/url_path", methods=["GET", "POST", ...])
  # 第二中方式：使用app.HTTP_METHOD()装饰，常用参数：path，示例如下
  @app.get('/url_path')
  @app.post('/url_path')
  ...
  # 第三种方式：使用app.add_route()方法，常用参数:view_func_name, path, methods
  app.add_route(view_func_name, "/url_path", methods=["GET", "POST", ...])
  
  # 对于类视图只能使用函数视图的第三种添加路由的方式，而且注册时要调用类的as_view方法，并且methods参数无效：
  app.add_route(ViewClass.as_view(), "/url_path")
  
  # 路由参数：
  '''
  支持在路由中设置参数：通过尖括号表示，使用冒号分割参数名和匹配规则，匹配规则支持regex；使用路由参数时，视图函数或方法中需要接受一个同名的形参，路由示例如下：
  	# /url_path/<param_name:[a-zA-Z]{4,8}>
  '''
  ```

  ```python
  # 第三步：request对象的常用属性
  request.agrs # 获取查询字符串参数,当想要获取同一个键的多个值时使用
  			 # 示例：?name=laowang&name=xiaowang -->{'name':['laowang', 'xiaowang']}
  
  request.raw_agrs. # 获取查询字符串参数,当同一个键有多个值时只取第一个
  			 	# 示例：?name=laowang&name=xiaowang -->{'name':'laowang'}
  request.form #(dict） - post表单变量。
  
  request.json  #JSON body
  request.files # 具有名称，正文和类型的文件信息列表
  ......
  # 更多属性请自己看教程
  ```

  ```python
  # 第四步：可使用的Response对象
  from sanic.response import text, json, html, stream, file_stream, file
  '''
  其实刚才从response导出的对象，都是函数，这些函数的功能是返回一个合适的response对象
  除了stream和file_stream返回的对象是StreamingHTTPResponse的实例之外
  其他的函数返回都是HTTPResponse的实例
  ''' 
  # 修改响应头和状态码，直接在函数中传入实参即可
  # 要修改头部或状态代码，将头部或状态参数传递给这些函数，
  # 示例如下
  from sanic import response
  
  @app.route('/json')
  def handle_request(request):
      return response.json(
          {'message': 'Hello world!'},
          headers={'X-Served-By': 'sanic'},
          status=200
      )
  
  ```

  ```python
  # 第五步：使用蓝图
  # 创建蓝图
  from sanic.response import json
  from sanic import Blueprint
  
  bp = Blueprint('my_blueprint', url_prefix="bptest")
  
  
  @bp.route('/')
  async def bp_root(request):
      return json({'my': 'blueprint'})
  
  # 注册蓝图
  from xxx import bp
  app.blueprint(blueprint=bp)
  
  ```

  ```python
  # 第六步：使用中间件
  '''
  定义中间:
  通过装饰器：app.middleware去装饰一个带async关键字的函数实现
  
  '''
  @app.middleware   # 在视图执行前，
  async def print_on_request(request):
      print("I am a spy")
  
  
  @app.middleware('request')  # 在视图执行前
  async def halt_request(request):
      print('I halted the request')
  
  
  @app.middleware('response') #在视图执行之后，
  async def halt_response(request, response):
      print('I halted the response')
      return response  # 必须返回
  
  ```

  #### ⚠️更多使用方式和功能请参考教程文档自学。目前此框架还不成熟，市场上基本不使用。了解作为加分项即可。

---

#### 03-快速了解和学习使用前端模版引擎art-template「如果觉得Vue难，可以将该插件作为替代方案」

```
了解art-template：
	art-template 是由腾讯开发的一个简约、超快的模板引擎「模板插件」。
	前端技术日新月异，前端字符串模板引擎已经逐步被 DOM 模板引擎所取代，以至于 art-template 一度停止维护。现在，art-template 重新回归，带来了全新的 v4 版本。v4 对 NodeJS 进行了更好的支持，并且拥有领先的渲染性能，同时带来了全家桶：express-art-template 与 koa-art-template。
对于浏览器端，art-template@4.0 带来了基于 WebPack 的 art-template-loader，它能更好的支持预编译，生成非常简洁的代码用于浏览器端使用，它完全可取代年久失修的 TmodJS。

优点：
    拥有接近 JavaScript 渲染极限的的性能
    调试友好：语法、运行时错误日志精确到模板所在行；支持在模板文件上打断点（Webpack Loader）
    支持 Express、Koa、Webpack
    支持模板继承与子模板
    浏览器版本仅 6KB 大小
    
语法：
    art-template同时支持两种模板语法，标准语法和原始语法。 标准语法可以让模板更容易读写；原始语法具有强大的逻辑处理能力。

    标准语法：
        格式为{{ }}, 输出语法的例子：{{value}}、{{data.key}}、{{data[‘key’]}}、 {{a||b}}

    原始语法： 
       格式为{% %}的形式，输出语法的例子如{{= value}}、{{%= data.key%}}、{{%= data[‘key’]%}}、{{% = a||b%}}

快速上手教程：
https://github.com/kerbalwzy/aboutPython/blob/master/LAN_fileServer/static/index.html
http://www.jq22.com/jquery-info1097
https://blog.csdn.net/diligentkong/article/details/73836581
			
官方文档：https://aui.github.io/art-template/zh-cn/docs/index.html
```

---

#### 04-WEB后端开发过程中的异常处理常规步骤

```
前后端分离情况下：
	1.确认请有没有从前端发送出去，如果没有发送出去，则是前端js代码的问题
	2.如果请求发送了，确认后端是否接收到
	3.如果后端接收到了，确认后端是否返回了响应
	
	4.如果前面三个都没问题
		1.确认参数是否正确，这里的参数不要只局限于查询字符串和请求体，也要考虑请求头信息
		2.确认自己对接收到的参数的验证规则是否正确，将条件判断写明白，不要偷懒
		3.确认对数据【库】的操作是否正确
		4.确认构造响应体前对数据的序列化操作是否正确
		5.确认构造的响应体和可能需要添加的响应头是否符合前端的要求
	
	5.如果是多个视图之间的数据在业务的流程中存在关联，则需要对提供基础数据的视图做检查，检查步骤参考前面四步
	
	6.如果前端控制台或者后端的终端中出现了报错信息，问题解决步骤：
		1.查看异常对象的类型，根据类型大致确认原因
		2.查看异常的详细信息，进一步确认异常的发生原因，方便定位异常
		3.根Traceback里面的以File开头的信息，定位异常发生的位置；如果信息太多找不到，通过在代码中多个位置输出print("位置定位表示字符串")，快速的定位异常的范围
		4.如果上面的步骤都还没有解决问题，百度「你绝对不是第一个遇到这个问题的人」
		5.找黑马就业支持QQ
		6.找助教
```

