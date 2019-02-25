import os, time
import psutil
import random
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import csv
from bs4 import BeautifulSoup
import logging

logging.basicConfig(filename='example.log', level=logging.DEBUG)
logger = logging.getLogger('myapp')
hdlr = logging.FileHandler('myapp.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)

capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"


def scrollDown(driver, value):
    driver.execute_script("window.scrollBy(0," + str(value) + ")")


def chrome_open(driver, keyword, url):
    logger.info("0")
    print("0")
    driver.set_window_size(1200, 1000)
    logger.info("1")
    print("1")
    try:
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30)
        driver.get(url)
        # time.sleep(1)
    except Exception as e:
        logger.info("Loading timed out. Killing browser.\n %s " % url)
        print("Loading timed out. Killing browser.\n %s " % url)
        logger.info(e)
        print(e)
        driver.delete_all_cookies()
        print("deleted all cookies of driver")
        driver.close()
        return None

    logger.info("2")
    print("2")

    while True:
        try:
            all_iframes = driver.find_elements_by_tag_name("iframe")
            if all_iframes is None:
                print("all_iframe is None")
            if len(all_iframes) > 0:
                print("Ad Found\n")
                driver.execute_script("""
                    var elems = document.getElementsByTagName("iframe"); 
                    for(var i = 0, max = elems.length; i < max; i++)
                         {
                             elems[i].hidden=true;
                         }
                                      """)
                print('Total Ads: ' + str(len(all_iframes)))
            else:
                print('No frames found')
            wait = WebDriverWait(driver, 15)
            wait.until(EC.presence_of_element_located((By.ID, 'owner-name')))
            break
        except Exception as e:
            logger.info("ID=owner-name loading timed out. Killing browser.\n %s " % url)
            print("ID=owner-name loading timed out. Killing browser.\n %s " % url)
            logger.info(e)
            print(e)
            driver.close()
            return None
    logger.info("3")
    print("3")
    res = 0
    scroll_count = 0

    while True:
        try:
            driver.set_script_timeout(30)
            scrollDown(driver, 500)
            # time.sleep(1)
        except Exception as e:
            logger.info("Scrolling timed out. Killing browser.\n %s " % url)
            print("Scrolling timed out. Killing browser.\n %s " % url)
            logger.info(e)
            print(e)
            driver.close()
            return None

        scroll_count = scroll_count + 1
        logger.info("Scrolling Number : " + str(scroll_count))
        print("Scrolling Number : " + str(scroll_count))

        new_page = driver.page_source
        soup1 = BeautifulSoup(new_page, 'html.parser')
        spans = soup1.find_all("yt-formatted-string", class_="style-scope ytd-comment-renderer", id="content-text")
        inx = 0
        for span in spans:
            inx = inx + 1
            if inx > 20:
                return 0
            if keyword in span.text:
                res = inx
                return res

        if inx > 20:
            break

    return res


def create_driver(capa):
    driver = webdriver.Chrome(desired_capabilities=capa)
    return driver


import datetime

if __name__ == '__main__':
    logger.info("----------new start---------")
    urls = []
    keyword = ""
    with open('keyword.txt', 'r') as f:
        keyword = f.read()
    with open('url-list.txt', 'r') as f:
        x = f.read()

    urls = x.split("\n")

    fw = open('result.csv', 'w')
    fw.write('')
    fw.close()
    index = 0
    driver = create_driver(capa)
    for url in urls:
        index = index + 1
        if "http" in url:
            t1 = datetime.datetime.now()
            while True:
                a = psutil.virtual_memory()
                used_ram_size = a.used / 1024 / 1024
                logger.info("RAM used : %s MB" % used_ram_size)
                print("RAM used : %s MB" % used_ram_size)
                if used_ram_size > 6930:
                    driver.close()
                    logger.info("RAM size over 930 MB, recreated")
                    print("RAM size over 930 MB, recreated")
                    time.sleep(5)
                    driver = create_driver(capa)
                res = chrome_open(driver, keyword, url)
                if res is None:
                    rnd = random.randint(5, 20)
                    logger.info("random seconds: %s" % rnd)
                    print("random seconds: %s" % rnd)
                    time.sleep(rnd)
                    driver = create_driver(capa)
                else:
                    break

            logger.info(str(index) + " th: " + str(res) + "--------------")
            print(str(index) + " th: " + str(res) + "--------------")
            with open('result.csv', 'a', newline='\n') as csvfile:
                csv_writer = csv.writer(csvfile, delimiter='\t', quoting=csv.QUOTE_NONE)
                csv_writer.writerow([url, res])
            t2 = datetime.datetime.now()
            delta = t2 - t1
            logger.info("elapsed time : %s" % delta)
            print("elapsed time : %s" % delta)
        if index % 100 == 0:
            logger.info("-------100th , recreate driver------")
            print("-------100th , recreate driver------")
            driver.close()
            time.sleep(5)
            driver = create_driver(capa)
    driver.close()
