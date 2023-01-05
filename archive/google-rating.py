import csv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep
from fake_useragent import UserAgent

chrome_options = Options()
service = ChromeService(executable_path=ChromeDriverManager().install())
# chrome_options.add_argument("--headless")
ua = UserAgent()
a = ua.random
user_agent = ua.random
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
# chrome_options.add_argument('--headless')
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument('disable-infobars')
driver = webdriver.Chrome(options=chrome_options)

ratings = []
accepted = False
stores = ['Royal wotton',
          'Newmarket ',
          'Great Yarmouth',
          'Braintree',
          'Cirencester',
          'St Ives ',
          'Rickmansworth ',
          'Trowbridge',
          'Berkhamsted ',
          'Abingdon',
          'Peterborough South',
          'Bath',
          'Haverhill',
          'Oxford Rosehill',
          'Peterborough Lincoln Road',
          'Cambridge',
          'Gerrards Cross ',
          'Lowestoft',
          'Ipswich',
          'Mildenhall ',
          'Chippenham ',
          'Stroud London',
          'Glastonbury',
          'Melksham ',
          'Oxford Marston',
          'Felixstowe ',
          'Midsomer Norton',
          'Biggleswade',
          'Frome',
          'Ely']


def runRatingScraper(append_str, store_name):
    search_string = append_str + ' ' + store_name
    driver.get("https://www.google.com/maps/place/?q={query}".format(query=search_string))
    try:
        rating = driver.find_element(By.XPATH,
                                     "/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[1]/span/span[1]")
        ratings.append(rating.text)
        return rating.text
    except Exception as ex:
        ratings.append("n.a")


def write_ratings_to_csv():
    filename = "papa-johns-rating.csv"
    data_file = open(filename, 'w', newline='', encoding='utf-8')
    header = ["store_name", "store_rating"]
    csv_writer = csv.DictWriter(data_file, fieldnames=header)
    csv_writer.writeheader()
    for s in stores:
        rating = runRatingScraper("Papa Johns Pizza", s)
        csv_writer.writerow({"store_name": s, "store_rating": rating})
        driver.implicitly_wait(5)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    driver.get("https://www.google.com/?q=papajhons")
    driver.implicitly_wait(6)
    if not accepted:
        try:
            driver.implicitly_wait(20)
            accept_cookie_btn = driver.find_element(By.XPATH,
                                                    "/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button")
            if accept_cookie_btn:
                accept_cookie_btn.click()
            accepted = True
        except Exception as e:
            print("consent btn found", e)
    write_ratings_to_csv()
    print(ratings)
