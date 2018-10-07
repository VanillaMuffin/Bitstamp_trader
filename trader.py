#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from time import sleep, gmtime, strftime
import requests
import os
import sys

MAX_RATIO = 0.8
MIN_RATIO = 0.5

USERNAME = ""
PASSWORD = ""

def sell():

    browser = login()

    browser.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[1]/h3[1]').click()
    browser.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[2]/div[3]/ul/li[3]/span[1]').click()
    
    xpr_balance = browser.find_element_by_xpath('//*[@id="selected-account-balance-XRP"]').text
    xpr_balance_float = float(xpr_balance)

    if(xpr_balance_float > 10):

        browser.get("https://www.bitstamp.net/market/order/instant/")

        browser.find_element_by_xpath('//*[@id="content-wrapper"]/div/div/div/div[2]/ul[1]/li[3]').click()

        sell_box = browser.find_element_by_css_selector('#instant_sell_form > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > input:nth-child(1)')
        sell_box.send_keys(xpr_balance)
        sleep(0.5)

        browser.find_element_by_link_text('Sell XRP').click()
        browser.save_screenshot('/root/data/sell_screenshot.png')

        out = "echo " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ": "
        out += 'exchanged {}: XPR to EUR'.format(xpr_balance) + ">> /root/data/trader.log"
        os.system(out)

    browser.close()

def buy():

    browser = login()

    browser.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[1]/h3[1]').click()
    browser.find_element_by_xpath('/html/body/div[2]/div[3]/div[1]/div[2]/div[3]/ul/li[3]/span[1]').click()

    eur_balance = browser.find_element_by_xpath('//*[@id="selected-account-balance-EUR"]').text
    eur_balance_float = float(eur_balance)

    if(eur_balance_float > 10):

        browser.get("https://www.bitstamp.net/market/order/instant/")

        browser.find_element_by_xpath('//*[@id="content-wrapper"]/div/div/div/div[2]/ul[1]/li[1]').click()

        buy_box = browser.find_element_by_xpath('//*[@id="id_amount"]')
        buy_box.send_keys(eur_balance)
        sleep(0.5)

        browser.find_element_by_link_text('Buy XRP').click()

        out = "echo " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ": "
        out += 'exchanged {}: EUR to XPR'.format(eur_balance) + ">> /root/data/trader.log"
        os.system(out)

    browser.close()    
    

def login():

    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Firefox(firefox_options=options) 

    browser.get("https://www.bitstamp.net/account/login/")
    sleep(1)

    u = browser.find_element_by_xpath("//*[@id='id_username']")
    p = browser.find_element_by_xpath("//*[@id='id_password']")
    u.send_keys(USERNAME)
    p.send_keys(PASSWORD)
    browser.find_element_by_xpath('//*[@id="login_form"]/input[2]').click()

    return browser



response = requests.get("https://www.bitstamp.net/api/v2/ticker/xrpeur/")
data = response.json()
current_ratio = float(data["last"])


if(current_ratio  > MAX_RATIO):
    sell()

if(current_ratio < MIN_RATIO):
    buy()

else:
    print(str(MIN_RATIO) + " < " + str(round(current_ratio, 3)) + " < " + str(MAX_RATIO))

os.system("rm /root/scripts/*.log")    

#
