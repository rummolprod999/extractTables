import glob
import hashlib
import json
import os
import shutil
import sys
from urllib.parse import unquote

import requests
import tabula
from pyexcel import merge_all_to_a_book

tmp = None
list_file = []


def extract():
    j = ''.join(sys.argv[1:]).encode('utf-8')
    hash = hashlib.md5(j).hexdigest()
    tmp = f"{hash}/temp"
    for f in sys.argv[1:]:
        try:
            getFile(f, hash)
        except Exception as ex:
            print(ex)
    shutil.rmtree(tmp)
    print(list_file)
    return json.dumps(list_file)


def getFile(f, hash):
    file = download(f, hash)
    tables = tabula.read_pdf(file, pages="all")
    for idx, table in enumerate(tables):
        filename = file.replace("/temp", "") + str(idx) + ".xlsx"
        table.to_excel(filename)
        list_file.append(filename)


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
    temp_file = f"{hash}/temp/reader_{filename}"
    filepath = os.path.join(hash, 'temp')
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    with open(temp_file,
              'wb') as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)
    return os.path.abspath(temp_file)


if __name__ == '__main__':
    extract()
