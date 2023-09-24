
import time
from urllib.parse import unquote
import requests


def print_hi(name):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0",
        "Referer": "https://dl.twrp.me/gauguin/twrp-3.5.2_10-0-gauguin.img",
    }
    r = requests.get(
        " http://zakupki.gov.ru/44fz/filestore/public/1.0/download/priz/file.html?uid=D3FC0FBCFE924423AA6EFDDD0AF182BB",
        stream=True, headers=headers)

    ext = unquote(r.headers['Content-disposition'].split(';')[1].split('=')[1].strip('"'))
    with open(ext,
              'wb') as f:
        for chunk in r.iter_content(1024):  # iterate on stream using 1KB packets
            f.write(chunk)



if __name__ == '__main__':
    print_hi('PyCharm')

