import scrapy

class MetacriticSpider(scrapy.Spider):
    name = "metacritic_spider_gamedetails"

    #These are the urls we want to scrape the product from, we loop through all the pages later
    start_urls = [
        "https://www.metacritic.com/browse/games/release-date/available/ps5/date",
        "https://www.metacritic.com/browse/games/release-date/available/ps4/date",
        "https://www.metacritic.com/browse/games/release-date/available/xbox-series-x/date",
        "https://www.metacritic.com/browse/games/release-date/available/xboxone/date",
        "https://www.metacritic.com/browse/games/release-date/available/switch/date",
        "https://www.metacritic.com/browse/games/release-date/available/pc/date",
        "https://www.metacritic.com/browse/games/release-date/available/ios/date",
        "https://www.metacritic.com/browse/games/release-date/available/stadia/date"
    ]

    #Here we get the link for each game, so we can get all the details
    def parse(self, response):

        # Extract data from each game page
        for game_link in response.css("td.clamp-summary-wrap a.title::attr(href)").getall():
            yield scrapy.Request(url=f"https://www.metacritic.com{game_link}", callback=self.parse_game) #callback the subsequent function to continue

    #Loop through all the pages of the platforms
        next_page_link = response.css('a[rel="next"]')
        if next_page_link:
            next_page = next_page_link.attrib.get('href')
            if next_page:
                yield response.follow(next_page, callback=self.parse)

    # Extract data from a single game page, with css selectors
    def parse_game(self, response):
        #title = response.css("div.product_title h1::text").get()
        title = response.xpath("//div[contains(@class, 'product_title')]//h1/text()").get()
        genre = response.css("li.summary_detail.product_genre span:not(.label)::text").getall()
        reldate = response.css("li.summary_detail.release_data span.data::text").get()
        platform = response.css("span.platform a::text").get().strip()
        metascore = response.css("span[itemprop='ratingValue']::text").get()
        pcrc = response.css("ol.score_counts li.score_count:nth-child(1) span.count::text").get()
        mcrc = response.css("ol.score_counts li.score_count:nth-child(2) span.count::text").get()
        ncrc = response.css("ol.score_counts li.score_count:nth-child(3) span.count::text").get()
        userscore = response.css("div.metascore_w.user.large.game::text").get()
        purc = response.css("div.module.reviews_module.user_reviews_module li.score_count:nth-child(1) span.count::text").get()
        murc = response.css("div.module.reviews_module.user_reviews_module li.score_count:nth-child(2) span.count::text").get()
        nurc = response.css("div.module.reviews_module.user_reviews_module li.score_count:nth-child(3) span.count::text").get()
        dev = response.css("li.summary_detail.developer span.data a::text").getall()
        nopl = response.css("li.summary_detail.product_players span.data::text").get()
        key = title.replace(" ","").lower()[:6] + "_" + title.replace(" ","").lower()[-2:] + "_" + platform.replace(" ","").lower()[:2] + "_" + platform.replace(" ","").lower()[-2:]

        # Yield the scraped data
        yield {
            "Title": title,
            "Genre": genre,
            "Rel. date": reldate,
            "Platform": platform,
            "MetaScore": metascore,
            "Positive Critic Reviews Count": pcrc,
            "Mixed Critic Reviews Count": mcrc,
            "Negative Critic Reviews Count": ncrc,
            "UserScore": userscore,
            "Positive User Reviews Count": purc,
            "Mixed User Reviews Count": murc,
            "Negative User Reviews Count": nurc,
            "Developer": dev,
            "No. of players": nopl,
            "Key": key,
        }

