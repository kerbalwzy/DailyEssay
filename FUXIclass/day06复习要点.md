复习要点：第六天：WEB开发—网络请求与协议

---

01-HTML【超文本标记语言 HyperText Markup Language】

```
基本概念：
	超文本就是指页面内可以包含图片、链接，甚至音乐、程序等非文字元素。
	超文本标记语言的结构包括“头”部分、和“主体”部分，其中“头”部提供关于网页的信息，“主体”部分提供网页的具体内容。
	
标签语法：
    学习html语言就是学习标签的用法，html常用的标签有20多个，学会这些标签的使用，就基本上学会了HTML的使用。
    标签的作用：被浏览器解析后，提供基础的内容展示样式和操作事件。
	
常见的和网络请求相关的标签有哪些？
	link标签：用来请求一个CSS样式文件
	script标签：可以请求一个js的脚本文件
	a标签：指向一个网络地址，可以通过点击事件让浏览器跳转到对应的网页
	img标签：显示一张图片，当图片的地址发生变化时，浏览器会自动重新请求刷新图片
	video标签：加载一个视频，浏览器会根据标签中的地址发送请求获取视频数据，并可以设置标签是否自动播放
	form标签：表单，可以通过submit类型的input标签的点击事件向后端发送一个POST请求
	iframe标签：在文档中再创建一个文档【页面中嵌套页面】

更多标签知识学习地址：
	http://www.w3school.com.cn/html/index.asp
```

---

02-CCS【层叠样式表 Cascading *S*tyle *S*heets】

```
基本概念：
	为了让网页元素的样式更加丰富，也为了让网页的内容和样式能拆分开，CSS由此思想而诞生，CSS是 Cascading Style Sheets 的首字母缩写，意思是层叠样式表。有了CSS，html中大部分表现样式的标签就废弃不用了，html只负责文档的结构和内容，表现形式完全交给CSS，html文档变得更加简洁。

如何理解「层叠」这个概念？
	对一个标签使用CSS选择器做样式定义时，可以分多次定义，也可以重复定义。并且根据不同选择器的权重值选择加载哪个选择器设置的样式，权重越大越优先；
	
加载方式：内联式【标签内的style属性】，嵌入式【style标签】，外链式【link】

基本语法：
	选择器 { 属性：值； 属性：值； 属性：值；}

    选择器是将样式和页面元素关联起来的名称，属性是希望设置的样式属性，每个属性有一个或多个值。属性和值之间用冒号，一个属性和值与下一个属性和值之间用分号，最后一个分号可以省略，代码示例：
    div{ 
        width:100px !important; 
        height:100px; 
        background:gold; 
    }

CSS选择器和其权重：
	常见的选择器：标签选择器、类选择器、id选择器、层级选择器【空格隔开】、组选择器【用逗号隔开，批量设置样式】
	权重值：
        1、内联样式，如：style=””，权重值为1000
        2、ID选择器，如：#content，权重值为100
        3、类，伪类，如：.content、:hover 权重值为10
        4、标签选择器，如：div、p 权重值为1
        5、层级选择器：权重值为其各层的选择器权重值之和
        6、!important:表示强制应用该样式，可以看作权重值：10000
    
盒子模型：
	标签元素在页面中其实都是一个个的方块，可以看成一个盒子；盒子模型是用来帮助我们设置样式的。影响盒子模型计算的主要因素有：元素本身大小，内外边距，边框
	
前端开发基本流程：
	创建项目目录————>切图————>新建html文件，新建css文件————>参照效果图，编写html和css代码

更多CSS知识学习网址：
	http://www.w3school.com.cn/css/css_jianjie.asp
```

---

03-JavaScript

