## Mac上安装protoc、grpc、以及Go语言插件protoc-gen-go

- ### 安装protoc (通过homebrew安装)

  ```shell
  brew install protoc
  ```

- ### 下载grpc及Go语言插件protoc-gen-go及相关依赖

  ##### 如果你能`科学上网`事情很简单

  - 将你的`科学上网工具客户端`设置为`全局代理`

  - 设置终端代理, 命令如下(⚠️端口要选对, 直接复制这里不一定有用):

    ```shell
    export http_proxy=http://127.0.0.1:1087
    export https_proxy=http://127.0.0.1:1087
    ```

  - 执行下载命令, 会将相关依赖都安装到你的$GOPATH/src下

    ```shell
    go get -u google.golang.org/grpc
    ```

  ##### 如果你不能`科学上网`事情就稍微有些麻烦了😅

  - 通过git去下载这些文件,并存放到指定的目录

    ```shell
    git clone https://github.com/grpc/grpc-go.git $GOPATH/src/google.golang.org/grpc    git clone https://github.com/golang/net.git $GOPATH/src/golang.org/x/net    
    git clone https://github.com/golang/text.git $GOPATH/src/golang.org/x/text    
    go get -u github.com/golang/protobuf/{proto,protoc-gen-go}    
    git clone https://github.com/google/go-genproto.git $GOPATH/src/google.golang.org/genproto
    ```

- ### 让protoc可以为Go自动生成文件

  - 生成Go语言插件的可执行文件

    ```shell
    cd $GOPATH/src/github.com/golang/protobuf/protoc-gen-go 
    go build
    ```

  - ##### 在当前目录下, 你就多了一个`protoc-gen-go`的可执行文件, 并将这个可执行文件移动到和 `protoc`可执行文件到相同的目录, 至于在哪, Mac上通过`whihc protoc`即可获取.

  - 接下来你就可以愉快的写代码了

- ### 起步教程见如下文章:

  - [grpc-纯Go的客户端与服务端demo](./GrpcDemo.md)

    - [Golang使用grpc的环境安装](#)

  - [grpc-纯Python的客户端与服务端demo](../PythonDocs/GrpcDemo.md)

    - [Python使用grpc的环境安装](../PythonDocs/GrpcEnvWithPython.md)

  - #### ⚠️ 其实这里Python的客户端也能访问Go的服务端, Go的客户端也能访问Python的服务端, 因为我用的是同一个proto文件, 这就是GRPC的魅力所在