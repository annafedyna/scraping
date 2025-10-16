from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time 

driver = webdriver.Chrome()
driver.get("https://realpython.github.io/fake-jobs/")

job_links = []

# Step 1: Collect all job links
for job in driver.find_elements(By.CLASS_NAME, "card-content"):
    title = job.find_element(By.CLASS_NAME, "title").text
    link = job.find_element(By.XPATH, ".//a[2]").get_attribute("href")
    job_links.append((title, link))

# Step 2: Visit each job page
for title, link in job_links:
    driver.get(link)
    time.sleep(2)
    description = driver.find_element(By.XPATH, "//div[@class='content']//p").text
    print(f"{title}\n{description}\n")