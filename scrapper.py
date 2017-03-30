import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException

def init_driver():
	driver = webdriver.Firefox()
	driver.wait = WebDriverWait(driver, 30)
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
		quick_links = driver.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"ctl00_ctl00_MenuLinks1_COGMegamenu\"]/ul/li[1]/a")))
		driver.get("https://cogmembers.org/apps/roster/membersearch.aspx")
	except TimeoutException:
		print("Cannot find Quick Links")

def get_list(driver):
	discipline = get_config()["discipline"]
	try:
		# discipline = driver.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"ctl00_ctl00_ContentPlaceHolder1_cphMainContent_ddlDiscipline\"]/option[contains(text(), {0}]".format(discipline["name"]))))

		# xpath = "//*[@id=\"ctl00_ctl00_ContentPlaceHolder1_cphMainContent_ddlDiscipline\"]/option[text()=\"{0}\"]".format(discipline["name"])

		# print(xpath)

		discipline_name = driver.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"ctl00_ctl00_ContentPlaceHolder1_cphMainContent_ddlDiscipline\"]/option[text()=\"{0}\"]".format(discipline["name"]))))
		discipline_name.click()

		# discipline_type = driver.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"ctl00_ctl00_ContentPlaceHolder1_cphMainContent_ddlDisciplineType\"]/option[contains(text(), {0})]".format(discipline["type"]))))

		# discipline_type = driver.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"ctl00_ctl00_ContentPlaceHolder1_cphMainContent_ddlDisciplineType\"]/option[contains(text(), \"Primary Discipline Only\")]")))
		# discipline_type.click()

		# search = driver.wait.until(EC.element_to_be_clickable((By.ID, "ctl00_ctl00_ContentPlaceHolder1_cphMainContent_btnSearchRoster")))
		# search.click()
	except TimeoutException:
		print("Discipline boxes not found")



if __name__ == "__main__":
	driver = init_driver()	
	login(driver)
	go_roster(driver)
	get_list(driver)
	time.sleep(25)
	driver.quit()