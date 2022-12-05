import sys  # for cl args
import os  # for env variables
import requests  # for interacting with websites
import re  # for regex expressions
import shlex  # for smart spliting
from bs4 import BeautifulSoup  # for navigating html
import math
import time

base_url = 'https://konachan.com/'
post_url = 'https://konachan.com/post?page={}&tags={}'

# xml version
post_url = 'https://konachan.com/post.xml?page={}&tags={}'


def fetch_data(tags, page_no=1):
    raw_html_data = requests.get(post_url.format(page_no, tags))
    if raw_html_data.status_code == 200:
        return raw_html_data
    else:
        print('Failed')
        print(f"Website status code: {raw_html_data.status_code}")
        exit(0)


def download_image(url, directory="", author="Unspecified", number=-1):
    # jpeg / png / jpg picker
    if '.' in url[-4:]:
        file_type = url[-3:]
    else:
        file_type = url[-4:]

    try:
        # download image
        image_bytes = requests.get(url)
        if len(directory) == 0:
            if not os.path.exists("Images"):
                os.mkdir("Images")
            with open(f'Images/{author}_image_{number}.{file_type}', 'wb') as f:
                f.write(image_bytes.content)
        else:
            if not os.path.exists(directory):
                os.mkdir(directory)
            with open(f'{directory}/{author}_image_{number}.{file_type}', 'wb') as f:
                f.write(image_bytes.content)

    except:
        return f"{author}_image_{number}: " + "Failed"
    return f"{author}_image_{number}:" + " Ok"


def paginator(soup):
    paginator = soup.prettify().split('\n')[1]
    paginator = [int(text.replace('"', '').split('=')[1])
                 for text in paginator[1:len(paginator)-1].split()[1:3]]
    return paginator


def process_posts(rawtext):
    posts = rawtext.find_all('post')
    posts_processed = {}
    for post in posts:
        # id : <post data>
        post = str(post)
        post = post[6:len(post)-8]
        post = shlex.split(post)
        # find id
        post_id = ""
        attr_list = {}
        for attr in post:
            if attr[:2] == "id":
                post_id = attr[3:]
            if attr[:8] == "file_url":
                attr_list["file_url"] = attr[9:]
            if attr[:6] == "author":
                attr_list["author"] = attr[7:]
            if attr[:9] == "file_size":
                attr_list["file_size"] = "{:.2f}MB".format(
                    int(attr[10:]) / (1024 * 1024))
            if attr[:6] == "height":
                attr_list["height"] = attr[7:]
            if attr[:5] == "width":
                attr_list["width"] = attr[6:]
        posts_processed[post_id] = attr_list

    return posts_processed


if __name__ == "__main__":
    start = time.time()

    cli_args = list(sys.argv)[1:]
    no_of_images = int(cli_args[0])
    tags = '+'.join(cli_args[1:])

    response = fetch_data(tags)
    soup = BeautifulSoup(response.text, features='xml')

    pagination = paginator(soup)

    if (pagination[0] < no_of_images):
        print("Lmao, you a crazy fool, not that many images man")
    else:
        no_of_images_downloaded = 0
        pages = math.floor(no_of_images / 21) + 1
        for page in range(1, pages+1):
            raw_page_data = fetch_data(tags, page)
            page_soup = BeautifulSoup(
                raw_page_data.text, features='xml')
            posts_metadata = process_posts(page_soup)
            for post, post_data in posts_metadata.items():
                print(
                    f'{post}: From {post_data["author"]} - File Size: {post_data["file_size"]}')
                print(download_image(
                    url=post_data["file_url"], author=post_data["author"], number=no_of_images_downloaded+1))
                no_of_images_downloaded += 1
                if (no_of_images_downloaded >= no_of_images):
                    end = time.time()
                    print(f"Done ({round(end - start, 4)})s")
                    exit()

    # print(posts_metadata)
    # print(pagination)
