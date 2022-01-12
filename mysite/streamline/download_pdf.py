import urllib.request

#Simple script to download a pdf from a link - wont be used in project, just used 
#to make sure the pdf if got, no filename handling
def download_file(download_url, filename="pdf"):
    pdf_path = ""
    response = urllib.request.urlopen(download_url)    
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()
 
