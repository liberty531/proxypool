# 在内置异常不够用的情况下，我们可以通过继承内置的异常类来自定义异常类
class PoolEmptyError(Exception):# 可以通过继承Exception来定义一个全新的异常

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):# 可以定义该方法用来定制触发异常时打印异常值的格式
        return repr('代理池已经枯竭')#Python 有办法将任意值转为字符串：将它传入repr() 或str() 函数。
                                    #函数str() 用于将值转化为适于人阅读的形式，而repr() 转化为供解释器读取的形式。

