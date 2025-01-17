import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

url = "https://coliver.streamlit.app/"

driver = webdriver.Chrome(service=Service("C:\chromedriver\chromedriver.exe"))
driver.get(url)
time.sleep(10)
try:
    driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div/div/div/div/button').click()
    time.sleep(60)
except:
    print("no button for restarting")
    pass

driver.quit()
