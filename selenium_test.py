#! python
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from test1.testt import AES_test
import time

driver = webdriver.Chrome("./chromedriver_win32/chromedriver.exe") #開啟Chrome
driver.get("https://cryptii.com/pipes/aes-encryption")
count = 0

for i in range(2):
    hex_string ="0aac999f50088c8f59cde5781c787ae6"
    hex_key=    "D66A048AF9066E68C78BE48D6800267D88B2CD2049E442C5E743E5D2465513CC"
    iv="00000000000000000000000000000000"
    count += 1
    origin_input ="asdfghjkl"

    prpcrpto= AES_test(hex_string,hex_key)
    prpcrpto_text=prpcrpto.aes_decrypt()

    
    try:
        # driver.get("https://cryptii.com/pipes/aes-encryption") #前往這個網址
        wait = WebDriverWait(driver, 1)
        elem_bytes = wait.until(EC.element_to_be_clickable((By.XPATH,'/html/body/div/article/div/div[1]/div[1]/div/header/button[1]')))
        elem_bytes.click()
        #elem_bytes = driver.find_element_by_xpath("/html/body/div/article/div/div[1]/div[1]/div/header/button[1]").click()
        
        time.sleep(1)
        change_to_text = driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/div/div/ul/li/ul/li[1]/button").click()
        #time.sleep(1)
        s1 = Select(driver.find_element_by_id('u3'))
        s1.select_by_value("1")

        elem_u6 = driver.find_element_by_id("u6")
        elem_u6.clear()
        elem_u6.send_keys(hex_key)
        elem_u7 = driver.find_element_by_id("u7")
        elem_u7.clear()
        elem_u7.send_keys(iv)
        elem_textarea_hexstring = driver.find_element_by_xpath("/html/body/div/article/div/div[1]/div[3]/div/div[2]/textarea")
        elem_textarea_hexstring.clear()
        elem_textarea_hexstring.send_keys(hex_string)

        elem_textarea_oringin_input =driver.find_element_by_xpath("/html/body/div[1]/article/div/div[1]/div[1]/div/div[2]/textarea").get_attribute("value")

      
        driver.refresh()

        with open("web_result.txt","a") as f:
            formattext ="Test item : "+ "account \n"+"result : " + str(count) + "\n" + "oringin input :  " + origin_input +"\n"+ "aes-encryption" + " : " + elem_textarea_oringin_input + "\n"
            f.write(formattext)
            countstring = str(count) + "\n"
            f.write(countstring)
        print("finished!!!!!!")
    except:
        raise
        print("")

    finally:
        print(count)

driver.close()