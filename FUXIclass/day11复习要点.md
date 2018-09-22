复习要点：第十一天 DRF框架之视图与视图集

---

##### 01-DRF中的 两个视图基类 、 Request与Response对象

- 视图集类一：APIView

```
APIView是DRF提供的所有视图的基类，继承自Django的View父类。
	导入方式：rest_framework.views.APIView

APIView与Django原生View的不同之处在于：
    1.传入到视图方法中的是DRF的Request对象，而不是Django的HttpRequeset对象；
    2.视图方法可以返回DRF的Response对象，视图会为响应数据设置（render）符合前端要求的格式；
    3.任何APIException异常都会被捕获到，并且处理成合适的响应信息；
	4.在进行dispatch()分发前，会对请求进行身份认证、权限检查、流量控制。

该视图类支持定义的属性：
    authentication_classes 列表或元祖，身份认证类
    permissoin_classes 列表或元祖，权限检查类
    throttle_classes 列表或元祖，流量控制类
    renderer_classes 列表或元祖，控制使用的渲染器。视图类中的规定优先级大于全局的默认配
    
在APIView中仍以常规的类视图定义方法来实现get() 、post() 或者其他请求方式的方法。
```

- DRF提供的Request与Response对象

  ```
  1.Request对象
  继承于DRF框架的视图类的视图方法中接收的request对象不再是Django默认的HttpRequest对象，而是REST framework提供的扩展了HttpRequest类的Request类的对象。
  
  Request对象的数据是自动根据前端发送数据的格式进行解析之后的结果。
  	原理：DRF提供了Parser「解析器」，在接收到请求后会自动根据请求头中Content-Type指明的请求数据类型（如JSON、表单等）将请求数据进行解析，解析为类字典对象保存到Request对象中。因此，无论前端发送的哪种格式的数据，我们都可以以统一的方式读取数据。
  
  常用属性
  1）.data
  	request.data返回解析之后的请求体数据。类似于Django中标准的request.POST、request.FILES、request.body 属性，但提供如下特性：
      包含了解析之后的文件和非文件数据
      包含了对POST、PUT、PATCH等请求方式解析后的数据
      利用了REST framework的parsers解析器，不仅支持表单类型数据，也支持JSON数据
  2）.query_params
  	request.query_params与Django标准的request.GET相同，只是更换了更正确的名称而已。
  	
  ```

  ```
  2. Response对象「rest_framework.response.Response」
  DRF提供了一个响应类Response，使用该类构造响应对象时，响应的具体数据内容会被转换（render渲染）成符合前端需求的类型。
  
  DRF提供了Renderer「渲染器」，用来根据请求头中的Accept（接收数据类型声明）来自动转换响应数据到对应格式。如果前端请求中未进行Accept声明，则会采用默认方式处理响应数据，我们可以通过配置来修改默认响应格式。
  渲染器使用的官方文档：http://www.django-rest-framework.org/api-guide/renderers/
  
  构造响应体对象的方式：
  	Response(data, status=None, template_name=None, headers=None, content_type=None)
  	其中的参数data数据不能是render处理之后的数据，只需传递python的内建类型数据即可，REST framework会使用renderer渲染器处理data。但是data不能是复杂结构的数据，如Django的模型类对象，对于这样的数据我们可以使用Serializer序列化器序列化处理后（转为了Python字典类型）再传递给data参数。
  
      参数说明：
          data: 为响应准备的序列化处理后的数据；
          status: 状态码，默认200；
          template_name: 模板名称，如果使用HTMLRenderer 时需指明；
          headers: 用于存放响应头信息的字典；
          content_type: 响应数据的Content-Type，通常此参数无需传递，REST framework会根据前端所需类型数据来设置该参数。
  
  创建好的response对象的常用属性：
  	1）.data 			传给response对象的序列化后，但尚未render处理的数据
      2）.status_code		状态码的数字
      3）.content			经过render处理后的响应数据
  
  状态码：
  为了方便设置状态码，REST framewrok在rest_framework.status模块中提供了常用状态码常量。具体内容参考课件
  ```

