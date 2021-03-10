import scrapy


class CSSQuotesSpider(scrapy.Spider):
    name = 'toscrape-css'

    # Shorthand for defining start_requests w/o extra arguments
    # start_urls = ['http://quotes.toscrape.com/page/1/']

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    # def parse(self, response):
    #     # saving browser html to local file after start_requests callback
    #     page = response.url.split("/")[-2]
    #     filename = 'quotes-%s.html' % page
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log('Saved file %s' % filename)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        # FOLLOWING LINKS: METHOD 1 - request the 'href' attribute
        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
            # next_page = response.urljoin(next_page)  # build a full URL to next pg
            # yield scrapy.Request(next_page, callback=self.parse) # yield returned Request obj
            # yield response.follow(next_page, callback=self.parse)  # supports relative URLs directly

        # FOLLOWING LINKS: METHOD 2 - response.follow() w/ <a> tag
        # # For ``<a>`` elements there is a shortcut: ``response.follow`` uses their href attribute.
        # for a in response.css('ul.pager a'):
        #     yield response.follow(a, callback=self.parse)

        # FOLLOWING LINKS: METHOD 3 - response.follow_all() with <a> tags and CSS
        # anchors = response.css('ul.pager a')
        # yield from response.follow_all(anchors, callback=self.parse)
        yield from response.follow_all(css='ul.pager a', callback=self.parse)
