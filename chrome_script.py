from selenium import webdriver
import os
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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

path_to_log = '/Users/yourname/Desktop/'
log_errors = open(path_to_log + 'log_errors.txt', mode = 'w')

seconds = 5 + (random.random() * 5)
time.sleep(seconds)

try:
	# some_object = WebDriverWait(browser, 120).until(EC.element_to_be_located((By.CSS_SELECTOR, 'img[alt=\"Some Button\"]')))
	some_object = WebDriverWait(browser, 120).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'img[alt=\"Some Button\"]')))
except TimeoutException:
	log_errors.write('couldnt locate button XYZ when searching')

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
     "(KHTML, like Gecko) Chrome/15.0.87")

path_to_phantomjs = './phantomjs' # change path as needed
browser = webdriver.PhantomJS(executable_path = path_to_phantomjs, desired_capabilities = dcap)
