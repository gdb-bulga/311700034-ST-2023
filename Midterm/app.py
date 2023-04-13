from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
#driver = webdriver.Chrome(ChromeDriverManager().install())
wait = WebDriverWait(driver, 10)

# 1
driver.get("https://docs.python.org/3/tutorial/index.html")

# 找到下拉選單元素
language_select = Select(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.switchers select'))))

# 選擇 "zh-tw"
language_select.select_by_value('zh-tw')

# 等待下拉選單選擇完成
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.switchers select option[value="zh-tw"][selected="selected"]')))

# 印接下來的文字
print(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'section[id="the-python-tutorial"] h1'))).text)
print(wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'section[id="the-python-tutorial"] p'))).get_attribute('innerHTML'))


# 2
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.inline-search input'))).send_keys('class', Keys.RETURN)  
wait.until(lambda driver: len(driver.find_elements(By.CSS_SELECTOR, 'div[id="search-results"] ul li a')) >= 5)
result = driver.find_elements(By.CSS_SELECTOR, 'div[id="search-results"] ul li a')
for i in result[:5]:
    print(i.text)


driver.quit()
