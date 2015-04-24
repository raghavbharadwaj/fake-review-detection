# Get Amazon brand for given product ID
#
# Author: Arry Fajar Firdaus
#
# for Amazon dataset obtained from
# http://times.cs.uiuc.edu/~wang296/Data/
# 
from glob import glob
from os.path import basename
from urllib.request import urlopen, URLError, Request
from bs4 import BeautifulSoup
from time import sleep
import gzip

req_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; "
        +"WOW64; rv:35.0) Gecko/20100101 Firefox/35.0",
    "Accept-Encoding": "gzip, deflate",
}

doneflag = {}
with open("../../datasets/amazon_dataset/"
        +"amazon_video_surveillance_brands.txt", 'r') as fh:
    for line in fh:
        doneflag[line.split()[0]] = 1

fh = open("../../datasets/amazon_dataset/"
    +"amazon_video_surveillance_brands.txt", 'a')
for fn in glob('../../datasets/amazon_dataset/video_surveillance/*.json'):
    product_id = basename(fn).split('.')[0]
    if product_id in doneflag:
        continue
    print(product_id)
    request = Request(
        'http://www.amazon.com/dp/'+product_id, headers=req_header)
    retry = 0
    brand = ''
    restart = False
    while True:
        try:
            resp = urlopen(request)
            break
        except URLError as e:
            if str(e.code) == '404':
                brand = '__NOT_FOUND__'
                break
            if not retry:
                print("Can't retrieve", product_id, ':',
                        str(e.code), str(e.reason))
            retry += 1
            print("Retrying (%d)" % retry)
            sleep(5)
            if retry == 5:
                restart = True
                break
    if restart:
        continue
    if brand != '__NOT_FOUND__':
        f = gzip.GzipFile(fileobj=resp)
        html_data = f.read().decode('utf-8', 'ignore')
        soup = BeautifulSoup(html_data)
        brand_ = soup.select("#brand")
        if not brand_:
            continue
        else:
            brand = brand_[0].string
    fh.write(product_id + " " + brand + "\n")
    #print(product_id, brand)
    #sleep(1)