- 视图基类GenericAPIView

```
GenericAPIView继承自APIVIew，增加了对于列表视图和详情视图可能用到的通用支持方法。通常使用时，可搭配一个或多个Mixin扩展类。
	导入方式：rest_framework.generics.GenericAPIView

GenericAPIView与Django原生View的不同之处在于：请参考类的继承。

该视图类支持定义更多的属性：
    列表视图与详情视图通用：
        queryset 列表视图的查询集
        serializer_class 视图使用的序列化器
    列表视图使用：
        pagination_class 分页控制类
        filter_backends 过滤控制后端
    详情页视图使用：
        lookup_field 查询单一数据库对象时使用的条件字段，默认为'pk'，这里是从路由中获取
        lookup_url_kwarg 查询单一数据时URL中的参数关键字名称，默认与look_field相同

该视图类提供的方法：
	列表视图与详情视图通用：
		get_queryset(self) 返回视图使用的查询集，是列表视图与详情视图获取数据的基础，默认返回queryset属性，可以重写。
		get_serializer_class(self) 返回序列化器类，默认返回serializer_class，可以重写
		get_serializer(self, args, *kwargs) 返回序列化器对象，被其他视图或扩展类使用，如果我们在视图中想要获取序列化器对象，可以直接调用此方法。注意，在提供序列化器对象的时候，REST framework会向对象的context属性补充三个数据：request、format、view，这三个数据对象可以在定义序列化器时使用。
		
	详情视图使用：
		get_object(self) 返回详情视图所需的模型类数据对象，默认使用lookup_field参数来过滤queryset。 在试图中可以调用该方法获取详情信息的模型类对象。若详情访问的模型类对象不存在，会返回404。该方法会默认使用APIView提供的check_object_permissions方法检查当前对象是否有权限被访问。
```

---

#### 02-Mixin扩展类与DRF内置的功能视图类

```
理解作用：帮助我们写视图内部的逻辑代码
使用方法：配合GenericAPIView类一起作为自己创建的视图类的父类使用「多继承」

1）ListModelMixin
列表视图扩展类，提供list(request, *args, **kwargs)方法快速实现列表视图，返回200状态码。该Mixin的list方法会对数据进行过滤和分页。

2）CreateModelMixin
创建视图扩展类，提供create(request, *args, **kwargs)方法快速实现创建资源的视图，成功返回201状态码。
如果序列化器对前端发送的数据验证失败，返回400错误。

3）RetrieveModelMixin
详情视图扩展类，提供retrieve(request, *args, **kwargs)方法，可以快速实现返回一个存在的数据对象。
如果存在，返回200， 否则返回404。

4）UpdateModelMixin
更新视图扩展类，提供update(request, *args, **kwargs)方法，可以快速实现更新一个存在的数据对象。
同时也提供partial_update(request, *args, **kwargs)方法，可以实现局部更新。
成功返回200，序列化器校验数据失败时，返回400错误。

5）DestroyModelMixin
删除视图扩展类，提供destroy(request, *args, **kwargs)方法，可以快速实现删除一个存在的数据对象。
成功返回204，不存在返回404。
```

```
DRF框架中已经封装好的，同时继承于GenericAPIView类和Mixin扩展类的几个功能视图类
1） CreateAPIView
提供 post 方法
继承自： GenericAPIView、CreateModelMixin

2）ListAPIView
提供 get 方法
继承自：GenericAPIView、ListModelMixin

3）RetireveAPIView
提供 get 方法
继承自: GenericAPIView、RetrieveModelMixin

4）DestoryAPIView
提供 delete 方法
继承自：GenericAPIView、DestoryModelMixin

5）UpdateAPIView
提供 put 和 patch 方法
继承自：GenericAPIView、UpdateModelMixin

6）RetrieveUpdateAPIView
提供 get、put、patch方法
继承自： GenericAPIView、RetrieveModelMixin、UpdateModelMixin

7）RetrieveUpdateDestroyAPIView
提供 get、put、patch、delete方法
继承自：GenericAPIView、RetrieveModelMixin、UpdateModelMixin、DestoryModelMixin

```

