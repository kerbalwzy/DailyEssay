## DjangoRestFramework框架必知必会

#### 一、前后端不分离与分离的两种应用模式

- ##### 前后端不分离

  ```
  在前后端不分离的应用模式中，前端页面看到的效果都是由后端控制，由后端渲染页面或重定向，也就是后端需要控
  制前端的展示，前端与后端的耦合度很高。
  这种应用模式比较适合纯网页应用，但是当后端对接App时，App可能并不需要后端返回一个HTML网页，而仅仅是数
  据本身，所以后端原本返回网页的接口不再适用于前端App应用，为了对接App后端还需再开发一套接口。
  ```

- ##### 前后端分离

  ```
  在前后端分离的应用模式中，后端仅返回前端所需的数据，不再渲染HTML页面，不再控制前端的效果。至于前端用户
  看到什么效果，从后端请求的数据如何加载到前端中，都由前端自己决定，网页有网页的处理方式，App有App的处理
  方式，但无论哪种前端，所需的数据基本相同，后端仅需开发一套逻辑对外提供数据即可。
  在前后端分离的应用模式中 ，前端与后端的耦合度相对较低。
  ```

- ##### 接口或API

  ```
  在前后端分离的应用模式中，我们通常将后端开发的每个视图都称为一个接口，或者API，前端通过访问接口来对数据
  进行增删改查。
  ```

---

#### 二、REST接口开发的核心任务

- ### `将数据库数据序列化为前端所需要的格式，并返回；`

- ### `将前端发送的数据反序列化为模型类对象，并保存到数据库中。`

---

#### 三、序列化与反序列化概念

- ##### 序列化

  ```
  将程序中的一个数据结构类型转换为其他格式（字典、JSON、XML等），例如将Django中的模型类对象装换为JSON
  字符串，这个转换过程我们称为序列化。
  ```

- ##### 反序列化

  ```
  将其他格式（字典、JSON、XML等）转换为程序中的数据，例如将JSON字符串转换为Django中的模型类对象，这个
  过程我们称为反序列化。
  ```

----

#### 四、DjangoRestFramework框架中request对象的2个常用属性

- ##### query_params属性

  ```
  request.query_params与Django标准的request.GET相同，只是更换了更正确的名称而已。
  ```

- ##### data属性

  ```
  request.data 返回解析之后的请求体数据。类似于Django中标准的request.POST和 request.FILES属性，但提供如下特性：
      包含了解析之后的文件和非文件数据
      包含了对POST、PUT、PATCH请求方式解析后的数据
      利用了REST framework的parsers解析器，不仅支持表单类型数据，也支持JSON数据
  ```

---

#### 五、DRF中序列化与反序列化功能的基本使用步骤

- ##### 序列化功能

  ```
  1.根据模型类和数据需求去创将一个序列化器类
  2.查询出一个模型类的对象或查询集
  3.创建对应的序列化器对象，将模型类的对象或查询集作为初始化实参传给形参instance，当是查询集时需要额外
  附带一个参数：many=True。
  4.通过序列化器对象的 data 属性，即可获得获得序列化之后的数据。
  注：步骤就是这么简单，重点在于定义序列化器类时给字段设置的数据类型和约束条件。如果与模型类不匹配可能会
  出现问题。
  ```

- ##### 反序列化功能

  ```
  1.获取从前端发送来的数据，并将数据转换为Python的字典类型。
  2.创建对应的序列化器对象，将数据字典作为初始化实参传给形参data。如果是update操作，instance形参也要
  接实参，还如果是部分update的话，需要额外附带一个参数：partial=True
  3.调用序列化器的 is_valid()方法检验数据，此方法返回一个布尔值，当结果为True时才能继续执行代码。可以
  通过在这个方法中传入参数：raise_exception=True，当验证失败时会直接中止当前视图并向前端返回一个HTTP
  400 Bad Request的响应。
  4.验证成功，可以通过序列化器对象的validated_data属性获取验证后的数据，拿去做其他使用。也可以通过调用
  序列化器对象的save方法,尝试将数据保存到数据库.
  ```

----

#### 六、DRF中的序列化器

- ##### 模型类序列化器与普通序列化器的区别

  ```
  ModelSerializer与常规的Serializer相同，但提供了：
      基于模型类自动生成一系列字段
      基于模型类自动为Serializer生成validators「一系列的验证器」
      包含默认的create()和update()的实现「用于更新或保存数据库中的数据」
  ```

- ##### 模型类序列化器类中内部定义的 Meta类「固定名称」的常用类属性及含义

  ```
  model 				指明参照哪个模型类
  fields 				指明为模型类的哪些字段生成
  exclude 			可以明确排除掉哪些字段
  ead_only_fields		指明只读字段，即仅用于序列化输出的字段
  extra_kwargs 		参数为ModelSerializer添加或修改原有的选项参数
  ```

- ##### 关联对象的层级嵌套序列化解决方案

  ```
  1.在普通序列化器类和模型类序列化器类中作为 类属性显示声明:
  属性值可以是以下几种:
  1.serializers.PrimaryKeyRelatedField(*args)			关联字段的主键
  2.serializers.HyperlinkedRelatedField(*args)		关联对象数据的接口链接
  3.serializers.SlugRelatedField(*args)				关联对象的指定字段数据
  4.直接是关联对象的序列化器								关联对象的所有数据
  
  2.在模型类序列化器的内部定义的 Meta类「固定名称」的嵌套序列化层级属性:
  	depth	来简单的生成嵌套表示，depth应该是整数，表明嵌套的层级数量。
  ```

