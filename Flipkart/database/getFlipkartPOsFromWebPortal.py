import pyautogui
import time


f = open("purchase-orders-20-08-2020-03_36_12.csv")

lines = f.readlines()
f.close()

pyautogui.FAILSAFE = False

skipFirstLine = True
pyautogui.click(950,1050)
time.sleep(3)
for line in lines:
	if skipFirstLine:
		skipFirstLine = False
		continue
	po = line.split(",")[0]
	pyautogui.click(200,60)
	time.sleep(2)
	pyautogui.write('https://vendorhub.flipkart.com/v2/#/operations/po/details/'+po + '\n', interval=0.1)
	time.sleep(2)
	pyautogui.click(1800,350)
	time.sleep(2)