## switch结构的两个特殊注意点

#### 一、当case关键字后用`,`(逗号)隔开多个条件时, 内在的逻辑关系其实是`or	`(或)逻辑; 即只要满足其中一个条件, 此分支都会被执行.

###### ⚠️代码示例如下, 你输入1或者2, 第二个分支都会执行

```go
package main

import "fmt"

func main() {
    var num int
	fmt.Print("Please enter a number between 0 and 3：")
	_, err := fmt.Scanln(&num)
	if err != nil { panic(err) }
	switch num {
	case 0:
		fmt.Println("The num is 0")
	case 1, 2:
		fmt.Println("The num is 1 or 2")
	case 3:
		fmt.Println("The num is 3")
	default:
		fmt.Println("The num is not between 0 and 3")
	}
}
```

----

#### 二、在分支中添加`fallthrough`后, 只要当前分支执行了, 那么下一分支也一定会执行

###### ⚠️代码示例如下, 分支6、7、8、default都会执行, 请仔细体味注释的那句话, 

```go
package main

import "fmt"

func main() {
    k := 6
	switch k {
	case 5:
		fmt.Println("was <= 5")
		fallthrough
	case 6:
		fmt.Println("was <= 6")
		fallthrough
		// 添加fallthrough后, 在此分支执行了的情况下, 下一分支一定被执行
	case 7:
		fmt.Println("was <= 7")
		fallthrough
		// 添加fallthrough后, 在此分支执行了的情况下, 下一分支一定被执行
	case 8:
		fmt.Println("was <= 8")
		fallthrough
		// 添加fallthrough后, 在此分支执行了的情况下, 下一分支一定被执行
	default:
		fmt.Println("default")
}
```