```
基本概念：
	JavaScript一种直译式脚本语言，是一种动态类型、弱类型的语言。它的解释器被称为JavaScript引擎，为浏览器的一部分，广泛用于客户端的脚本语言，最早是在HTML（标准通用标记语言下的一个应用）网页上使用，用来给HTML网页增加动态功能。主要解决的问题是前端与用户交互
	
强弱类型====》强调的是不同数据类型之间能否直接运算
动态类型====》强调的是变量定义时是否需要声明类型，以及在后续的代码运行过程中是否允许修改类型

嵌入方式：
	1、行间事件（主要用于事件）：<input type="button" name="" onclick="alert('ok！');">
	2、页面script标签嵌入：<script type="text/javascript"> alert('ok！');</script>
	3、外部引入：<script type="text/javascript" src="js/index.js"></script>

⚠️：JavaScript和Java没有任何关系，也是一门独立的类似于Python的高级编程语言。

常见的事件（jQuery时间函数列表）：
	blur() 元素失去焦点
    focus() 元素获得焦点
    click() 鼠标单击
    mouseover() 鼠标进入（进入子元素也触发）
    mouseout() 鼠标离开（离开子元素也触发）
    mouseenter() 鼠标进入（进入子元素不触发）
    mouseleave() 鼠标离开（离开子元素不触发）
    hover() 同时为mouseenter和mouseleave事件指定处理函数
    ready() DOM【页面】加载完成
    submit() 用户递交表单

更多JS知识学习网址：
	http://www.w3school.com.cn/js/index.asp

⚠️：了解一个概念：W3C标准
	https://baike.baidu.com/item/W3C%E6%A0%87%E5%87%86/8367679
```

04-jQuery和Vue

```
jquery基本介绍：
	jQuery是目前使用最广泛的javascript函数库。据统计，全世界排名前100万的网站，有46%使用jQuery，远远超过其他库。微软公司甚至把jQuery作为他们的官方库。
	jQuery的版本分为1.x系列和2.x、3.x系列，1.x系列兼容低版本的浏览器，2.x、3.x系列放弃支持低版本浏览器，目前使用最多的是1.x系列的。
	jquery是一个函数库，一个js文件，页面用script标签引入这个js文件就可以使用。
		<script type="text/javascript" src="js/jquery-1.12.2.js"></script>
	jquery的口号和愿望 Write Less, Do More（写得少，做得多）

1、http://jquery.com/ 官方网站
2、https://code.jquery.com/ 版本下载

vue基本介绍：
    Vue.js是前端三大新框架：Angular.js、React.js、Vue.js之一，Vue.js目前的使用和关注程度在三大框架中稍微胜出，并且它的热度还在递增。
    Vue.js可以作为一个js库来使用，也可以用它全套的工具来构建系统界面，这些可以根据项目的需要灵活选择，所以说，Vue.js是一套构建用户界面的渐进式框架。
    Vue的核心库只关注视图层，Vue的目标是通过尽可能简单的API实现响应的数据绑定，在这一点上Vue.js类似于后台的模板语言。
    Vue也可以将界面拆分成一个个的组件，通过组件来构建界面，然后用自动化工具来生成单页面(SPA - single page application)系统。
	Vue的一个重要特点：
		数据的双向绑定————「页面上的显示的数据能够实时跟随变量保存的数据变化，页面上的数据修改也能实时的影响到保存这个数据变量」
	
1、https://cn.vuejs.org/v2/guide/	官方网站教程
2、https://cn.vuejs.org/v2/guide/installation.html  下载安装
```

05-局部刷新与js网络请求

```js
// 局部刷新：在不重新加载整个网页的条件下，重新加载网页上的部分内容


// 使用ajax向服务器发送网络请求的标准写法「简单例子」：
$.ajax({					// 参数对象
    url: '/target_url',		// 目标网址
    type: 'GET',			// 请求方式
    dataType: 'json',		// 希望接受的数据类型
    data:{code:300268},// 发送给后端的数据
})		// 假如返回的是：return JsonResponse(data={"name":"laowang"})
.done(function(resp) {		// 请求成功时执行
    alert(resp.data.name);
})
.fail(function() {			// 请求失败时执行
    alert('请求失败，未能获取想要的数据！');
});
//判断请求是否发送成功的标准：
//	1.浏览器判断请求有没有成功发送
//	2.浏览器根据服务器反馈的状态码判断请求有没有成功
//  3.浏览器对比请求头与响应头，检查返回的数据信息是否符合请求头的要求，如果不符合认为失败；

// 更多参数：https://api.jquery.com/jQuery.ajax/#jQuery-ajax-settings

// 使用axios向服务器发送网路请求的标准写法「简单例子」：
axios({						// 参数对象
  method: 'post',			// 请求方式
  url: '/target_url',		// 目标网址
  data: {					// 发送给后端的数据
    firstName: 'Fred',		
    lastName: 'Flintstone'
  }
})
.then(function (response) {	// 请求成功时执行
  console.log(response);
})
.catch(function (error) { 	// 请求失败时执行
  console.log(error);
});
// 学习更多操作：https://github.com/axios/axios#axios
// 注意⚠️：发送网络请求建议使用ajax！！！！，因为从上面的链接学习来看，还有很多浏览器是不支持axios的。
// 注意⚠️：ajax不需要要单独在网页中再嵌入一个js文件，直接内置在了jQuery中；
```

