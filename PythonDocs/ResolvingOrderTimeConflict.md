### 解决订单商品使用权时间重叠问题--以订酒店房间为案例

----

- 难点:如何保证不会添加出 对同一个房间 存在 住房时间冲突 的订单? 即假如想在我想入住 007号房 ,想要入住时间是 3月10日–3月20日 ,那么如果已经存在对这个 007号房的有效订单与我的想要入住的时间有重叠,那么后台就不能让房客成功下这个订单, 防止出现一房同时被两个人租用的乌龙情况.

  - ⚠️注意一 :  默认开始时间为开始日期的当天14点整, 结束时间为结束日期当天12点整

- 分析:

  - ##### 1.查出这个007号房间的所有订单

  - ##### 2.在这些订单中找到入住时间与我的入住时间存在重叠的订单,即冲突订单

  - ##### 3.如果冲突订单的数量 `>0` 则意味这我不能对这个订单进行入住

  - ##### 4.订单时间冲突图像分析

    ![image-20190322101038331](https://github.com/kerbalwzy/DailyEssay/blob/master/media/HMHome/image-20190320174804344.png)

    - ###### 思路一: 直接找冲突订单有哪些情况,从上图可以分析出,如果是冲突订单有以下三种(or)情况:

      - 1.冲突订单的结束时间在我想要预定的时间范围内

      - 2.冲突订单的开始时间在我想要预定的时间范围内

      - 3.冲突订单的开始时间到结束时间完全包裹或者等于我想要预定的时间

      - 以上三种情况的ORM的查询条件代码如下:

        ```python
        or_(
            # 对应图中的order3与分析情况1
            and_(Order.end_date > begin_date, Order.end_date <= end_date),
            # 对应图中的order4与分析情况2
            and_(Order.begin_date >= begin_date, Order.begin_date < end_date),
            # 图中的order5已经被分析情况1,2所包含
            # 对应图中的order6与分析情况3 
            and_(Order.begin_date <= begin_date, Order.end_date >= end_date)
            # 是否需要添加“=”号,请仔细思考“⚠️注意一”
        )
        ```

    - ###### 思路二: 找不冲突的订单有哪些情况,然后取反获取到冲突的订单.不冲突的情况有以下两种(or)情况:

      - 1.不冲突的订单的结束时间一定在我想要预定的开始时间之前

      - 2.不冲突的订单的开始时间一定在我想要预定的结束时间之后

      - 加入取反操作后的以上两种情况的ORM的查询条件如下:

        ```python
        not_(
            # 情况1,2之间的关系为or, 是否需要添加“=”号,请仔细思考“⚠️注意一”
        	or_(Order.end_date < begin_date, Order.begin_date > end_date)
        )
        ```

- 代码:

  - 使用`assert`断言取代if判断,用抛出异常的方式最终用一个`try...except...`来返回我们自定义的验证响应
  - 将对某些参数的验证步骤特别多的代码(`check_order_date`)抽取成函数,简化主逻辑代码
  - 将某些需要经常写的,但是可以复用的代码抽取出来(`save_orm_object`)
    - !1. 一个代码块的代码不要太长
    - !2.不要写太多的`if`判断
    - !3.不要写太多的`try...except..`
    - !4.同样操作的代码不要写很多遍,抽取出来复用!!!

```python
from datetime import datetime
from sqlalchemy import or_,and_


def check_order_date(begin_date_str, end_date_str):
    """
    用来检查用户在提交订单时,输入的入住时间和退房时间(begin_date_str和end_date_str)是否符合要求
    如果符合要求, 返回datetime类型的begin_date和end_date, 以及入住了几晚的天数统计 days_count
    如果不符合要求, 抛出异常
    """
    # 今天的日期的14点 datetime(例如:2019-03-20 14:00:00), 默认要求2点后才允许入住
    today = datetime.today()
    today = datetime(today.year, today.month, today.day, 14, 0, 0)
    # 将入住时间转换为 datetime 类型的 日期的 14:00:00
    tmp_date = datetime.strptime(begin_date_str, '%Y-%m-%d')
    begin_date = datetime(tmp_date.year, tmp_date.month, tmp_date.day, 14, 0, 0) 
    # 将退房时间转换为 datetime 类型的 日期的 12:00:00
    tmp_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    end_date = datetime(tmp_date.year, tmp_date.month, tmp_date.day, 12, 0, 0)
    # 检验参数是否符合要求
    assert begin_date < end_date, Exception("开始日期大于结束日期")
    assert begin_date >= today, Exception("开始日期小于今日")
    # 计算入住几晚, 由于入住时间为14点, 退房时间为12点, 会造成少算一晚入住时间,所以+1
    days_count = (end_date - begin_date).days + 1
    return begin_date, end_date, days_count

def save_orm_object(ORM_class,**kwargs):
    """
    用来创建并保存ORM数据模型类对象
    要求kwargs传入参数时,键名与ORM_class的Column属性变量名保持一致
    :parame ORM_class 要创建的ORM数据模型类对象的类
    :parame kwarges 需要在创建对象时保存的数据
    :return orm_ob 创建并保存好数据后的ORM数据模型类对象
    """
    try:
        # 创建数据模型类对象
        orm_ob = ORM_class()
        # 给模型类对象的指定属性赋值
        for key, value in kwargs.items():
            setattr(orm_ob, key, value) 
        db.session.add(orm_ob)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return e
    return orm_ob
    
        
@api_blu.route('/orders', methods=['POST'])
@login_required
def add_order():
	"""
  	用户下单订房功能
    """
    # 获取到当前用户的id
    user_id = g.user_id
    # 1.获取到传入的参数
    params = request.get_json()
    house_id = params.get('house_id')
    start_date_str = params.get('start_date')
    end_date_str = params.get('end_date')
    # !!!使用断言,抛出异常的方式返回数据
    try:
        # 2.检查参数的是否齐全
        assert all([house_id, start_date_str, end_date_str]), Exception("参数错误")
        house_id = int(house_id)
    	# 3.检查入住时间是否合法, 并转换为默认最早入住时间与最晚退房时间, 并获取入住天数统计
        begin_date, end_date, days = check_order_date(start_date_str, end_date_str)
    	# 4.检查要租住的房间是否存在
        house = House.query.get(house_id)
        assert house != None, Exception("房间不存在")
    	# 5.检查房客是否是房东本人,避免自我刷单行为
        assert house.user_id != user_id, Exception("不能预定自己的房间")
        # 6.检查改房间是否存在冲突订单
        conflict_order_count = Order.query.filter(
            # 过滤一: 只找当前房间的订单
            Order.house_id==house_id
        ).filter(
            # 过滤二: 查找冲突的订单
            # 采用思路二
            not_(
                or_(Order.end_date < begin_date, Order.begin_date > end_date)
            )		
        ).filter(
            # 过滤三: 避开无效订单
            Order.status.notin_(["CANCELED", "REJECTED"])
        ).count()
        assert conflict_order_count == 0, Exception("房间在该时间段内已经被预定")
        
        # 7.生成订单对象,保存订单数据
        order_data = {
            "user_id":user_id,
            "house_id":house_id,
            "begin_date":begin_date,
            "end_date":end_date,
            "days":days,
            "house_price":house.price
            "amount": days * house.price
        }
        ret = save_orm_object(ORM_class=Order, **order_data)
        assert isinstance(ret, Order), ret
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.ERR, errmsg=str(e))
 
    # 8. 返回下单结果
    return jsonify(errno=RET.OK, errmsg="OK", data={"order_id": order.id})

```

