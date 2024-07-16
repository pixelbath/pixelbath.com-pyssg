A small static site generator written in Python, based extemely heavily off [this static site generator](https://github.com/theacodes/blog.thea.codes/) by [Thea Flowers](https://thea.codes/). My goals in this project are [similar to hers](https://blog.thea.codes/a-small-static-site-generator/): to have my own thing while keeping it minimalistic. I looked into other generators like Jekyll and even Eleventy, but they all felt like they were just trying to do too much or be a generic solution.

Thanks, Thea!

## Requirements
* Python 3
* `pip install markdown python-frontmatter jinja2 pygments bs4 lxml`

## Build
* `python build.py`
* Site will be in the `/output` folder

## TODO
* Base path to re-path all images to a common root
    * will also need to parse relative/absolute image links in MD
* Emoji plugin
* RSS
* Keys plugin
    * Update to exclude code blocks like RewriteRules
* Paths for things like:
    * Tutorials
    * About
    * Work - maybe make this a single page
* Image resizing
    * To theme?
    * To spec?
* Link classes - buttons, specifically
* Fix/implement functionality or content for:
    * clear-photoshops-swatch-palette - styled button icon
    * host-based-ad-blocking - PHP snippet
    * generative-art-google-logo - image captions
    * the-importance-of-order - image resizing/linking (if necessary, maybe just restrict size unless explicitly linking higher res)