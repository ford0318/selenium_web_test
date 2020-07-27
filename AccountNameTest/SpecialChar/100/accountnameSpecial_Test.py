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
senstivecontent = beginstr+centerstr+endstr
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

def data_input_submit(line,accountname,senstivecontent):
    # 輸入應用程式名稱
        elem_input_appname = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/div[1]/div/input')
        elem_input_appname.send_keys(line)
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
    

test_result =""
char1list=[] 
unexp_success_count=0
unexp_fail_count=0
id_count=0
failure_count=0
if state_count:
    with open('randspecialletter.txt','r') as f:
        for line in f.readlines():
            char1list.append(line)


    loop_count = 0
    for line in char1list:
        appname+=1
        app_name = str(appname)
        loop_count+=1
        accountname = line.strip()
        try:
            # 進入輸入頁面
            web_flow()
            # 輸入資料
            data_input_submit(app_name,accountname,senstivecontent)

            # 處理跳窗 & 重新輸入
            if EC.alert_is_present()(driver):
                alerttext= driver.switch_to.alert.text
                alerttext = alerttext.strip()
                with open('string.txt','a') as f:
                    f.write("enter input page\n")
                    f.write(alerttext)
                    f.write('\n=====================\n')

                punclist_len = len([i for i in line if i in string.punctuation and i not in ['-','_','(',')','[',']','.']])
                
                puc = str(punclist_len)
                with open('punclist_len.txt','a') as f:
                    f.write('LENGTH : ')
                    f.write(puc)
                    f.write('\n')
                    f.write('line :')
                    f.write(line)
                    f.write('\n')

                if alerttext == "app create success":
                    # 有特殊文字卻通過
                    # ABNORMAL CASE
                    if punclist_len > 0:
                        failure_count+=1
                        test_result = "*********   FAIL abnormal accept  *********"
                        with open("UnexpectedSuccess.txt","a") as f:
                                unexp_success_count+=1
                                strunexp_success_count = str(unexp_success_count)
                                unexpectedsuccess = 'Unexpected success acc.Count: ' + strunexp_success_count +'\n' +f'ERROR STRING: {line}'
                                f.write(unexpectedsuccess)
                                f.write("\n")
                                f.write("Input string is : ")
                                f.write(line)
                                f.write("\n================================================================================\n")
                        
                        EC.alert_is_present()(driver).accept()

                        elem_radio = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/div/table/tbody/tr[1]/td[1]/input')
                        elem_radio.send_keys(Keys.SPACE)
                        elem_delete = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/center/button[3]')
                        elem_delete.click()

                        elem_delete_commit =find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/div[7]/div/button')
                        elem_delete_commit.click()

                        if EC.alert_is_present()(driver):
                            EC.alert_is_present()(driver).accept()

                    else:
                        # NORMAL CASE
                        #choose radios
                        EC.alert_is_present()(driver).accept()
                        elem_radio = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/div/table/tbody/tr[1]/td[1]/input')
                        elem_radio.send_keys(Keys.SPACE)
                        elem_delete = find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/center/button[3]')
                        ActionChains(driver).move_to_element(elem_delete).click(elem_delete).perform()
                        elem_delete_commit =find_elem('//*[@id="page-wrapper"]/div[3]/div/div/div/div[2]/form/div[7]/div/button')
                        ActionChains(driver).move_to_element(elem_delete_commit).click(elem_delete_commit).perform()

                        if EC.alert_is_present()(driver):
                            EC.alert_is_present()(driver).accept()

                        test_result = "*********   PASS accept specific character   *********"
                        
                # alert 擋下
                else:
                    # punclist_len = len([i for i in line if i in string.punctuation])
                    if punclist_len > 0:
                        # 有特殊文字擋下
                        # NORMAL CASE  
                        EC.alert_is_present()(driver).accept()
                        test_result = "*********   PASS reject punctuation   *********"
                        
                    else:
                        #沒有符號不能通過
                        # Exist In DB - NORMAL CASE
                        doc_list =[x for x in collection.find({},{ "name": line })]
                        if len(doc_list) > 0:
                            EC.alert_is_present()(driver).accept()
                            test_result = "*********   PASS  without punctuation  *********"
                        else:
                        #沒有符號不能通過
                            # Not Exitst In DB - ABNORMAL CASE
                            failure_count+=1
                            test_result = "*********   FAIL  without punctuation *********"
                            with open("UnexpectedFail.txt","a") as f:
                                unexp_fail_count+=1
                                strunexp_fail_count = str(unexp_fail_count)
                                unexpectedfail = 'This is unexpected fail :'+'\n'+'acc.Count: ' + strunexp_fail_count +'\n' +f'THE ERROR STRING: {line}'
                                f.write(unexpectedfail)
                                f.write('\n')
                                item = str(doc_list[0])
                                f.write(item)
                                f.write("\n================================================================================\n")
                            EC.alert_is_present()(driver).accept()

        except Exception as e:
            with open('Exception.txt','a') as f:
                except_message = str(e)
                f.write(except_message)

        finally:
            id_count+=1
            id_str = str(id_count)
            with open("Result.txt",'a') as f:
                punctuation_count = len([i for i in line if i in string.punctuation])
                line_len = len(line)
                normalchar_len = line_len - punctuation_count
                f.write("ID : ")
                f.write(id_str)
                f.write("\n")
                f.write("Special Char Test Case : Total length -  ")
                line_len_str = str(line_len)
                f.write(line_len_str)
                f.write("\n")

                f.write("Normal char len :                        ")
                normalchar_len_str = str(normalchar_len)
                f.write(normalchar_len_str)
                f.write("\n")

                f.write("Special char len :                       ")
                punctuation_count_str = str(punctuation_count)
                f.write(punctuation_count_str)
                f.write("\n")

                punctuationsetlist = list(set([i for i in line if i in string.punctuation]))
                str_punctuationsetlist = str(punctuationsetlist)

                f.write("Special char inside :   ")
                f.write(str_punctuationsetlist)
                f.write("\n\n")
                f.write("ORIGIN INPUT :  ")
                f.write(line)
                f.write("\n")
                f.write("Result:\n")
                f.write(test_result)
                f.write("\n========================================================\n")

    with open('UnexpectedSuccess.txt','a') as f:
        str_loop = str(loop_count)
        f.write('Total loops : ')
        f.write(str_loop)
        f.write('\n')
        f.write("Failure counts: \n")
        count_failure = str(failure_count)
        f.write(count_failure)
    elem_logout = find_elem('//*[@id="page-wrapper"]/div[1]/nav/ul/li[2]/a')
    elem_logout.click() 
    driver.close()