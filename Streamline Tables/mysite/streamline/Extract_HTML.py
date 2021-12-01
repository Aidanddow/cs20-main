import urllib.request
import ssl

def readURL(url):

    context = ssl._create_unverified_context()
    fp = urllib.request.urlopen(url, context=context)
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()

    print(mystr)

