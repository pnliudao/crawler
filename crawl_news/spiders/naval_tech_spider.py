import scrapy
import re
import datetime

class QuotesSpider(scrapy.Spider):
    name = "naval-technology"

    def start_requests(self):
        start = 'https://www.naval-technology.com/projects-a-z/'
        yield scrapy.Request(url=start, callback=self.parse_urls)

    def parse_urls(self, response):
        # 从『文章列表』界面获取每篇文章的链接
        urls = response.xpath("//div[@class='cell small-6 medium-8 self-center']/a/@href").getall()
        for url in urls:
            print("url -----> ",url)
            # 对于每篇文章，爬取具体内容
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 从response获取这篇文章的信息

        title = response.xpath("//h1[@class='article-title']/text()").get()
        datatype = "naval-technology"
        texts = response.xpath("//div[@class='grid__col-9 prj__content']//text()").getall()
        text = self.process_content(texts)

        abstract = response.xpath("//div[@class='prj-header__meta_desc']/text()").get()
        time = response.xpath("//span[@class='meta-item c-date__published']/text()").get()
        images = response.xpath("//figure/img/@src").getall()
        yield {
            'title': title,
            'type': datatype,
            'abstract': abstract,
            'time': time,
            'timestamp': self.timeTrans(time),
            'images': images,
            'text': text,
        }

    def process_content(self, txts):
        strs = []
        for txt in txts:
            intro = re.sub('\n+', '', txt).strip()
            if txt.find('Related projects') >= 0:
                break
            if len(intro) > 0:
                strs.append('<p>'+intro+'</p>')
        intros = '\n'.join(strs).strip()
        return intros

    def timeTrans(self, t):
        ctime = datetime.datetime.strptime(t, "%b %d,%Y")
        return ctime


# 运行程序：
# 参考 https://docs.scrapy.org/en/latest/intro/tutorial.html#storing-the-scraped-data
# 输出为 json lines 格式，应对于每个网站提交一个 .j1 文件。