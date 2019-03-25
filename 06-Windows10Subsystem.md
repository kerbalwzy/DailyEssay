## WIN10下使用Ubuntu子系统代替虚拟机

###### WIN10版本要求：Windows 10 2016年七月周年更新版本或以上（即Build 14316及以上版本）

---

##### 问题一：为什么要使用虚拟机？

- 让项目代码的开发环境尽量贴近于项目上线运行的生产运行环境
  - Ubuntu免费！！！但是不排除公司有钱使用收费的服务器系统
- 各种数据库在Linux系统上安装更加方便
  - MySQL、Redis、MongoDB等数据库在Ubuntu上安装算是方便的了，如果在Windows上安装可能出现各种奇奇怪怪的问题，毕竟在座的使用的都是Windows用户操作系统，而不是WindowsServer服务器系统。
- 有一些开发过程中需要使用的包，只能在特定的操作系统中使用。虽然这种情况很少见。

---

##### 问题二：如何使用Windows的Ubuntu子系统代替虚拟机？

- 各种数据库安装在Ubuntu子系统中
  - 子系统会自动映射主系统的所有端口。并且与主系统共享IP地址。
  - 但是，如果想要子系统中的端口能被局域网内的其他主机访问，必须修改主系统的防火墙规则，将相应的端口开放。或者完全关闭主系统的防火墙。
- 主系统中开发写代码时，连接各种数据库还是直接当成本地数据库使用。即IP地址使用“127.0.0.1”
- 开发时的虚拟环境还是直接使用主系统中的虚拟机环境
  - 主系统创建虚拟环境使用PyCharm自带的创建虚拟环境的共功能即可。一般虚拟环境夹都自动放在项目目录下
  - 使用主系统中的虚拟环境是为了在编写代码时有自动补全，和PyCharm不会给你划红线！！
- 项目开发完成后，在子系统中做测试。这里的虚拟环境就要使用子系统的虚拟环境了
  - 为了让测试环境尽量贴近生产环境
  - 可以在子系统中安装virtualenv和virtualenvwarpper创建和管理虚拟环境

---

##### 问题三：如何安装Windowsd的Ubuntu子系统？

- 打开windows10开发人员模式，打开步骤为：设置-->更新和安全-->针对开发人员，点击开发人员模式打开即可

  ![1541383571363](https://github.com/kerbalwzy/aboutPython/blob/master/media/win10withUbuntu/1541383571363.png)

  ![1541383633833](https://github.com/kerbalwzy/aboutPython/blob/master/media/win10withUbuntu/1541383633833.png)

- 在控制面板中添加linux子系统，安装步骤为：控制面板-->程序-->启用或关闭windows功能，勾选”适用于windows的linux的子系统“，点击确定，如图

  ![1541383771763](https://github.com/kerbalwzy/aboutPython/blob/master/media/win10withUbuntu/1541383771763.png)

![1541383845542](https://github.com/kerbalwzy/aboutPython/blob/master/media/win10withUbuntu/1541383845542.png)

- 在Microsoft Store搜索框中输入Ubuntu搜索，在搜索结果中点击获取这些应用。选择相应的发行版本下载即可。之后按照提示设置即可

  ![1541384130298](https://github.com/kerbalwzy/aboutPython/blob/master/media/win10withUbuntu/1541384130298.png)

  ![1541384190822](https://github.com/kerbalwzy/aboutPython/blob/master/media/win10withUbuntu/1541384190822.png)

  ![1541384232348](https://github.com/kerbalwzy/aboutPython/blob/master/media/win10withUbuntu/1541384232348.png)

- 下载完成之后，一般会自动安装，安装好之后就可以在菜单栏中找到了。第一次启动可能需要点击应用。以后就是开机自启动了。通过在【运行】中直接输入 “bash” 就可以进入子系统的终端了

  ![1541384448698](https://github.com/kerbalwzy/aboutPython/blob/master/media/win10withUbuntu/1541384448698.png)

  ![1541384480144](https://github.com/kerbalwzy/aboutPython/blob/master/media/win10withUbuntu/1541384480144.png)

![1541384662124](https://github.com/kerbalwzy/aboutPython/blob/master/media/win10withUbuntu/1541384662124.png)

- 接下来就是对子系统做一些必要的软件安装和更新了

  - 1.将apt的下载镜像源更新到国内阿里云【教程如下】：

    - https://blog.csdn.net/u014793936/article/details/81591169
    - 执行 apt-get update 命令
    - 执行 apt-get upgrade 命令

  - 2.安装Python必备模块和Vim编辑器【ubuntu18应该是默认就装好了Python3的，如果没有也可自己安装。Python2同样可以自己安装】

    - apt install python3-dev
    - apt install python3-pip
    - apt install vim

  - 3.安装各种数据库【数据库安装好之后有可能不会自动启动，需要自己手动启动】

    - 安装MySQL：【自己百度！官方教程<优先> + 各种博客】,<注意选择MySQL的版本，推荐5.7>
    - 安装Redis： apt install redis-server
    - 安装MongoDB【爬虫学习时要用】：apt install mongodb

  - 4.安装virtualenv 和 virtualenvwrapper

    - pip3  install virtualenv  virualenvwrapper

    - 安装完成后到家目录下，创建 `.virtualenvs` 文件夹 编辑 `.bashrc` 文件 

      - cd ~

      - mkdir .virtualenvs

      - vi .bashrc

      - 在最后添加下面几行,然后保存并退出：

        ```shell
        export WORKON_HOME=$HOME/.virtualenvs
        export PROJECT_HOME=$HOME/Devel
        export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
        source /usr/local/bin/virtualenvwrapper.sh
        ```

      - source .bashrc

      - 接下来就可以使用你的 mkvirtualenv 、workon 等命令了

----

##### 四、修改Windows主系统的防火墙，让一些特定端口可以被远程访问：

​	教程：https://jingyan.baidu.com/article/09ea3ede7311dec0afde3977.html

​	搞这个主要是为了，让你的项目在子系统中部署后，能给班上的其它同学用他们自己的电脑访问。

---

##### 五、解决同学们担心的，Windows使用ASCII或GBK作为默认编码， Ubuntu18使用UTF-8作为默认编码的问题

- 通过修改PyCharm的配置，让我们的文件都使用 UTF-8 编码

  ![1541388006991](https://github.com/kerbalwzy/DailyEssay/blob/master/media/win10withUbuntu/1541388080951.png)

- 配置Python文件创建时的基本模板

  ![1541388080952](https://github.com/kerbalwzy/aboutPython/blob/master/media/win10withUbuntu/1541388080952.png)

