#Import necessary packages
from seleniumbase import Driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC

#Import color library
from colorama import Fore, init, Back, Style
init(autoreset=True)

#Import data formatting stuff
from bs4 import BeautifulSoup
import os
import time
import random

#Initiate a driver
driver = Driver(uc=True, headless=False)

#Define basic Necessities
query = input(Style.BRIGHT + "Query: ")
URL = f"https://www.amazon.in/s?k={query}"
MAX_PAGES = int(input(Style.BRIGHT + "No. of pages to scrap: "))
wait = WebDriverWait(driver, 5)

#Make the raw html data folder
os.makedirs('RAW_HTML', exist_ok=True)

#Now the html extraction begins
try:
    driver.get(url=URL)
    for i in range(MAX_PAGES):
        #Wait till the product elements appear
        selector = (By.CSS_SELECTOR, "div[role='listitem'] div.sg-col-inner")
        wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[role='listitem']")))

        page = i + 1 #Page number currently on

        #Make the sub-directory
        os.makedirs(f'RAW_HTML/page-{page}', exist_ok=True)

        #Message showing success of page retreival
        print(Fore.YELLOW + f"Retrieved page-{page}:")

        #Set a variable elems = all the products section objects
        elems = driver.find_elements(By.CSS_SELECTOR, "div[role='listitem'] div.sg-col-inner")

        #Loop through the elems variable, extract the html and beautify it with bs4
        product = 1
        for elem in elems:
            raw_html = elem.get_attribute('innerHTML')
            #now format the raw html
            soup = BeautifulSoup(raw_html, 'html.parser')
            html = soup.prettify()

            with open(f'RAW_HTML/page-{page}/product-{product}.html', 'w', encoding='utf-8') as f:
                f.write(html)

            #Message showing success of html extraction
            print(Fore.GREEN + f"-> Retrieved Product-{product}")

            #Move to the next product
            product += 1

        #Move to the next page
        if MAX_PAGES != 1:
            button_select = (By.XPATH, "//a[@role='button' and normalize-space(text())='Next']")
            next_button = wait.until(EC.element_to_be_clickable(button_select))
            next_button.click()
        time.sleep(random.uniform(2, 3))

    #Print message to show that html extraction was successful
    print(Style.BRIGHT + "HTML extraction done, starting data extraction...")
    time.sleep(2)

except Exception as e:
    print(Fore.RED + f"ERROR: {e}")