## Python开发时,在Ubunut中安装虚拟环境

- ### Ubuntu中安装虚拟环境

  - 1.通过命令`sudo apt install python3-dev python3-pip`安装两个基础软件

    ```text
    python3-dev是什么?
    是包含Python3类库的头文件和相关pkg-config的一个单独的包
    以下情况你是需要python3-dev的:
    	你需要自己安装一个源外的python3类库, 而这个类库内含需要编译的调用python3 api的c/c++文件
    	你自己写的一个程序编译需要链接libpythonXX.(a|so)
    (注:以上不含使用ctypes/ffi或者裸dlsym方式直接调用libpython.so)
    其他正常使用python3或者通过安装源内的python3类库的不需要python3-dev.
    ```

  - 2.通过命令`pip3 install virtualenv virtualenvwrapper`安装创建和管理虚拟环境的包. 这里之所以使用pip3,是为了后续在创建虚拟环境时不需通过`-p`参数来指定就可以直接创建Python3解释器的虚拟环境.当然完成这个默认设置还需要在接下来的步骤中做一点其他操作

  - 3.在$HOME(家目录)下,创建一个`.virtualenvs`的隐藏文件夹,这个文件夹就是用来保存你未来创建的虚拟环境文件夹的父级目录

  - 4.编辑$HOME(家目录)下的`.bashrc`文件,在文件的末尾添加如下内容:

    ```bash
    # set virtualenv config
    # 指定所有虚拟环境资源文件夹所在的父级目录
    export WORK_HOME=$HOME/.virtualenvs
    # 指定默认使用的基础解释器,也正是因为这一步配置让我们可以在创建虚拟环境时不用再通过 -p 指定就默认创建基于Python3的虚拟环境
    export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
    # source 一下virtualenvwrapper.sh文件,让我们可以在终端可以使用 mkvirtualenv、workon等命令.
    # 这个文件的路径通过 whereis “filename” 命令查找
    source /usr/share/virtualenvwrapper.sh
    ```

  - 5.在$HOME目录下输入命令`source .bashrc` ,加载我们刚刚修改的配置

  - 6.接下来你就可以在任意目录下通过`mkvirtualenv venv_name`来创建虚拟环境啦,新建的虚拟环境默认的解释器版本就是Python3, 并且所有文件资源都存放在$HOME/.virtualenvs/venv_name/目录下.创建好后,虚拟环境自动激活,你可以通过`deactivate`退出虚拟环境,也可再次使用时通过`workon venv_name`来重新激活虚拟环境.

  - 7.接下来为了提高pip安装模块包时的网络速度,我们可以将pip的下载源配置到国内,在$HOME目录下创建一个`.pip`文件夹,并在文件夹内创建`pip.conf`文件,文件内容如下:

    ```conf
    [global]
    index-url = http://mirrors.aliyun.com/pypi/simple/
    
    [install]
    trusted-host=mirrors.aliyun.com
    ```

- ##### ⚠️注意事项:

  在使用虚拟环境时,总有人在安装python的包时,通过“sudo pip3 install xxx”这样去安装要使用的模块,造成的结果就是模块包被安装到了系统的python解释器的dist-package中去,而不是虚拟环境中去.这事因当你使用 sudo 时, 终端的环境变量使用了root用户的环境变量,这个时候你使用的 pip3 是系统默认的 pip3, 所以就安装到了系统的解释器的dist-package中去了.


