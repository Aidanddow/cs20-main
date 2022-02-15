'''
Need to install bs4 and lxml in advance
% pip install bs4
% pip install lxml

To run by itself,
% python extract.py <url>
'''

import sys, os
import xlwt
from pathlib import Path
from bs4 import BeautifulSoup
import requests
from streamline.models import Table_HTML

def extract(url, web_page, save_path=None):
    '''
    Takes a url, finds all html tables and processes them,
    saving their data to xls files.
    '''
    print(f"--- Reading {url}")

    header = {'User-Agent': 'Mozilla/5.0'}
    session = requests.session()
    html = session.get(url, headers=header)
    soup = BeautifulSoup(html.text,'lxml')
    
    # Get titles of tables
    titleList = [title.text for title in soup.select('header[class*="table"]')]
    
    footnotes = [footnote for footnote in soup.select('div[class*="footnote"]')]
    footnoteList = process_footnote(footnotes)
    
    # Get doi from url
    global doi
    doi = extract_doi(url)

    tableList = soup.find_all('table')
    
    for num, table in enumerate(tableList):
        print(f"--- Processing Table {num+1}")
        tableArray, formattedData = process_table(table)

        if len(footnoteList) > num:
            footnoteData = footnoteList[num]
        else:
            footnoteData = None

        # If a title exists for this table, pass it
        if len(titleList) > num:
            if "Table" in titleList[num]:
                title = titleList[num]
        else:
            title = None
        
        write_to_csv(tableArray, formattedData, footnoteData, num, web_page, title=title, path=save_path)
    
    print("--- Finished Processing Tables!")
    
    # Give number of tables to views to create ids in database for each one
    return len(tableList)
    

def process_footnote(footnotes):
    '''
    Takes footnotes for all tables and generates an list
    '''
    footnoteList = []
    for footnote in footnotes:
        alist = [li.text for li in footnote.find_all("li")]
        footnoteList.append(alist)

    return footnoteList


def process_table(table):
    '''
    Takes a html table element and generates an array corresponding to the row and column data
    '''
    dataList  = []
    formattedDataList = []

    try: 
        theadList = [th.text for th in table.find_all('th')]
        dataList.append(theadList)

    # No table header information
    except:
        pass
    
    trNodes = table.find_all('tr')
    
    # Get data from table
    for tr in trNodes:
        tds = []
        for td in tr.find_all('td'):
            # Remove link tag
            link = td.find('a')
            if link:
                link.extract()
            sup = td.find('sup')
            if sup:
                sup.extract()
            # Get the text for each cell, replacing empty strings with a dash
            if td.text != "":
                data = td.text.replace("\n", "")
            else:
                data = "-"
            tds.append(data)
        if len(tds) != 0:
            dataList.append(tds)
    
    # Get data in bold and italics format
    boldNodes1 = table.find_all('strong')
    boldNodes2 = table.find_all('b')
    italicsNode = table.find_all('i')
    italicsList = [i.text for i in italicsNode]
    boldList = [bold.text for bold in boldNodes1]

    for bold in boldNodes2:
        boldList.append(bold.text)
    
    formattedDataList.append(boldList)
    formattedDataList.append(italicsList)

    return dataList, formattedDataList
    
    
def write_to_csv(table, formattedData, footnoteData, num, web_page, title=None, path=None):
    '''
    Takes a 2D array and writes the data to an xls file in the Desktop
    '''
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
    # Count the last row 
    line = 0
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
        line = row_index
    
    if footnoteData:
        # Add "FootNote" title
        line += 3
        sheet.write(line, 0, "FootNote")
        # Go to the next row
        line += 1
        # Write footnotes(surronding texts) into file
        for footnote in footnoteData:
            sheet.write(line, 0, footnote)
            line += 1

    # Save the file to "path/{num}.xls"
    global doi
    fname = f"table{web_page.id}_{num+1}_{doi}.xls"

    path = os.path.join(path, fname)
    wbk.save(path)

    # Creates a new table entry every time a new file is saved
    Table_HTML.objects.create(html_id=web_page, file_path = path)
    
    print(f"--- Saved table {num+1} to {path}")


def extract_doi(url):
    '''
    Should extract the doi from a url
    (Working for url of papers because only papers have doi)
    # URL will be formatted as follows
    # http:://website.domain/path?doi
    '''
    try:
        doi = url.split("doi")[1]
        doi = doi.split("?")[0][1:]
        doi = doi.replace("/","_")
        print(f"doi = {doi}")
    except IndexError:
        doi = ""

    return doi


if __name__ == '__main__':
    try:
        url = sys.argv[1]
        #url = "https://dom-pubs.onlinelibrary.wiley.com/doi/10.1111/dom.12903"
        doi = extract_doi(url)

        CSV_PATH = os.path.join(Path.home(), "Desktop")
        extract(url, web_page=0, save_path=CSV_PATH)

    except Exception as e:
        print('--- Error', e)
