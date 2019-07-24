## MySQL误删了root用户或者忘记了root用户的密码怎么办?
---
- ### 停止MySQL服务

  - PS 😂 : 尽量通过`kill -9`命令强制停止MySQL-Server. 尽管不知道为什么, 比如在ubuntu中我使用了`service mysql restart`重启后登录还是会继续让我输入账号密码, 所以`kill -9`的灵异作用我也不能解释

- 进入MySQL的配置文件，找到my.cnf或者mysqld.conf

- 在my.cnf或mysqld.conf文件中添加如下配置信息，设置跳过用户验证
```
    [mysqld]
    skip-grant-tables
```
- ### 重新启动MySQL服务

- 直接通过MySQL命令进去MySQL数据库，此时不需要输入账户和密码
```
    mysql
```
- ### 使用myslq数据库并刷新权限，创建一个新的root用户，并再次刷新权限
```mysql
use mysql;

flush privileges;

# 重新创建root用户时记得要在末尾添加 with grant option,
# 否我们在后续使用root用户创建其他用户时讲报权限错误
# 平常在root用户下创建其他普通新用户时不需要添加该语句
grant all privileges on *.* to 'root'@'localhost' identified by 'mysql' with grant option;

flush privileges;
```
- ### 还原配置文件，注释掉刚刚添加的跳过用户验证的设置
- 再次重新启动MySQL服务后即可通过 root 用户 密码为 mysql 登陆数据库
```shell
    mysql -uroot -pmysql
```
