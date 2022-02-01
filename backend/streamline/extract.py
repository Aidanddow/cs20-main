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
def extract(url, page_id=0, save_path=None):
    print(f"--- Reading {url}")

    try:
        driver = initialize_driver()
        driver.get(url)

        # Get titles of tables
        titles = driver.find_elements(By.TAG_NAME, "header")
        titleList = [title.text for title in titles]

        tableList = driver.find_elements(By.TAG_NAME, "table")
        
        # Get doi from url (Not Working)
        global doi
        doi = extract_doi(url)
        
        for num, table in enumerate(tableList):
            print(f"--- Processing Table {num+1}")
            tableArray, formattedData = process_table(table)

            # If a title exists for this table, pass it
            try:
                if len(titleList) > num and "Table" in titleList[num+1]:
                    title = titleList[num+1]
                else:
                    title = None
            except:
                title = None
            
            write_to_csv(tableArray, formattedData, num, page_id, title=title, path=save_path)
        
        print("--- Finished Processing Tables!")
        driver.quit()

    except FileNotFoundError:
        print(f"--- No folder \"{save_path}\" found")
            
    except Exception as error:
        print("--- Error:", error)
    
    
    #give number of tables to views to create ids in database for each one 
    number_of_tables = len(tableList)
    return number_of_tables

        

'''
Takes a html table element and generates an array corresponding to the row and column data
'''
def process_table(table):
    dataList  = []
    formattedDataList = []

    try: 
        theadNodes = table.find_elements(By.TAG_NAME, "th")
        theadList = [th.text for th in theadNodes]
        dataList.append(theadList)

    # No table header information
    except NoSuchElementException:
        pass
    
    tbodyNodes = table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
    
    # Get data from table
    for tr in tbodyNodes:
        tds = tr.find_elements(By.TAG_NAME, "td")

        # Get the text for each cell, replacing empty strings with a dash
        dataTr = [t.text if t.text != "" else "-" for t in tds]
        dataList.append(dataTr)
    
    # Get data in bold and italics format
    try: 
        boldNodes1 = table.find_elements(By.TAG_NAME, "strong")
        boldNodes2 = table.find_elements(By.TAG_NAME, "b")
        italicsNode = table.find_elements(By.TAG_NAME, "i")
        boldList = [bold.text for bold in boldNodes1]
        for bold in boldNodes2:
            boldList.append(bold.text)
        italicsList = [i.text for i in italicsNode]
        
        formattedDataList.append(boldList)
        formattedDataList.append(italicsList)
        
    except NoSuchElementException:
        pass

    return dataList, formattedDataList
    
    
'''
Takes a 2D array and writes the data to an xls file in the Desktop
'''

def write_to_csv(table, formattedData, num, page_id, title=None, path=None):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
    
    # font and style
    style = xlwt.XFStyle()
    font = xlwt.Font()
    
    
    # Write title into excel
    if title:
        sheet.write(0, 0, title)
    
    # Loop through arrays and write data into xls sheet
    for row_index, row in enumerate(table):
        for col_index, data in enumerate(row):
            if data in formattedData[0]:
                font.bold = True
                style.font = font
                sheet.write(row_index+1, col_index, data, style=style)
            elif data in formattedData[1]:
                font.italic = True
                style.font = font
                sheet.write(row_index+1, col_index, data, style=style)
            else:
                sheet.write(row_index+1, col_index, data)

    # Save the file to "path/{num}.xls"
    global doi
    fname = f"table{page_id}_{num+1}_{doi}.csv"

    path = os.path.join(path, fname)
    wbk.save(path)
    print(f"--- Saved table {num+1} to {path}")

    
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

'''
Should extract the doi from a url
(Working for url of papers because only papers have doi)
'''
def extract_doi(url):
    # URL will be formatted as follows
    # http:://website.domain/path?doi
    try:
        doi = url.split("doi")[1]
        doi = doi.split("?")[0][1:]
        doi = doi.replace("/","_")
    except IndexError:
        doi = ""

    return doi
    


if __name__ == '__main__':
    try:
        url = sys.argv[1]
        doi = extract_doi(url)

        CSV_PATH = os.path.join(Path.home(), "Desktop")
        extract(url, save_path=CSV_PATH)

    except Exception as e:
        print('--- Error', e)