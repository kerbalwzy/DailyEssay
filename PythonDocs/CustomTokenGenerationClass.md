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
import hmac

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

    def __init__(self, secret_key=DEMO_TOKEN_SECRET_KEY,
                 time_out=30, split_tag="\b\b\b\b"):

        self.__secret_key = secret_key.encode()
        self.__time_out = time_out
        self.__split_tag = split_tag

    def create_token(self, data):
        """
        生成加密token， 包含三部分信息：经过编码后的数据(data)，有效期截止时间戳(end_time)，认证密钥(signature)

        首先使用pickle将 原始数据、有效期截止时间 都转化为Bytes类型
        原始数据使用b64进行编码, 有效截止时间戳使用b16进行编码

        使用hmac模块，对 原始数据+有效截止时间 获取一个MD5的加密字符串作为认证密钥

        将三个编码或加密后得到的字符串使用self.__split_tag拼接成一个字符串， 作为原始的token字符串(raw_token)

        将raw_token进行b85编码的结果作为最终返回的Token

        :param data: 原始数据 Type
        :return: token: 生成的token String
        """
        data = pickle.dumps(data)
        end_time = pickle.dumps(time.time() + self.__time_out)

        data = base64.b64encode(data)
        end_time = base64.b16encode(end_time)

        # 使用hmac获取数据的认证密钥，用来在认证token时检查内容是否被修改过
        signature = hmac.new(self.__secret_key, msg=(data + end_time), digestmod="MD5").hexdigest()

        token_raw = self.__split_tag.join([signature, data.decode(), end_time.decode()])
        token = base64.b85encode(token_raw.encode()).decode()

        return token

    def parse_token(self, token):
        """
        解析token，解密方式为create_token的逆向解析

        如果解析的过程中出现异常或者Token过期或者认证密钥对比失败都会抛出异常

        否则返回原始数据

        :param token: String
        :return: data: Type
        """
        try:
            token_raw = base64.b85decode(token.encode()).decode()
            signature, data, end_time = token_raw.split(self.__split_tag)

            data = data.encode()
            end_time = end_time.encode()

            # 对比检查认证密钥
            h = hmac.new(self.__secret_key, msg=(data + end_time), digestmod="MD5")
            signature_want = h.hexdigest()
            print(signature_want + "\n", signature)
            assert signature == signature_want, "Token Error"

            # 检查有效期是否已过
            end_time = pickle.loads(base64.b16decode(end_time))
            assert end_time > time.time(), "Time Out"

            data = pickle.loads(base64.b64decode(data))
        except Exception:
            raise TokenError()
        else:
            return data

```

在我的测试中, 对于一个Python中字典类型的原始数据最终能可以生成的Token是下面这样的, 并且也能从Token中解析出原始数据, 如果Token不正确或者时间过期也能抛出异常.

![image-20190702232902025](https://github.com/kerbalwzy/DailyEssay/blob/master/media/work-afterclass/image-20190702232902025.png)

###### ⚠ 接下来你就参考一下代码写出自己的Token生成类,并测试功能吧
