
<a id="readme-top"></a>
<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Web Scraping</h3>
  <p align="center">
    This repository contains some projects using different Python libraries!
    <br />
   
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Content</summary>
  <ol>
    <li>
      <a href="#about-the-project">About </a>
    </li>
    <li>
      <a href="#getting-started">Repo Structure</a>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About

A collection of simple examples demonstrating how to use BeautifulSoup and Selenium for web scraping.
Additionally, it includes a more advanced project located in the scrapy/ folder that combines Scrapy and Selenium to scrape data from the Letterboxd website — featuring pagination handling and saving sorted data into the file.

Purpose: projects are created purely for educational purposes to explore and understand different web scraping tools and workflows.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Repo Structure

```bash
SCRAPING/
├── beautiful-soup4/
│ └── beautiful_s.py 
│
├── scrapy/
│ ├── letterbox/
│ │ ├── scrapy.cfg
│ │ └── urls_with_filmlists_letterbox.txt
│ │
│ └── tutorial/
│ ├── scrapy.cfg
│ └── tutorial/
│
├── selenium/
│ └── selenium_fake-jobs.py 
│
└── .gitignore
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

 1) Install Prerequisites
  ```sh
  pip install requirements.txt
  ```
  2) Navigate to scrapy project folder
  ```sh
  cd scrapy\letterbox
  or 
  cd scrapy\tutorial
  ```
  3) Run spider
  ```sh
  scrapy crawl films
  or 
  scrapy crawl quotes
  ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing
Feel free to add new ideas !


<p align="right">(<a href="#readme-top">back to top</a>)</p>
