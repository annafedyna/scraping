import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from scrapy.selector import Selector
from ..items import LetterboxItem
import time
import json
from pprint import pprint

class LetterSpider(scrapy.Spider):
    name = "films"
    FILMS_LIMIT = 200

    def __init__(self, *args, **kwargs):
        super(LetterSpider, self).__init__(*args, **kwargs)

        urls = kwargs.get('urls', None)

        if urls:
            self.urls = self.urls if isinstance(self.urls, list) else [self.urls]
        else:
            print("\nNo URLs provided, loading from default file...\n")
            file_path = "urls_with_filmlists_letterbox.txt"
            try:
                with open(file_path, "r") as f:
                    self.urls = [line.strip() for line in f if line.strip()]
            except FileNotFoundError:
                print(f"File not found: {file_path}")
                self.urls = []


        options = webdriver.ChromeOptions()  # Set up Selenium Chrome driver
        options.add_argument("--headless") 
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def start_requests(self):
        urls = self.urls
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_list)
    
    def parse_list(self, response):
        """ Makes a list of all the film links """
        self.driver.get(response.url)
        sel = Selector(text=self.driver.page_source)

        film_links = sel.xpath("//div[@class='poster film-poster']/a/@href").getall()
        if film_links and len(film_links) > self.FILMS_LIMIT:
            film_links = film_links[:self.FILMS_LIMIT]

        for link in film_links:
            full_url = response.urljoin(link)
            yield scrapy.Request(url=full_url, callback=self.parse_film)

    def parse_film(self, response):
        """ Collect film info """
    
        self.driver.get(response.url) # render the page

        sel = Selector(text=self.driver.page_source)
        title = sel.xpath("//h1[contains(@class, 'headline-1')]/span[contains(@class, 'name')]/text()").get()   
        if title:
            title = title.replace("\xa0", " ").strip()

        release_year = sel.xpath("//span[@class='releasedate']/a/text()").get()
        # rating = sel.xpath("//span[contains(@class, 'average-rating')]//a/text()").get().strip()

        script = sel.xpath("//script[contains(text(), 'genre')]/text()").get()
        if script:
            cleaned_script = script.replace("/* <![CDATA[ */", "").replace("/* ]]> */", "").strip()
            json_data = json.loads(cleaned_script)
            genres = json_data["genre"]
            rating = json_data["aggregateRating"]["ratingValue"]
        else:
            print("================ NO Scripts Containing Genre ==============")

        item = LetterboxItem()
        item["film_name"] = title
        item["film_year"] = release_year
        item["film_rating"] = rating
        item["film_genres"] = genres
        yield item

    def closed(self, reason):
        self.driver.quit()
