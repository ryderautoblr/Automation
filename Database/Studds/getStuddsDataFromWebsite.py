# importing the libraries
import requests
import sys
sys.path.insert(1,"../../pathInit/")
import pathInit
from bs4 import BeautifulSoup
import re
import IPython
import pandas
import urllib.request
import os

base_url="https://www.studds.com/"

def getWebPage(url):
    html_content = requests.get(url).text
    print (html_content)
    soup = BeautifulSoup(html_content,"html.parser")
    return soup

def checkMissingPages(pageLinks):
    links = pageLinks[1:]
    pages = [1]
    for page in links:
        pageNo = page.split("/")[-1]
        if "searchquery" in page: pageNo = page.split("/")[-3]
        pages.append(int(pageNo))
    pages.sort()
    i = 1
    lastPage = -1
    while i < (len(pages)-1):
        if (pages[i] + 1) != pages[i+1]:
            lastPage = pages[i]
            return True,lastPage
        i += 1
    return False, None

def getPageLinksFromPage(link):
    pageLinks = []
    soup = getWebPage(base_url + link)
    pageTag = soup.find('div',class_='paginator')
    if pageTag is None: pageTag = soup.find('ul',class_='paginator')
    if pageTag is not None:
        for a in pageTag.find_all('a',href=True):
            link = a['href']
            if link not in pageLinks:
                pageLinks.append(link) 
    return pageLinks 
    
def getPageLinks(categoryLink):
    pageLinks = []
    pageLinks.append(categoryLink)
    isMissing = True
    link = categoryLink
    while isMissing:
        tempPageLinks = getPageLinksFromPage(link)
        for temp in tempPageLinks:
            if temp not in pageLinks:
                pageLinks.append(temp)    
        isMissing, lastPage = checkMissingPages(pageLinks)
        if isMissing: 
            link = categoryLink + "/" + str(lastPage)
            if "searchquery" in categoryLink: 
                words = categoryLink.split("/")
                link = "/".join(words[:-3]) +"/" + str(lastPage) + "/" + "/".join(words[-2:] )
    return pageLinks

def getProductsLinksFromPageLink(page):
    productLinks = []
    soup = getWebPage(base_url + page)
    productTags = soup.find_all('div',class_="product-inner-wrap")
    if productTags is not None:
        for product in productTags:
            productLink = product.find('a',href=True)
            productLinks.append(productLink['href'])
    return productLinks

def getProductLinksFromCategoryLink(categoryLink):
    productLinks = []
    categoryPageLinks = []
    pageLinks = getPageLinks(categoryLink)
    for page in pageLinks:
        productLinks.extend(getProductsLinksFromPageLink(page))
    return productLinks

def getMrp(productSoup):
    mrpInWords = re.findall('\d+',productSoup.find('em',class_='main-price').text.strip())
    mrpInStr = ''
    for w in mrpInWords[:-1]:
        mrpInStr += w
    mrp = int(mrpInStr)
    return mrp

def getGeneralDesc(infoTag,techTag):
    descStr = ''
    tag = infoTag.find('h2')
    while tag.find_next_sibling()!=techTag:
        descStr += tag.text
        tag = tag.find_next_sibling()

    #Tech Specs
    techSpecs = dict()
    techSubTags = techTag.find_all('div',class_='container-technics')
    for tag in techSubTags:
        ulTag = tag.find('ul')
        if ulTag is not None:
            spanTags = ulTag.find_all('span')
            h4Tag = tag.find('h4')
            data = []
            for s in spanTags:
                data.append(s.text)
            techSpecs[tag.find('h4').text] = ";".join(data)


    #Rest Desc
    restDescDict = dict()
    tempTag = techTag.find_next_sibling('h2')
    while tempTag != None:
        divTag = tempTag.find_next_sibling('div',class_='row')
        if divTag is None:  
            pTag = tempTag.find_next_sibling('p')
            if pTag is not None:
                restDescDict[tempTag.text] = pTag.text
            break
        if tempTag.text.replace(u'\xa0', u''):
            if divTag is None: 
                pTag = tempTag.find_next_sibling('p')
                if pTag is not None:
                    restDescDict[tempTag.text] = pTag.text
                break
            else:
                restDescDict[tempTag.text] = divTag.find('p').text
        tempTag = divTag.find('h2')
    
    return descStr,techSpecs,restDescDict
    
def getTableDesc(tableTag):
    entries = tableTag.find_all('tr')
    techSpecs = dict()

    for tag in entries:
        tdTags = tag.find_all('td')
        key = tdTags[0].text
        techSpecs[key]= []
        techSpecs[key].append(tdTags[1].find('span').text)
        pTags = tdTags[1].find_all('p')
        for p in pTags:
            techSpecs[key].append(p.text)
     
    return techSpecs

