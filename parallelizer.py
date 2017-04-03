import json
import time
import csv
import re
import math
import shutil
import glob
# from bs4 import BeautifulSoup

from subprocess import Popen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException, WebDriverException

# class csvItem(scrapy.Item):
# 	last_name = scrapy.Field()
# 	email = scrapy.Field()

login_counter = 0

def init_driver():
	# dcap = dict(DesiredCapabilities.PHANTOMJS)
	# dcap["phantomjs.page.settings.userAgent"] = (
	#      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
	#      "(KHTML, like Gecko) Chrome/15.0.87")

	# path_to_phantomjs = './phantomjs' # change path as needed
	# driver = webdriver.PhantomJS(executable_path = path_to_phantomjs)
	# driver = webdriver.PhantomJS(executable_path = path_to_phantomjs, desired_capabilities = dcap)

	path_to_chromedriver = './chromedriver'
	driver = webdriver.Chrome(executable_path = path_to_chromedriver)

	# driver = webdriver.Firefox()

	driver.wait = WebDriverWait(driver, 60)
	return driver

def get_config():
	# cfg = ConfigParser().read("config.cfg")
	# return cfg
	with open("config.json") as json_data_file:
		cfg = json.load(json_data_file)
	return cfg

def login(driver):
	user = get_config()["user"]
	driver.get("https://cogmembers.org/login.aspx")
	try:
		username_inputbox = driver.wait.until(EC.presence_of_element_located((By.ID, "txtUserName")))
		username_inputbox.send_keys(user["name"])

		password_inputbox = driver.wait.until(EC.presence_of_element_located((By.ID, "txtPassword")))
		password_inputbox.send_keys(user["password"])

		button = driver.wait.until(EC.element_to_be_clickable((By.ID, "btnLogin")))
		button.click()
	except TimeoutException:
		print("Cannot find login elements")

def go_roster(driver):
	# driver.get("https://cogmembers.org/apps/roster/membersearch.aspx")
	try:
		exception_occured = False
		quick_links = driver.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"ctl00_ctl00_MenuLinks1_COGMegamenu\"]/ul/li[1]/a")))
		driver.get("https://cogmembers.org/apps/roster/membersearch.aspx")
	except TimeoutException:
		print("Cannot find Quick Links")
		try:
			driver.wait.until(EC.invisibility_of_element_located((By.ID, "ek_messagelist")))
		except TimeoutException:
			print("something is wrong on login")
			exception_occured = True

	if exception_occured:
		global login_counter
		login_counter += 1
		if login_counter < 3:
			login(driver)
			go_roster(driver)
		else:
			driver.quit()
			exit()

def get_list(driver):
	discipline = get_config()["discipline"]
	try:
		discipline_name = driver.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"ctl00_ctl00_ContentPlaceHolder1_cphMainContent_ddlDiscipline\"]/option[text()=\"{0}\"]".format(discipline["name"]))))
		discipline_name.click()

		discipline_type = driver.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"ctl00_ctl00_ContentPlaceHolder1_cphMainContent_ddlDisciplineType\"]/option[text()=\"{0}\"]".format(discipline["type"]))))
		discipline_type.click()

		search = driver.wait.until(EC.element_to_be_clickable((By.ID, "ctl00_ctl00_ContentPlaceHolder1_cphMainContent_btnSearchRoster")))
		search.click()
	except TimeoutException:
		print("Discipline boxes not found")

def view_all(driver):
	try:
		exception_occured = False
		xpath = "//a[contains(@id, 'ctl00_ctl00_ContentPlaceHolder1_cphMainContent_rgSummary_lbtnViewSize') and contains(text(), 'View All')]"
		view_all = driver.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
		view_all.click()
		try:
			driver.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@id, 'ctl00_ctl00_ContentPlaceHolder1_cphMainContent_rgSummary_lbtnViewSize') and contains(text(), 'View Less')]")))
		except TimeoutException:
			print("Cannot find View Less")
			exception_occured = True

		if exception_occured:
			view_all(driver)

	except TimeoutException:
		print("View All button not found")

