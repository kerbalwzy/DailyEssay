## 使用djangorestframework-jwt自带的认证视图进行用户登录验证源代码浅析

#### 路由: url(r'^authorizations/, obtain_jwt_token),

#### obtain_jwt_token来自`$PYTHON_ENVTIONS_PATH/site-packages/rest_framework_jwt/views.py`的102行和74-80行,代码如下

```python
class ObtainJSONWebToken(JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = JSONWebTokenSerializer

"""
中间省略部分不相关代码
"""
obtain_jwt_token = ObtainJSONWebToken.as_view()
```

#### 既然指定了`serializer_class = JSONWebTokenSerializer` 说明是使用了DRF框架做验证, 那么验证用户登录时传输的参数的代码就是在序列化器类的代码中

#### 序列化器类来自于`$PYTHON_ENVTIONS_PATH/site-packages/rest_framework_jwt/serializers.py`22-69行, 代码如下:

```python
class JSONWebTokenSerializer(Serializer):
    """
    省略部分代码
    """
    def validate(self, attrs):
        # 获取参数: 用户登录名称 + 密码
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            # 用户登录时传入的参数完整, 则验证用户并获取用户对象
            # 获取用户对象的代码在下面👇这行代码中!!!
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)
```

#### 获取用户对象的关键代码在第50行 `user = authenticate(**credentials)`; 而`authenticate`到包自$PYTHON_ENVTIONS_PATH/site-packages/django/contrib/auth/__init__.py`的64行至81行, 代码如下:

```python
def authenticate(request=None, **credentials):
    """
    If the given credentials are valid, return a User object.
    """
    # 获取验证后端的backend对象的关键代码在下面👇这行!!!
    for backend, backend_path in _get_backends(return_tuples=True):
        try:
            user = _authenticate_with_backend(backend, backend_path, request, credentials)
        except PermissionDenied:
            # This backend says to stop in our tracks - this user should not be allowed in at all.
            break
        if user is None:
            continue
        # Annotate the user object with the path of the backend.
        user.backend = backend_path
        return user

    # The credentials supplied are invalid to all backends, fire signal
    user_login_failed.send(sender=__name__, credentials=_clean_credentials(credentials), request=request)
```

#### 获取验证后端的backend对象的关键代码在第68行`for backend, backend_path in _get_backends(return_tuples=True):`;而`_get_backends`对象来当前代码文件的26-36行,代码如下:

```python
def _get_backends(return_tuples=False):
    backends = []
    # 关键代码在下面👇这行!!!!
    for backend_path in settings.AUTHENTICATION_BACKENDS:
        backend = load_backend(backend_path)
        backends.append((backend, backend_path) if return_tuples else backend)
    if not backends:
        raise ImproperlyConfigured(
            'No authentication backends have been defined. Does '
            'AUTHENTICATION_BACKENDS contain anything?'
        )
    return backends
```

#### 关键代码在第28行: `for backend_path in settings.AUTHENTICATION_BACKENDS`, 而`settings`导包自`from django.conf import settings`, 那么这里的settings等同于我们项目启动时使用的`meiduo_mall.settings.dev`而我们在dev.py中添加了配置代码如下:

```python
# 告知Django使用自定义的认证后端
AUTHENTICATION_BACKENDS = [
    'users.utils.UsernameMobileAuthBackend',
]
```

那么通过使用`load_backend('users.utils.UsernameMobileAuthBackend')`就可以了获取到我们自定义的验证后端,返回user对象; load_backend对象的源代码就不做更多的深入了,大致的原理是使用了标准库中`importlib`的` import_module`对象, 该对象能让我们通过字符串的导包路径倒入一个对象.



