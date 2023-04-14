import scrapy

class MetacriticSpider(scrapy.Spider):
    name = "bol_spider"

    #These are the urls we want to scrape the product from, we loop through all the pages later
    start_urls = [
        "https://www.bol.com/nl/nl/l/games-voor-de-ps5/51867/",
        "https://www.bol.com/nl/nl/l/games-voor-de-ps4/38904/",
        "https://www.bol.com/nl/nl/l/games-voor-de-pc/38907/",
        "https://www.bol.com/nl/nl/l/games-voor-de-xbox-one/38905/",
        "https://www.bol.com/nl/nl/l/games-voor-de-xbox-series-x/51868/",
        "https://www.bol.com/nl/nl/l/games-voor-de-nintendo-switch/38906/",
    ]

    def parse(self, response):
        for game_link in response.css('a.product-title::attr(href)').getall():
            yield scrapy.Request(url=f"https://www.bol.com{game_link}", callback=self.parse_game) #callback the subsequent function to continue
    
    #Loop through all the pages of the platforms
        next_page_link = response.css('li.pagination__controls.pagination__controls--next a::attr(href)').get()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse)

    def parse_game(self, response):
        title = response.css('h1.page-heading span[data-test="title"]::text').get()
        platform = response.css('.specs__row:nth-child(2) .specs__value::text').get().strip()
        price = response.css("span[data-test='price']::text").get().strip()

        yield {
            "Title": title,
            "Platform": platform,
            "Price": price,
            "Key": title.replace(" ","").lower()[:6] + "_" + title.replace(" ","").lower()[-2:] + "_" + platform.replace(" ","").lower()[:2] + "_" + platform.replace(" ","").lower()[-2:]
        }

