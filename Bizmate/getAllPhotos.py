import xlrd
import xlsxwriter
import sys
sys.path.insert(1,"../pathInit/")
import pathInit
import chromeUtils
from bs4 import BeautifulSoup

websiteHome = "https://www.ryderauto.in/product-details.php?pid="

count = 0
loc = "Products_Ryderauto_10_04_2021.xls"
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0)

workbook = xlsxwriter.Workbook('ryderautoPhotos.xlsx')
worksheet = workbook.add_worksheet()

startRow = 1
rows = sheet.nrows

pids = []
names = []
pidCol = 1
nameCol = 3

driver = chromeUtils.chromeDriver()
downloadObj = chromeUtils.download()

for r in range(startRow,rows):
    pids.append(str(sheet.cell_value(r, pidCol)))
    names.append(str(sheet.cell_value(r, nameCol)))

startIndex = 0
for index in range(startIndex,len(pids)):
    pid = pids[index]
    link = websiteHome+pid
    imgStr = ""
    soup = driver.getSoup(link,'prodqty')
    imageLinks = set()
    imgNames = []
    imgTags = soup.find('div',class_="container-indent").find_all('img')
    for tag in imgTags:
        if "RYDERAUTO" in tag['src'] and ".png" in tag['src'] and "brandimage" not in tag['src']: imageLinks.add(tag['src'])
    if len(imageLinks):
        for imageIndex,imageLink in enumerate(imageLinks):
            #imageLink = imageLink.replace(" ","%20")
            imgName = names[index].replace("  "," ").replace(" ","_").replace("/","__").replace("(","___").replace(")","____") + "_" + str(imageIndex) + ".png"
            imgNames.append(imgName)
            downloadObj.downloadImage(imageLink,imgName)
            
        imgStr = ";".join(imgNames) 
    else:
        print ("Error: Img Not Found",index,pid)
    worksheet.write(index,0,pid)
    worksheet.write(index,1,names[index])
    worksheet.write(index,2,imgStr)
workbook.close()