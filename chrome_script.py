from selenium import webdriver
import os

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

browser.switch_to_default_content()

browser.switch_to_frame('mainFrame')

dyn_frame = browser.find_element_by_xpath('//frame[contains(@name, "fr_resultsNav")]')
framename = dyn_frame[0].get_attribute('name')
browser.switch_to_frame(framename)

# browser.switch_to_frame('mainFrame.5.child')

browser.find_element_by_css_selector('img[alt=\"Download Documents\"]').click()

browser.switch_to_window(browser.window_handles[1])
browser.find_element_by_xpath('//select[@id="delFmt"]/option[text()="Text"]').click()
browser.find_element_by_css_selector('img[alt=\"Download\"]').click()

results_url = browser.find_element_by_partial_link_text('.TXT').get_attribute('href')

os.system('wget {}'.format(results_url))


chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory': '/Users/yourname/Desktop/Lexis/'}
chrome_options.add_experimental_option('prefs', prefs)
browser = webdriver.Chrome(executable_path = path_to_chromedriver, chrome_options = chrome_options)


browser.switch_to_default_content()
browser.switch_to_frame('mainFrame')
dyn_frame = browser.find_element_by_xpath('//frame[contains(@name, "fr_resultsNav")]')
framename = dyn_frame[0].get_attribute('name')
browser.switch_to_frame(framename)