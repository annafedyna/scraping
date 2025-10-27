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
    custom_settings = {
        "ITEM_PIPELINES": {
            'letterbox.pipelines.LetterboxPipeline': 300,
        },
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 1,
        "AUTOTHROTTLE_MAX_DELAY": 10,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 1.0,
        "RANDOMIZE_DOWNLOAD_DELAY": True,
        "DOWNLOAD_DELAY": 2,
    }

    def __init__(self, sort_by=None, films_limit=None, *args, **kwargs):
        super(LetterSpider, self).__init__(*args, **kwargs)

        urls = kwargs.get('urls', None)
        self.sort_by = sort_by
        self.films_limit = films_limit

        if urls:
            self.urls = self.urls if isinstance(self.urls, list) else [self.urls]
        else:
            print("\n ==== No URLs provided, loading from default file... ==== \n")
            file_path = "urls_with_filmlists_letterbox.txt"
            try:
                with open(file_path, "r") as f:
                    self.urls = [line.strip() for line in f if line.strip()]
            except FileNotFoundError:
                print(f"File not found: {file_path}")
                self.urls = []


        options = webdriver.ChromeOptions()  # Set up Selenium Chrome driver
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--headless") 
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def handle_error(self, failure):
        """Handle request-level errors such as timeouts, DNS errors, etc."""
        request = failure.request
        self.logger.error(f"Request failed for {request.url}")

    def start_requests(self):
        """ Creates requests for urls and tells what to do when they load """
        urls = self.urls
        for url in urls:
            if not isinstance(url, str) or not url.startswith("http"):
                self.logger.warning(f"Skipping invalid URL: {url}")
                continue
            self.logger.info(f"Starting request: {url}")
            yield scrapy.Request(url=url, callback=self.parse_list, errback=self.handle_error)
    
    def parse_list(self, response):
        """ Makes a list of all the film links """
        try:
            self.driver.get(response.url)
            sel = Selector(text=self.driver.page_source)

            film_links = sel.xpath("//div[@class='poster film-poster']/a/@href").getall()
            if not film_links:
                self.logger.warning(f"No film links found on {response.url}")
                return
            if self.films_limit and film_links and len(film_links) > self.films_limit:
                film_links = film_links[:self.films_limit]

            for link in film_links:
                full_url = response.urljoin(link)
                yield scrapy.Request(url=full_url, callback=self.parse_film, errback=self.handle_error)

            next_page = sel.xpath("//div[@class='paginate-nextprev']/a[@class='next']/@href").get()
            page_number = next_page[-2]
            if next_page:
                full_next_page_url = response.urljoin(next_page)
                print(f"============== Next Page Number: {page_number} ================")
                yield scrapy.Request(
                    url=full_next_page_url,
                    callback=self.parse_list,
                    errback=self.handle_error
                )
        except Exception as e:
            self.logger.error(f"Unexpected error parsing {response.url}: {e}")

    def parse_film(self, response):
        """ Collect film info """
        try:
            self.driver.get(response.url) # render the page
            sel = Selector(text=self.driver.page_source)
        except Exception as e:
            self.logger.error(f"Selenium failed to load {response.url}: {e}")
            return
        
        try:
            title = sel.xpath("//h1[contains(@class, 'headline-1')]/span[contains(@class, 'name')]/text()").get()   
            if title:
                title = title.replace("\xa0", " ").strip()

            release_year = sel.xpath("//span[@class='releasedate']/a/text()").get()

            script = sel.xpath("//script[contains(text(), 'genre')]/text()").get()
            if script:
                cleaned_script = script.replace("/* <![CDATA[ */", "").replace("/* ]]> */", "").strip()
                json_data = json.loads(cleaned_script)
                genres = json_data["genre"]
                rating = json_data["aggregateRating"]["ratingValue"]
            else:
                print("================ NO Scripts Containing Genre ==============")
                self.logger.warning(f"No <script> containing genre found on {response.url}")
        except Exception as e:
            self.logger.error(f"Failed to parse film page {response.url}: {e}")

        item = LetterboxItem()
        item["film_name"] = title
        item["film_year"] = release_year
        item["film_rating"] = rating
        item["film_genres"] = genres
        yield item

    def closed(self, reason):
        self.driver.quit()
