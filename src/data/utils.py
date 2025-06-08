import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def init_driver():
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    return webdriver.Chrome(options=options)

def parse_html(url, driver):
    driver.get(url)
    try: WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'strong.duration'))
    )
    except Exception as e:
        print(f"Error loading page {url}: {e}")
        return 0
    return 1

def extract_data(driver):
    duration = driver.find_element(By.CSS_SELECTOR, 'strong.duration').text.strip()
    name1 = driver.find_element(
        By.CSS_SELECTOR, 'input#input_search\\:r2\\:'
    ).get_attribute('value')
    name2 = driver.find_element(
        By.CSS_SELECTOR, 'input#input_search\\:r3\\:'
    ).get_attribute('value')
    return duration, name1, name2
