# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LetterboxItem(scrapy.Item):
    film_name = scrapy.Field()
    film_year = scrapy.Field()
    film_rating = scrapy.Field()
    film_genres = scrapy.Field()
