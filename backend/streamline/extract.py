'''
Need to install selenium and webdriver-manager in advance
% pip install selenium
% pip install webdriver_manager

To run by itself,
% python extract.py <url>
'''

import sys, os
import time
import tkinter
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
def extract(url, save_path=None):
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
            tableArray = process_table(table)

            # If a title exists for this table, pass it
            title = titleList[num] if len(titleList) > num else None
            write_to_csv(tableArray, num, title=title, path=save_path)
        
        print("--- Finished Processing Tables!")

    except FileNotFoundError:
        print(f"--- No folder \"{save_path}\" found")
            
    except Exception as error:
        print("--- Error:", error)

    finally:
        driver.quit()

'''
Takes a html table element and generates an array corresponding to the row and column data
'''
def process_table(table):
    dataList  = []

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

    return dataList
    
    
'''
Takes a 2D array and writes the data to an xls file in the Desktop
'''

def write_to_csv(table, num, title=None, path=None):
    csv = title + "\n" if title else ""
    
    table = [",".join(i) for i in table]
    csv += "\n".join(table)

    global doi
    fname = f"table{num+1}_{doi}.csv"

    path = os.path.join(path, fname)
    with open(path, "w") as f:
        f.write(csv)

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
Should extract the doi from a url (Not Working)
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