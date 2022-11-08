import time
from selenium import webdriver
from selenium.webdriver.common.by import By       #importing libraries
from selenium.webdriver.support.select import Select
from selenium.webdriver.remote.webdriver import NoSuchElementException
import os
from selenium.common.exceptions import WebDriverException
import logging


def districtDriver(slink):
    districtElements = getDistrict(slink)
    for dlink in districtElements:
            logging.info("   "+dlink.text)
            try: # using try block handling the Exception
                MakeDistrictFolder(slink.text, dlink.text) # this line call to create a folders
                blockDriver(slink,dlink)
            except FileExistsError: # handling FileExistsError
                blockDriver(slink,dlink)
               
def blockDriver(slink,dlink):
    blockElement = getBlock(dlink)
    for blink in blockElement:
        logging.info("      "+blink.text)
        try: # using try block handling the Exception
            MakeBlockFolder(slink.text, dlink.text, blink.text) # creating folders
            ExpentiturFun(slink, dlink, blink)
        except FileExistsError: # handling FileExistsError
            continue

# creating web driver
def driverFun(link):
    driver = webdriver.Chrome(executable_path='C:\chromed\chromedriver.exe') # get connection from Chrome using webdriver
    try:
        driver.get(link)
    except WebDriverException:
        driver.quit()
        driver = driverFun(link)
    return driver

# creating folders by defining functions
# using os command-(mkdir)
def MakeStateFolder(slink):
    os.mkdir('C:\\webScrape\\'+slink)

def MakeDistrictFolder(slink, dlink):
    os.mkdir('C:\\webScrape\\'+slink+'\\'+dlink)

def MakeBlockFolder(slink, dlink, blink):
    os.mkdir('C:\\webScrape\\'+slink+'\\'+dlink+'\\'+blink)


# taking webpage elements
# this will return the elements in list format
def getState(link):
    driver = driverFun(link)
    # Finding elements using Xpath
    # for-loop to get elements and stored in a list
    statesElement = [slink for slink in driver.find_elements(By.XPATH, '//*[@id="form1"]/div[3]/center/table/tbody/tr/td/a')] 
    return statesElement

def getDistrict(link):
    driver = driverFun(link.get_attribute('href'))
    districtElememnt = [dlink for dlink in driver.find_elements(By.XPATH, '//*[@id="gvdist"]/tbody/tr/td/a')]
    return districtElememnt

def getBlock(dlink):
    driver = driverFun(dlink.get_attribute('href'))
    blockElements = [blink for blink in driver.find_elements(By.XPATH, '//*[@id="gvdpc"]/tbody/tr/td/a')]
    return blockElements



# Downloading files one by one in a specific location
def ExpentiturFun(slink, dlink, blink):
    # Next four line is to make a driver connection and set a specific location
    op = webdriver.ChromeOptions()
    p = {'download.default_directory': 'C:\\webScrape\\' +slink.text+'\\'+dlink.text+'\\'+blink.text}
    op.add_experimental_option('prefs', p)
    driver = webdriver.Chrome(executable_path='C:\chromed\chromedriver.exe', options=op)
    Expentitureprocess(driver,slink,dlink,blink,1)

def Expentitureprocess(driver,slink,dlink,blink,no):
    link = blink.get_attribute('href')
    driver.get(link)
    try: # using try block handling the Exception
        expenditure = driver.find_element(By.LINK_TEXT, 'Amount Sanctioned/Expenditure On Works')
        driver.get(expenditure.get_attribute('href'))
        # selecting dropdown elements in a website
        dropdown = driver.find_element(By.XPATH, '/html/body/form/div[3]/center/table/tbody/tr[1]/td[4]/b/font/select')
        panchayat = Select(dropdown)
        list = panchayat.options
        count = 2
        for i in range(2,len(list)):
            driver.get(link)
            try: # using try block handling the Exception
                expenditure = driver.find_element(By.LINK_TEXT, 'Amount Sanctioned/Expenditure On Works')
                driver.get(expenditure.get_attribute('href'))
                dropdown = driver.find_element(By.XPATH, '/html/body/form/div[3]/center/table/tbody/tr[1]/td[4]/b/font/select')
                panchayats = Select(dropdown)
                panchayats.select_by_index(i)
                driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_Btnreport"]').click()
                driver.find_element(By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_LinkButton1"]').click()
                time.sleep(30)
                if(i == 2):
                    path1 = 'C:\\webScrape\\'+slink.text+'\\'+dlink.text+'\\'+blink.text+'\\Est_Expwork.xls'
                else:
                    m = i-count
                    path1 = 'C:\\webScrape\\'+slink.text+'\\'+dlink.text+'\\'+blink.text+'\\Est_Expwork ('+str(m)+').xls'
                if os.path.isfile(path1):
                    print(str(i)+" download completed")
                else:
                    logging.info("      "+"no :"+str(i)+"File download is not completed")
                    count +=1
                    print("not completed")
            except WebDriverException: # handling WebDriverException
                logging.error("      no : "+str(i)+" ==> panchayat. no data found")
    except NoSuchElementException:# handling NoSuchElementException
        if(no >=5):
            os.rmdir('C:\\webScrape\\'+slink.text+'\\'+dlink.text+'\\'+blink.text)
            logging.error("        the Expenditure link service is unavailable")
        else:
            no += 1
            Expentitureprocess(driver,slink,dlink,blink,no)


# this codes is a main function
logging.basicConfig(filename="log.txt", level=logging.INFO, filemode="w")
link = "https://nrega.nic.in/Netnrega/sthome.aspx"
# list variable 
stateElements = getState(link)
for slink in stateElements:
    try:
        logging.info(slink.text)
        MakeStateFolder(slink.text)
        districtDriver(slink)
    except FileExistsError:
        districtDriver(slink)
