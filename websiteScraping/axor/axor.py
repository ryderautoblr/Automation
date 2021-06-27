import sys
sys.path.insert(1,"../../pathInit/")
import pathInit
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException


import chromeUtils
import time
import pickle

waitTimeForLoad = 10

def waitForStuddsPageToLoad(driver):
    try:
        myElem = WebDriverWait(driver, waitTimeForLoad).until(EC.presence_of_element_located((By.CLASS_NAME,'main-logo-red')))
        print ("Page is ready!")
    except TimeoutException:
        print ("Loading took too much time!")


websiteHome = "https://www.axorhelmets.com/index.php"
chromeObj = chromeUtils.chromeDriver()
driver = chromeObj.driver
driver.maximize_window()


driver.get(websiteHome)

dropdownElements = driver.find_elements_by_class_name("dropdown")
categoryElements = []
for e in dropdownElements:
    if "HELMETS" in e.text:
        categoryElements.append(e)
    if "RIDING" in e.text:
        categoryElements.append(e)

categoryLinks = []
for e in categoryElements:
    aTags = e.find_elements_by_tag_name('a')
    for a in aTags:
        categoryLinks.append(a.get_attribute('href'))

pageLinks = []
for c in categoryLinks:
    driver.get(c)
    pageLinks.append(c)
    try:
        pageElement = driver.find_element_by_class_name("pagination")
    except NoSuchElementException:
        continue
    aTags = pageElement.find_elements_by_tag_name('a')
    for a in aTags:
        if a.text.isdigit():
            pageLinks.append(a.get_attribute('href'))

productLinks = []
for p in pageLinks:
    driver.get(p)
    time.sleep(1)
    productElements = driver.find_elements_by_class_name("image")
    for pE in productElements:
        aTag = pE.find_element_by_tag_name('a')
        link = aTag.get_attribute('href')
        if link not in productLinks:
            productLinks.append(link)
print (len(productLinks))


# productLinks = ["https://www.axorhelmets.com/index.php?route=product/product&path=20_84&product_id=314"]
productData = dict()
for link in productLinks:
    driver.get(link)
    productData[link] = dict()

    #get name
    e = driver.find_element_by_id('pname')
    productData[link]["name"] = e.text
    # print ("name",e.text)

    #model colour
    e = driver.find_element_by_id('model-color')
    productData[link]["color"] = e.text
    # print ("color",e.text)    
    
    #mrp
    mrpEs = driver.find_elements_by_class_name('list-unstyled')
    rsE = None
    for mrpE in mrpEs:
        if "Rs" in mrpE.text:
            rsE = mrpE
            productData[link]['mrp'] = mrpE.text
            # print (mrpE.text)

    #description
    parentE = rsE.find_element_by_xpath("..")
    spanE = parentE.find_elements_by_tag_name("span")[1]
    productData[link]['desc'] = spanE.text
    # print (spanE.text)

    #Size
    sizeDiv = driver.find_element_by_class_name('form-group')
    radioEs = sizeDiv.find_elements_by_class_name('radio')
    productData[link]['size'] = []
    for radio in radioEs:
        if radio.text.strip():
            # print (radio.text.strip())
            productData[link]['size'].append(radio.text.strip())

    #Images
    imageEs = driver.find_elements_by_class_name('thumbnail')
    productData[link]['imageLinks'] = []
    for imageE in imageEs:
        imageLink = imageE.get_attribute("href")
        if imageLink not in productData[link]['imageLinks']: productData[link]['imageLinks'].append(imageLink)
        # print (imageLink)

        
f = open("axorDataObj","wb")
pickle.dump(productData,f)
f.close()

driver.quit()
exit()
