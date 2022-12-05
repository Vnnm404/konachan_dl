#<div align="center">
<h1>konachan_dl</h1>
<p>konachan_dl is a script used to download images from <a href="konachan.com">konachan</a> quickly.</p>
<p>It downloads images directly onto your drive where ever you want and does so in parallel to achieve faster download speeds, all in your terminal! We also compare performance to the a naive approach to downloading images from the site.</p>
<a href="#getting-started">Getting started</a> • <a href="#installation">Installation</a> • <a href="#analysis">Analysis</a>
</div>

## Getting Started

![Demo][assets/demo.gif]

```sh
python konachan_dl.py -n 5 -t 2 hatsune_miku vocaloid # downloads 5 images with the tags hatsune_miku+vocaloid

python konachan_dl.py -n 1 -t 1 -r long_hair # (random) downloads one random picture with tag long_hair

python konachan_dl.py -n 1 -t 1 -p ~/folder vocaloid # (path) downloads one picture with tag vocaloid into the directory ~/folder

python konachan_dl.py -n 1 -t 1 -f blush # (force) downloads one picture with tag blush and doesn't show the confirmation prompt
```

## Installation

Simpy run the python script as any other with `python konachan_dl.py`.
It can be downloaded using `git clone <url>`.

## Analysis

In this repo, a simple script is provided that demonstrates the naive 1 by 1 approach to scraping konachan for images. We compare the scripts with batch downloads of 5 and 20 images.

*1 by 1 on 5 images*
![Slow5][assets/slow.png]

*konachan_dl on 5 images*
![Fast5][assets/fast.png]

This may seem unimpressive but this difference in speed is only magnified with larger downloads as demonstrated with 20 images.

*1 by 1 on 20 images*
![Slow20][assets/slow20.png]

*konachan_dl on 5 images*
![Fast20][assets/fast20.png]

The numbers speak for themselves.
Here are two beautiful images the scraper got in these performance runs

![showcase1][assets/showcase1.jpg]

![showcase2][assets/showcase2.png]