## Grpc-纯Golang的客户端与服务端demo

- #### 设计demo项目结构目录如下图:

  - `protos/demo.pb.go`文件是后续通过`protoc`工具自动生成的, 不需要自己创建

  ![image-20190915155200408](/Users/wzy/GitPrograms/DailyEssay/media/grpc/image-20190915155200408.png)

- #### 接下来就是编写我们的`protos/demo.proto`文件了, 使用的语法是`proto3`

  (PS: 语法文档<https://developers.google.cn/protocol-buffers/docs/proto3>)

````protobuf
// 语法版本声明，必须放在非注释的第一行
// Syntax version declaration. Must be placed on the first line of non-commentary.

syntax = "proto3";
// The document of proto3: https://developers.google.com/protocol-buffers/docs/proto3

// 包名定义, Python中使用时可以省略不写
// Package name definition, which can be omitted in Python.
package demo;

/*
`message`是用来定义传输的数据的格式的, 等号后面的是字段编号
消息定义中的每个字段都有唯一的编号
总体格式类似于Python中定义一个类或者Golang中定义一个结构体
*/
/*
`message` is used to define the structure of the data to be transmitted, after the equal sign
is the field number. Each field in the message definition has a unique number.
The overall format is similar to defining a class in Python or a structure in Golang.
*/
message Request {
    int64 client_id = 1;
    string request_data = 2;
}

message Response {
    int64 server_id = 1;
    string response_data = 2;
}

// `service` 是用来给gRPC服务定义方法的, 格式固定, 类似于Golang中定义一个接口
// `service` is used to define methods for gRPC services in a fixed format, similar to defining
//an interface in Golang
service GRPCDemo {
    // 一元模式(在一次调用中, 客户端只能向服务器传输一次请求数据, 服务器也只能返回一次响应)
    // unary-unary(In a single call, the client can only send request once, and the server can
    // only respond once.)
    rpc SimpleMethod (Request) returns (Response);

    // 客户端流模式（在一次调用中, 客户端可以多次向服务器传输数据, 但是服务器只能返回一次响应）
    // stream-unary (In a single call, the client can transfer data to the server several times,
    // but the server can only return a response once.)
    rpc ClientStreamingMethod (stream Request) returns (Response);

    // 服务端流模式（在一次调用中, 客户端只能一次向服务器传输数据, 但是服务器可以多次返回响应）
    // unary-stream (In a single call, the client can only transmit data to the server at one time,
    // but the server can return the response many times.)
    rpc ServerStreamingMethod (Request) returns (stream Response);

    // 双向流模式 (在一次调用中, 客户端和服务器都可以向对方多次收发数据)
    // stream-stream (In a single call, both client and server can send and receive data
    // to each other multiple times.)
    rpc BidirectionalStreamingMethod (stream Request) returns (stream Response);
}
````

- #### 使用`protoc`工具自动生成Go语言代码文件`protos/demo.pb.go`

```shell
protoc -I ./protos ./protos/demo.proto --go_out=plugins=grpc:./protos
```

- #### 接下来就是写代码了	 [GitHub代码仓库](<https://github.com/kerbalwzy/gRPCDataTransmissionDemo>)

`client/client.go`

```go
package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"sync"
	"time"

	"google.golang.org/grpc"

	demo "../protos"
)

const (
	ServerAddress = "127.0.0.1:23333"
	ClientId   = 0
)

func main() {

	conn, err := grpc.Dial(ServerAddress, grpc.WithInsecure())
	if err != nil {
		log.Fatal(err.Error())
	}
	defer conn.Close()

	client := demo.NewGRPCDemoClient(conn)

	CallSimpleMethod(client)

	CallClientStreamingMethod(client)

	CallServerStreamingMethod(client)

	CallBidirectionalStreamingMethod(client)
}

// 一元模式(在一次调用中, 客户端只能向服务器传输一次请求数据, 服务器也只能返回一次响应)
// unary-unary(In a single call, the client can only send request once, and the server can
// only respond once.)
func CallSimpleMethod(client demo.GRPCDemoClient) {
	log.Println("--------------Call SimpleMethod Begin---------------")
	request := demo.Request{ClientId: ClientId, RequestData: "SimpleMethod called by Golang client"}

	// context是用来保存上下文的, 比如我们可以在里面设置这个调用的请求超时时间
	ctx, cancel := context.WithTimeout(context.TODO(), time.Second*5)
	defer cancel()
	response, err := client.SimpleMethod(ctx, &request)
	if nil != err {
		log.Print("Call SimpleMethod error:", err.Error())
		return
	}
	log.Printf("Get SimpleMethod Response: Sid = %d, RespMsg= %s", response.ServerId, response.ResponseData)
	log.Println("--------------Call SimpleMethod Over----------------")
}

// 客户端流模式（在一次调用中, 客户端可以多次向服务器传输数据, 但是服务器只能返回一次响应）
// stream-unary (In a single call, the client can transfer data to the server several times,
// but the server can only return a response once.)
func CallClientStreamingMethod(client demo.GRPCDemoClient) {
	log.Println("--------------Call ClientStreamingMethod Begin--------------")
	// 获取流信息传输对象stream
	// get the data transmission worker `stream`
	stream, err := client.ClientStreamingMethod(context.Background())
	if nil != err {
		log.Fatal(err)
	}

	// 连续向server发送5次信息
	// send data to server 5 times
	request := &demo.Request{ClientId: ClientId}
	for i := 0; i < 5; i++ {
		request.RequestData = fmt.Sprintf("Golang Client stream message(%d)", i)
		err := stream.Send(request)
		if nil != err {
			log.Println(err)
		}
	}

	// 关闭发送, 并等待接收服务器的响应, 接收完成退出循环
	// close the sender, and wait the server's response data
	for {
		response, err := stream.CloseAndRecv()
		if io.EOF == err {
			log.Println("recv data from server done")
			goto OVER
		}
		if nil != err {
			log.Println(err)
		}
		log.Printf("recv data from server(%d) massege: %s", response.ServerId, response.ResponseData)
	}

OVER:
	log.Println("--------------Call ClientStreamingMethod Over---------------")
}

// 服务端流模式（在一次调用中, 客户端只能一次向服务器传输数据, 但是服务器可以多次返回响应）
// unary-stream (In a single call, the client can only transmit data to the server at one time,
// but the server can return the response many times.)
func CallServerStreamingMethod(client demo.GRPCDemoClient) {
	log.Println("--------------Call ServerStreamingMethod Begin--------------")
	// 调用的同时就给server发送了第一次(仅一次)数据
	// send data to server and get the data transmission worker `stream`
	request := &demo.Request{ClientId: ClientId, RequestData: "SStreamMethod called by Golang client"}
	stream, err := client.ServerStreamingMethod(context.Background(), request)
	if nil != err {
		log.Fatal(err)
	}
	// 不断尝试接收server返回的数据
	for {
		response, err := stream.Recv()
		if io.EOF == err {
			log.Println("recv done")
			goto OVER
		}
		if nil != err {
			log.Println(err)
		}
		log.Printf("recv from server(%d) message : %s", response.ServerId, response.ResponseData)
	}

OVER:
	log.Println("--------------Call ServerStreamingMethod Over---------------")
}

// 双向流模式 (在一次调用中, 客户端和服务器都可以向对方多次收发数据)
// stream-stream (In a single call, both client and server can send and receive data
// to each other multiple times.)
func CallBidirectionalStreamingMethod(client demo.GRPCDemoClient) {
	log.Println("--------------Call BidirectionalStreamingMethod Begin---------------")
	stream, err := client.BidirectionalStreamingMethod(context.Background())
	if nil != err {
		log.Fatal(err)
	}

	wt := new(sync.WaitGroup)
	go func() {
		// 接收数据
		// recv data
		wt.Add(1)
		defer wt.Done()
		for {
			response, err := stream.Recv()
			if io.EOF == err {
				log.Println("recv from server done")
				break
			}
			if nil != err {
				log.Println(err)
			}
			log.Printf("recv from server(%d) message: %s", response.ServerId, response.ResponseData)
		}
	}()

	// 发送数据
	// send data
	log.Println("begin to send message to server...")
	for i := 0; i < 5; i++ {
		request := &demo.Request{ClientId: ClientId, RequestData: fmt.Sprintf("Golang client message(%d)", i)}
		err := stream.Send(request)
		if nil != err {
			log.Println(err)
		}
	}

	_ = stream.CloseSend()
	wt.Wait()

	log.Println("--------------Call BidirectionalStreamingMethod Over---------------")
}

```

`server/server.go`

```go
package main

import (
	"context"
	"fmt"
	"io"
	"log"
	"net"
	"sync"

	"google.golang.org/grpc"

	demo "../protos"
)

const (
	ServerAddress = "127.0.0.1:23333"
	ServerId      = 0
)

func main() {
	listener, err := net.Listen("tcp", ServerAddress)
	if nil != err {
		log.Fatal(err)
	}

	server := grpc.NewServer()
	demo.RegisterGRPCDemoServer(server, &DemoServer{Id: ServerId})

	log.Println("------------------start Golang gRPC server")
	err = server.Serve(listener)
	if nil != err {
		log.Fatal(err)
	}
}

// 随便创建一个结构体，并实现 demo.GRPCDemoServer 接口
// create a struct and implement the `demo.GRPCDemoServer` interface
type DemoServer struct {
	Id int64
	wt sync.WaitGroup
}

// 一元模式(在一次调用中, 客户端只能向服务器传输一次请求数据, 服务器也只能返回一次响应)
// unary-unary(In a single call, the client can only send request once, and the server can
// only respond once.)
func (obj *DemoServer) SimpleMethod(ctx context.Context, request *demo.Request) (*demo.Response, error) {
	log.Printf("SimpleMethod call by Client: Cid = %d Message = %s", request.ClientId, request.RequestData)
	response := &demo.Response{ServerId: obj.Id, ResponseData: "Go server SimpleMethod Ok!!!!"}
	return response, nil
}

// 客户端流模式（在一次调用中, 客户端可以多次向服务器传输数据, 但是服务器只能返回一次响应）
// stream-unary (In a single call, the client can transfer data to the server several times,
// but the server can only return a response once.)
func (obj *DemoServer) ClientStreamingMethod(stream demo.GRPCDemo_ClientStreamingMethodServer) error {
	log.Println("ClientStreamingMethod called, begin to get requests from client ... ")
	// 开始不断接收客户端发送来端数据
	for {
		request, err := stream.Recv()
		if io.EOF == err {
			log.Println("recv done")
			response := &demo.Response{ServerId: ServerId, ResponseData: "Go server ClientStreamingMethod OK!!!!"}
			return stream.SendAndClose(response) // 事实上client只能接收到resp不能接收到return返回端error
		}
		if nil != err {
			log.Println(err)
			return err
		}
		log.Printf("recv from client(%d) message : %s", request.ClientId, request.RequestData)
	}
}

// 服务端流模式（在一次调用中, 客户端只能一次向服务器传输数据, 但是服务器可以多次返回响应）
// unary-stream (In a single call, the client can only transmit data to the server at one time,
// but the server can return the response many times.)
func (obj *DemoServer) ServerStreamingMethod(request *demo.Request, stream demo.GRPCDemo_ServerStreamingMethodServer) error {
	clientId, clientMsg := request.ClientId, request.RequestData
	log.Printf("ServerStreamingMethod called by client(%d) init message:= %s", clientId, clientMsg)

	// 开始多次向client发送数据
	// send data to the client several times
	log.Println("ServerStreamingMethod begin to send message to client...")
	for i := 0; i < 5; i++ {
		msg := fmt.Sprintf("Go server ServerStreamingMethod (%d) OK!!!!", i)
		response := &demo.Response{ServerId: obj.Id, ResponseData: msg}
		if err := stream.Send(response); nil != err {
			log.Println(err)
		}
	}
	log.Printf("send message to client(%d) over", clientId)

	return nil
}

// 双向流模式 (在一次调用中, 客户端和服务器都可以向对方多次收发数据)
// stream-stream (In a single call, both client and server can send and receive data
// to each other multiple times.)
func (obj *DemoServer) BidirectionalStreamingMethod(stream demo.GRPCDemo_BidirectionalStreamingMethodServer) error {

	obj.wt.Add(1)
	// 接收数据
	// recv data
	go func() {
		defer obj.wt.Done()
		log.Println("BidirectionalStreamingMethod called, begin to recv data from client ... ")
		for {
			request, err := stream.Recv()
			if io.EOF == err {
				log.Println("recv from client over")
				break
			}
			if nil != err {
				log.Println(err)
			}
			log.Printf("recve from client(%d) message: %s", request.ClientId, request.RequestData)

		}

	}()

	// 开始多次向client发送数据
	// send data to the server several times
	log.Println("BidirectionalStreamingMethod begin to send message to client...")
	for i := 0; i < 5; i++ {
		msg := fmt.Sprintf("Go server BidirectionalStreamingMethod (%d) OK!!!!", i)
		response := &demo.Response{ServerId: obj.Id, ResponseData: msg}
		if err := stream.Send(response); nil != err {
			log.Println(err)
		}
	}

	obj.wt.Wait()
	return nil
}

```

