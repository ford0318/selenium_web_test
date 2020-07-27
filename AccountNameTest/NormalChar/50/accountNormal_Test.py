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

# accountname = "testaccount1"
appname = 0
beginstr="-----BEGIN CERTIFICATE-----"
endstr="-----END CERTIFICATE-----"
centerstr="asdfghjkl"
senstive_content = beginstr+centerstr+endstr
hostname="127.0.0.1"
testkey="TestPPK"

driver = webdriver.Chrome("../../../chromedriver_win32/chromedriver.exe") #開啟Chrome
driver.get("http://192.168.100.193:8000/")
action = ActionChains(driver)
wait = WebDriverWait(driver, 1)

def find_elem(elem_xpath):
    return wait.until(EC.presence_of_element_located((By.XPATH, elem_xpath)))

state_count = True
def login_flow():
   
    if EC.alert_is_present()(driver):
        alerttext = driver.switch_to.alert.text
        alerttext = alerttext.strip()
        if alerttext == 'Connection timeout, Please login again':
            with open('LoginError.txt','a') as f:
                f.write(alerttext)
            EC.alert_is_present()(driver).accept()
        # The account was login
    elemLogName = wait.until(EC.presence_of_element_located((By.XPATH,'//input[@name="username"]')))
    elemLogName.send_keys("rkms")
    elemPwd = wait.until(EC.presence_of_element_located((By.XPATH,'//input[@name="password"]')))
    elemPwd.send_keys("2Password!")
    elemPwd.send_keys(Keys.ENTER)

    if EC.alert_is_present()(driver):
        alerttext = driver.switch_to.alert.text
        alerttext = alerttext.strip()
        if alerttext =='The account was login':
            with open('LoginError.txt','a') as f:
                f.write(alerttext)
            EC.alert_is_present()(driver).accept()
        driver.close()
        state_count = False
    


def web_flow():
        elem_sysmange = find_elem('//*[@id="side-menu"]/li[4]/a')
        ActionChains(driver).move_to_element(elem_sysmange).click(elem_sysmange).perform()

        elem_app = find_elem('//*[@id="side-menu"]/li[4]/ul/li[3]/a')
        ActionChains(driver).move_to_element(elem_app).click(elem_app).perform()
        # elem_app.click()

        elem_create = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/center/button[1]')
        ActionChains(driver).move_to_element(elem_create).click(elem_create).perform()
        # elem_create.click()

def data_input_submit(appname,accountname,senstivecontent):
    # 輸入應用程式名稱
        elem_input_appname = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/div[1]/div/input')
        elem_input_appname.send_keys(appname)
        # 輸入帳號   
        elem_input_account = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/div[3]/div/input')
        elem_input_account.send_keys(accountname)
        # 輸入機敏   
        elem_input_sensitive = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/div[5]/div/textarea')
        elem_input_sensitive.send_keys(senstivecontent)
        # 輸入server ip/host name 
        elem_input_host = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/div[7]/div/input')
        elem_input_host.send_keys(hostname)
        # 輸入金鑰名稱
        elem_input_key = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/div[9]/div/input')
        elem_input_key.send_keys(testkey)
        # 確定
        elem_submit = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/div[13]/div/button[2]')
        ActionChains(driver).move_to_element(elem_submit).click(elem_submit).perform()
try:
    login_flow()
except Exception as e:
    with open('ExceptionLogin.txt','a') as f:
        except_message = str(e)
        f.write(except_message)

char1list=[] 
success_counts = 0
failure_count = 0
loops_count = 0
result='Error'
with open('randnormalletter.txt','r') as f:
    # 讀取一般字元應用程式名稱測試
    for line in f.readlines():
        char1list.append(line)

for account_name in char1list:
    loops_count+=1
    loops_str = str(loops_count)
    appname+=1
    app_name = str(appname)
    try:
        web_flow()
        data_input_submit(app_name,account_name,senstive_content)

        # elem_radio = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/div/table/tbody/tr[15]/td[1]/input')
        # elem_radio.click()

        
        # elem_submit = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/div[11]/div/button[2]')
        # elem_submit.click()
        if EC.alert_is_present()(driver):
            alerttext= driver.switch_to.alert.text
            alerttext = alerttext.strip()
            if alerttext =='app create success':
                result = "*********   PASS   *********"
                success_counts+=1
                with open('success.txt','a') as f:
                    f.write('ID: ')
                    f.write(loops_str)
                    f.write('\n')
                    f.write('ORIGIN INPUT: ')
                    f.write('\n')
                    f.write(account_name)
                    f.write("=========================================")
                    f.write('\n')



                EC.alert_is_present()(driver).accept()

                elem_radio = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/div/table/tbody/tr/td[1]/input')
                elem_radio.send_keys(Keys.SPACE)

        
                elem_delete = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/center/button[3]')
                elem_delete.click()

                elem_delete_commit =find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/div[7]/div/button')
                elem_delete_commit.click()

                if EC.alert_is_present()(driver):
                    EC.alert_is_present()(driver).accept()
                    
                continue

            else:
                result = '*********   Error   *********'
                with open('UnexpectedError.txt','a') as f:
                    failure_counts+=1
                    count_failure = str(failure_counts)
                    f.write('Failure counts: ')
                    f.write(count_failure)
                    f.write('\n')
                    f.write('ID : ')
                    f.write(loops_str)
                    f.write('\n')
                    f.write('Alert Message : ')
                    f.write(alerttext)
                    f.write("\n")
                    f.write('ORIGIN INPUT : ')
                    f.write(account_name)
                    f.write('\n')
                    f.write("====================================")
                    f.write("\n")

                EC.alert_is_present()(driver).accept()
                continue
    except:
        raise

    finally:
        with open('Report.txt','a') as f:
            f.write('ID: ')
            f.write(loops_str)
            f.write('\n')
            f.write('ORIGIN INPUT: ')
            f.write('\n')
            f.write(account_name)
            f.write('Result : ')
            f.write(result)
            f.write('\n')
            f.write("=========================================")
            f.write('\n')

elem_logout = find_elem('//*[@id="page-wrapper"]/div[1]/nav/ul/li[2]/a')
elem_logout.click() 
driver.close()