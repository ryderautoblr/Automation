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

print (len(productLinks))
# productLinks = ["https://ls2helmetsindia.com/in/p/FF324-METRO-EVO-COMPLEX-MATT-BLACK-WHITE-BLUE-WITH-PEAK/467"]
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
        h2Tags = e.find_elements_by_tag_name('h2')
        for h2Tag in h2Tags:
            text = ''
            if h2Tag.text == "TECHNICAL SPECIFICATIONS ":
                divTag = h2Tag.find_element_by_xpath("./following-sibling::div")
                tdTags = divTag.find_elements_by_tag_name("td")
                for td in tdTags:
                    try:
                        hTag = td.find_element_by_tag_name("h4")
                        ulTag = td.find_element_by_tag_name("ul")
                        productData[link]['desc'].append((hTag.text,ulTag.text))
                    except:
                        pass
                continue
            title = h2Tag.text
            try:
                divTag = h2Tag.find_element_by_xpath("./following-sibling::div")
                pTag = divTag.find_element_by_tag_name("p")
                text = pTag.text
            except:
                try:
                    pTag = h2Tag.find_element_by_xpath("./following-sibling::p")
                    text = pTag.text
                except:
                    pass
            productData[link]['desc'].append((title,text))
    except:
        pass
    
    # print (productData[link]['desc'])

    #Images
    imageE = driver.find_element_by_class_name('productimg')
    imageEs = imageE.find_elements_by_tag_name('a')
    productData[link]['imageLinks'] = []
    for imageE in imageEs:
        imageLink = imageE.get_attribute("href")
        if imageLink not in productData[link]['imageLinks']: productData[link]['imageLinks'].append(imageLink)
        # print (imageLink)


print (len(productData.keys()))
f = open("ls2DataObj","wb")
pickle.dump(productData,f)
f.close()

driver.quit()
exit()

