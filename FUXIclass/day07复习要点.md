复习要点：第七天-跨域请求、ORM对象关系映射

---

#### 01-WSGI协议相关

```
首先介绍几个关于WSGI相关的概念：
    WSGI：全称是Python Web Server Gateway Interface，WSGI不是服务器，python模块，框架，API或者任何软件，只是一种规范，描述web server如何与web application通信的规范。server和application的规范在PEP3333中有具体描述。要实现WSGI协议，必须同时实现web server和web application，当前运行在WSGI协议之上的web框架有Torando,Flask,Django

    uwsgi：与WSGI一样是一种通信协议，是uWSGI服务器的独占协议，用于定义传输信息的类型(type of information)，每一个uwsgi packet前4byte为传输信息类型的描述，与WSGI协议是两种东西，据说该协议是fcgi协议的10倍快。【https://uwsgi-docs-zh.readthedocs.io/zh_CN/latest/Protocol.html】

    uWSGI：是一个web服务器,C语言编写，实现了WSGI协议、uwsgi协议、http协议等。

WSGI协议中规范的实现：
	web-server部分：
		1，监听请求并将请求报文解析为一个environ字典，这个字典包含了请求信息和服务器的一些信息
		2，提供一个给web-application设置响应行信息和头信息的callable对象，一般这个对象的名字是start_response，并且这个对象接受两个必须的参数，status(状态码+状态描述string)和response_headers(响应消息的头)
		3，调用web-application端的callable对象
	web-application部分：
		1，Application必须是一个可调用的对象（实现了__call__ 函数的方法或者类的对象）
		2，接受两个参数 environ（WSGI 的环境信息） 和 start_response（开始响应请求的函数）
		3，Application对象内部返回最终的值之前要先调用start_response
		4，Application被调用后的返回值是iterable的数据。
	
WSGI协议其实是定义了一种server与application解耦的规范，即可以有多个实现WSGI server的服务器，也可以有多个实现WSGI application的框架，那么就可以选择任意的server和application组合实现自己的web应用。例如uWSGI和Gunicorn都是实现了WSGI server协议的服务器，Django，Flask是实现了WSGI application协议的web框架，可以根据项目实际情况搭配使用。

实际环境使用的WSGI服务器
	因为每个web框架都不是专注于实现服务器方面的，因此，在生产环境部署的时候使用的服务器也不会简单的使用web框架自带的服务器，这里，我们来讨论一下用于生产环境的服务器有哪些？

1.gunicorn
Gunicorn（从Ruby下面的Unicorn得到的启发）应运而生：依赖Nginx的代理行为，同Nginx进行功能上的分离。由于不需要直接处理用户来的请求（都被Nginx先处理），Gunicorn不需要完成相关的功能，其内部逻辑非常简单：接受从Nginx来的动态请求，处理完之后返回给Nginx，由后者返回给用户。
由于功能定位很明确，Gunicorn得以用纯Python开发：大大缩短了开发时间的同时，性能上也不会很掉链子。同时，它也可以配合Nginx的代理之外的别的Proxy模块工作，其配置也相应比较简单。
配置上的简单，大概是它流行的最大的原因。

2.uWSGI【具体使用复习项目部署的时候再配合着Nginx一起复习】
因为使用C语言开发，会和底层接触的更好，配置也是比较方便，目前和gunicorn两个算是部署时的唯二之选。

3.bjoern【比约恩】
Python WSGI界最牛逼性能的Server其中一个是bjoern，纯C，小于1000行代码，就是看不惯uWSGI的冗余自写的。
使用方法：http://hao.jobbole.com/bjoern/
开源地址：https://github.com/jonashaag/bjoern#libev
```

---

#### 02-科普WEB开发常见安全问题：

	https://blog.csdn.net/fengyinchao/article/details/50775121

---

#### 03-同源策略与跨域请求

- ##### 什么叫做浏览器的同源策略？

  参照GitHub上某位前端大佬的说法如下：

  https://github.com/acgotaku/WebSecurity/blob/master/docs/content/Browser_Security/Same-Origin-Policy.md#same-origin-policy

  同源策略（Same Origin Policy）是一种约定，它是浏览器最核心也是最基本的安全功能，如果缺少了同源策略，则浏览器的正常功能可能会受到影响。可以说Web是构建在同源策略的基础之上的，浏览器只是针对同源策略的一种实现。

  **浏览器的同源策略，限制了来自不同源的“document”或脚本，对当前“document”读取或设置某些属性。**

  这一策略是极其重要的，试想如果没有同源策略，可能 a.com 的一段 JavaScript 脚本，在 b.com 未曾加载此脚本时，也可以随意涂改 b.com 的页面（在浏览器的显示中）。为了不让浏览器的页面行为发生混乱，浏览器提出了“Origin”（源）这一概念，来自不同 Origin的对象无法互相干扰。 对于JavaScript来说，以下情况被认为是同源与不同源的：

  | URL                                       | OutCome | Reason             |
  | ----------------------------------------- | ------- | ------------------ |
  | <http://test.icehoney.me/test1.html>      | Success |                    |
  | <http://test.icehoney.me/dir1/test2.html> | Success |                    |
  | https://test.icehoney.me/secure.html      | Failure | Different protocol |
  | <http://test.icehoney.me:81/secure.html>  | Failure | Different port     |
  | <http://blog.icehoney.me/secure.html>     | Failure | Different host     |

  由上表可知，影响“源”的因素有：host（域名或IP地址，如果是IP地址则看做一个根域名）、子域名、端口、协议。 

