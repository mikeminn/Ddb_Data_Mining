import scrapy

class MetacriticSpider(scrapy.Spider):
    name = "metacritic_spider_criticreviews"

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
            #please note: we append critic-reviews to the game url to go to the respective page
            yield scrapy.Request(url=f"https://www.metacritic.com{game_link}/critic-reviews", callback=self.parse_game) #callback the subsequent function to continue

    #Loop through all the pages of the platforms
        next_page_link = response.css('a[rel="next"]')
        if next_page_link:
            next_page = next_page_link.attrib.get('href')
            if next_page:
                yield response.follow(next_page, callback=self.parse)

    # Extract data from a single game page, with css selectors
    def parse_game(self, response):
        for review in response.css("li.review.critic_review"):

            #get the title, we store it in a variable as we retrieve the key from it
            title = response.css('div.product_title h1::text').get()

            #get the platform, we store it in a variable as we retrieve the key from it
            platform = response.css("span.platform a::text").get().strip()

            #Source       
            #The source can be denoted in two instances (one links through to the website of the source), we first check the first one, if that returns none we get the second one.
            if review.css('div.review_critic a::text').get() != None:
                source = review.css('div.review_critic a::text').get()
            else:
                source = review.css('div.review_critic > div.source::text').get()

            #Review 
            #Some reviews do not have a score yet, and thus return None. We check this and return "Unscored" if they return None.
            if review.css('div.review_grade div.metascore_w::text').get() != None:
                score = review.css('div.review_grade div.metascore_w::text').get().strip()
            else:
                score = "Unscored"

            yield {
                "Title": title,
                "Rel. date": response.css("li.summary_detail.release_data span.data::text").get(),
                "Platform": platform,
                "Source": source, 
                "Date": review.css('div.date::text').get(),
                "Review Grade": score,
                "Review text": review.css('div.review_body::text').get().strip(),
                "Key": title.replace(" ","").lower()[:6] + "_" + title.replace(" ","").lower()[-2:] + "_" + platform.replace(" ","").lower()[:2] + "_" + platform.replace(" ","").lower()[-2:]
            }

            #the review section might consist of multiple pages, here we go to the next page
            next_page = response.css(".flipper.next a::attr(href)").get()
            if next_page is not None:
                yield response.follow(next_page, self.parse_game)

