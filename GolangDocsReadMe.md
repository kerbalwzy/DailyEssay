# DailyEssay - Golang

### [01-switch结构的两个注意点](https://github.com/kerbalwzy/DailyEssay/blob/master/GolangDocs/SpecialPoint_switch.md)

```
- 当case关键字后用,(逗号)隔开多个条件时, 内在的逻辑关系其实是or(或)逻辑; 即只要满足其中一个条件, 此分支都会被执行.
- 在分支中添加fallthrough后, 只要当前分支执行了, 那么下一分支也一定会执行
```

### [02-直接声明数组和使用new关键字声明数组的区别](<https://github.com/kerbalwzy/DailyEssay/blob/master/GolangDocs/SpecialPoint_array.md>)

```
- 直接声明是值类型, 使用了new关键字是指针类型
- %v 打印数据默认格式, %T 打印数据类型
```

### [03-递归在Golang中的优势](https://github.com/kerbalwzy/DailyEssay/blob/master/GolangDocs/recursionInGo.md)

```
- Golang中函数调用栈使用可变大小栈
- Golang中使用递归不必考虑溢出和安全问题
```

### [04-重要的并发安全, 解决资源竞争问题](<https://github.com/kerbalwzy/DailyEssay/blob/master/GolangDocs/concurrentlySecure.md>)

```
- 容量为1的channel
- sync.Mutex 互斥锁
- sync.RWMutex 读写锁
```

