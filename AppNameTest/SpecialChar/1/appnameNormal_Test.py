import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
# from test1.testt import AES_test
import time
import random 
import string
import pymongo 
from pymongo import MongoClient
from pprint import pprint
import rand_char_1
import testt
from time import sleep
from pprint import pprint
# AES_test = testt.AES_test()

client = MongoClient('mongodb://192.168.100.193:27017')
db = client.RKMS_DB
collection = db.kms_app
db.authenticate("rkms","2Password!")

driver = webdriver.Chrome("../../../chromedriver_win32/chromedriver.exe") #開啟Chrome
driver.get("http://192.168.100.193:8000/")
action = ActionChains(driver)
wait = WebDriverWait(driver, 1)
if EC.alert_is_present()(driver):
    EC.alert_is_present()(driver).accept()

    
elemLogName = wait.until(EC.presence_of_element_located((By.XPATH,'//input[@name="username"]')))
elemLogName.send_keys("rkms")
elemPwd = wait.until(EC.presence_of_element_located((By.XPATH,'//input[@name="password"]')))
elemPwd.send_keys("2Password!")
elemPwd.send_keys(Keys.ENTER)
accountname = "testaccount1"
beginstr="-----BEGIN CERTIFICATE-----"
endstr="-----END CERTIFICATE-----"
centerstr="asdfghjkl"
senstivecontent = beginstr+centerstr+endstr
hostname="127.0.0.1"
testkey="TestPPK"


alerttext=""
def find_elem(elem_xpath):
    return wait.until(EC.presence_of_element_located((By.XPATH, elem_xpath)))

char1list=[] 
with open('randnormalletter.txt','r') as f:
    # 讀取一般字元應用程式名稱測試
    for line in f.readlines():
        char1list.append(line)

for line in char1list:
    try:
        elem_sysmange = find_elem('//*[@id="side-menu"]/li[4]/a')
        ActionChains(driver).move_to_element(elem_sysmange).perform()
        elem_sysmange.click()

        elem_app = find_elem('//*[@id="side-menu"]/li[4]/ul/li[3]')
        ActionChains(driver).move_to_element(elem_app).perform()
        elem_app.click()
        

        elem_create = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/center/button[1]')
        ActionChains(driver).move_to_element(elem_create).perform()
        elem_create.click()

        elem_input_appname = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/div[1]/div/input')
        elem_input_appname.send_keys(line)

        elem_input_account = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/div[3]/div/input')
        elem_input_account.send_keys(accountname)

        elem_input_sensitive = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/div[5]/div/textarea')
        elem_input_sensitive.send_keys(senstivecontent)

        elem_input_host = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/div[7]/div/input')
        elem_input_host.send_keys(hostname)
        
        elem_input_key = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/div[9]/div/input')
        elem_input_key.send_keys(testkey)

        elem_submit = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/div[11]/div/button[2]')
        elem_submit.click()


        # elem_radio = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/div/table/tbody/tr[15]/td[1]/input')
        # elem_radio.click()

        
        # elem_submit = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/div[11]/div/button[2]')
        # elem_submit.click()
        if EC.alert_is_present()(driver):
            alerttext= driver.switch_to.alert.text
            alerttext = alerttext.strip()
            if alerttext =='app create success':
                f = open('alert.txt','a')
                f.write(alerttext)
                f.write("\n")
                f.close()

                EC.alert_is_present()(driver).accept()

                elem_radio = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/div/table/tbody/tr[16]/td[1]/input')
                elem_radio.send_keys(Keys.SPACE)

        
                elem_delete = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/center/button[3]')
                elem_delete.click()

                elem_delete_commit =find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/div[7]/div/button')
                elem_delete_commit.click()

                if EC.alert_is_present()(driver):
                    EC.alert_is_present()(driver).accept()
                    
                continue

            else:
                f = open('alert2fail.txt','a')
                f.write(alerttext)
                f.write("\n")
                f.close()
                EC.alert_is_present()(driver).accept()
                # elem_logout = find_elem('//*[@id="page-wrapper"]/div[1]/nav/ul/li[2]/a')
                # elem_logout.click()
                continue
    except:
        raise

    finally:
        with open('final.txt','a') as f:
            f.write(alerttext)
            f.write('\n')

elem_logout = find_elem('//*[@id="page-wrapper"]/div[1]/nav/ul/li[2]/a')
elem_logout.click() 
driver.close()