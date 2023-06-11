# Import libraries
import concurrent.futures
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import warnings
warnings.filterwarnings('ignore')

# Import libraries
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import warnings
warnings.filterwarnings('ignore')

def scraper( publish_year:int, page_number:int) -> list:
    print(f'Scraper called...')
    print(f'Start Scraping for year {publish_year} and page {page_number}')
    
    base_url = f'https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=iccke&highlight=true&returnType=SEARCH&\
    matchPubs=true&returnFacets=ALL&ranges={publish_year}_{publish_year}_Year&pageNumber={page_number}'
    
    try:
        options = webdriver.FirefoxOptions()
        #options.add_argument("--headless=new")
        options.headless = True

        driver = webdriver.Firefox(options=options)
        driver.get(base_url)                
        page_source = driver.page_source
        driver.quit()

        soup = BeautifulSoup(page_source)
        titles = soup.find_all('h3', {'class': 'text-md-md-lh'})
        titles = [title.a.text for title in titles if title.a]
        
        if titles:
            print(f'Titles for year {publish_year} and page {page_number} scraped successfully :)')
            
        else:
            print(f'list of titles: {titles}')
            
        return titles
    
    except Exception as  e:
        print('Error time :(')
        print(publish_year, page_number)
        print(e)

def write(args:tuple) -> None:
    publish_year, page_number = args
    
    titles_2021 = {}
    titles_2022 = {}
    
    if publish_year == 2021:
        titles_2021[page_number] = scraper(publish_year, page_number)
    
    elif publish_year == 2022:
        titles_2022[page_number] = scraper(publish_year, page_number)
    else:
        print("Invalid year!")
        
    # write titles to file
    with open(f'../Scraped titles/titles_{publish_year}.txt', 'a') as f:
        titles = titles_2021 if publish_year == 2021 else titles_2022
        for key in titles.keys():
            for title in titles[key]:
                f.write(f"{title.strip()}\n")
                
if __name__ == "__main__":
    arguments = [(year, number) for year in [2021, 2022] for number in [1, 2, 3, 4]]
    
    # Clear files contents
    open(f'../Scraped titles/titles_{2021}.txt', 'w').close()
    open(f'../Scraped titles/titles_{2022}.txt', 'w').close()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(write, arguments) 