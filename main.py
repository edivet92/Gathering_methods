from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient('127.0.0.1', 27017)
email_db = client['email_db']

s = Service('./chromedriver.exe')
options = Options()
options.add_argument('start-maximized')
options.add_experimental_option('excludeSwitches', ["enable-automation", 'enable-logging'])

options.add_experimental_option("useAutomationExtension", False)
driver = webdriver.Chrome(service=s, options=options)
driver.get("https://account.mail.ru/login")

login = driver.find_element(By.XPATH, '//input[@name="username"]')
login.send_keys('edivet92')
login.send_keys(Keys.ENTER)
sleep(1)
pswd = driver.find_element(By.XPATH, '//input[@name="password"]')
pswd.send_keys('!Very666Good!')
pswd.send_keys(Keys.ENTER)
sleep(5)#иначе не успевает все подгрузиться и следующий код не работает

first_letter = driver.find_element(By.XPATH, "//a[contains(@class, 'llc_first')]").get_attribute('href')
driver.get(first_letter)
sleep(2)

while not driver.find_element(By.XPATH, "//span[@title='Следующее']").get_attribute('disabled'):
    sleep(2)
    letter = {
    '_id': driver.current_url[26:42],
    'recieve_date': driver.find_element(By.XPATH, "//div[@class='letter__date']").text,
    'letter_author': driver.find_element(By.XPATH, "//div[@class='letter__author']/span[@class='letter-contact']").text,
    'theme': driver.find_element(By.XPATH, '//h2').text,
    'letter_text': driver.find_element(By.XPATH, "//div[@class='letter-body']").text
    }
    try:
        email_db.mail_ru.insert_one(letter)
    except DuplicateKeyError:
        pass
    next_button = driver.find_element(By.XPATH, "//span[@title='Следующее']")
    driver.execute_script('arguments[0].click();', next_button)
print('Fuck Yeah!!!')