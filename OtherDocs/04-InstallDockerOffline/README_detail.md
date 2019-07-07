# ubuntu离线安装适配操作系统版本的Docker

---

### 1.访问适用于ubuntu版本的官方docker的deb包下载地址根目录:

### https://download.docker.com/linux/ubuntu/dists     	`访问结果如下:`

![image-20181127185554947](https://github.com/kerbalwzy/aboutPython/blob/master/media/installDockerOffline/image-20181127185554947.png)

### 2.查看自己的Ubuntu系统的版本代号, 根据代号在浏览器上选择相应的文件夹进入

![1543316641791](https://github.com/kerbalwzy/aboutPython/blob/master/media/installDockerOffline/1543316641791.png)

### 3.在浏览器中访问合适的文件夹连接, 下载三个 deb 文件

![image-20181127194043435](https://github.com/kerbalwzy/aboutPython/blob/master/media/installDockerOffline/image-20181127194043435.png)

### 4.下载并添加Docker仓库的GPG密钥「有以下两种方式可以使用」

- 在终端输入命令:`curl -s https://get.docker.io/gpg | sudo apt-key add -  ` 
- 直接用浏览器访问:https://get.docker.io/gpg 下载文件, 然后在终端输入 `sudo apt-key add ./gpg`

### 5.尝试通过deb文件安装docker, 安装过程中缺少什么依赖包就安装什么!

- ⚠️要先添加密钥gpg,再尝试直接通过deb文件安装docker,⚠️使用sudo 提供 root 权限「我这直接是root用户」

![1543312421236](https://github.com/kerbalwzy/aboutPython/blob/master/media/installDockerOffline/1543312421236.png)

- 假如出现如上的报错,安装所需要的依赖包

![1543313041671](https://github.com/kerbalwzy/aboutPython/blob/master/media/installDockerOffline/1543313041671.png)

-  假如出现如上的报错,安装所需要的依赖包, 然后再尝试安装 docker 的deb包

![1543313171947](https://github.com/kerbalwzy/aboutPython/blob/master/media/installDockerOffline/1543313171947.png)

### 6.无报错安装后可以通过命令`docker version`查看自己的docker版本信息,检查是否安装成功

![1543313263141](https://github.com/kerbalwzy/aboutPython/blob/master/media/installDockerOffline/1543313263141.png)