def run_subprocesses(driver):
	try:
		record_count = driver.wait.until(EC.presence_of_element_located((By.ID, "ctl00_ctl00_ContentPlaceHolder1_cphMainContent_rgSummary_lblRecordCount")))
				
		matchObj = re.match(r'viewing ((\d)*) records', record_count.text, re.M|re.I)
		print(matchObj.group(1))

		processes = []
		one_step = get_config()["one_step"]
		file_count = math.ceil(int(matchObj.group(1)) / one_step)
		for index in range(file_count):
			processes.append(Popen('python scrapper.py {0} {1}'.format(index, one_step), shell=True))
		for process in processes:
			process.wait()
	except TimeoutException:
		print("Cannot find total record find.")

def result_file_merge(driver):
	with open('results.csv', 'w') as outfile:
		output = csv.writer(outfile)
		output.writerow(["last name", "email"])

	with open('results.csv', 'ab') as outfile:
		for filename in sorted(glob.glob('result_*.csv')):
			with open(filename, 'rb') as readfile:
				shutil.copyfileobj(readfile, outfile)

def write_to_csv(driver, index, output):
	lastname = driver.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ctl00_ContentPlaceHolder1_cphMainContent_radgrMembers_ctl00__{0}"]/td[1]/a'.format(index))))
	# lastname = row.find_elements(By.TAG_NAME, 'td')[0].find_element(By.TAG_NAME, 'a')
	lastname_text = lastname.text
	print(lastname_text)
	try:
		lastname.click()
	except WebDriverException:
		print('closing exception handling....')
		write_to_csv(driver, index)

	# time.sleep(5)

	email = driver.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="divToPrint"]/div[2]/table/tbody/tr/td[2]/table[3]/tbody/tr/td/a')))
	
	print(email.text)
	output.writerow([lastname_text, email.text])

	close = driver.wait.until(EC.element_to_be_clickable((By.ID, 'ctl00_ctl00_ContentPlaceHolder1_cphMainContent_LinkButton1')))
	close.click()
	time.sleep(10)

	

def save_to_csv(driver):
	# try:
		driver.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "tr")))
		with open("results.csv", "w") as f:
			output = csv.writer(f)
			output.writerow(["last name", "email"])

			tbody = driver.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ctl00_ContentPlaceHolder1_cphMainContent_radgrMembers_ctl00"]/tbody')))
			# rows = tbody.find_elements(By.TAG_NAME, "tr")
			time.sleep(10)

			# print(tbody.get_attribute('innerHTML'))
			# soup = BeautifulSoup(tbody.html)
			rows = tbody.find_elements(By.TAG_NAME, "tr")
			print("row length:", len(rows))


			for index, row in enumerate(rows):
				write_to_csv(driver, index, output)
				# lastname = driver.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ctl00_ContentPlaceHolder1_cphMainContent_radgrMembers_ctl00__{0}"]/td[1]/a'.format(index))))
				# # lastname = row.find_elements(By.TAG_NAME, 'td')[0].find_element(By.TAG_NAME, 'a')
				# lastname_text = lastname.text
				# print(lastname_text)
				# try:
				# 	lastname.click()
				# except WebDriverException:


				# email = driver.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="divToPrint"]/div[2]/table/tbody/tr/td[2]/table[3]/tbody/tr/td/a')))
				
				# print(email.text)

				# close = driver.find_element(By.ID, 'ctl00_ctl00_ContentPlaceHolder1_cphMainContent_LinkButton1')
				# close.click()

				# output.writerow([lastname_text, email.text])

			print("Done writing file")

	# except TimeoutException:
	# 	print("Cannot get some elements")





if __name__ == "__main__":
	driver = init_driver()	
	login(driver)
	go_roster(driver)
	get_list(driver)
	view_all(driver)
	run_subprocesses(driver)
	result_file_merge(driver)
	# save_to_csv(driver)
	# time.sleep(25)
	# driver.quit()