from selenium import webdriver
import time

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.add_argument('--headless')
options.binary_location = "/usr/bin/chromium-browser"
driver = webdriver.Chrome(chrome_options=options)
driver.get('https://python.org')
time.sleep(3)

elements = driver.find_elements_by_xpath('//a')
for e in elements:
    print(e.text)

driver.close()