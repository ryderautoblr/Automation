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
import pyautogui
import re

waitTimeForLoad = 10
    
def scrollToElement(driver,element):
    driver.execute_script("return arguments[0].scrollIntoView(true);", element)
    time.sleep(3)

def hoverElement(driver,element):
    hover = ActionChains(driver).move_to_element(element)
    hover.perform()

def getPageNoFromLink(link):
    paths = link.split("/")
    if paths[-2].isdigit():
        return int(paths[-1])
    return 1


websiteHome = "https://ls2helmetsindia.com/"
chromeObj = chromeUtils.chromeDriver()
driver = chromeObj.driver
driver.maximize_window()

'''
driver.get(websiteHome)

e = driver.find_element_by_class_name("parent")
hoverElement(driver,e)
categoryLinks = []
aTags = e.find_elements_by_tag_name('a')
for a in aTags:
    categoryLinks.append(a.get_attribute('href'))

pageLinks = []
for c in categoryLinks:
    print(c)
    isMissing = True
    searchLink = c
    pagesDict = dict()
    while isMissing:
        driver.get(searchLink)
        if searchLink not in pageLinks: pageLinks.append(searchLink)
        try:
            pageElement = driver.find_element_by_class_name("paginator")
        except NoSuchElementException:
            isMissing = False
            continue
        aTags = pageElement.find_elements_by_tag_name('a')

        for a in aTags:
            link = a.get_attribute('href')
            pageNo = getPageNoFromLink(link)
            
            pagesDict[pageNo] = link
            if link not in pageLinks: pageLinks.append(link)
            # print (link)

        #get missing page -1 page
        isMissing = False
        pages = list(pagesDict.keys())
        pages.sort()
        for i in range(1,len(pages)):
            if pages[i] != (pages[i-1]+1):
                isMissing = True
                searchLink = pagesDict[pages[i-1]]
                break

productLinks = []
for p in pageLinks:
    driver.get(p)
        
    productElements = driver.find_elements_by_class_name("product-inner-wrap")
    for pE in productElements:
        aTag = pE.find_element_by_tag_name('a')
        link = aTag.get_attribute('href')
        if link not in productLinks:
            productLinks.append(link)
            # print (link)

    # break
print (len(productLinks))

f = open("ls2ProductLinks","wb")
pickle.dump(productLinks,f)
f.close()

'''

dbfile = open('ls2ProductLinks', 'rb')     
productLinks = pickle.load(dbfile)
dbfile.close()

productLinks = ["https://ls2helmetsindia.com/in/p/FF324-METRO-EVO-COMPLEX-MATT-BLACK-WHITE-BLUE-WITH-PEAK/467"]
productData = dict()
for i,link in enumerate(productLinks):
    if i%10==0:
        print (i)
        f = open("ls2DataObj","wb")
        pickle.dump(productData,f)
        f.close()

    driver.get(link)
    productData[link] = dict()

    #get name
    e = driver.find_element_by_class_name('name')
    productData[link]["name"] = e.text
    print ("name",e.text)
    
    #mrp
    mrpE = driver.find_element_by_class_name('main-price')
    mrp = mrpE.text
    productData[link]['mrp'] = mrp
    print (mrp)
 
    #description
    productData[link]['desc'] = []
    try:
        e = driver.find_element_by_id('box_description')
        print (e.text)
        continue

        productData[link]['desc'].append(('overview',e.text))

        es = driver.find_elements_by_class_name('product__features__item')
        for e in es:
            titleE = e.find_element_by_class_name('product__features__item-title')
            desc = e.get_attribute('data-original-title')
            # print (titleE.text,desc)
            productData[link]['desc'].append((titleE.text,desc))
    except:
        pass
    try:
        e = driver.find_element_by_class_name('product__description')
        productData[link]['desc'].append(('',e.text))
    except:
        pass
    print ("desc",productData[link]['desc'])

    continue
    

    #Size
    sizeEs = driver.find_elements_by_class_name('variable-item-span')
    productData[link]['size'] = []
    for e in sizeEs:
        productData[link]['size'].append(e.text)
        # print (e.text)


    #Images
    imageEs = driver.find_elements_by_class_name('swiper-slide')
    productData[link]['imageLinks'] = []
    for imageE in imageEs:
        imageTag = imageE.find_element_by_tag_name('img')
        imageLink = imageTag.get_attribute("src")
        if imageLink not in productData[link]['imageLinks']: productData[link]['imageLinks'].append(imageLink)
        # print (imageLink)
        
f = open("ls2DataObj","wb")
pickle.dump(productData,f)
f.close()

driver.quit()
exit()

