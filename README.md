<div align="center">
<h1>konachan_dl</h1>
<p>konachan_dl is a script used to download images from <a href="konachan.com">konachan</a> quickly.</p>
<p>It downloads images directly onto your drive where ever you want and does so in parallel to achieve faster download speeds, all in your terminal! We also compare performance to the a naive approach to downloading images from the site.</p>
<a href="#getting-started">Getting started</a> • <a href="#installation">Installation</a> • <a href="#analysis">Analysis</a>
</div>

## Getting Started

![demo](https://user-images.githubusercontent.com/94549325/205708834-5a0f6dad-5ef8-4eab-8aae-14f2c7553a6e.gif)

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
<img width="376" alt="slow" src="https://user-images.githubusercontent.com/94549325/205708885-f3756ebf-dd89-44a5-b2f7-f1db24bbde6d.png">

*konachan_dl on 5 images*   
<img width="401" alt="fast" src="https://user-images.githubusercontent.com/94549325/205708953-1862feb3-2a4e-447c-af5a-fe83b137fe27.png">

This may seem unimpressive but this difference in speed is only magnified with larger downloads as demonstrated with 20 images.

*1 by 1 on 20 images*   
<img width="376" alt="slow" src="https://user-images.githubusercontent.com/94549325/205708999-c210118d-da65-4189-9125-14d960ceb818.png">

*konachan_dl on 5 images*   
<img width="406" alt="fast20" src="https://user-images.githubusercontent.com/94549325/205709037-daf3c522-e3ba-4071-b67b-afac1763d846.png">

The numbers speak for themselves.
Here are two beautiful images the scraper got in these performance runs   

![showcase1](https://user-images.githubusercontent.com/94549325/205709068-fe3f9b39-b8f3-434b-93ee-7006007d9176.jpg)
   
![showcase2](https://user-images.githubusercontent.com/94549325/205709106-d20c20b8-c2c5-49bd-9bb5-785b186d1303.png)
