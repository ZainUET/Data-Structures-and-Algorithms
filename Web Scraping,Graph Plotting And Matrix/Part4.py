from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://eduko.spikotech.com/Course"

chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get(BASE_URL)

time.sleep(5)

soup = BeautifulSoup(driver.page_source, "html.parser")

cards = soup.find_all("div", class_="card")

print(f"Found {len(cards)} course cards")

rows = []
for card in cards:
    title_tag = card.find("h4", class_="card-title")
    title = title_tag.get_text(strip=True) if title_tag else ""

    h7_tags = card.find_all("h7")
    instructor = h7_tags[0].get_text(strip=True) if len(h7_tags) > 0 else ""
    semester = h7_tags[1].get_text(strip=True) if len(h7_tags) > 1 else ""

    desc_tag = card.find("p", class_="card-text")
    description = desc_tag.get_text(strip=True) if desc_tag else ""

    link_tag = card.find("a", href=True)
    detail_link = urljoin(BASE_URL, link_tag['href']) if link_tag else ""

    rows.append(["", title, description, "", "", "", "", "", "", instructor, semester])

with open("EdukoCourses.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["CourseCode", "Title", "Description", "CLO1", "CLO2", "CLO3", "CLO4", "TextBook1", "TextBook2", "Instructor", "Semester"])
    writer.writerows(rows)

driver.quit()

print(f"Saved {len(rows)} courses to EdukoCourses.csv")
