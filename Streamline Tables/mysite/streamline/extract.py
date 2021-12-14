'''
Need to install selenium and webdriver-manager in advance
% pip install selenium
% pip install webdriver_manager

To run by itself,
% python extract.py <url>
'''

import sys, os
import time
import xlwt
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


'''
Takes a url, finds all html tables and processes them,
saving their data to xls files.
'''
def extract(url, target_path=None):
    print(f"Reading {url}")

    try:
        driver = initialize_driver()

        # Go to url
        driver.get(url)

        # Get titles of tables
        titles = driver.find_elements(By.TAG_NAME, "HEADER")
        titleList = [title.text for title in titles]

        tableList = driver.find_elements(By.TAG_NAME, "table")

        for num, table in enumerate(tableList):
            print(f"Processing Table {num+1}")
            tableArray = process_table(table)

            # If a title exists for this table, pass it
            if len(titleList) > num:
                title = titleList[num]
            else:
                title = None

            write_to_xls(tableArray, num, title=title, path=target_path)
        
        print("Finished Processing Tables!")

    except FileNotFoundError:
        print(f"No folder \"{target_path}\" found")
            
    except Exception as error:
        print("Error:", error)

    finally:
        time.sleep(5)
        driver.quit()


'''
Takes a html table element and generates an array corresponding to the row and column data
'''
def process_table(table):
    dataList  = []

    try: 
        # If there is table header information, retrieve it
        theadNodes = table.find_element(By.TAG_NAME, "thead").find_element(By.TAG_NAME, "tr").find_elements(By.TAG_NAME, "th")
        theadList = [th.text for th in theadNodes]
        dataList.append(theadList)

    except NoSuchElementException:
        pass
    
    tbodyNodes = table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
    
    # Get data from table
    for tr in tbodyNodes:
        tds = tr.find_elements(By.TAG_NAME, "td")

        # Get the text for each cell, replacing empty strings with a dash
        dataTr = [t.text if t.text != "" else "-" for t in tds]
        dataList.append(dataTr)

    return dataList
    
    
'''
Takes a 2D array and writes the data to an xls file in the Desktop
'''
def write_to_xls(table, num, title=None, path=None):
    
    # Initialize the workbook and add a sheet
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
    
    # Write title into excel
    if title:
        sheet.write(0, 0, title)
    
    # Loop through arrays and write data into xls sheet
    for row_index, row in enumerate(table):
        for col_index, data in enumerate(row):
            sheet.write(row_index, col_index, data)

    # Save the file to "path/{num}.xls"
    fname = f"table{num+1}.xls"

    if path:
        path = os.path.join(path, fname)
    else:
        # Default to the desktop
        path = os.path.join(Path.home(), "Desktop", fname)

    path = os.path.join(Path.home(), "Desktop", fname)
    wbk.save(path)
    print(f"Saved table {num+1} to {path}")
    

'''
 Initializes and returns the web driver
'''
def initialize_driver(headless=True):
    # Initialize the webdriver, headless hides popup window
    options = webdriver.ChromeOptions()
    options.headless = headless

    # Create a new instance of selenium
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
   
    # Runs the code on the driver
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument", {
        "source":
                """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
                """
        })
    return driver


if __name__ == '__main__':
    try:
        url = sys.argv[1]
        extract(url)
    except:
        print("Please provide a URL")