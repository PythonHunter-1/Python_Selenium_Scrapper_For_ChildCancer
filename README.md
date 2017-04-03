# Python Selenium scrapper for ChildCancer

## Pre-condition

This project works on chrome. 

To run on firefox, you need to install geckodriver firstly.

## Environment setup

This project can run on python 3.

* At first, install python 3 and virtual env.

* After then, create venv by using below command. 

$ python3 -m venv selenium_venv

$ source selenium_venv/bin/activate

* Upgrade pip and install selenium

$ pip install --upgrade pip

$ pip install selenium

* To get results.csv, copy config.json.example to config.json and set spec values.

* If all goes well, run below command.

$ python parallelizer.py