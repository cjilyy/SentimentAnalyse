# -*- coding: utf-8 -*-
# author: Arvin Cao
# time: 2015-06


import requests
from scrapy.selector import HtmlXPathSelector
URL = 'http://www.eastmoney.com/'
DOMAIN = 'eastmoney.com'
KEY_WORD_1 = 'news'
SUFFIX = '.html'
__xpath__all_category = '//div[@class="topNav"]//a/@href'  # 获取各频道url
__xpath__all_news = '//a/@href'                            # 获取页面内所有url
__xpath__title = '//h1/text()'                             # 获取新闻标题
__xpath__date = '//div[@class="Info"]/span[1]/text()'      # 获取新闻发布时间
__xpath_content = '//div[@id="ContentBody"]//text()'       # 获取新闻内容


def get_pagesource(url):
    # 获取网页的源文件
    r = requests.get(url)
    try:
        return r.content.decode('gbk')
    except UnicodeError:
        return r.content.decode('utf8')


def pagesource2xpath(pagesource):
    # 将HTML源文件转化为Xpath对象
    return HtmlXPathSelector(text=pagesource)


def get_all_urls(hxs):
    # 获取页面内所有新闻相关的URL
    result = []
    urls = hxs.select(__xpath__all_news).extract()
    for url in urls:
        if DOMAIN in url and SUFFIX in url and KEY_WORD_1 in url:
            result.append(url)
    return result


def get_content(table):
    # 获取Xpath产生的数据
    result = ''
    for item in table:
        result += item.strip()
    return result


def parse(hxs):
    # 新闻详情页面，数据解析
    title = get_content(hxs.select(__xpath__title).extract())
    date = get_content(hxs.select(__xpath__date).extract())
    content = get_content(hxs.select(__xpath_content).extract())
    result = {'title': title, 'date': date, 'content': content}
    return result


def test():
    # 获取所有频道URL
    hxs = pagesource2xpath(get_pagesource(URL))
    urls = hxs.select(__xpath__all_category).extract()
    # 遍历所有频道，获取所有新闻相关的URL
    result = []
    for url in urls:
        if DOMAIN in url:
            print '[CATEGORY_URL]:' + url
            new_hxs = pagesource2xpath(get_pagesource(url))
            result += get_all_urls(new_hxs)
    print len(result)
    # 遍历所有新闻URL，采集新闻详情
    news = []
    for url in result:
        new_hxs = pagesource2xpath(get_pagesource(url))
        paper = parse(new_hxs)
        if paper['date'] != '' or paper['title'] != '' or paper['content'] != '':
            print '[NEWS]:', paper
            news.append(paper)
    return news


if __name__ == '__main__':
    test()
