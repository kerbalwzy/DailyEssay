复习要点：第九天 Django框架的基本使用

---

01-PythonWEB框架相关认识

```
	劳伦斯出版集团为了开发以新闻内容为主的网站，而开发出来了这个框架，于2005年7月在BSD许可证下发布。这个名称来源于比利时的爵士音乐家DjangoReinhardt。
	
	Django的主要目的是简便、快速的开发数据库驱动的网站。它强调代码复用，多个组件可以很方便的以"插件"形式服务于整个框架，Django有许多功能强大的第三方插件，你甚至可以很方便的开发出自己的工具包。这使得Django具有很强的可扩展性。它还强调快速开发和DRY(DoNotRepeatYourself)原则。
	
特点：
	对比Flask框架，Django原生提供了众多的功能组件，让开发更简便快速。
    提供项目工程管理的自动化脚本工具
    数据库ORM支持（对象关系映射，英语：Object Relational Mapping）
    模板
    表单
    Admin管理站点
    文件管理
    认证权限
    session机制
    缓存
    
MVC设计模式：
	M全拼为Model，主要封装对数据库层的访问，对数据库中的数据进行增、删、改、查操作。
    V全拼为View，用于封装结果，生成页面展示的html内容。
    C全拼为Controller，用于接收请求，处理业务逻辑，与Model和View交互，返回结果。

Django的MVT：
	M全拼为Model，与MVC中的M功能相同，负责和数据库交互，进行数据处理。
    V全拼为View，与MVC中的C功能相同，接收请求，进行业务处理，返回应答。
    T全拼为Template，与MVC中的V功能相同，负责封装构造要返回的html。
    
```

---

02-使用Django搭建项目

```
如何激活通过pycharm创建的虚拟环境：
	前往虚拟环境的文件夹的bin目录，并执行：source  ./activate   
	
安装好Django之后，可以通过如下的命令创建项目和应用：
	django-admin startproject 项目名称「这里暂时命名为FUXI」
	项目文件夹内容：
		与项目同名的目录
            settings.py 是项目的整体配置文件。
            urls.py 是项目的URL配置文件。
            wsgi.py 是项目与uWSGI兼容的Web服务器入口。
        manage.py 是项目管理文件，通过它管理项目
        
	cd 项目文件夹
	django-admin startapp 应用名称「这里暂时命名为example」
	创建好应用之后，项目文件中会多出一个子应用模块
	子应用模块的文件夹内容：
		自己补充
		
	在项目目录下创建static文件夹和templates文件夹
    
    在项目目录下创建ownNginx.conf,用来保持本项目要用到的nginx配置
    
	在项目目录下创建settings包：
		修改原配置文件，将时区本地化
		修改原配置文件，将static文件夹的路径和template文件夹的路径设置好。
		
		将原先的配置文件复制进去，并复制三份，分别重名为，develop.py, testing.py, product.py
        修改product.py文件，关闭debug模式
		作用：在实际的开发中，我们往往需要多套配置来适应不同阶段的使用需求。
		这三个配置文件的主要不同之处：
			是否开启调试模式
			数据库选择不一样
			其他第三方资源的配置不一样
	
	开发时使用develop.py的配置，通过修改manager.py文件中的代码实现同过命令行选择不同的配置文件；
	代码如下：
	
	if __name__ == '__main__':
        setting_file_name = sys.argv[1]
        print(setting_file_name)
        if setting_file_name not in ["develop", "testing", "product"]:
            print("请在运行manager.py文件时,在原命令之前添加选择配置文件的参数"
                  "\n目前可选的配置文件名: develop | testing | product")
            exit()

        os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                              'FUXI.settings.{}'.format(setting_file_name)
                              )
        try:
            from django.core.management import execute_from_command_line
        except ImportError as exc:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            ) from exc

        commands = sys.argv[0:1] + sys.argv[2:]
        execute_from_command_line(commands)
        """
        因为是我们自己定义的要多运行文件时多接收一个参数,为了不影响原始Django框架代码的运行,
        我们这里要将我们多添加的参数去掉后在传给框架使用.之所以不是用pop操作,而是使用切片生成新命令列表,
        是因为在调试模式下,启动会由一次预检.使用pop函数会影响我们程序的启动.
        """

       
	注册我们刚刚创建的应用。
	
```

---

03-函数视图、request对象、response对象、cookie和session。

