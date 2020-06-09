import json
import re
from .utils import get_page
from pyquery import PyQuery as pq


class ProxyMetaclass(type):#定义元类，从而创建新的子类
    def __new__(cls, name, bases, attrs):#__new__()方法是在创建实例之前被调用的，它的作用是创建一个实例
        count = 0
        attrs['__CrawlFunc__'] = []#attrs属性下新建的一个分属性，名字叫做__CrawlFunc__
        for k, v in attrs.items():#attrs代表的是接下来要创建的子类里的所有方法，包括以crawl_开头的，这里items是遍历里面所有的方法
            if 'crawl_' in k:     #k,v分别表示key,value
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):#callback回调函数，将下面所有以crawl_开头的函数重新调用一遍
        proxies = []
        for proxy in eval("self.{}()".format(callback)):#通过 {} 和 : 来代替以前的 %,将format内的变量值带入{}内，eval() 函数用来执行一个字符串表达式，并返回表达式的值，callback是个回调函数，就是把所有crawl_开头的函数调用一遍
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies
    '''
        
    def crawl_daxiang(self):
        url = 'http://vtp.daxiangdaili.com/ip/?tid=559363191592228&num=50&filter=on'
        html = get_page(url)
        if html:
            urls = html.split('\n')
            for url in urls:
                yield url
          
    def crawl_daili66(self, page_count=4):
        """
        获取代理66
        :param page_count: 页码
        :return: 代理
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_proxy360(self):
        """
        获取Proxy360
        :return: 代理
        """
        start_url = 'http://www.proxy360.cn/Region/China'
        print('Crawling', start_url)
        html = get_page(start_url)
        if html:
            doc = pq(html)
            lines = doc('div[name="list_proxy_ip"]').items()
            for line in lines:
                ip = line.find('.tbBottomLine:nth-child(1)').text()
                port = line.find('.tbBottomLine:nth-child(2)').text()
                yield ':'.join([ip, port])

    def crawl_goubanjia(self):
        """
        获取Goubanjia
        :return: 代理
        """
        start_url = 'http://www.goubanjia.com/free/gngn/index.shtml'
        html = get_page(start_url)
        if html:
            doc = pq(html)
            tds = doc('td.ip').items()
            for td in tds:
                td.find('p').remove()
                yield td.text().replace(' ', '')
                '''


    def crawl_ip3366(self):
        for page in range(1, 5):
            start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)
            html = get_page(start_url)
            ip_adress = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            # \s * 匹配空格，起到换行作用
            re_ip_adress = ip_adress.findall(html)
            for adress, port in re_ip_adress:
                result = adress+':'+ port
                yield result.replace(' ', '')#replace() 方法把字符串中的 old（旧字符串） 替换成 new(新字符串)，如果指定第三个参数max，则替换不超过 max 次, replace 不会改变原 string 的内容

    '''def crawl_data5u(self):
        for i in ['gngn', 'gnpt']:
            start_url = 'http://www.data5u.com/free/{}/index.shtml'.format(i)
            html = get_page(start_url)
            ip_adress = re.compile(' <ul class="l2">\s*<span><li>(.*?)</li></span>\s*<span style="width: 100px;"><li class=".*">(.*?)</li></span>')
            # \s * 匹配空格，起到换行作用
            re_ip_adress = ip_adress.findall(html)
            for adress, port in re_ip_adress:
                result = adress+':'+port
                yield result.replace(' ','')
                '''

    def crawl_kuaidaili(self):
        for i in range(1, 4):
            start_url = 'https://www.kuaidaili.com/free/inha/{}'.format(i)
            html = get_page(start_url)
            ip_adress = re.compile('<tr>\s*<td.*?>(.*?)</td>\s*<td.*?>(.*?)</td>')
            # \s* 匹配空格，起到换行作用
            re_ip_adress = ip_adress.findall(html)
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')

    
    def crawl_xicidaili(self):
        for i in range(1, 4):
            start_url = 'https://www.xicidaili.com/nn/{}'.format(i)
            html = get_page(start_url)
            ip_adress = re.compile('<tr.*?>\s*<td.*?>\s*<img.*?></td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            # \s* 匹配空格，起到换行作用
            re_ip_adress = ip_adress.findall(html)
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')

    '''def crawl_premproxy(self):
        for i in ['China-01','China-02','China-03','China-04','Taiwan-01']:
            start_url = 'https://premproxy.com/proxy-by-country/{}.htm'.format(i)
            html = get_page(start_url)
            if html:
                ip_adress = re.compile('<td data-label="IP:port ">(.*?)</td>') 
                re_ip_adress = ip_adress.findall(html)
                for adress_port in re_ip_adress:
                    yield adress_port.replace(' ','')

    def crawl_xroxy(self):
        for i in ['CN','TW']:
            start_url = 'http://www.xroxy.com/proxylist.php?country={}'.format(i)
            html = get_page(start_url)
            if html:
                ip_adress1 = re.compile("title='View this Proxy details'>\s*(.*).*")
                re_ip_adress1 = ip_adress1.findall(html)
                ip_adress2 = re.compile("title='Select proxies with port number .*'>(.*)</a>") 
                re_ip_adress2 = ip_adress2.findall(html)
                for adress,port in zip(re_ip_adress1,re_ip_adress2):
                    adress_port = adress+':'+port
                    yield adress_port.replace(' ','')
                    '''

