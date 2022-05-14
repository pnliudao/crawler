import scrapy
class QuotesSpider(scrapy.Spider):

    name = "news"
    start_urls = [
        'https://quotes.toscrape.com/page/1/',
        'https://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
# 运行程序：
# 参考 https://docs.scrapy.org/en/latest/intro/tutorial.html#storing-the-scraped-data
# 输出为 json lines 格式，应对于每个网站提交一个 .j1 文件。