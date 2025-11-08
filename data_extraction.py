#import data refining libraries
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

#Import color library
from colorama import Fore, init, Back, Style
init(autoreset=True)

#import our html_extraction file
#from html_extraction import MAX_PAGES, FOLDER_NAME
MAX_PAGES, FOLDER_NAME = 5, "RAW_HTML"

#Make a function to get the number of sub-folders
def count_subfolder(PATH_TO_FOLDER: str):
    try:
        contents = os.listdir(PATH_TO_FOLDER)

        #Define a counter
        count = 0

        for item in contents:
            full_path = os.path.join(PATH_TO_FOLDER, item)

            #Check if item is a folder
            if os.path.isdir(full_path):
                count += 1

        return count
    
    except:
        print(Fore.RED + Style.BRIGHT + f"ERROR: {PATH_TO_FOLDER} does not exist!")

#Make a function to format price string
def price_formatter(price_str: str):
    string_no_decimal = re.sub(r"\..*", "", price_str)
    final_digits = re.sub(r"\D", "", string_no_decimal)
    return int(final_digits)

#Make a function to format review string
def review_formatter(review_str: str):
    return re.sub(r"\D", "", review_str)

#now we will loop through the pages
PRODUCT_NAME = []
PRICE = []
RATING = []
N_REVIEWS = []

for i in range(1, MAX_PAGES + 1):
    page_path = os.path.join(FOLDER_NAME, f"page-{i}")

    #Put all the html files in a list
    products = os.listdir(page_path)

    #Loop through the html files
    for product in products:
        html_file_path = os.path.join(page_path, product)

        #Read the html
        with open(html_file_path, "r", encoding="utf-8") as f:
            html = f.read()
            #Define the soup for the html file
            soup = BeautifulSoup(html, 'html.parser')

            #Get the product name
            try:
                product_name = soup.select_one('div.puisg-col-inner h2').get_text().strip()
                PRODUCT_NAME.append(product_name)
            except:
                PRODUCT_NAME.append(None)

            #Get the price
            try:
                price_str = soup.select_one('span.a-price span').get_text().strip()
                price_int = price_formatter(price_str=price_str)
                PRICE.append(price_int)
            except:
                PRICE.append(None)

            #Get the rating
            try:
                rating_str = soup.select_one('div.a-row.a-size').get_text().strip
                rating = float(rating_str)
                RATING.append(rating)
            except:
                RATING.append(None)

            #Get the number of reviews
            try:
                n_review_str = soup.select_one('a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style') .get('aria-label')
                n_reviews = review_formatter(n_review_str)
                N_REVIEWS.append(int(n_reviews))
            except:
                N_REVIEWS.append(None)


            
print(PRODUCT_NAME)
print(PRICE)
print(RATING)
print(N_REVIEWS)
    