def getBulletSpecs(infoTag):
    descStr = ''
    h2Tag = infoTag.find('h2')
    if h2Tag is not None: descStr = h2Tag.text
    isUlTag = True
    restDescDict = dict()
    pTag = infoTag.find('p')
    while pTag is not None:
        ulTag = pTag.find_next_sibling('ul')
        if ulTag is not None: 
            restDescDict[pTag.text] = []
            liTags = ulTag.find_all('li')
            for liTag in liTags:
                restDescDict[pTag.text].append(liTag.text)
            pTag = ulTag.find_next_sibling('p')
        else: 
            isUlTag = False
            h3Tag = pTag.find_next_sibling('h3')
            if h3Tag is None: return descStr,restDescDict
            restDescDict[pTag.text] = h3Tag.text + ";"
            h4Tag = pTag.find_next_sibling('h4')
            restDescDict[pTag.text] += h4Tag.text
            pTag = h4Tag.find_next_sibling('p')

    if isUlTag:
        for key in restDescDict.keys():
            restDescDict[key] = ";".join(restDescDict[key])

    return descStr,restDescDict        

def getDescription(productSoup):
    infoTag = productSoup.find('div',class_='product-modules')
    descStr = ''
    techSpecs = ''
    restDescDict = ''
    if infoTag is not None:
        title = infoTag.find('h3').text  
        techTag = infoTag.find('div',class_='container')
        if techTag is not None:
            descStr, techSpecs,restDescDict = getGeneralDesc(infoTag,techTag)
        else:
            tableTag = productSoup.find('table')
            if tableTag is not None:
                techSpecs = getTableDesc(tableTag)
            else:
                decStr, restDescDict = getBulletSpecs(infoTag)


    return descStr,techSpecs,restDescDict

def getPhotoLinks(productSoup):
    innerBox = productSoup.find('div',class_='innersmallgallery')
    photoLinksSmall = []
    photoLinksBig = []
    if innerBox is not None:
        imgTags = innerBox.find_all('img')
        for imgTag in imgTags:
            photoLinksSmall.append(base_url + imgTag['src'])
            photoLinksBig.append(base_url + imgTag.parent['href'])
    else:
        imgTag = productSoup.find('div',class_='productimg f-grid-6')
        aTag = imgTag.find('a')
        if aTag is not None:
            photoLinksBig.append(base_url + aTag['href'])
        
    return photoLinksSmall,photoLinksBig

def downloadPhotos(name,photoLinksSmall,photoLinksBig):
    baseFolderBig = "./Big/"
    baseFolderSmall = "./Small/"
    if not os.path.exists(baseFolderBig + name):
        os.makedirs(baseFolderBig + name)
    if not os.path.exists(baseFolderSmall + name):
        os.makedirs(baseFolderSmall + name)

    for i in range(len(photoLinksSmall)):    
        urllib.request.urlretrieve(photoLinksSmall[i], baseFolderSmall + name + "/" + name + "_" + str(i).zfill(3) + ".jpg")

    for i in range(len(photoLinksBig)):    
        urllib.request.urlretrieve(photoLinksBig[i], baseFolderBig + name + "/" + name + "_" + str(i).zfill(3) + ".jpg")


def getProductInfo(link):
    productSoup = getWebPage(base_url + link)
    #Get Name
    name = productSoup.find('h1',class_='name').text.strip() 
    #MRP
    mrp = getMrp(productSoup)
    #Get Description
    descStr,techSpecs,restDescDict = getDescription(productSoup)
    #Get Photos
    photoLinksSmall,photoLinksBig = getPhotoLinks(productSoup)
    #downloadPhotos(name,photoLinksSmall,photoLinksBig)

    print (name)
    dataDict = dict()
    dataDict['Name'] = name
    dataDict['MRP'] = mrp
    dataDict['Desc'] = descStr
    dataDict['Small Photos'] = ";".join(photoLinksSmall)
    dataDict['Big Photos'] = ";".join(photoLinksBig)

    dataDF = pandas.DataFrame([dataDict])
    techDF = pandas.DataFrame([techSpecs])
    restDescDF = pandas.DataFrame([restDescDict])
    finalData = pandas.concat([dataDF,techDF,restDescDF],axis=1)

    return finalData

def fetchData():
    homeSoup = getWebPage(base_url)
    exit()

    # Get categories 
    categoryLinks = []
    tag = homeSoup.find('div',class_='submenu level1')
    parentTags = tag.find_all('li',class_='parent')
    for tag in parentTags:
        for a in tag.find_all('a',href=True):
            categoryLinks.append(a['href'])

    searchStr = ['OF','FF','MX']
    searchTags = []
    for s in searchStr:
        searchTags.append("/in/searchquery/%s/1/phot/5?url=%s" % (s,s))
    #categoryLinks.extend(searchTags)    

    print (categoryLinks)
    
    productLinksAll = []
    #Get product Links
    for c in categoryLinks:
        print (c)
        productLinks = getProductLinksFromCategoryLink(c)
        # print (len(productLinks),productLinks)
        for p in productLinks:
            if p not in productLinksAll:
                productLinksAll.append(p)
        # break

    print (len(productLinksAll))
    summaryDFList = []
    for i,p in enumerate(productLinksAll):
        #if i<189: continue
        print (i,p)
        finalDataDF = getProductInfo(p)
        summaryDFList.append(finalDataDF)
        # if i==10: break

    df = summaryDFList[0].append(summaryDFList[1:])
    df.to_excel("LS2_Database.xlsx")

if __name__ == "__main__":
    fetchData() 
