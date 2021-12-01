'''
Need to install selenium and webdriver-manager in advance
pip install selenium
pip install webdriver-manager
'''

import sys, os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
import time
import xlwt
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def extract(urlFromDjango):

    print("Reading", urlFromDjango)

    option = ChromeOptions()
    # option.add_argument('--window-size=1920,1080')
    # option.add_argument('--headless')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    #option.add_argument("--disable-blink-features=AutomationControlled")
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
                """
    })
    driver.minimize_window()

    try:
        
        url=urlFromDjango

        driver.get(url)
        time.sleep(3)

        titles = driver.find_elements(By.TAG_NAME, "HEADER")
        titleList = []
        for title in titles:
            titleList.append(title.text)
        
        tableList = driver.find_elements(By.TAG_NAME, "table")

        for i, table in enumerate(tableList):
            wbk = xlwt.Workbook()
            sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
            
            dataListB = []
            dataList = []

            t = time.time()
            theTime = int(round(t * 1000))
            
            try: 
                threadNodes = table.find_element(By.TAG_NAME, "thread").find_element(By.TAG_NAME, "tr").find_elements(By.TAG_NAME, "th")
                for th in theadNodes:
                    # print(th.text)
                    dataList.append(th.text)
            
            except Exception:
                print("NO thead")

            dataListB.append(dataList)
            #print(dataArrayB)
        
            tbodyNodes = table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
            for tr in tbodyNodes:
                dataTr=[]
                tds=tr.find_elements(By.TAG_NAME, "td")
                for td in tds:
                    text=td.text
                    if text=="":
                        text='-'
                    dataTr.append(text)
                dataListB.append(dataTr)
            '''
            print(dataArrayB)
            print(dataArrayB[0][2])
            '''
            print(titleList)
            
            # write title into excel
            try:
                if "Table" in titleList[i]:
                    sheet.write(0,0,titleList[i])
            except Exception:
                pass
            
            # write every data into excel
            for i in range(len(dataListB)):
                for j in range(len(dataListB[i])):
                    sheet.write(i+1, j, dataListB[i][j])

            fname = f"{str(i)}.xls"
            path = os.path.join(Path.home(), "Desktop", fname)

            wbk.save(path)

    except Exception as error:
        print("My Error:{0}".format(error))

    finally:
        time.sleep(5)
        driver.quit()