- ##### 从后端的角度思考🤔：

  出现跨域请求限制和我们后端的代码没有任何关系，都是浏览器在做约束。实际上这个跨域的请求我们后端服务器是有接收到的，而且我们通常情况下也选择正常的给这个请求返回数据。但是由于在响应头中少了一些特定的字段，浏览器认为这些响应的数据是后端在不知情的情况下返回的，没有真正确认这个请求的合法性。所以浏览器虽然拿到了数据，但是不会解析并返回给请求的发送方，而是在控制台上抛出一个跨域请求的权限错误提示。

- ##### 对比有无跨域请求情况时，请求信息的不同

  发送GET请求时，对比发现在请求头信息中多出了一个 Origin 字段信息

  发送POST请求时，我们发现POST请求莫名奇妙的变成了OPTIONS请求，这是因为浏览器发现是跨域的POST请求后会先发送一个OPTIONS请求进行预检，确认服务器的响应信息中允许该请求时才会再次真正的发送POST请求。先不管真正的POST请求，对比发现在请求头信息中多出了 Access-Control-Request-XXX 等字段信息。说明在跨域请求时，浏览器会主动的将一些特殊信息发送给服务器。

- ### 如何通过添加响应头就直接解决跨域请求限制的问题？

  ##### HTTP访问控制（CORS）之HTTP 响应首部字段

  ### Access-Control-Allow-Origin

  响应首部中可以携带一个 `Access-Control-Allow-Origin` 字段，其语法如下:`

  ```
  Access-Control-Allow-Origin: <origin> | *
  ```

  其中，origin 参数的值指定了允许访问该资源的外域 URI。对于不需要携带身份凭证的请求，服务器可以指定该字段的值为通配符，表示允许来自所有域的请求。

  例如，下面的字段值将允许来自 [http://mozilla.com](http://mozilla.com/) 的请求：

  ```
  Access-Control-Allow-Origin: http://mozilla.com
  ```

  如果服务端指定了具体的域名而非“*”，那么响应首部中的 Vary 字段的值必须包含 Origin。这将告诉客户端：服务器对不同的源站返回不同的内容。

  ### Access-Control-Expose-Headers

  在跨域访问时，XMLHttpRequest对象的getResponseHeader()方法只能拿到一些最基本的响应头，Cache-Control、Content-Language、Content-Type、Expires、Last-Modified、Pragma，如果要访问其他头，则需要服务器设置本响应头。

  `Access-Control-Expose-Headers`头让服务器把允许浏览器访问的头放入白名单，例如：

  ```
  Access-Control-Expose-Headers: X-My-Custom-Header, X-Another-Custom-Header
  ```

  这样浏览器就能够通过getResponseHeader访问`X-My-Custom-Header`和 `X-Another-Custom-Header` 响应头了。

  ### Access-Control-Max-Age

  `Access-Control-Max-Age`头指定了preflight请求的结果能够被缓存多久，请参考本文在前面提到的preflight例子。

  ```
  Access-Control-Max-Age: <delta-seconds>
  ```

  `delta-seconds` 参数表示preflight请求的结果在多少秒内有效。

  ### Access-Control-Allow-Credentials

  `Access-Control-Allow-Credentials`头指定了当浏览器的`credentials`设置为true时是否允许浏览器读取response的内容。当用在对preflight预检测请求的响应中时，它指定了实际的请求是否可以使用`credentials`。

  请注意：简单 GET 请求不会被预检；如果对此类请求的响应中不包含该字段，这个响应将被忽略掉，并且浏览器也不会将相应内容返回给网页。

  ```
  Access-Control-Allow-Credentials: true
  ```

  ### Access-Control-Allow-Methods

  `Access-Control-Allow-Methods`首部字段用于预检请求的响应。其指明了实际请求所允许使用的 HTTP 方法。

  ```
  Access-Control-Allow-Methods: <method>[, <method>]*
  ```

  ### Access-Control-Allow-Headers

  `Access-Control-Allow-Headers`首部字段用于预检请求的响应。其指明了实际请求中允许携带的首部字段。

  ```
  Access-Control-Allow-Headers: <field-name>[, <field-name>]*
  ```

  ⚠️：SO，了解了这么多，是不是该写代码去验证一下啊？？

  https://github.com/kerbalwzy/aboutPython/blob/master/work-miniFrame.md#%E4%BA%8C%E8%A7%A3%E5%86%B3%E8%B7%A8%E5%9F%9F%E8%AF%B7%E6%B1%82%E9%99%90%E5%88%B6%E7%9A%84%E7%AE%80%E5%8D%95%E6%96%B9%E6%B3%95%E8%AE%A4%E8%AF%86%E6%B5%8F%E8%A7%88%E5%99%A8%E7%9A%84%E5%90%8C%E6%BA%90%E7%AD%96%E7%95%A5

  总结：

- #### 在处理跨域请求时，第一步是判断这个请求是否是跨域而来的，如果是再根据请求方式往响应头里添加告知浏览器允许跨域请求的请求头信息。

  #### 针对跨域而来的GET或POST请求，必需要在响应头中添加：

  #### `Access-Control-Allow-Origin`、`Access-Control-Allow-Credentials`

  #### 而针对特殊的OPTIONS预检请求，必需要在响应头中添加：

  #### `Access-Control-Allow-Origin`、`Access-Control-Allow-Credentials`

  #### `Access-Control-Allow-Methods`、`Access-Control-Allow-Headers`

---

#### 04-ORM对象关系映射

```
基本概念：
	对象-关系映射（OBJECT/RELATIONALMAPPING，简称ORM），是随着面向对象的软件开发方法发展而产生的。用来把对象模型表示的对象映射到基于SQL的关系模型数据库结构中去。这样，我们在具体的操作实体对象的时候，就不需要再去和复杂的 SQL 语句打交道，只需简单的操作实体对象的属性和方法 [2]  。ORM 技术是在对象和关系之间提供了一条桥梁，前台的对象型数据和数据库中的关系型的数据通过这个桥梁来相互转化
	简单理解：
		在Python中将我们对模型类的操作翻译成SQL语句去执行，将执行的数据结果又重新翻译成我们的Python中的对象；

