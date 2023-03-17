from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 1
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.nycu.edu.tw/")

driver.find_element(By.CSS_SELECTOR,'a[href = "https://www.nycu.edu.tw/news-network/"]').click()
driver.find_elements(By.CSS_SELECTOR,'div.eael-tabs-content ul li')[0].click()

print(driver.find_element(By.CSS_SELECTOR,'header h1').get_attribute('innerHTML'))
p = driver.find_elements(By.CSS_SELECTOR,'div[class = "entry-content clr"] p')
for i in p:
    print(i.get_attribute('innerHTML'))

# 2
driver.switch_to.new_window('tab')
driver.get("https://www.google.com.tw")
driver.find_element(By.CSS_SELECTOR,'div input[class = "gLFyf"]').send_keys('311700034', Keys.RETURN)  

print(driver.find_elements(By.CSS_SELECTOR,'div[class = "v7W49e"] h3[class = "LC20lb MBeuO DKV0Md"]')[1].get_attribute('innerHTML'))