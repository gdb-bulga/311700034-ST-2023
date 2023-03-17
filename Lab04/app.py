from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
#driver = webdriver.Chrome(ChromeDriverManager().install())
wait = WebDriverWait(driver, 60)

# 1
driver.get("https://www.nycu.edu.tw/")

wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'a[href = "https://www.nycu.edu.tw/news-network/"]'))).click()
wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'div.eael-tabs-content ul[class="su-posts su-posts-list-loop"] li a')))[0].click()

print(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'div[id="content-wrap"] header h1'))).get_attribute('innerHTML'))
p = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'div[id="content-wrap"] div[class = "entry-content clr"] p')))
for i in p:
    print(i.get_attribute('innerHTML'))

# 2
driver.switch_to.new_window('tab')
driver.get("https://www.google.com.tw")
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'div input[class = "gLFyf"]'))).send_keys('311700034', Keys.RETURN)  

print(wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'div[class = "v7W49e"] h3[class = "LC20lb MBeuO DKV0Md"]')))[1].get_attribute('innerHTML'))

driver.quit()
