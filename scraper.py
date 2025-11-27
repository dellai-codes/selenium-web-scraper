from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
from typing import List, Dict

class SeleniumScraper:
    def __init__(self, url: str):
        self.url = url
        self.html = None
        self.soup = None
        self.driver = None

    def start_browser(self):
        options = Options()
        options.add_argument("--headless")  # run in background
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def fetch_page(self):
        try:
            print(f"[+] Fetching: {self.url}")
            self.driver.get(self.url)
            self.html = self.driver.page_source
            self.soup = BeautifulSoup(self.html, "html.parser")
            print("[+] Page fetched successfully")
        except Exception as e:
            print(f"[!] Error fetching page: {e}")
            raise

    def extract_titles(self) -> List[str]:
        return [t.get_text(strip=True) for t in self.soup.find_all(["h1", "h2", "h3"]) if t.get_text(strip=True)]

    def extract_links(self) -> List[str]:
        return [a["href"] for a in self.soup.find_all("a", href=True)]

    def extract_images(self) -> List[str]:
        return [img["src"] for img in self.soup.find_all("img", src=True)]

    def scrape(self) -> Dict:
        if not self.driver:
            self.start_browser()
        self.fetch_page()
        return {
            "url": self.url,
            "titles": self.extract_titles(),
            "links": self.extract_links(),
            "images": self.extract_images()
        }

    def save_to_json(self, data: Dict, filename: str = "output.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"[+] Data saved to {filename}")

    def close_browser(self):
        if self.driver:
            self.driver.quit()
            print("[+] Browser closed")


if __name__ == "__main__":
    url = "https://example.com/"
    scraper = SeleniumScraper(url)
    try:
        data = scraper.scrape()
        scraper.save_to_json(data)
    finally:
        scraper.close_browser()
