### HMHome项目实训难点功能——添加住房订单功能

----

- 难点:如何保证不会添加出 对同一个房间 存在 住房时间冲突 的订单? 即假如想在我想入住 007号房 ,想要入住时间是 3月10日–3月20日 ,那么如果已经存在对这个 007号房的有效订单与我的想要入住的时间有重叠,那么后台就不能让房客成功下这个订单, 防止出现一房同时被两个人租用的乌龙情况

- 分析:

  - ##### 1.查出这个007号房间的所有订单

  - ##### 2.在这些订单中找到入住时间与我的入住时间存在重叠的订单,即冲突订单

  - ##### 3.如果冲突订单的数量 `>0` 则意味这我不能对这个订单进行入住

  - ##### 4.订单时间冲突图像分析

    ![image-20190320174804344](https://github.com/kerbalwzy/DailyEssay/blob/master/media/HMHome/image-20190320174804344.png)

- 代码:

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
        
   		for key, value in kwargs.items():
            # 给模型类对象的指定属性赋值
        	setattr(orm_ob, key, value)
            
        # 将数据保存到数据库 
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
            					Order.house_id==house_id
        						).filter(
        							or_(
                                		and_( # 对应图中的order3
                                            Order.begin_date <= start_date
                                        	Order.end_date >= start_date, 
                                        ),
                                        and_( # 对应图中的order4
                                        	Order.begin_date <= end_date,
                                            Order.end_date >= end_date
                                        ),
                                        and_( # 对应图中的order5
                                        	Order.begin_date >= start_date,
                                            Order.end_date <= end_date
                                        ),
                                        and_( # 对应图中的order6
                                        	Order.begin_date <= start_date,
                                            Order.end_date >= end_date
                                        )
                                	)
        						).filter(
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

