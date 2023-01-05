import base64
import time

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from decouple import config


USRNAME = config('DLVRO_USERNAME')
UPWD = config('DLVRO_PWD')


def login():
    login_url = 'https://restaurant-hub.deliveroo.net/login'

    chrome_options = Options()
    service = ChromeService(executable_path=ChromeDriverManager().install())
    chrome_options.add_argument("--headless")
    ua = UserAgent()
    a = ua.random
    user_agent = ua.random
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Firefox()
    driver.get(login_url)
    try:
        time.sleep(5)
        driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
        time.sleep(5)
        email_input = driver.find_element(By.XPATH,
                                          "/html/body/div[1]/div[1]/div[1]/div/form/div[2]/label[1]/span/div/input")
        email_input.send_keys(USRNAME)
        pwd_input = driver.find_element(By.XPATH,
                                        "/html/body/div[1]/div[1]/div[1]/div/form/div[2]/label[2]/span/div/input")
        pwd_input.send_keys(UPWD)
        driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[1]/div/form/div[2]/button").click()
        time.sleep(20)
        getDeliverooStatusViaAutomation(driver, 280021, 155923)
    except Exception as e:
        print(e)


def getDeliverooStatusViaAutomation(driver, brand_id, store_id):
    deliveroo_url = 'https://restaurant-hub.deliveroo.net/live-orders/settings?orgId={b_id}&branchId={s_id}'.format(
        b_id=brand_id,
        s_id=store_id)

    driver.get(deliveroo_url)
    online_h4 = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/main/div[2]/div/div[2]/div[1]/div/div/div/h4")
    print(online_h4.text)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    string = USRNAME + ":" + UPWD
    token = base64.b64encode(string.encode('utf-8'))
    getStoreStatus(280021, 155923, token)
