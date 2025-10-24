# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class LetterboxPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        sort_by_arg = crawler.settings.get('sort_by', "rating")
        return cls(sort_by_arg)

    def __init__(self, sort_by_arg=None):
        self.sort_by = sort_by_arg
        self.films = []
        self.count_films = 0

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        print("========== Sort By ========", self.sort_by)
        print("========== Film: ==========", item)
        film = {
            "film_name" : adapter.get("film_name"),
            "film_year" : adapter.get("film_year"),
            "film_rating" : adapter.get("film_rating"),
            "film_genres" : adapter.get("film_genres")
        }

        if not any(film["film_name"] == added_film["film_name"] for added_film in self.films):
            self.films.append(film)
            self.count_films += 1
    
    def write_films_json(self, spider):
        self.films.sort(key = lambda film : film["film_" + self.sort_by])
        with open('films.json', 'w', encoding='utf-8') as f:
            json.dump(self.films, f, indent=4, ensure_ascii=False)
        spider.logger.info(f"Saved {self.count_films} films to films.json")

    def close_spider(self, spider):
        self.write_films_json(spider)