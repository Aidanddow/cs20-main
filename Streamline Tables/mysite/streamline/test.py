import urllib.request

def readURL(url):
    print("HEREHREHRHEHRHEHREH ", url)
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()

    print(mystr)