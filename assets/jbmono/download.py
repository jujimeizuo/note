import os
import sys
import requests


def download(url, url_prefix, prefix = './'):
    if url[0] == '.':
        url = url[2:]    
    elif url[0] == '/':
        url = url[1:]
    filename = url.split('/')[-1]
    # print(url, filename)
    file = requests.get(url_prefix + url)
    # print(url_prefix + url)
    open(prefix + filename, 'wb').write(file.content)


def scan(path):
    file = open(path)
    lines = file.readlines()
    for line in lines:
        if 'url' in line:
            # url = line.split('\'')[1]
            start = line.find('(')
            end = line.find(')')
            url = line[start + 1: end]
            # print(url)
            download(url, 'https://cdn.tonycrane.cc/jbmono/', './files/')
    file.close()


if __name__=="__main__":
    path = sys.argv[1]
    scan(path)
# download('/jbmono/jetbrainsmono.css', 'https://cdn.tonycrane.cc/lxgw')
