import hashlib
import os
import sys
import time
from urllib.parse import unquote

import tabula
import requests


def extract():
    j = ''.join(sys.argv[1:]).encode('utf-8')
    hash = hashlib.md5(j).hexdigest()
    for f in sys.argv[1:]:
        try:
            getFile(f, hash)
        except Exception as ex:
            print(ex)


def getFile(f, hash):
    file, tmp = download(f, hash)
    tables = tabula.read_pdf(file, pages="all")
    print(tables)


def download(f, hash):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0",
        "Referer": "http://zakupki.gov.ru",
    }
    r = requests.get(
            f,
            stream=True, headers=headers)
    ext = list(filter(lambda o: o.find("filename=") != -1, r.headers['Content-disposition'].split(';')))
    filename = unquote(ext[0].split('=')[1].strip('"'))
    temp_file = f"{hash}/temp/{filename}"
    filepath = os.path.join(hash, 'temp')
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    with open(temp_file,
              'wb') as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)
    return (os.path.abspath(temp_file), f"{hash}/temp")


if __name__ == '__main__':
    extract()