---

#### 03-视图集ViewSet

```
作用：使用视图集ViewSet，可以将一系列逻辑相关的动作放到一个视图类中：
        list() 提供一组数据
        retrieve() 提供单个数据
        create() 创建数据
        update() 保存数据
        destory() 删除数据
     ViewSet视图集类不再实现get()、post()等方法，而是实现动作 action 如 list() 、create() 等。
	 视图集只在配置路由时使用as_view()方法的时候，才会将action动作与具体请求方式对应上。

视图集的action属性：
	实际开发中的用处：在视图集中，我们可以通过action对象属性来获取当前请求视图集时的action动作是哪个。并通过重写get_serializer_class(self)方法根据action属性来选择使用哪个序列化器。

视图集中自定义更多的action动作：
    添加自定义动作需要使用rest_framework.decorators.action装饰器。
    以action装饰器装饰的方法名会作为action动作名，与list、retrieve等同。
    action装饰器可以接收两个参数：
        methods: 该action支持的请求方式，列表传递["GET","POST",...]
        detail: 表示是action中要处理的是否是视图资源的对象（即是否通过url路径获取主键）
            True 表示使用通过URL获取的主键对应的数据对象
            False 表示不使用URL获取主键
 
DRF中常用的已经封装好的了的视图集父类：
	1） ViewSet
    继承自APIView，作用也与APIView基本类似，提供了身份认证、权限校验、流量管理等。
    在ViewSet中，没有提供任何动作action方法，需要我们自己实现action方法。

    2）GenericViewSet
    继承自GenericAPIView，作用也与GenericAPIVIew类似，提供了get_object、get_queryset等方法便于列表视图与详情信息视图的开发。

    3）ModelViewSet
    继承自GenericAPIVIew，同时包括了ListModelMixin、RetrieveModelMixin、CreateModelMixin、UpdateModelMixin、DestoryModelMixin。

    4）ReadOnlyModelViewSet
    继承自GenericAPIVIew，同时包括了ListModelMixin、RetrieveModelMixin。

使用视图集时的路由配置示例：
    urlpatterns = [
        url(r'^books/$', views.BookInfoViewSet.as_view({'get': 'list'})),
        url(r'^books/latest/$', views.BookInfoViewSet.as_view({'get': 'latest'})),
        url(r'^books/(?P<pk>\d+)/$', views.BookInfoViewSet.as_view({'get': 'retrieve'})),
        url(r'^books/(?P<pk>\d+)/read/$', views.BookInfoViewSet.as_view({'put': 'read'})),
    ]
    ⚠️：视图集只在配置路由时使用as_view()方法的时候，才会将action动作与具体请求方式对应上。
    
```

---

#### 04-路由Routers

```
对于视图集ViewSet，我们除了可以自己手动指明请求方式与动作action之间的对应关系外，还可以使用Routers来帮助我们快速实现路由信息。

REST framework提供了两个router
    SimpleRouter
    DefaultRouter

使用方法：
	1） 创建router对象，并注册视图集
		register(prefix, viewset, base_name)
        参数：prefix 		该视图集的路由前缀
             viewset 	  视图集
             base_name    路由名称的前缀
	
	2）添加路由数据
		urlpatterns = [
    		...
		]
        urlpatterns += router.urls
        
        或者：
        urlpatterns = [
            ...
            url(r'^', include(router.urls))
        ]


DefaultRouter与SimpleRouter的区别是，DefaultRouter会多附带一个默认的API根视图，返回一个包含所有列表视图的超链接响应数据。

学习使用DRF自动生成接口文档
```

---

#### 05-DRF框架的使用学习重点

- #### 定义模型类序列器

- 序列化与反序列化功能的使用

- Request和Response对象

- GenericAPIView

- #### Mixin扩展类

- #### 视图集

- #### 构建API文档页面
