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

def download_image(url, directory, number):
    urllib.request.urlretrieve(url, directory + '/' + str(number) + '.jpg')

def create_image(dir, name):
    images = [Image.open(dir + '/' + x) for x in os.listdir(dir)]
    widths, heights = zip(*(i.size for i in images))

    max_width = max(widths)
    total_height = sum(heights)

    new_im = Image.new('RGB', (max_width, total_height))

    y_offset = 0
    for i in images:
        new_im.paste(i, (0, y_offset))
        y_offset += i.size[1]

    new_im.save(name + '.png')

def main():
    tmp_dir = 'tmp'
    site = BeautifulSoup(make_req(sys.argv[1]), 'html.parser')
    imagelist = site.find(id="_imageList")
    images = imagelist.find_all('img')
    imagelinks = []
    for i in images:
        imagelinks.append(i.get('data-url'))

    title = ''.join(e for e in site.title.string if e.isalnum())

    CHECK_FOLDER = os.path.isdir(tmp_dir)

    if not CHECK_FOLDER:
        os.makedirs(tmp_dir)
        print("created folder: ", tmp_dir)

    print("Downloading images for: ", title)
    for i in range(len(imagelinks)):
        download_image(imagelinks[i], tmp_dir, i)

    print("Creating final image")
    create_image('tmp', title)

    print('Deleting temporary files')
    rmtree('tmp')

if __name__ == "__main__":
    main()
