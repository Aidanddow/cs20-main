import os
import pandas as pd
import ocrmypdf
import tabula
import pdfplumber
import camelot

def fileToOCR(filePath, ocrPath=None):
    
    if(ocrPath==None):
        ocrPath = os.path.splitext(filePath)[0]+"OCR.pdf"
    
    # Check if the converted file already exists (if the input path is not equal to the output path)
     
    if filePath!=ocrPath and os.path.isfile(ocrPath):
        return ocrPath
    
    # Convert the file and return its path, return the given file path if it is already converted
    try:
        ocrmypdf.ocr(filePath, ocrPath, deskew=True)
        return ocrPath
    except:
        return filePath


def tabula2csv(file, pages="1", ocrPath = None):
    # TABULA USEFULL FUNCTIONS at https://pypi.org/project/tabula-py/

    outPath = "_".join((os.path.splitext(file)[0],pages,"TABULA.csv"))
        
    tabula.convert_into(fileToOCR(file, ocrPath), outPath, output_format="csv", pages=pages, stream=True)
    
    return outPath


def getTable(file, pages="1", library="camelot", ocrPath = None):
    tables = None
    
    ocr = fileToOCR(file, ocrPath)
    
    if(library=="camelot"):
        tables = camelot.read_pdf(ocr, pages=pages, flavor="stream")
        
    if(library=="tabula"):
        tables = tabula.read_pdf(ocr, pages=pages, stream=True)
    return tables


pathData = "data"
filePath = os.path.join(pathData, "paperTest.pdf") 
pages = "5"


# Testing camelot
tables = getTable(filePath,pages=pages,library="camelot")

for i in range(tables.n):
    print(tables[i].df)


# Testing tabula
tables = getTable(filePath,pages=pages,library="tabula")
print(tables)


# Testing pdfPlumber
path = fileToOCR(filePath)
print(path)

pdf = pdfplumber.open(path)
page = pdf.pages[5]
print(page.extract_table())

