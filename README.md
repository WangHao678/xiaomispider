**目标**

```python
1、网址 ：百度搜 - 小米应用商店，进入官网
2、目标 ：所有应用分类
   应用名称
   应用链接
```

**实现步骤**

- **1、确认是否为动态加载**

```python
1、页面局部刷新
2、右键查看网页源代码，搜索关键字未搜到
# 此网站为动态加载网站，需要抓取网络数据包分析
```

- **2、F12抓取网络数据包**

```python
1、抓取返回json数据的URL地址（Headers中的Request URL）
   http://app.mi.com/categotyAllListApi?page={}&categoryId=2&pageSize=30
        
2、查看并分析查询参数（headers中的Query String Parameters）
   page: 1
   categoryId: 2
   pageSize: 30
   # 只有page在变，0 1 2 3 ... ... ，这样我们就可以通过控制page的值拼接多个返回json数据的URL地址
```

- **将抓取数据保存到csv文件**

```python
# 注意多线程写入的线程锁问题
from threading import Lock
lock = Lock()
# 加锁
lock.acquire()
python语句
# 释放锁
lock.release()
```