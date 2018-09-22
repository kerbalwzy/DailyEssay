复习要点：第二天

---

01-文件读写

	使用with上下文管理器打开文件
	
	文件打开的13种方式
	
	超大容量文件读取指定部分的内容：
	
		通过修改文件读取指针的定位实现，tell()函数获取当前指针位置，seek(offset, from)函数移动指针；offset：偏移量「分正负值」，from：方向「0:表示文件开头，1:表示当前位置，2:表示文件末尾」
		⚠️：定位读取只支持在 rb 模式下使用。
	
	使用os模块进行文件或文件夹的相关操作

---

02-类与对象

	Python中，一切皆对象
	
	面向对象编程的好处：重复代码只需封装好写一次就可反复调用；代码逻辑更加清晰；
	面向对象编程三要素：封装，继承，多态
	
	定义类的两种方式：
	
		通过class关键字定义类
	
		通过元类type定义类
	
	类的继承与方法重写
		Python3中，直接使用 super().method_name() ,就可以调用父类的方法
		
		class Father:
	        def __init__(self):
	            self.father_name = "laowang"
	        def run(self):
	            print("爸爸去哪")     
	        def introduce():
	        	print("I'm from china")
	
		class Son(Father):
	        def __init__(self):
	            self.name = "xiaowang"
	            super().__init__()
	        def run(self):
	            super().run()
	            print("我要跟着你去")
	
	    if __name__ == '__main__':
	        xiaowang = Son()
	        print("my name:", xiaowang.name)
	        print("father name:", xiaowang.father_name)
	        xiaowang.run()
	        xiaowang.introduce()
	
	实现单例模式的两种方法：1、重写魔法方法new；
						2、限制类的导出，只允许导出创建好的一个实例对象「前提是不需要对这个对象做一些更改」
	
	实现类方法、静态方法、将方法当作属性使用的操作、将对象当作函数调用、对象属性或者方法的私有化；
	
	del obj_name 比较少用，用于在程序的运行过程中主动销毁一个对象。当销毁一个类的对象时，会调用该对象的魔法方法del。
	
	可迭代对象与迭代器：
	
		实现了iter魔法方法的对象就是可迭代对象
	
		同时实现了iter和next魔法方法的对象就是迭代器
	
		迭代器一定是可迭代对象，但是可迭代对象不一定是迭代器

---

03-模块（包）

	init文件的作用以及通过init文件限制可以导出模块或对象
		__init__.py的在文件夹中，可以使文件夹变为一个python模块，python的每个模块对应的包中都有一个__init__.py文件的存在
	
		通常__init__.py文件为空，但是我们还可以为它增加其他的功能，我们在导入一个模块时候（也叫包），实际上导入的是这个模块的__init__.py文件。我们可以在__init__.py导入我们需要的模块，不需要一个个导入
	
		_init__.py 中还有一个重要的变量，叫做 __all__。我们有时会使出一招“全部导入”，也就是这样：from PackageName import *，这时 import 就会把注册在包 __init__.py 文件中 __all__ 列表中的子模块和子包导入到当前作用域中来。
		面向百度学习init文件的使用：
		https://www.cnblogs.com/Lands-ljk/p/5880483.html
	
	通过字符串导入模块
		使用improtlib包，通过模块名的字符串，导入模块：
		# from test01 import NAME
	    import importlib
	
	    path = "test01.NAME"
	    import_path, obj_name = path.rsplit(".", 1)
	
	    m_ob = importlib.import_module(import_path)
	    obj = getattr(m_ob, obj_name)
	    print(bj)
	
	添加环境变量搜索路径
		当你导入一个模块，Python解析器对模块位置的搜索顺序是：
	        当前目录
	        如果不在当前目录，Python则搜索在shell变量PYTHONPATH下的每个目录。
	        如果都找不到，Python会察看默认路径。UNIX下，默认路径一般为/usr/local/lib/python/
	        模块搜索路径存储在system模块的sys.path变量中。变量里包含当前目录，PYTHONPATH和由安装过程决定的默认目录。
	        
	   	添加额外的搜索路径：
	   		在程序开始运行时，使用 sys.path.insert("路径")
	   		
	   		import sys
	        sys.path.insert(0,"/home/itcast/Desktop/serverEngine")
	        print(sys.path)
	        import serverClient as fp
	        print(fp)

---

04-异常处理

	如何捕获异常和相关处理方法
		可以通过try，except 关键字捕获异常，捕获到异常之后，我们可以选择忽略或做其他处理
	如何抛出自定义的异常
		创建继承于Exception基类的自定义异常类，通过raise关键字抛出这个自定义异常类的对象
	写代码的过程中如何通过异常信息快速定位和解决问题
		1，直接通过终端中打印的异常信息，判定异常出现的位置
		2，通过打印标志性字符，一步步缩小范围，判定异常出现的位置
		3，使用IDE的调试模式，一步步的运行程序，判定异常出现的位置
		
	使用logging模块做日志记录，记录我们程序的运行的信息
		log日志的常用信息记录等级：debug，info，warning，error
		面向百度学习使用Python中的logging模块
		https://www.cnblogs.com/qianyuliang/p/7234217.html

---



				

				

				