```
在example应用中的views.py定义一个函数，并注册好路由，测试能否正常访问；

1.尝试在路由路径中接受参数：
 	在配置路由时使用re_path或者url对像。路由字符串中使用正则表达式的命名分组方式给参数预留位置和限定匹配条件。
 	在视图函数中，多添加一个与路由正则表示中参数组名相同的形参

2.尝试增加接收查询字符串的参数
	使用 ret = request.GET.get("key")
	当同一个键对应有多个值的时候，去查询字符串中这个键最一次出现时对应的值
	使用 ret = request.GET.getlist("key")
	可以通过getlist获取到它对应的所有的值，并放在了列表中；

3.尝试增加请求体包含的参数
前后端分离时处理CSRF验证问题：https://blog.csdn.net/hyesc/article/details/80611283
我们可以通过查看django.middleware.csrf中_set_token函数的代码查看可以在配置文件中设置哪些CSRF的配置

设置csrf_token的视图函数可以简单的写为，我们这里也可以选择返回空白字符串，
让响应头自己去在cookie中保存csrftoken键值对：
    from django.middleware.csrf import get_token
    def set_csrf_token(request):
        """
        向浏览器的cookie中保存csrftoken键值对的视图,
        配置好路由后在需要的页面中使用ajax直接请求即可.
        可以在配置文件中通过CSRF_COOKIE_AGE设置有效期(单位:秒).
        有效期内重复访问该视图不会更新token值
        :param request: 请求体对象
        :return: 返回空字符串
        """
        csrf_token_value = get_token(request)
        return JsonResponse({"token": csrf_token_value})
        
POST请求体的参数。可以通过request.POST.get("KEY")获取
使用post请求时，如果有查询字符串，一样可以通过request.GET获取到查询字符串中的参数

非表单类型的请求体数据，Django无法自动解析，可以通过request.body属性获取最原始的请求体数据，自己按照请求体格式（JSON、XML等）进行解析。request.body返回bytes类型。
当处理JSON格式的数据时：
	前端：将js对象转化为JSON字符串： JSON.stringify(data)
		 声明：contentType:"application/json"     // 在请求头中告诉后端我们发送的数据格式
	后端：可以通过 request.body 获取到byte类型的数据，然后使用json模块做解析

可以通过request.META属性获取请求头headers中的数据，request.META为字典类型。
MATE还包含了服务器添加的一些数据

其他常用HttpRequest对象属性
    method：一个字符串，表示请求使用的HTTP方法，常用值包括：'GET'、'POST'。
    user：请求的用户对象。
    path：一个字符串，表示请求的页面的完整路径，不包含域名和参数部分。
    encoding：一个字符串，表示提交的数据的编码方式。
    如果为None则表示使用浏览器的默认设置，一般为utf-8。
    这个属性是可写的，可以通过修改它来修改访问表单数据使用的编码，接下来对属性的任何访问将使用新的encoding值。
    FILES：一个类似于字典的对象，包含所有的上传文件。

4.尝试返回不同类型的数据。	
前后端分离情况下：主要是返回JsonResponse的对象
	帮助我们将数据转换为json字符串
	设置响应头Content-Type为application/json
	
通过response对象设置响应头：
	reponse["key"] = "value"

5.尝试设置和读取session及cookie
	通过request.COOKIES可以获取cookie信息
	通过resp_ob.set_cookie(key,value,....)可以向响应头中添加set-cookie键值对，告知浏览器保存cookie信息
	
	
	session配置保存到redis「该配不是一定要有的，可以使用默认的」：
	pip install django-redis
	# 确保redis数据库能够使用
	CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"
    
    使用session的默认配时，要先执行一遍数据库迁移操作，保证使用的数据库中会有一个叫做django-session的表
    
    session依赖cookie：
    	当你使用request.session设置和保存session信息后，返回的response对象会设置个cookie信息，保存的数据是sessionid。当你第二次通过request.session获取相应的session信息时，其实是根据请求头中的cookie中保存的sessionid查到的。
    
```

---

04-类视图

```
在example应用中的views.py定义一个类视图，并注册好路由，先添加一个get方法，测试能否正常访问；
demo：
	from django.views.generic import View

    class TestClassView(View):
    """类视图：处理注册"""

    def get(self, request):
        """处理GET请求，返回注册页面"""
        return JsonResponse(dict(msg="class view ok"))

    def post(self, request):
        """处理POST请求，实现注册逻辑"""
        return JsonResponse(dict(msg="class view post"))

注册路由：
	path('testClass/', views.TestClassView.as_view()),
	
类视图的优点：
	1.使我们的视图代码的功能区分更加清晰
	2.代码可读性好
	3.类视图相对于函数视图有更高的复用性， 如果其他地方需要用到某个类视图的某个特定逻辑，直接继承该类视图即可
	

类视图的实现原理分析：
	# 简单理解
    # views.TestClassView.as_view()  >> view
    # view() >> self.dispatch()
    # self.dispatch() >> getattr(self, method) >> handler()

为类视图中的方法添加装饰器「1.在路由中装饰，2.在类视图中装饰，3.使用扩展类装饰」：
	推荐直接在类视图中装饰[第二种]，并且使用method_decorator去处理。因为有的时候一个装饰器可能需要同时被函数视图和类视图使用。并且在类视图中可能只有部分的方法需要被装饰。

⚠️：类视图中的方法，接收参数、返回响应和普通的函数视图是一样的。

```

