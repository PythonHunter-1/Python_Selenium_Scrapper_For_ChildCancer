from selenium import webdriver

path_to_chromedriver = './chromedriver';
browser = webdriver.Chrome(executable_path = path_to_chromedriver)

url = 'https://www.lexisnexis.com/hottopics/lnacademic/?verb=sf&amp;sfi=AC00NBGenSrch'
browser.get(url)

browser.switch_to_frame('mainFrame')
browser.find_element_by_id('terms').clear()
browser.find_element_by_id('terms').send_keys('balloon')

browser.find_element_by_xpath('//*[@id="ddlDateOptions"]/option[contains(text(), "Today")]').click()
browser.find_element_by_xpath('//*[@id="byType"]/option[text()="All News (English)"]').click()
browser.find_element_by_css_selector('input[type=\"submit\"]').click()