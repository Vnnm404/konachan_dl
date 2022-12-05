import sys
import asyncio
import aiohttp
import aiofiles
import time
import math
import random
from bs4 import BeautifulSoup
from pathlib import Path, PureWindowsPath

# windows specific, otherwise asyncio loop weird behaviour
if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

base_url = 'https://konachan.com/'
# xml version
post_url = 'https://konachan.com/post.xml?page={}&tags={}'


async def fetch(client, tags, page=1):
    async with client.get(post_url.format(page, '+'.join(tags))) as resp:
        if resp.status != 200:
            print(f"HTML Respones Code {resp.status} on Page {page}")
            print(f"Images from page {page} may be corrupted")
        return await resp.text()


def process(soup, post_data):
    for post in soup.posts.find_all('post'):
        post_data_list = {}
        post_data_list['link'] = post.get('file_url')
        post_data_list['author'] = post.get('author')
        post_data_list['id'] = post.get('id')
        post_data_list['h'] = post.get('height')
        post_data_list['w'] = post.get('width')
        post_data_list['size'] = round(
            int(post.get('file_size')) / (1024 * 1024), 2)
        post_data.append(post_data_list)
    return post_data


def paginator(soup):
    pagination = [int(soup.posts.get('count')), int(soup.posts.get('offset'))]
    return pagination


async def download(client, url, path, retry=0):
    if '.' in url[-4:]:
        file_type = url[-3:]  # png / jpg
    else:
        file_type = url[-4:]  # jpeg

    async with client.get(url) as resp:
        if retry == 1:
            final_path = path
        else:
            final_path = path / f'image_{time.time_ns()}.{file_type}'

        if resp.status != 200:
            print(f"HTML Respones Code for Image {resp.status}")
            print(f"This image may be corrupted")

        f = await aiofiles.open(final_path, mode='wb')
        await f.write(await resp.read())
        await f.close()


def process_cli(args):
    cli_cmds = {}
    print(args)
    for cmd in range(len(args)):
        if args[cmd] == '-n':
            cli_cmds['n'] = int(args[cmd+1])
        if args[cmd] == '-t':
            tags = []
            number = int(args[cmd+1])
            for ti in range(1, number+1):
                tags.append(args[cmd+1+ti])
            cli_cmds['t'] = tags
        if '-r' in args:
            cli_cmds['r'] = True
        if args[cmd] == '-p':
            cli_cmds['p'] = args[cmd+1]
        if '-f' in args:
            cli_cmds['f'] = True
    return cli_cmds


async def batch_download(client, post_data, no_pages_to_scrape, path):
    batches = []
    for i in range(21, no_pages_to_scrape * 21 + 1, 21):
        batches.append(post_data[i-21:i])

    coroutine_batches = []
    for batch in batches:
        coroutine_batches.append(
            [download(client, post['link'], path) for post in batch])

    print("Downloading .. ")
    start_time = time.time()
    for cobatch in coroutine_batches:
        await asyncio.gather(*cobatch)
        print(f"Finished {len(cobatch)} Images")
    end_time = time.time()
    print(f"Done in {round(end_time-start_time, 2)}s")


async def main():
    cli_args = process_cli(sys.argv[1:])
    print(cli_args)

    # process path
    if 'p' in cli_args:
        path = Path(cli_args['p'])
        if (not path.is_dir()):
            print("Not a directory")
            exit(0)
        if (not path.exists()):
            if 'f' in cli_args:
                print("Directory doesn't exists, creating it.")
                ok = True
            else:
                print("Directory doesn't exist, create it?")
                ok = input("(y/n): ")
            if ok:
                try:
                    path.mkdir()
                except:
                    print("Failed to create directory")
                    print("Using current directory")
                    path = Path.cwd()
    else:
        path = Path(Path.cwd()) / "konachan_dl"
        if (not path.exists()):
            path.mkdir()

    async with aiohttp.ClientSession(trust_env=True) as client:
        raw = await fetch(client, cli_args['t'])

        soup = BeautifulSoup(raw, features='xml')
        pagination = paginator(soup)
        no_pages = math.ceil(pagination[0] / 21)

        # check if the user asks for too many images
        if (cli_args['n'] > pagination[0]):
            print("Not Enough Images Available for the Given Parameters")
            exit(0)

        # calculate number of pages needed to meet users requests'
        no_pages_to_scrape = math.ceil(cli_args['n'] / 21)

        page_list = list(range(1, no_pages+1))
        if 'r' in cli_args:
            random.shuffle(page_list)
        page_list = page_list[:no_pages_to_scrape]

        post_data = []
        for page in page_list:
            raw = await fetch(client, cli_args['t'], page)
            soup = BeautifulSoup(raw, features="xml")
            post_data = process(soup, post_data)

        # process posts
        if 'r' in cli_args:
            random.shuffle(post_data)
        post_data = post_data[:cli_args['n']]

        # calculate total file size
        total_file_size = 0
        for post in post_data:
            total_file_size += post['size']
        print(f"Download size: {round(total_file_size, 2)}mb")
        if 'f' in cli_args:
            ok = 'y'
        else:
            ok = input("Continue? (y/n): ")
        if ok[:1].lower() == 'n':
            print("Closing.")
            path.rmdir()  # cleanup
            exit(0)

        # download in batches to avoid 503
        await batch_download(client, post_data, no_pages_to_scrape, path)

asyncio.run(main())
