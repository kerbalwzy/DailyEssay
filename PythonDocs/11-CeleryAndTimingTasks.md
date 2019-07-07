## 01-快速认识Celery

- ##### 分布式任务队列异步框架Celery, 它可以让任务执行同主程序完全脱离, 甚至不在同一台主机内. 它通过队列来调度任务, 不用担心并发量高时系统负载过大. 它可以用来处理复杂系统性能问题, 却又相当灵活易用.

- ##### Celery的架构组成:

  ```reStructuredText
  消息中间人 Broker
      消息中间人，就是任务调度队列，通常以独立服务形式出现。它是一个生产者消费者模式，即主程序将任务放入队列中，而后台职程则会从队列中取出任务并执行。任务可以按顺序调度，也可以按计划时间调度。Celery组件本身并不提供队列服务，你需要集成第三方消息中间件。Celery推荐的有RabbitMQ和Redis，另外也支持MongoDB、SQLAlchemy、Memcached等，但不推荐。
  
  任务执行单元 Worker，也叫职程
      即执行任务的程序，可以有多个并发。它实时监控消息队列，获取队列中调度的任务，并执行它。
  
  执行结果存储 Backend
      由于任务的执行同主程序分开，如果主程序想获取任务执行的结果，就必须通过中间件存储。同消息中间人一样，存储也可以使用RabbitMQ、Redis、MongoDB、SQLAlchemy、Memcached等，建议使用带持久化功能的存储中间件。另外，并非所有的任务执行都需要保存结果，这个模块可以不配置。
  ```

- ##### 消息中间人(Broker)的选择:

  ```
  中间人推荐使用 RabbitMQ 或 Redis
  
  RabbitMQ安装教程: https://blog.csdn.net/u010889616/article/details/80643892
  ⚠️：按上面的教程安装完成后，服务已经自动启动。想开启网页管理，需要再在终端中执行命令:
  	开启WEB管理平台: sudo rabbitmq-plugins enable rabbitmq_management
      停止服务: sudo rabbitmqctl stop /或者  sudo service rabbitmq-server stop
      开启服务: sudo service rabbitmq-server start
  
  Redis安装:  这个网上教程一大把, 非常简单, 自己去找吧
  ```



## 02-快速使用Celery

- ##### 创建一个空文件夹, 新建tasks.py文件,写入如下的代码:

```python
from celery import Celery

app = Celery('demo',
             broker='amqp://admin:admin@localhost/FUXI',
             backend='redis://localhost:6379/0')
@app.task
def add(x, y):
    return x + y

"""
创建了一个Celery实例app，名称为’demo’；

中间人用：RabbitMQ，URL为’amqp://admin:admin@localhost/FUXI’;
⚠️：FUXI是我后面通过RabbitMQ的web控制面板创建的虚拟空间，并且通过命令给admin用户添加了该空间的使用权限
如果你对RabbitMQ的使用不熟悉, 可以先找教程学习一下, 或者将broker参数的值也设置为redis数据库的链接地址

存储人用：Redis，URL为’redis://localhost:6379/0’

定义了一个Celery任务”add”，可以返回两个参数的和。当函数使用”@app.task”修饰后，即为可被Celery调度的任务。注意⚠️: 在使用“@app.task” 装饰具体的任务时, task千万别写成了tasks
"""
```

- ##### 接下来让我们启动后台职程, 职程会监听Broker等待任务, 打开终端, 在当前文件夹路径下输入如下命令

```shell
celery worker -A tasks --loglevel=info
```

参数`-A`指定了Celery实例对象(这里就是app变量)所在的模块的导包路径, 会自动在本模块中搜索Celery的实例对象. 但是我更加建议你直接指定到实例对象的导包路径即 `-A tasks.app`; 参数`--loglevel`为指定日志等级, 默认为`Warning`等级, 可以缩写为`-l`

- ##### 最后就是在另外一个进程中调用你的Celery异步任务啦

```python
现在，让我们发些任务出来吧
新开一个终端, 切换到tasks.py所在的目录
输入命令python3, 打开python3的终端交互式编程环境，输入下面的指令：

>>> from tasks import add
>>> add.delay(2, 5)

输出的效果如下, 这其实是delay方法的返回值啦, 可以看出这个AsyncResult的实例对象
<AsyncResult: 4c079d93-fd5f-47f0-8b93-c77a0112eb4e>

代码分析:
这个”delay()”方法会将任务发送到消息中间人队列，并由之前启动的后台职程来执行。所以这时Python控制台上只会返回”AsyncResult”信息。如果你看下之前启动职程的终端窗口，你会看到多了一条日志”Task tasks.add[4c079d93-fd5f-47f0-8b93-c77a0112eb4e] succeeded in 0.0211374238133s: 7″。说明”add”任务已经被调度并执行成功，并且返回7。

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
状态，异常，返回值等信息都是通过JSON序列化存在Redis里的，这些信息的内容很好理解吧。
```

- ##### 关于 delay() 和 apply_async()

  我们之前调用任务使用了”delay()”方法，它其实是对”apply_async()”方法的封装，使得你只要传入任务所需的参数即可。对于特殊的任务调度需求，你需要使用”apply_async()”，其常用的参数有：

  - countdown: 指定多少秒后任务才被执行
  - eta: 指定任务被调度的时间，参数类型是datetime
  - expires: 任务过期时间，参数类型可以是int（秒），也可以是datetime
  - retry: 任务发送失败的重试次数
  - priority: 任务优先级，范围是0-9
  - aserializer: 参数和返回值的序列化方式



## 03-使用Celery创建定时任务

```python
from celery import Celery
from celery.schedules import crontab

app = Celery("workertest",
             broker='amqp://admin:admin@localhost/FUXI',  
             # broker使用了RabbitMQ链接地址,你也可以使用Redis的链接地址
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
# 这样启动职程之后, 这个add任务就是定时去执行了
```

