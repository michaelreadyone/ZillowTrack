import time
from selenium import webdriver as wd
from selenium.webdriver.common.action_chains import ActionChains

driver = wd.Chrome()

target_url = 'https://www.zillow.com/'
driver.get(target_url)
driver.maximize_window()

# time.sleep(2)

# buy_button = driver.find_element_by_link_text('Buy')
# buy_button.click()
time.sleep(2)


element = driver.find_element_by_css_selector('#px-captcha')
action = ActionChains(driver)
action.click_and_hold(element)
action.perform()
time.sleep(10)
action.release(element)
action.perform()
time.sleep(0.2)
action.release(element)