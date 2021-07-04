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

def waitForVegaPageToLoad(element):
    px = (0,0,0)
    while px == (0,0,0):
        im = pyautogui.screenshot()
        px = im.getpixel((element.location['x'],element.location['y']))
        # print (px)
    
def scrollToElement(driver,element):
    driver.execute_script("return arguments[0].scrollIntoView(true);", element)
    time.sleep(3)

def hoverElement(driver,element):
    hover = ActionChains(driver).move_to_element(element)
    hover.perform()
    '''
    print (element.location_once_scrolled_into_view['x'],element.location_once_scrolled_into_view['y'])
    pyautogui.moveTo(element.location_once_scrolled_into_view['x'],element.location_once_scrolled_into_view['y'])
    '''
    time.sleep(3)

websiteHome = "https://vegaauto.com/"
chromeObj = chromeUtils.chromeDriver()
driver = chromeObj.driver
driver.maximize_window()

'''
driver.get(websiteHome)

dropdownElements = driver.find_elements_by_class_name("menu-item")
categoryLinks = []
for e in dropdownElements:
    if "About Us" in e.text: break
    if "Corporate" in e.text: continue
    aTag = e.find_element_by_tag_name('a')
    categoryLinks.append(aTag.get_attribute('href'))
    print (aTag.get_attribute('href'))

subCategoryLinks = []
for link in categoryLinks:
    driver.get(link)

    waitE = WebDriverWait(driver, waitTimeForLoad).until(EC.presence_of_element_located((By.CLASS_NAME,'parent__category-list')))
    waitForVegaPageToLoad(waitE)
    subCategoryEs = driver.find_elements_by_class_name("parent__category-item")
    for e in subCategoryEs:
        subCategoryLinks.append(e.get_attribute('href'))
        

pageLinks = []
for c in subCategoryLinks:
    isMissing = True
    searchLink = c
    pagesDict = dict()
    while isMissing:
        driver.get(searchLink)
        waitE = WebDriverWait(driver, waitTimeForLoad).until(EC.presence_of_element_located((By.CLASS_NAME,'parent__category-list')))
        waitForVegaPageToLoad(waitE)
        pageLinks.append(searchLink)
        try:
            pageElement = driver.find_element_by_class_name("woocommerce-pagination")
        except NoSuchElementException:
            isMissing = False
            continue
        aTags = pageElement.find_elements_by_tag_name('a')

        for a in aTags:
            if a.text.isdigit():
                link = a.get_attribute('href')
                pagesDict[int(a.text)] = link
                if link not in pageLinks: pageLinks.append(link)
                print (link)

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
    waitE = WebDriverWait(driver, waitTimeForLoad).until(EC.presence_of_element_located((By.CLASS_NAME,'woocommerce-loop-product__link')))
    waitForVegaPageToLoad(waitE)
        
    productElements = driver.find_elements_by_class_name("woocommerce-loop-product__link")
    for pE in productElements:
        aTag = pE
        link = aTag.get_attribute('href')
        if link not in productLinks:
            productLinks.append(link)
            print (link)
print (len(productLinks))

f = open("vegaProductLinks","wb")
pickle.dump(productLinks,f)
f.close()

'''

dbfile = open('vegaProductLinks', 'rb')     
productLinks = pickle.load(dbfile)
dbfile.close()

# productLinks = ["https://vegaauto.com/product/off-road-dv-gangster-black-red-helmet/"]
productData = dict()
for i,link in enumerate(productLinks):
    if i%10==0:
        print (i)
        f = open("vegaDataObj","wb")
        pickle.dump(productData,f)
        f.close()

    driver.get(link)
    waitE = WebDriverWait(driver, waitTimeForLoad).until(EC.presence_of_element_located((By.CLASS_NAME,'product_title')))
    waitForVegaPageToLoad(waitE)
    productData[link] = dict()

    #get hierarchy
    e = driver.find_element_by_class_name('woocommerce-breadcrumb')
    productData[link]["hierarchy"] = e.text
    # print ("hierarchy",e.text)

    #get name
    e = driver.find_element_by_class_name('product_title')
    productData[link]["name"] = e.text
    # print ("name",e.text)
    
    #mrp
    mrpE = driver.find_element_by_class_name('woocommerce-Price-amount')
    mrp = mrpE.text
    # mrp = re.findall(r'\d+\.\d+', mrp)[0]
    productData[link]['mrp'] = mrp
    # print (mrp)

    
    #description
    productData[link]['desc'] = []
    try:
        e = driver.find_element_by_class_name('woocommerce-product-details__short-description')

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
    # print ("desc",productData[link]['desc'])


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
        
f = open("vegaDataObj","wb")
pickle.dump(productData,f)
f.close()

driver.quit()
exit()

