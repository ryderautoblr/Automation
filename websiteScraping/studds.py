import sys
sys.path.insert(1,"../pathInit/")
import pathInit
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

import chromeUtils
import time
import pickle

waitTimeForLoad = 10

def scrollToElement(driver,element):
    driver.execute_script("return arguments[0].scrollIntoView(true);", element)
    
def waitForStuddsPageToLoad(driver):
    try:
        myElem = WebDriverWait(driver, waitTimeForLoad).until(EC.presence_of_element_located((By.CLASS_NAME,'main-logo-red')))
        print ("Page is ready!")
    except TimeoutException:
        print ("Loading took too much time!")


websiteHome = "https://www.studds.com/"
chromeObj = chromeUtils.chromeDriver()
driver = chromeObj.driver
driver.maximize_window()

driver.get(websiteHome)
productsElement = driver.find_element_by_xpath("//*[contains(text(), 'PRODUCTS')]")
productsElement.click()
categoryElements = driver.find_elements_by_class_name("category-s")
categoryLinks = []
for e in categoryElements:
    categoryLinks.append(e.get_attribute("href"))
    
subCategoryLinks = []
for categoryLink in categoryLinks:
    driver.get(categoryLink)
    e = WebDriverWait(driver, waitTimeForLoad).until(EC.presence_of_element_located((By.CLASS_NAME,"cat-single")))
    if e is None:
        print ("Not Found Category",categoryLink)
        continue
    es = driver.find_elements_by_class_name("cat-single")
    for e in es:
        subCategoryLinks.append(e.get_attribute("href"))

productLinks = []
for subCategoryLink in subCategoryLinks:
    driver.get(subCategoryLink)
    e = WebDriverWait(driver, waitTimeForLoad).until(EC.presence_of_element_located((By.CLASS_NAME,"cat-single")))
    if e is None:
        print ("Not Found Category",subCategoryLink)
        continue
    es = driver.find_elements_by_class_name("cat-single")
    lastFoundElement = None
    lastFoundIndex = -1
    while(lastFoundIndex != (len(es)-1)):
        for i,e in enumerate(es):
            if e.text:
                if e.get_attribute("href") not in productLinks:
                    productLinks.append(e.get_attribute("href"))
                lastFoundElement = e
                lastFoundIndex = i

        scrollToElement(driver,lastFoundElement)

print (len(productLinks))


'''
####################################################
# Get Product Links From Database
####################################################

dbfile = open('studdsDataObj', 'rb')     
db = pickle.load(dbfile)
dbfile.close()

productLinks = []
for key in db.keys():
    productLinks.append(db[key]["link"])


####################################################
'''
productData = dict()
# productLinks = ["https://www.studds.com/motorcycle-accessory/mobike-side-luggage/cruiser-box"]
# productLinks = ["https://www.studds.com/helmet/full-face-helmet/shifter-d1-decor"]
for productLink in productLinks:
    driver.get(productLink)



    #Product Name
    e = driver.find_element_by_class_name("sec-title")
    productTitle = e.text
    if productTitle in productData.keys():
        print (productTitle,productLink)



    productData[productTitle] = dict()

    #Category Link
    productData[productTitle]['link'] = productLink

    #Product price
    productPriceE = WebDriverWait(driver, waitTimeForLoad).until(EC.presence_of_element_located((By.CLASS_NAME,'product-price')))
    productData[productTitle]['mrp'] = productPriceE.text

    #get sub products
    es = driver.find_elements_by_class_name("prod-var-single")
    productData[productTitle]['products'] = []
    for e in es:
        hover = ActionChains(driver).move_to_element(e)
        hover.perform()
        productNameE = WebDriverWait(driver, waitTimeForLoad).until(EC.presence_of_element_located((By.CLASS_NAME,'prod-var-name')))
        time.sleep(0.1)
        imageE = e.find_element_by_tag_name("img")
        productData[productTitle]['products'].append((e.text,imageE.get_attribute("src")))    
    if not es:
        e = driver.find_element_by_class_name("main-helmet")
    

    #get product sizes
    es = driver.find_elements_by_class_name("size-desc")
    productData[productTitle]['sizes'] = []
    isPrev = False
    for e in es:
        sizeNameE = e.find_element_by_class_name("size-name")
        
        if isPrev:
            driver.find_element_by_xpath("//body").click()
            productSizeE = WebDriverWait(driver, waitTimeForLoad).until(EC.invisibility_of_element_located((By.CLASS_NAME,'product-size')))
            time.sleep(0.1)
        
        e.click()
        productSizeE = WebDriverWait(driver, waitTimeForLoad).until(EC.presence_of_element_located((By.CLASS_NAME,'product-size')))
        time.sleep(0.1)
        isPrev = True
        
        productSizeE = e.find_element_by_class_name("product-size")
        productData[productTitle]['sizes'].append((sizeNameE.text,productSizeE.text))
        
    #get descriptions
    es = driver.find_elements_by_class_name("det-title")

    productData[productTitle]['description'] = []
    for e in es:
        parentE = e.find_element_by_xpath('..')
        parentE = parentE.find_element_by_xpath('..')
        scrollToElement(driver,parentE)
        parentE.click()
        productData[productTitle]['description'].append(parentE.text.split("\n"))

    print (productData[productTitle])
        
f = open("studdsDataObj","wb")
pickle.dump(productData,f)
f.close()

driver.quit()
exit()
