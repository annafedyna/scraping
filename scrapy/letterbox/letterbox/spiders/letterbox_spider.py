import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from scrapy.selector import Selector
from ..items import LetterboxItem
import time

class LetterSpider(scrapy.Spider):
    name = "films"
    FILMS_LIMIT = 0

    def __init__(self):
        options = webdriver.ChromeOptions()  # Set up Selenium Chrome driver
        options.add_argument("--headless") 
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def start_requests(self):
        urls = [
            "https://letterboxd.com/munthxer/list/2025/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_list)
    
    def parse_list(self, response):
        """ Makes a list of all the film links """
        self.driver.get(response.url)
        sel = Selector(text=self.driver.page_source)

        film_links = sel.xpath("//div[@class='poster film-poster']/a/@href").getall()
        if film_links and len(film_links) > 50:
            film_links = film_links[:50]

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
        rating = sel.xpath("//span[contains(@class, 'average-rating')]//a/text()").get().strip()
        genres = sel.xpath("//div[@id='tab-genres']//div[@class='text-sluglist'][1]//a[@class='text-slug']/text()").getall()

        item = LetterboxItem()
        item["film_name"] = title
        item["film_year"] = release_year
        item["film_rating"] = rating
        item["film_genres"] = genres
        yield item

    def closed(self, reason):
        self.driver.quit()