----

#### 七、DRF中的类视图基类与视图集

- ##### APIView基类

  ```
  APIView是REST framework提供的所有视图的基类，继承自Django的View父类。
  
  APIView与View的不同之处在于:
    传入到视图方法中的是REST framework的Request对象，而不是Django的HttpRequeset对象;
    视图方法可以返回RESTframework的Response对象，视图会为响应数据设置（render）符合前端要求的格式;
    任何APIException异常都会被捕获到，并且处理成合适的响应信息;
    在进行dispatch()分发前，会对请求进行身份认证、权限检查、流量控制。
  
  支持定义的属性：
    authentication_classes 列表或元祖，身份认证类
    permissoin_classes 列表或元祖，权限检查类
    throttle_classes 列表或元祖，流量控制类
  
  在APIView中仍以常规的类视图定义方法来实现get() 、post() 或者其他请求方式的方法。
  ```

- ##### GenericAPIView基类

  ```
  继承自APIVIew，增加了对于列表视图和详情视图可能用到的通用支持方法。通常使用时，可搭配一个或多个Mixin扩展类。
  
  支持定义的属性：
      列表视图与详情视图通用：
          queryset 列表视图的查询集
          serializer_class 视图使用的序列化器
      列表视图使用：
          pagination_class 分页控制类
          filter_backends 过滤控制后端
      详情页视图使用：
          lookup_field 查询单一数据库对象时使用的条件字段，默认为'pk'
          lookup_url_kwarg 查询单一数据时URL中的参数关键字名称，默认与look_field相同
  
  提供的方法：
      列表视图与详情视图通用：
          get_queryset(self) 返回视图使用的查询集，是列表视图与详情视图获取数据的基础，默认返回
          queryset属性，可以重写.
          
          get_serializer_class(self) 返回序列化器类，默认返回serializer_class，可以重写.
          
  		get_serializer(self, args, *kwargs) 返回序列化器对象，被其他视图或扩展类使用，如果我们
  		在视图中想要获取序列化器对象，可以直接调用此方法。
  	
  	详情视图使用：
          get_object(self) 返回详情视图所需的模型类数据对象，默认使用lookup_field参数来过滤
          queryset。 在试图中可以调用该方法获取详情信息的模型类对象。若详情访问的模型类对象不存在，会
          返回404。该方法会默认使用APIView提供的check_object_permissions方法检查当前对象是否有权
          限被访问。
  ```

- ##### 视图集与自定义action动作

  ```
  使用视图集ViewSet，可以将一系列逻辑相关的动作放到一个类中：
      list() 提供一组数据
      retrieve() 提供单个数据
      create() 创建数据
      update() 保存数据
      destory() 删除数据
  ViewSet视图集类不再实现get()、post()等方法，而是实现动作 action 如 list() 、create() 等。
  在视图集中，我们可以通过action对象属性来获取当前请求视图集时的action动作是哪个。
  
  常用视图集父类:
  	1)ViewSet
          继承自APIView，作用也与APIView基本类似，提供了身份认证、权限校验、流量管理等。
          在ViewSet中，没有提供任何动作action方法，需要我们自己实现action方法。
  
      2）GenericViewSet
          继承自GenericAPIView，作用也与GenericAPIVIew类似，提供了get_object、get_queryset等方
          法便于列表视图与详情信息视图的开发。
  
      3）ModelViewSet
      	继承自GenericAPIVIew，同时包括了ListModelMixin、RetrieveModelMixin、
      	CreateModelMixin、UpdateModelMixin、DestoryModelMixin。
  
      4）ReadOnlyModelViewSet
      	继承自GenericAPIVIew，同时包括了ListModelMixin、RetrieveModelMixin。
  ```

  ```
  视图集中定义附加action动作
  在视图集中，除了上述默认的方法动作外，还可以添加自定义动作。
  
  添加自定义动作需要使用rest_framework.decorators.action装饰器。
  
  以action装饰器装饰的方法名会作为action动作名，与list、retrieve等同。
  action装饰器可以接收两个参数：
      methods: 该action支持的请求方式，列表传递
      detail: 表示是action中要处理的是否是视图资源的对象（即是否通过url路径获取主键）
          True 表示使用通过URL获取的主键对应的数据对象
          False 表示不使用URL获取主键
  ```

----

#### 八、DRF框架的优、缺点

- ```
  特点「优点」：
  	提供了定义序列化器Serializer的基类，可以快速根据 Django ORM 或者其它库自动序列化/反序列化；
      提供了丰富的类视图、Mixin扩展类，简化视图的编写；
      丰富的定制层级：函数视图、类视图、视图集合到自动生成 API，满足各种需要；
      多种身份认证和权限认证方式的支持；
      内置了限流系统；
      直观的 API web 界面；
      可扩展性，插件丰富
   
  缺点：
  	封装过于完善，自己写的代码很少。一旦程序出现异常，排除异常比较困难。
  ```
