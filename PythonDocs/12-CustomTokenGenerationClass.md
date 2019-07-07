## 创建自定义的Token生成类

##### 在日常的HttpServer功能开发中, 我们常常需要给前端返回一些关键的、特殊的数据用来记录用户的操作状态或权限验证.

#####  而这些数据如果以原始的明文传输给前端去保存, 并不安全, 可能会被别有用心的人非法使用或者暴露用户的隐私. 

##### 这时候我们就需要将这些数据进行编码、加密,使其在前端保存后是常人难以识别的字符串. 

##### 在Python中有很多第三方包都可以帮助我们实现这个需求, 但是能不能自己实现一个呢? 接下来的代码就是教你自己实现一个能生成Token字符串的类, 并且在检验Token时还能比对过期时间

```python
# coding:utf-8
import pickle
import base64
import time

# 用来验证的密钥字符串
DEMO_TOKEN_SECRET_KEY = "jxina@89rqknzs_9349@133&^$93NKNFA&jhfak"

"""
如果是在框架中,你可以使用框架在配置中使用的secret_key, 例如在Django框架的项目中可以如下去写:
from django.conf import settings as S
DEMO_TOKEN_SECRET_KEY = getattr(S, "DEMO_TOKEN_SECRET_KEY", False) or S.SECRET_KEY
"""

class TokenError(Exception):
    def __str__(self):
        return "无效的Token"


class DemoToken:
	"""
	自定义的Token生成类, 在对象初始化时支持参数 
	secret_key 	密钥字符串 String
	time_out 	有效时间 int
	split_tag 	拼接和切割的标识字符串 String
	并且这三个参数都是缺省参数
	
	提供生成Token的公共方法: create_token
	提供解析Token的公共方法: parse_token
	"""
    def __init__(self, secret_key=DEMO_TOKEN_SECRET_KEY, time_out=60 * 2, split_tag="\b\b\b\b"):
        self.__secret_key = secret_key
        self.__time_out = time_out
        self.__split_tag = split_tag

    def create_token(self, data):
        """
        生成加密token， 包含三部分信息：原始数据，密钥字符串，有效截止时间戳
        首先使用pickle将这三部分内容都转化为Bytes类型
        然后进行base64的加密， 原始数据使用b64, 密钥字符串使用b32, 时间戳使用b16
        将三个加密后得到的字符串使用self.__split_tag拼接成一个字符串， 作为token_raw
        将token_raw使用b85加密的结果作为最终返回的Token

        :param data: 原始数据 Type
        :return: token: 生成的token String
        """
        dp = pickle.dumps(data)
        sp = pickle.dumps(self.__secret_key)
        tp = pickle.dumps(time.time() + self.__time_out)

        dpbs = base64.b64encode(dp).decode()
        spbs = base64.b32encode(sp).decode()
        tpbs = base64.b16encode(tp).decode()

        token_raw = self.__split_tag.join([dpbs, spbs, tpbs])
        token = base64.b85encode(token_raw.encode()).decode()
        return token

    def parse_token(self, token):
        """
        解析token，解密方式为create_token的逆向解析
        如果解析的过程中出现异常或者Token过期或者密钥字符串不对都会抛出异常
        否则返回原始数据

        :param token: String
        :return: data: Type
        """

        token_raw = base64.b85decode(token.encode()).decode()
        dpbs, spbs, tpbs = token_raw.split(self.__split_tag)

        try:
            tpr = pickle.loads(base64.b16decode(tpbs.encode()))
            assert tpr > time.time(), "Time Out"

            spr = pickle.loads(base64.b32decode(spbs.encode()))
            assert spr == self.__secret_key, "Token Parse Error"

            dpr = pickle.loads(base64.b64decode(dpbs.encode()))
        except Exception:
            raise TokenError()

        else:
            return dpr

```

在我的测试中, 对于一个Python中字典类型的原始数据最终能可以生成的Token是下面这样的, 并且也能从Token中解析出原始数据, 如果Token不正确或者时间过期也能抛出异常.

![image-20190702232902025](https://github.com/kerbalwzy/DailyEssay/blob/master/media/work-afterclass/image-20190702232902025.png)

###### ⚠ 接下来你就参考一下代码写出自己的Token生成类,并测试功能吧
