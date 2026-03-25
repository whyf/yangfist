from selenium import webdriver
from time import sleep

driver = webdriver.Chrome()
driver.maximize_window()
url = 'https://devices.uat.zhhq.for-change.cn/'
driver.get(url)
sleep(5)
driver.find_element_by_xpath('//input[@class="el-input__inner" and @autocomplete="new-password"]').send_keys('admin1')
driver.find_element_by_xpath('//input[@class="el-input__inner" and @placeholder="请输入密码"]').send_keys('123')
driver.find_element_by_xpath('//input[@class="el-input__inner" and @placeholder="请输入验证码 (不区分大小写)"]').send_keys(1)
driver.find_element_by_xpath('//button[@type="button" and @class="el-button el-button--primary el-button--large submit_btn"]').click()
#资产管理
driver.find_element_by_xpath('//[@id="app"]/div/div[2]/div[1]/div/div[1]/div[1]/div/div/ul/li[3]/div/span]').click()