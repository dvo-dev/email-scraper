import re
from string import punctuation, whitespace
from typing import Pattern

from bs4 import BeautifulSoup
from bs4.element import ResultSet
from Levenshtein import distance as levenshtein_distance
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

URL: str = ''
email_regex: str = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
name_regex: str = r"/^[a-z ,.'-]+$/i"

# Use chrome webdriver for Selenium
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
service: Service = Service(executable_path=ChromeDriverManager().install())
driver: WebDriver = webdriver.Chrome(service=service, options=options)

# Retrieve contents of page with Selenium first
driver.get(URL)
page_src: str = driver.page_source
soup: BeautifulSoup = BeautifulSoup(markup=page_src, features='lxml')

# Parse for names with BeautifulSoup
sport_filter: Pattern = re.compile('baseball', re.IGNORECASE)
balls: ResultSet = soup.find_all(string=sport_filter)

# Reformat
names: list = list()
for b in balls:
    formatted: str = sport_filter.sub('', b)
    formatted = formatted.strip(whitespace + punctuation)
    if len(formatted) < 30:
        names.append(formatted)

# Parse for emails with BeautifulSoup
cleaned_emails: list = list()
emails: ResultSet = soup.find_all(string=re.compile(email_regex))
for e in emails:
    if len(e) < 69:
        cleaned_emails.append(e)

# Calculate how close "name" and emails are
email_guesses: set = set()
for n in names:
    best_email: str = None
    best_ratio: int = 9000
    for e in cleaned_emails:
        ratio: int = levenshtein_distance(n, e)
        print(f'Name: {n} Email: {e} Ratio: {ratio}')
        if ratio < best_ratio:
            best_email = e
            best_ratio = ratio
    email_guesses.add(best_email)

print(email_guesses)
