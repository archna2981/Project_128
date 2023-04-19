from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests

# Website's URL
START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"

# Webdriver
browser = webdriver.Chrome("C:/Users/Pragya/Downloads/Project_127/chromedriver_win32/chromedriver.exe")
browser.get(START_URL)

#Create an empty list
more_scaraped_data = []

def scrape_more_data(hyperlink):
    print(hyperlink)

    try:
        page = requests.get("hyperlink")

        soup = BeautifulSoup(page.content, "html.parsel")

        temp_list = []
        
        for tr_tag in soup.find_all("tr" , attrs={"class": "fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div" , attrs={"class":"value"})[0].contents[0])
                except:
                    temp_list.append("")

        more_scaraped_data.append(temp_list)

    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

star_df_1 = pd.read_csv("scraped_data.csv")

# Call method
for index, row in star_df_1.iterrows():

     ## ADD CODE HERE ##
    print(row['hyperlink'])
     # Call scrape_more_data(<hyperlink>)
    scrape_more_data(row['hyperlink'])
    print(f"Data Scraping at hyperlink {index+1} completed")

print(more_scaraped_data[0:10])

# Remove '\n' character from the scraped data
scrapped_data = []

for row in more_scaraped_data:
    replaced = []
    for el in row:
        el = el.replace("\n", "")
        replaced.append(el)
    
    scrapped_data.append(replaced)

print(scrapped_data)

#Define Header 
headers = ['Star_names','Distance','Mass','Radius','Luminosity']

#Define pandaas DataFrame 
new_star_df_1 = pd.DataFrame(scrapped_data, columns = headers)

#Convert to CSV 
new_star_df_1.to_csv('scraped_data.csv', index=True, index_label="id")



