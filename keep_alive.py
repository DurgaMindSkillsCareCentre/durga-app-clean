from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

URL = "https://ddurga.streamlit.app/"

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)

print("Opening app...")
driver.get(URL)

time.sleep(30)

print("App visited successfully")

driver.quit()
