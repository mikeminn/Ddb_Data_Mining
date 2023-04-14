import scrapy

class MetacriticSpider(scrapy.Spider):
    name = "metacritic_spider_userreviews"

    #These are the urls we want to scrape the games from, we loop through all the pages later
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

        #here we start the loop to go through all games on the page
        for game_link in response.css("td.clamp-summary-wrap a.title::attr(href)").getall():

            #please note: we append critic-reviews to the game url to go to the respective page
            yield scrapy.Request(url=f"https://www.metacritic.com{game_link}/user-reviews", callback=self.parse_game) #callback the subsequent function to continue

    #Loop through all the pages of the platforms
        next_page_link = response.css('a[rel="next"]')
        if next_page_link:
            next_page = next_page_link.attrib.get('href')
            if next_page:
                yield response.follow(next_page, callback=self.parse)

    # Extract data from a single game page, with css selectors
    def parse_game(self, response):
        
        #Here we start the loop to go through all the reviews on the page
        for review in response.css('ol.user_reviews > li'):
            title = response.css("div.product_title h1::text").get()
            platform = response.css("span.platform a::text").get().strip()

            #Text
            #The text can come from two sections, expanded and review_body. We first check expanded. If this returns None, we get the text from review_body.
            if review.css('span.blurb.blurb_expanded::text').get() != None:
                text = review.css('span.blurb.blurb_expanded::text').get().strip()
            else:
                text = review.css('.review_body span::text').get().strip()

            yield {
                "Title": title,
                "Rel. date": response.css("li.summary_detail.release_data span.data::text").get(),
                "Platform": platform,
                "Username": review.css('div.review_critic > div.name > a::text').get(),
                "Date": review.css('div.review_critic > div.date::text').get(),
                "Review Grade": review.css('div.review_grade div.metascore_w::text').get().strip(),
                "Upvotes": review.css('span.total_ups::text').get(),
                "Total votes": review.css('span.total_thumbs::text').get(),
                "Review text": text,
                "Key": title.replace(" ","").lower()[:6] + "_" + title.replace(" ","").lower()[-2:] + "_" + platform.replace(" ","").lower()[:2] + "_" + platform.replace(" ","").lower()[-2:]
            }

            #the review section might consist of multiple pages, here we go to the next page
            next_page = response.css(".flipper.next a::attr(href)").get()
            if next_page is not None:
                yield response.follow(next_page, self.parse_game)
