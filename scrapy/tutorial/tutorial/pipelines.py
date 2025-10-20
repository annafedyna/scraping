# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json 

class TutorialPipeline:
    def __init__(self):
        self.quotes = {}

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        author = adapter.get("author")
        text = adapter.get("quote_text")

        if author not in self.quotes:
            self.quotes[author] = [text]
        else :
            self.quotes[author].append(text)
        return item


    def close_spider(self, spider):
        # Save all collected quotes to a JSON file
        print("      -------------------------          ")
        # print("Quotes:" , self.quotes)
        with open('quotes_by_author.json', 'w', encoding='utf-8') as f:
            json.dump(self.quotes, f, indent=4, ensure_ascii=False)