---

05-中间件

```
⚠️ 中间件写好之后一定要记得注册哟

第一种方法：通过中间件工厂函数创建中间件
实践：通过中间件解决跨域请求的问题：

	def CORSMiddleware(get_response):
    """
    处理CORS跨域请求限制的中间件;
    在配置文件的CORS_ALLOWED_HOSTS_AND_METHOD列表中添加你允许的域名和该域名下运气请求的方式即可
    :param get_response: 框架内部用来在请求处理过程中获取视图响应的函数
    :return:返回中间层对象
    """
    # 当项目启动时执行,这里我们获取本后端允许访问的域名

    __CORS_dict = __GlobleSettings.CORS_ALLOWED_HOSTS_AND_METHOD
    __allow_hosts = __CORS_dict.keys()

    def middleware(request):
        # 每次请求前被调用的代码:
        __headers = request.META
        __origin_host = __headers.get("HTTP_ORIGIN")

        response = get_response(request)

        # 每次请求视图执行完后获取到响应体代码之后执行的代码
        if __origin_host and __origin_host in __allow_hosts:

            __allow_methods = __CORS_dict.get(__origin_host)

            if request.method == "OPTIONS":
                response["Access-Control-Allow-Origin"] = __origin_host
                response["Access-Control-Allow-Credentials"] = "true"
                response["Access-Control-Allow-Headers"] = __headers.get("HTTP_ACCESS_CONTROL_REQUEST_HEADERS")
                response["Access-Control-Allow-Method"] = ", ".join(__allow_methods)

            if request.method in __allow_methods:
                response["Access-Control-Allow-Origin"] = __origin_host
                response["Access-Control-Allow-Credentials"] = "true"

        return response

    return middleware
    
⚠️：当前中间件还没有解决跨域的CSRF验证问题    


第二种方法：通过继承中间件类创建中间件
简单理解：创建类，写固定名称的方法
https://www.cnblogs.com/zhaof/p/6281541.html

```

06-数据库与使用内置的ORM操作数据库

```
配置：
	默认使用的是sqlite3数据库：https://baike.baidu.com/item/SQLite/375020?fr=aladdin
使用其他数据库的配可以通过settings文件提供的URL查看：
	https://docs.djangoproject.com/en/2.1/ref/settings/#databases
	主要区别在于：使用的内置引擎不一样
	
定义模型类：
	模型类被定义在"应用/models.py"文件中。
	模型类必须继承自Model类，位于包django.db.models中。
	
有外键关系时要删除一个数据需要指定如何处理外键引用表的数据。不用太担心这个问题，工作中几乎不会删除数据，最多就做逻辑删除。被逻辑删除掉的数据，在查询时应当不显示，查的过程中过滤掉，可以通过自定义的Mangar管理器实现。

查询集，也称查询结果集、QuerySet，表示从数据库中获取的对象集合。
当调用如下过滤器方法时，Django会返回查询集（而不是简单的列表）：
    all()：返回所有数据。
    filter()：返回满足条件的数据。
    exclude()：返回满足条件之外的数据。
    order_by()：对结果进行排序。
    
两大特性
1）惰性执行
创建查询集不会访问数据库，直到调用数据时，才会访问数据库，调用数据的情况包括迭代、序列化、与if合用
2）缓存
使用同一个查询集，第一次使用时会发生数据库的查询，然后Django会把结果缓存下来，再次使用这个查询集时会使用缓存的数据，减少了数据库的查询次数。

限制查询集
可以对查询集进行取下标或切片操作，等同于sql中的limit和offset子句。
注意：不支持负数索引。
对查询集进行切片后返回一个新的查询集，不会立即执行查询。

大胆的猜测：
	Django中使用from django.core.paginator import Paginator 做分页处理时，Paginator对象可能就是对查询集做了切片处理，每次查询的分页数据其实是不同的查询语句的结果而已。这样可以不用先把所有数据查出来保存到内存，然后再进行分页。可以节省内存。

```

