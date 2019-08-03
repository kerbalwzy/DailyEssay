## 使用MD5和base64创建一个Token生成函数和校验函数

#### 使用JWTToken相似的字符串格式: 

##### Token字符串分三部分: 有效截止时间戳 + 载体 + 签名

##### 	有效截止时间戳 = 生成时间戳+有效时间(s)

##### 	载体 = 非敏感数据(gob序列化)

##### 	签名 = MD5(载体 + 盐值 + 有效截止时间戳)

(PS: 没错就是抄JWTToken😝)

-----

- ### MakeToken函数

`func MakeToken(data interface{}, salt string, expiry int64) (token string, err error)`

```go
func MakeToken(data interface{}, salt string, expiry int64) (token string, err error) {
	// 生成载体字符串
	var buff bytes.Buffer
	encoder := gob.NewEncoder(&buff)
	err = encoder.Encode(data)
	if nil != err {
		return "", err
	}
	gobData := buff.Bytes()
	bs64DataStr := base64.StdEncoding.EncodeToString(gobData)

	// 生成有效截止日期字符串
	var liveTimeStamp int64
	now := time.Now()
	if expiry <= 0 {
		// 如果有效时间<=0, 则将有效截止时间设置为到3000年后到此时
		liveTimeStamp = NYearLaterTimeStamp(now, 3000)
	} else {
		liveTimeStamp = time.Now().Unix() + expiry
	}
	liveTimeStampStr := fmt.Sprintf("%d", liveTimeStamp)
	bs64TimeStamp := base64.StdEncoding.EncodeToString([]byte(liveTimeStampStr))
	// 生成签名
	h := md5.Sum([]byte(bs64DataStr + bs64TimeStamp + salt))
	signature := fmt.Sprintf("%X", h)
	token = fmt.Sprintf("%s.%s.%s", bs64TimeStamp, bs64DataStr, signature)
	return token, err
}
```

- ### CheckToken函数

`func CheckToken(token, salt string, data interface{}) (ok bool, err error)`

```go
func CheckToken(token, salt string, data interface{}) (ok bool, err error) {
	//var bs64TimeStamp, bs64DataStr, signature string
	ret := strings.Split(token, ".")
	if len(ret) < 3 {
		err = errors.New("Invalid token string ")
		return
	}
	bs64TimeStamp := ret[0]
	bs64DataStr := ret[1]
	signature := ret[2]
	// 检查盐值
	h := md5.Sum([]byte(bs64DataStr + bs64TimeStamp + salt))
	if signature != fmt.Sprintf("%X", h) {
		err = errors.New("Invalid token string ")
		return
	}

	// 检查有效截止时间
	timeStampStr, err := base64.StdEncoding.DecodeString(bs64TimeStamp)
	if nil != err {
		return
	}
	timeStamp, err := strconv.Atoi(string(timeStampStr))
	if nil != err || int64(timeStamp) < time.Now().Unix() {
		return
	}

	// 将有效数据保存到对象
	gobData, err := base64.StdEncoding.DecodeString(bs64DataStr)
	if nil != err {
		return
	}
	var buff bytes.Buffer
	buff.Write(gobData)
	decoder := gob.NewDecoder(&buff)
	err = decoder.Decode(data)
	if nil != err {
		return
	}
	return true, nil

}
```

- #### NYearLaterTimeStamp函数	(生成N年后的今天的时间戳)

`func NYearLaterTimeStamp(now time.Time, year int) int64`

```go
func NYearLaterTimeStamp(now time.Time, year int) int64 {
	t := time.Date(now.Year()+year,
		now.Month(),
		now.Day(),
		now.Hour(),
		now.Minute(),
		now.Second(),
		now.Nanosecond(),
		time.UTC)
	return t.Unix()
}
```

