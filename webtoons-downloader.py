from bs4 import BeautifulSoup
import urllib.request, sys, os
import http.cookiejar
from shutil import rmtree
from PIL import Image

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'),('Referer', 'https://www.webtoons.com/')]
urllib.request.install_opener(opener)

def make_req(url):
    return urllib.request.urlopen(url).read().decode('utf-8')

def get_power(remainder):
    power_of_number = 0
    while remainder >= 10:
        remainder /= 10
        power_of_number += 1
    return power_of_number


def download_image(url, directory, number, max_zeros):
    number_string = ""
    remainder = number
    power_of_number = get_power(number)
    for _ in range(max_zeros - power_of_number):
        number_string += "0"
    number_string += str(number)
    extension = '.jpg'
    if '.gif' in url:
        extension = '.gif'
    urllib.request.urlretrieve(url, directory + '/' + number_string + extension)

def create_html(dir, title):
    html = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
            <html>
            <head>
                <meta content="text/html; charset=ISO-8859-1" http-equiv="content-type">
                <title>''' + title + '''</title>
            </head>
            <body>'''

    images = os.listdir(dir)
    images.sort()
    for image in images:
        html += '<img src="' + image + '"> <br>'
    html += '''</body>
    </html>'''
    with open(dir + "/index.html", 'w') as output:
        output.write(html)

def create_dir_if_not_exist(folder):
    CHECK_FOLDER = os.path.isdir(folder)

    if not CHECK_FOLDER:
        os.makedirs(folder)
        print("created folder: ", folder)

def main():
    site = BeautifulSoup(make_req(sys.argv[1]), 'html.parser')
    imagelist = site.find(id="_imageList")
    images = imagelist.find_all('img')
    imagelinks = []
    for i in images:
        imagelinks.append(i.get('data-url'))

    title = site.title.string
    title_parts = title.split('|')
    series = title_parts[1][1:]
    episode = title_parts[0][:-1]
    destination = series + '/' + episode

    create_dir_if_not_exist(series)
    create_dir_if_not_exist(destination)

    number_of_images = len(imagelinks)

    print("Downloading images for: ", title)
    for i in range(len(imagelinks)):
        download_image(imagelinks[i], destination, i, get_power(number_of_images))

    print("Creating final html")
    create_html(destination, title)

if __name__ == "__main__":
    main()
