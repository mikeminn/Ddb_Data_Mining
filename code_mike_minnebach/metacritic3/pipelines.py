# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

# useful for handling different item types with a single interface

#############################################################################
#                                                                           #
#                   UNCOMMENT TO USE WITH SQL_DETAILS.PY                    #
#                                                                           #
#############################################################################

# class Metacritic3Pipeline:
#     def __init__(self):
#         self.con = sqlite3.connect('test.db')
#         self.cur = self.con.cursor()
#         self.create_table()

#     def create_table(self):
#         self.cur.execute("""CREATE TABLE IF NOT EXISTS metascrape(
#         title TEXT,
#         reldate TEXT
#         )""")

#     def process_item(self, item, spider):
#         self.cur.execute("""INSERT OR IGNORE INTO metascrape VALUES (?,?)""",
#                         (item['title'], item['reldate']))
#         self.con.commit()
#         return item

