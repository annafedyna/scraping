import requests
from bs4 import BeautifulSoup
import csv

r = requests.get("https://realpython.github.io/fake-jobs/")
soup = BeautifulSoup(r.text, 'html.parser')

def save_to_csv(row):
    with open("jobs.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)
        f.close()

for job in soup.find_all('div', class_="card-content"):
    title = job.find("h2", class_="title").text.strip()
    company = job.find("h3", class_="company").text.strip()
    location = job.find("p", class_="location").text.strip()
    date = job.find("time").text.strip()
    learn = job.select("a")[0]["href"].strip()
    apply = job.select("a")[1]["href"].replace("\n", " ")
    row = [title,company,location,date,learn,apply]
    save_to_csv(row)