自己实现一个简单的ORM模块：
	代码示例【了解ORM模块在做什么事情即可】：
	https://github.com/justoneliu/web_app/blob/d3/www/orm.py
	
SQLAlchamy和Django内置的ORM模块在执行迁移时，是如何获取到我们定义的模型类的字段信息的？
	https://github.com/kerbalwzy/aboutPython/blob/master/work-miniFrame.md#%E4%B8%89%E4%BA%86%E8%A7%A3orm%E6%A8%A1%E5%9D%97%E6%98%AF%E5%A6%82%E4%BD%95%E9%80%9A%E8%BF%87%E6%A8%A1%E5%9E%8B%E7%B1%BB%E8%8E%B7%E5%8F%96%E5%88%B0%E6%95%B0%E6%8D%AE%E8%A1%A8%E5%AD%97%E6%AE%B5%E4%BF%A1%E6%81%AF%E7%9A%84
```

---

#### 05-GIT仓库代码管理

```
SVN：https://www.cnblogs.com/zhoumiao/p/5459552.html

基本了解：
	Git(读音为/gɪt/。)是一个开源的分布式版本控制系统，可以有效、高速的处理从很小到非常大的项目版本管理。 [1]  Git 是 Linus Torvalds 为了帮助管理 Linux 内核开发而开发的一个开放源码的版本控制软件。

Git的功能特性：
从一般开发者的角度来看，git有以下功能：
    1、从服务器上克隆完整的Git仓库（包括代码和版本信息）到单机上。
    2、在自己的机器上根据不同的开发目的，创建分支，修改代码。
    3、在单机上自己创建的分支上提交代码。
    4、在单机上合并分支。
    5、把服务器上最新版的代码fetch下来，然后跟自己的主分支合并。
    6、生成补丁（patch），把补丁发送给主开发者。
    7、看主开发者的反馈，如果主开发者发现两个一般开发者之间有冲突（他们之间可以合作解决的冲突），就会要求他们先解决冲突，然后再由其中一个人提交。如果主开发者可以自己解决，或者没有冲突，就通过。
    8、一般开发者之间解决冲突的方法，开发者之间可以使用pull 命令解决冲突，解决完冲突之后再向主开发者提交补丁。
从主开发者的角度（假设主开发者不用开发代码）看，git有以下功能：
    1、查看邮件或者通过其它方式查看一般开发者的提交状态。
    2、打上补丁，解决冲突（可以自己解决，也可以要求开发者之间解决以后再重新提交，如果是开源项目，还要决定哪些补丁有用，哪些不用）。
    3、向公共服务器提交结果，然后通知所有开发人员。
    
优点：
    适合分布式开发，强调个体。
    公共服务器压力和数据量都不会太大。
    速度快、灵活。
    任意两个开发者之间可以很容易的解决冲突。
    离线工作。
    
缺点：
    资料少（起码中文资料很少）。
    学习周期相对而言比较长。
    不符合常规思维。
    代码保密性差，一旦开发者把整个库克隆下来就可以完全公开所有代码和版本信息。

最常用命令：
	git add 
	git status
	git commit
	git push
	git pull
较常用命令：
	git branch
	git checkout
	git merge
其他命令：
    git clone 
    git rm 文件或目录
    git reset HEAD或版本号
    git reflog
    git log
    git status
    git diff 版本1 版本2
    git tag 标签名称
    git stash

具体操作：自己看课件复习！！！没有难度
```

