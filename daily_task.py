import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

url = "https://coliver.streamlit.app/"

driver = webdriver.Chrome(service=Service("C:\chromedriver\chromedriver.exe"))
driver.get(url)
time.sleep(10)
driver.quit()