## 重要的并发安全, 解决资源竞争问题

##### 并发性能是Golang的一个非常重要的优势点,  使用并发的时候保证并发的安全就非常重要啦(😂废话不说了)

##### 在Golang中解决并发时的资源竞争问题, 最基本的有以下两种方式:

- #### 第一种方式, 使用一个`容量为1的channel`解决问题, 利用的是有缓存的channel当容量满后产生阻塞的特性.

  ```go
  package main
  
  // 定义一个容量为1的channel, 其实保存什么类型的数据并不重要
  // 定义一个假定会被并发修改的变量specialSum
  var (
  	lockChan   = make(chan bool, 1)
  	specialSum int
  )
  
  // 定义一个修改specialSum的函数, 具体怎么改不重要, 重要的是这个函数会被并发访问
  // 在修改specialSum前, 给lockChan存入一个值, 那么容量就满了, 其它并发操作就会被阻塞
  // 在修改specialSum后, 从lockChan取出一个值, 用了空余容量, 其它某一个并发操作得到执行
  func ChangeSpecialSum(num int) {
  	lockChan <- true
  	defer func() { <-lockChan }()
  	//通过defer延迟调用更加能保证并发安全, 因为就算函数运行过程中出错也能保证不会永久阻塞
  
  	specialSum += num
  }
  
  // 定义一个读取specialSum的, 为了保存读取到的值准确, 也要实现并发安全
  func ReadSpecialSum() int {
  	lockChan <- true
  	defer func() { <-lockChan }()
  
  	return specialSum
  }
  ```

- #### 第二种方式, 使用`sync.Mutex`互斥锁, 和大多数语言里的互斥锁一样

  ```go
  package main
  
  import "sync"
  
  var (
  	mu sync.Mutex	// 将容量为1的channel替换为 互斥锁
  	specialSum int
  )
  
  func ChangeSpecialSum(num int) {
  	mu.Lock()
  	defer func() { mu.Unlock() }()
  
  	specialSum += num
  }
  
  func ReadSpecialSum() int {
  	mu.Lock()
  	defer func() { mu.Unlock() }()
      
  	return specialSum
  }
  
  ```

- #### 第三种方式, 使用`sync.RWMutex`读写锁, 保证修改操作的并发安全的同时提高读取操作的效率, 核心就是`只有当出现写操作时, 读取操作才会被互斥, 如果都是读取并发则不会互斥`

  ```go
  package main
  
  import "sync"
  
  var (
  	mu sync.RWMutex	// 将普通的互斥锁替换为 读写锁
  	specialSum int
  )
  
  func ChangeSpecialSum(num int) {
  	mu.Lock()
  	defer func() { mu.Unlock() }()
  
  	specialSum += num
  }
  
  func ReadSpecialSum() int {
  	mu.RLock()	// 修改读取操作的上锁与解锁的方法
  	defer func() { mu.RUnlock() }()
      
  	return specialSum
  }
  ```
