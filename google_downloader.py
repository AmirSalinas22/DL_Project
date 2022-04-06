from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

query = 'School zone sign'
limit = 200


options = Options()
options.add_argument("start-maximized") # OPENS WEB
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get('https://www.google.com/')

    # xpath = '//*[@id="input"]'

box = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
driver.implicitly_wait(10)
box.send_keys(query)
box.send_keys(Keys.ENTER)
driver.find_element(By.XPATH, '//*[@id="hdtb-msb"]/div[1]/div/div[2]/a').click()

#last_height = driver.execute_script('return document.body.scrollHeight')
#while True:
#    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
#    time.sleep(2)
#    new_height = driver.execute_script('return document.body.scrollHeight')
#    try:
#        driver.find_element(By.XPATH, '//*[@id="islmp"]/div/div/div/div[1]/div[2]/div[2]/input').click()
#        time.sleep(2)
#    except:
#        pass
#    if new_height == last_height:
#        break
#    last_height = new_height

for i in range(1, limit):
    try:
        driver.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div[' + str(i) + ']/a[1]/div[1]/img').screenshot(
            '..\\Traffic Signs\\School zone sign\\'+ str(query) + str(i)+ '.png')
    except:
        pass



