import scrapy
from ..items import TutorialItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    async def start(self):
        urls = [
            "https://quotes.toscrape.com/page/1/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # start_urls = [
    #     "https://quotes.toscrape.com/page/1/",
    # ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            item = TutorialItem()
            item["quote_text"] = quote.css("span.text::text").get()
            item["author"] = quote.css("small.author::text").get()
            # yield {
            #     "text": quote.css("span.text::text").get(),
            #     "author": quote.css("small.author::text").get(),
            #     # "tags": quote.css("div.tags a.tag::text").getall(),
            # }
            yield item

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        