06-HTTP协议

```
基本概念：
	超文本传输协议（HTTP）是用于传输诸如HTML的超媒体文档的 应用层协议。它被设计用于Web浏览器和Web服务器之间的通信，但它也可以用于其他目的。 HTTP遵循经典的客户端-服务端模型，客户端打开一个连接以发出请求，然后等待它收到服务器端响应。 
	HTTP是无状态协议，意味着服务器不会在两个请求之间保留任何数据（状态）。

遵循HTTP协议的报文构成：
	通常HTTP消息包括客户机向服务器的请求消息和服务器向客户机的响应消息。这两种类型的消息由一个起始行，一个或者多个头域，一个指示头域结束的空行和可选的消息体组成。
	
	简单理解：起始行+消息头+空行+消息体
        请求行：请求方式 + 路径 +协议版本
        请求头：额外描述请求的信息
        空行：	 分割，区分请求头和请求体
        请求体：都后端发送的数据「参数」，是可选的
        
        响应行：协议版本 + 状态码 + 状态描述
        响应头：额外描述响应的信息
        空行：	分割；
        响应体：后端返回的数据
	
无状态协议与状态保持————HTTP 是无状态，有会话的
    HTTP是无状态的：在同一个连接中，两个执行成功的请求之间是没有关系的。这就带来了一个问题，用户没有办法在同一个网站中进行连续的交互，比如在一个电商网站里，用户把某个商品加入到购物车，切换一个页面后再次添加了商品，这两次添加商品的请求之间没有关联，浏览器无法知道用户最终选择了哪些商品。而使用HTTP的头部扩展，Cookies就可以解决这个问题。把Cookies添加到头部中，创建一个会话让每次请求都能共享相同的上下文信息，达成相同的状态。
    
理解HTTP协议中的Cookie及其与Session的区别：https://itbilu.com/other/relate/Ny2IWC3N-.html
还有哪些方式可以在浏览器端保存这些状态信息？
	storage：localstorage | sessionstorage
		使用【js代码】：存：window.sessionstorage.setItem(key, value)
								 localstorage.
					  取：window.sessionstorage.getItem(key, value)
	直接存放在页面中，并隐藏不显示：CSRF的token值的保存【不推荐使用】
					 
其他基础知识：
	请求方式：
        GET方法：		请求一个指定资源的表示形式. 使用GET的请求应该只被用于获取数据.
        POST方法：		用于将实体提交到指定的资源，通常导致状态或服务器上的副作用的更改. 
        PUT方法：		用请求有效载荷替换目标资源的所有当前表示
        PATCH方法：	用于对资源应用部分修改。
        DELETE方法：	删除指定的资源。
        
        HEAD方法：		请求一个与GET请求的响应相同的响应，但没有响应体.
        OPTIONS方法：	用于描述目标资源的通信选项，预检工作。
        TRACE方法：	沿着到目标资源的路径执行一个消息环回测试。
        CONNECT方法：	建立一个到由目标资源标识的服务器的隧道。
	
    响应状态码：
    	基本： 
    	1xx: Informational - Request received, continuing process
        2xx: Success - The action was successfully received, understood, and accepted
        3xx: Redirection - Further action must be taken in order to complete the request
        4xx: Client Error - The request contains bad syntax or cannot be fulfilled
        5xx: Server Error - The server failed to fulfill an apparently valid request
		
		更多更详细：
    	https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status
    	
```

#### 常见的请求头及其说明：

