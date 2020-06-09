import redis
from proxypool.error import PoolEmptyError
from proxypool.setting import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY
from proxypool.setting import MAX_SCORE, MIN_SCORE, INITIAL_SCORE
from random import choice
import re



class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)#decode_responses=True存的数据是字符串格式,不加这个参数写入的则为字节类型
    
    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理，设置分数为初始分数
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        """
        mapping = {
            proxy: score,
        }
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):
            print('代理不符合规范', proxy, '丢弃')
            return
        if not self.db.zscore(REDIS_KEY, proxy):#Zscore 命令返回有序集中,成员的分数值,如果成员元素不是有序集 key 的成员,或 key不存在返回 nil 
            return self.db.zadd(REDIS_KEY, mapping)
    
    def random(self):
        """
        随机获取有效代理，首先尝试获取最高分数代理，如果不存在，按照排名获取，否则异常
        :return: 随机代理
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)#Zrangebyscore 返回有序集合中指定分数区间的成员列表,有序集成员按分数值递增(从小到大)次序排列,具有相同分数值的成员按字典序来排列
        if len(result):                                                #返回的是分数区间的值
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)#Zrevrange命令返回有序集中，指定区间内的成员,其中成员的位置按分数值递减(从大到小)来排列,具有相同分数值的成员按字典序的逆序排列
            if len(result):                              #zrevrange返回的是索引的区间值，也就是分数值由大到小的前100个值
                return choice(result)
            else:
                raise PoolEmptyError#显示引发异常，后面语句不再继续
    
    def decrease(self, proxy):
        """
        代理值减一分，小于最小值则删除
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减1')
            return self.db.zincrby(REDIS_KEY, -1,proxy )
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)
    
    def exists(self, proxy):
        """
        判断是否存在
        :param proxy: 代理
        :return: 是否存在
        """
        return not self.db.zscore(REDIS_KEY, proxy) == None # ?
    
    def max(self, proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy: 代理
        :return: 设置结果
        """
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, {proxy:MAX_SCORE})
    
    def count(self):
        """
        获取数量
        :return: 数量
        """
        return self.db.zcard(REDIS_KEY)
    
    def all(self):
        """
        获取全部代理
        :return: 全部代理列表
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
    
    def batch(self, start, stop):
        """
        批量获取
        :param start: 开始索引
        :param stop: 结束索引
        :return: 代理列表
        """
        return self.db.zrevrange(REDIS_KEY, start, stop - 1)


if __name__ == '__main__':
    conn = RedisClient()
    result = conn.batch(0, 88)
    print(result)
