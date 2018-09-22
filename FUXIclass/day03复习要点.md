复习要点：第三天

---

00 - 第一二天复习重点总结

```
Python中所有的变量都是引用，变量本身不保存数据，而是存放了数据的内存地址，这就是Python是一门动态类型语言的原因；体现：1，xxxx;2，修改可变类型(dict, list)的全局变量不需要global声明；3，引用可以传递

条件语句（if，elif,else，三元运算表达式）和循环语句(while,for):使用场景

函数：4种；参数（形参【缺省参数，不定长参数】，实参【引用传递】）。返回值：(有无返回值，多个返回值【元组】)
递归函数：1，有判断，2，有返回值，3，内部调用自己【取代循环】

面向对象编程：封装，继承，多态【Python天生支持多态】
类【对一些具有共同特性的事物的抽象概念】和对象【具体的事物对象】
类的一些操作：继承（多继承），重写（调用父类），各种魔法方法
单例模式【重写魔法方法new】，property装饰器——>将方法当作属性使用

对象创建的过程：new——>init
对象销毁时：del魔法方法

可迭代对象，实现了iter魔法方法
迭代器，同时实现iter魔法方法和next方法
生成器，带yield关键字的函数，将列表推到式的中括号改为小括号。 身边的生成器：range

列表推导式：[ item（关于item的运算） for item in generator 【条件判断（可省略）】]
字典推导式：{ key:value for key,vale in generator }
		  { key:value for key in generator1 for value in generator2 }
```

01 - 使用从官方下载的系统文件(.ios)在vmware14上创建虚拟机

```
VMware14是我们的虚拟机运行平台

Ubuntu18.04桌面版官方下载地址：
https://www.ubuntu.com/download/desktop

通过命令行安装vmware-tools使虚拟机可以自适应屏幕和与宿主机共享剪切板：
sudo apt install open-vm-tools open-vm-rools-desktop
创建好的虚拟机自带Python3
apt是Ubuntu自带的软件管理器
命令行中的参数以空格隔开

如果有需要可以选择更新软件的安装源到国内【百度一下】
卸载不必要的应用程序（软件）
```

02 - 在新建的虚拟机上联系我们常用的Linux命令

	普通常用： ping, ls、 cd、mkdir、mv、tree、cat、chmod、rm、cp、history，top
	
	搜索文件或文件内容：find、grep、whereis、mdfind
	
	查看进程状态： ps axj|grep  process_name
	
	查看端口状态：	netstat -nap|grep port	
	
	和部署和远程服务器相关的命令：ssh，scp

03-文件和文件夹相关命令

	创建文件和文件夹： touch file_name	vim file_name
	mkdir  dir_name
	
	文件夹的压缩与解压：tar、zip、unzip
	
	创建软硬链接：ln [-s]	source_instance	new_instance
	
	修改文件权限: chomd  +rwx target_file
	
	练习：通过chmod +x修.py文件的权限，直接通过文件运行代码
	扩展：如何在运行Python代码时，获取命令行中的参数

04-通过apt安装三个数据库「学习通过官方文档安装」

	安装mysql
	注意：请安装5.7版本。因为8.0版本有一些特殊变化，不是很方便使用
	https://dev.mysql.com/doc/mysql-apt-repo-quick-guide/en/#apt-repo-fresh-install
	安装redis
	sudo apt install redis
	安装mongodb
	sudo apt install mongodb

05-通过snap安装软件

	安装google
	https://blog.csdn.net/hellozex/article/details/80762705
	
	snap安装pycharm「pycharm也可以直接在ubuntu的应用商店里安装」
	sudo snap install [pycharm-professional|pycharm-community] --classic
	
	pycharm断网激活后运行联网使用：
		在/etc/hosts文件中添加一行：0.0.0.0	account.jetbrains.com
	
	第一次启动要通过命令行启动，启动之后收藏到程序坞