| 协议头              | 说明                                                         | 示例                                                    |
| ------------------- | ------------------------------------------------------------ | ------------------------------------------------------- |
| Accept              | 可接受的响应内容类型（`Content-Types`）。                    | `Accept: text/plain`                                    |
| Accept-Charset      | 可接受的字符集                                               | `Accept-Charset: utf-8`                                 |
| Accept-Encoding     | 可接受的响应内容的编码方式。                                 | `Accept-Encoding: gzip, deflate`                        |
| Accept-Language     | 可接受的响应内容语言列表。                                   | `Accept-Language: en-US`                                |
| Accept-Datetime     | 可接受的按照时间来表示的响应内容版本                         | `Accept-Datetime: Sat, 26 Dec 2015 17:30:00 GMT`        |
| Authorization       | 用于表示HTTP协议中需要认证资源的认证信息                     | `Authorization: Basic OSdjJGRpbjpvcGVuIANlc2SdDE==`     |
| Cache-Control       | 用来指定当前的请求/回复中的，是否使用缓存机制。              | `Cache-Control: no-cache`                               |
| Connection          | 客户端（浏览器）想要优先使用的连接类型                       | `Connection: keep-alive`                                |
| Cookie              | 由之前服务器通过`Set-Cookie`（见下文）设置的一个HTTP协议Cookie | `Cookie: Version=1; Skin=new;`                          |
| Content-Length      | 以8进制表示的请求体的长度                                    | `Content-Length: 348`                                   |
| Content-MD5         | 请求体的内容的二进制 MD5 散列值（数字签名），以 Base64 编码的结果 | `Content-MD5: oD8dH2sgSW50ZWdyaIEd9D==`                 |
| Content-Type        | 请求体的MIME类型 （用于POST和PUT请求中）                     | `Content-Type: application/x-www-form-urlencoded`       |
| Date                | 发送该消息的日期和时间（以[RFC 7231](http://tools.ietf.org/html/rfc7231#section-7.1.1.1)中定义的"HTTP日期"格式来发送） | `Date: Dec, 26 Dec 2015 17:30:00 GMT`                   |
| From                | 发起此请求的用户的邮件地址                                   | `From: user@itbilu.com`                                 |
| Host                | 表示服务器的域名以及服务器所监听的端口号。如果所请求的端口是对应的服务的标准端口（80），则端口号可以省略。 | `Host: www.itbilu.com:80``Host: www.itbilu.com`         |
| Max-Forwards        | 限制该消息可被代理及网关转发的次数。                         | `Max-Forwards: 10`                                      |
| Origin              | 发起一个针对[跨域资源共享](http://itbilu.com/javascript/js/VkiXuUcC.html)的请求（该请求要求服务器在响应中加入一个`Access-Control-Allow-Origin`的消息头，表示访问控制所允许的来源）。 | `Origin: http://www.itbilu.com`                         |
| Proxy-Authorization | 用于向代理进行认证的认证信息。                               | Proxy-Authorization: Basic IOoDZRgDOi0vcGVuIHNlNidJi2== |
| Range               | 表示请求某个实体的一部分，字节偏移以0开始。                  | `Range: bytes=500-999`                                  |
| Referer             | 表示浏览器所访问的前一个页面，可以认为是之前访问页面的链接将浏览器带到了当前页面。`Referer`其实是`Referrer`这个单词，但RFC制作标准时给拼错了，后来也就将错就错使用`Referer`了。 | Referer: http://itbilu.com/nodejs                       |
| User-Agent          | 浏览器的身份标识字符串                                       | `User-Agent: Mozilla/……`                                |
| Upgrade             | 要求服务器升级到一个高版本协议。                             | Upgrade: HTTP/2.0, SHTTP/1.3, IRC/6.9, RTA/x11          |
| Via                 | 告诉服务器，这个请求是由哪些代理发出的。                     | Via: 1.0 fred, 1.1 itbilu.com.com (Apache/1.1)          |
| Warning             | 一个一般性的警告，表示在实体内容体中可能存在错误。           | Warning: 199 Miscellaneous warning                      |

#### 常用的响应头及其说明

| 响应头                      | 说明                                                         | 示例                                                         |
| --------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Access-Control-Allow-Origin | 指定哪些网站可以`跨域源资源共享`                             | `Access-Control-Allow-Origin: *`                             |
| Accept-Patch                | 指定服务器所支持的文档补丁格式                               | Accept-Patch: text/example;charset=utf-8                     |
| Accept-Ranges               | 服务器所支持的内容范围                                       | `Accept-Ranges: bytes`                                       |
| Age                         | 响应对象在代理缓存中存在的时间，以秒为单位                   | `Age: 12`                                                    |
| Allow                       | 对于特定资源的有效动作;                                      | `Allow: GET, HEAD`                                           |
| Cache-Control               | 通知从服务器到客户端内的所有缓存机制，表示它们是否可以缓存这个对象及缓存有效时间。其单位为秒 | `Cache-Control: max-age=3600`                                |
| Connection                  | 针对该连接所预期的选项                                       | `Connection: close`                                          |
| Content-Disposition         | 对已知MIME类型资源的描述，浏览器可以根据这个响应头决定是对返回资源的动作，如：将其下载或是打开。 | Content-Disposition: attachment; filename="fname.ext"        |
| Content-Encoding            | 响应资源所使用的编码类型。                                   | `Content-Encoding: gzip`                                     |
| Content-Language            | 响就内容所使用的语言                                         | `Content-Language: zh-cn`                                    |
| Content-Length              | 响应消息体的长度，用8进制字节表示                            | `Content-Length: 348`                                        |
| Content-Location            | 所返回的数据的一个候选位置                                   | `Content-Location: /index.htm`                               |
| Content-MD5                 | 响应内容的二进制 MD5 散列值，以 Base64 方式编码              | Content-MD5: IDK0iSsgSW50ZWd0DiJUi==                         |
| Content-Range               | 如果是响应部分消息，表示属于完整消息的哪个部分               | Content-Range: bytes 21010-47021/47022                       |
| Content-Type                | 当前内容的`MIME`类型                                         | Content-Type: text/html; charset=utf-8                       |
| Date                        | 此条消息被发送时的日期和时间(以[RFC 7231](http://tools.ietf.org/html/rfc7231#section-7.1.1.1)中定义的"HTTP日期"格式来表示) | Date: Tue, 15 Nov 1994 08:12:31 GMT                          |
| ETag                        | 对于某个资源的某个特定版本的一个标识符，通常是一个 消息散列  | ETag: "737060cd8c284d8af7ad3082f209582d"                     |
| Expires                     | 指定一个日期/时间，超过该时间则认为此回应已经过期            | Expires: Thu, 01 Dec 1994 16:00:00 GMT                       |
| Last-Modified               | 所请求的对象的最后修改日期(按照 RFC 7231 中定义的“超文本传输协议日期”格式来表示) | Last-Modified: Dec, 26 Dec 2015 17:30:00 GMT                 |
| Link                        | 用来表示与另一个资源之间的类型关系，此类型关系是在[RFC 5988](https://tools.ietf.org/html/rfc5988)中定义 | `Link: `; rel="alternate"                                    |
| Location                    | 用于在进行重定向，或在创建了某个新资源时使用。               | Location: http://www.itbilu.com/nodejs                       |
| Proxy-Authenticate          | 要求在访问代理时提供身份认证信息。                           | `Proxy-Authenticate: Basic`                                  |
| Public-Key-Pins             | 用于防止中间攻击，声明网站认证中传输层安全协议的证书散列值   | Public-Key-Pins: max-age=2592000; pin-sha256="……";           |
| Refresh                     | 用于重定向，或者当一个新的资源被创建时。默认会在5秒后刷新重定向。 | Refresh: 5; url=http://itbilu.com                            |
| Retry-After                 | 如果某个实体临时不可用，那么此协议头用于告知客户端稍后重试。其值可以是一个特定的时间段(以秒为单位)或一个超文本传输协议日期。 | 示例1:Retry-After: 120示例2: Retry-After: Dec, 26 Dec 2015 17:30:00 GMT |
| Server                      | 服务器的名称                                                 | `Server: nginx/1.6.3`                                        |
| Set-Cookie                  | 设置`HTTP cookie`                                            | Set-Cookie: UserID=itbilu; Max-Age=3600; Version=1           |
| Status                      | 通用网关接口的响应头字段，用来说明当前HTTP连接的响应状态。   | `Status: 200 OK`                                             |
| Transfer-Encoding           | 用表示实体传输给用户的编码形式。包括：`chunked`、`compress`、 `deflate`、`gzip`、`identity`。 | Transfer-Encoding: chunked                                   |
| Upgrade                     | 要求客户端升级到另一个高版本协议。                           | Upgrade: HTTP/2.0, SHTTP/1.3, IRC/6.9, RTA/x11               |
| Vary                        | 告知下游的代理服务器，应当如何对以后的请求协议头进行匹配，以决定是否可使用已缓存的响应内容而不是重新从原服务器请求新的内容。 | `Vary: *`                                                    |
| Via                         | 告知代理服务器的客户端，当前响应是通过什么途径发送的。       | Via: 1.0 fred, 1.1 itbilu.com (nginx/1.6.3)                  |
| Warning                     | 一般性警告，告知在实体内容体中可能存在错误。                 | Warning: 199 Miscellaneous warning                           |
| WWW-Authenticate            | 表示在请求获取这个实体时应当使用的认证模式。                 | `WWW-Authenticate: Basic`                                    |

	





