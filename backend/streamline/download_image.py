import requests

#downloads the image from the url given, no filename handling
def download(image_url):
    img_data = requests.get(image_url).content
    with open('image_name.jpg', 'wb') as handler:   
        handler.write(img_data)
        
    return