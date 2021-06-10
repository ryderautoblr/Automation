import sys
sys.path.insert(1,"../pathInit/")
import pathInit
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import urllib.request
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class chromeDriver():
    def __init__(self):
        self.driver = webdriver.Chrome(pathInit.getBaseFolder() + 'webUtils\\chromedriver91.exe')  

    def getSoup(self,link,waitID=None):
        self.driver.get(link)
        if waitID is None: time.sleep(5)
        else: 
            element_present = EC.presence_of_element_located((By.ID, waitID))
            WebDriverWait(self.driver, 5).until(element_present)
        raw_html = self.driver.page_source
        soup = BeautifulSoup(raw_html, 'html.parser')
        return soup

    def close(self):
        self.driver.quit()

class download():
    def __init__(self):
        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','whatever')]
        urllib.request.install_opener(opener)

    def downloadImage(self,imageLink,imageName):
        retryAttempt = 5
        for attempt in range(retryAttempt):
            try:
                urllib.request.urlretrieve(imageLink, "Pictures/" + imageName)
            except:
                print ("Error! Downloading Image: addres: " + imageLink, "Name: ", imageName)
                print ("Trying: ",attempt+2)
                continue
            break 
