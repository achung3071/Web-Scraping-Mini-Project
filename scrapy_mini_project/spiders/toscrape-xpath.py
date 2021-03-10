import scrapy


class XPathQuotesSpider(scrapy.Spider):
    name = 'toscrape-xpath'

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('.//span[@class="text"]/text()').get(),
                'author': quote.xpath('.//small[@class="author"]/text()').get(),
                'tags': quote.xpath('.//div[@class="tags"]//a[@class="tag"]/text()').getall(),
            }
        yield from response.follow_all(xpath='//ul[@class="pager"]//a', callback=self.parse)
