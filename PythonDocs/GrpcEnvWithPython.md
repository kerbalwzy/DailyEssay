## Python中使用grpc的环境安装

PS: 😂先吐槽一下, Python安装grpc的使用环境真的是比Golang简单多了.

- #### 环境要求

  - ` Python 2.7` 或者 `Python 3.4` 或者`更高的版本`.
  -  `pip` version 9.0.1或更高版本.

- #### 安装grpc和grpc-tools

  ```shell
  python -m pip install grpcio --ignore-installed
  python -m pip install grpcio-tools
  ```

- ##### 好了, 只要上面👆没有报错,就装好了, 就这么简单

- #### 起步教程见如下文章:

  - [grpc-纯Go的客户端与服务端demo](../GolangDocs/GrpcDemo.md)

    - [Golang使用grpc的环境安装](../GolangDocs/GrpcEnvWithGolang_Mac.md)

  - [grpc-纯Python的客户端与服务端demo](./GrpcDemo.md)

    - [Python使用grpc的环境安装](#)

  - #### ⚠️其实这里Python的客户端也能访问Go的服务端, Go的客户端也能访问Python的服务端, 因为我用的是同一个proto文件, 这就是GRPC的魅力所在

