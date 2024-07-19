A small static site generator written in Python, based extemely heavily off [this static site generator](https://github.com/theacodes/blog.thea.codes/) by [Thea Flowers](https://thea.codes/). My goals in this project are [similar to hers](https://blog.thea.codes/a-small-static-site-generator/): to have my own thing while keeping it minimalistic. I looked into other generators like Jekyll and even Eleventy, but they all felt like they were just trying to do too much or be a generic solution.

Thanks, Thea!

## Requirements
* Python 3
* `pip install -r requirements.txt`

## Build
* `python build.py`
* Site will be in the `/output` folder

## TODO
* ~~Base path to re-path all images to a common root~~
    * ~~will also need to parse relative/absolute image links in MD~~
* ~~Emoji plugin~~
* ~~RSS~~ - validates
    * Get original post times again for that granularity - also use a default if not present
* ~~Keys plugin~~
    * ~~Update to exclude code blocks like RewriteRules~~
    * ~~Update source files to use new syntax~~
* Image resizing
    * To theme?
    * To spec?
* Doodads
    * File type icons (clear-photoshops-swatch-palette, visual-studio-cuddly-braces)
    * External link indicators
    * Syntax highlighting extras (line numbers, copy, etc)
    * Link buttons
* Fix/implement functionality or content for:
    * ~~host-based-ad-blocking - PHP snippet~~
    * ~~generative-art-google-logo - image captions~~
    * the-importance-of-order - image resizing/linking (if necessary, maybe just restrict size unless explicitly linking higher res)
* Other handy tags
    * ~~`<!-- more -->`~~ - works in summary pages and feed
    * ~~`<!--TOC-->`~~ - now [TOC]
* ~~Compile tags/cats~~
    * ~~group pages together~~
    * Generate pages for each
* ~~All posts pagination - reverse chrono~~
    * `/page/1/` redirect to `/`
* Comment system iframe
* LESS?
* ~~Dark mode, light mode~~
    * selector
* Responsive design
* Process gallery sections using bs4 - keep JS minimal
* Replicate existing site "close enough"
* Responsiveness
