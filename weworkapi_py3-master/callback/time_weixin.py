from threading import Timer
import  datetime


def MonitorSystem():
    print("MonitorSystem")
def MonitorNetWork():
    print("MonitorNetWork")
#记录当前时间
print(datetime.datetime.now())
#3S执行一次
sTimer = Timer(3, MonitorSystem)
#1S执行一次
nTimer = Timer(1, MonitorNetWork)
#使用线程方式执行
sTimer.start()
nTimer.start()
#等待结束
sTimer.join()
nTimer.join()
#记录结束时间
print(datetime.datetime.now())