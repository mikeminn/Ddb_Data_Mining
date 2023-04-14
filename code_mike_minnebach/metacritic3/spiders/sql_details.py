import scrapy

#############################################################################
#                                                                           #
#                   UNCOMMENT FOR USE WITH SQL_DETAILS.PY                   #
#    Also uncomment tagged items in items.py, pipelines.py and setting.py   #
#                                                                           #
#############################################################################

# from metacritic3.items import Metacritic3Item

# class MetacriticSpider(scrapy.Spider):
#     name = "sql_det"

#     #These are the urls we want to scrape the product from, we loop through all the pages later
#     start_urls = [
#         "https://www.metacritic.com/browse/games/release-date/available/ps5/date",
#         "https://www.metacritic.com/browse/games/release-date/available/ps4/date",
#         "https://www.metacritic.com/browse/games/release-date/available/xbox-series-x/date",
#         "https://www.metacritic.com/browse/games/release-date/available/xboxone/date",
#         "https://www.metacritic.com/browse/games/release-date/available/switch/date",
#         "https://www.metacritic.com/browse/games/release-date/available/pc/date",
#         "https://www.metacritic.com/browse/games/release-date/available/ios/date",
#         "https://www.metacritic.com/browse/games/release-date/available/stadia/date"
#     ]

#     #Here we get the link for each game, so we can get all the details
#     def parse(self, response):

#         # Extract data from each game page
#         for game_link in response.css("td.clamp-summary-wrap a.title::attr(href)").getall():
#             yield scrapy.Request(url=f"https://www.metacritic.com{game_link}", callback=self.parse_game) #callback the subsequent function to continue

#     #Loop through all the pages of the platforms
#         next_page_link = response.css('a[rel="next"]')
#         if next_page_link:
#             next_page = next_page_link.attrib.get('href')
#             if next_page:
#                 yield response.follow(next_page, callback=self.parse)

#     # Extract data from a single game page, with css selectors
#     def parse_game(self, response):
#         item = Metacritic3Item()
#         item['title'] = response.xpath("//div[contains(@class, 'product_title')]//h1/text()").get()
#         item ['reldate'] = response.css("li.summary_detail.release_data span.data::text").get()
#         item['platform'] = response.css("span.platform a::text").get().strip()

#         yield item
        

