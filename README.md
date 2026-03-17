# PySSG

A small static site generator written in Python, based extemely heavily off [this static site generator](https://github.com/theacodes/blog.thea.codes/) by [Thea Flowers](https://thea.codes/). My goals in this project are [similar to hers](https://blog.thea.codes/a-small-static-site-generator/): to have my own thing while keeping it minimalistic. I looked into other generators like Jekyll and even Eleventy, but they all felt like they were just trying to do too much or be a generic solution.

Thanks, Thea!

## Requirements
* [uv](https://docs.astral.sh/uv/)
  * macOS: `brew install uv`
  * Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  * Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
* `uv sync`

## Build
* `uv run build.py`
* Site will be in the `/output` folder

# Features
- Various `tag/tagname` and `category/categoryname` similar to WordPress
- Write in Markdown with FrontMatter metadata
- Text to Emoji: text in source becomes emoji

## Page format
Pages are regular Markdown documents in the `src/pages/` folder.

Page title is Heading 2 (`##`), pages look like this:
```
## Contact

Contact page content

### An H3 heading
```

### Table of Contents

For longer documents, a table of contents with clickable heading links can be inserted with the string `[TOC]` on its own line.

## Post format
This was built to replace a WordPress blog, so everything needed to generate various metadata links is contained in the Markdown filename combined with FrontMatter blocks at the top of each post:


As an example, for the URL `2011/03/after-effects-fullscreen-preview/`, the URL slug (the text bit) is provided by the filename `after-effects-fullscreen-preview.md`. The date portion, along with categories and tag data is provided by a FrontMatter block at the top of the file:
```yaml
---
title: 'After Effects: Fullscreen Preview'
date: 2011-03-03
categories: design, video
tags: 1080p, after effects, backslash, hdtv
---
```

The remainder of the document is Markdown. The template system takes care of the post title link, category/tag links, etc.

### Post summary

The optional special tag `<!-- more -->` can be inserted on its own line to demarcate the post summary region. Content before this tag will be used in aggregate pages (`/page/#/` and `/category/category-name`). Most useful after a short paragraph or two. If omitted, the entire post is used in aggregate pages.

## Text to Emoji

In cases where an emoji keyboard isn't available, the following strings are converted to emoji:
- `:))` -> 😆
- `:)` -> 🙂
- `;)` -> 😉
- `:D` -> 😁
- `:(` -> 🙁
- `:|` -> 😐
- `:/` -> 😕
- `:P` -> 😛
- `;P` -> 😜
- `:melt:` -> 🫠


## TODO
* ~~Base path to re-path all images to a common root~~
    * ~~will also need to parse relative/absolute image links in MD~~
* ~~Emoji plugin~~
* ~~Navigation (links looks like WordPress routes)~~
    * ~~Pagination - link format is `/page/pageNum/`~~
        * ~~First page has no "Newer Posts", last has no "Older Posts"~~
    * ~~Each post emits tags as links at the bottom - each tag links to `/tag/tag-name/`~~
    * ~~Each post lists categories below the title - each cat links to `/category/category-name/`~~
    * ~~Each post in the multi-post views links to its individual page~~
* ~~RSS~~ validates
    * Get original post times again for that granularity - also use a default if not present
* ~~Keys plugin~~
    * ~~Update to exclude code blocks like RewriteRules~~
    * ~~Update source files to use new syntax~~
* Theme system
    * ~~alignleft/alignright image max width (400px)~~
    * ~~aligncenter image max width~~
* Doodads
    * ~~File type icons (clear-photoshops-swatch-palette, visual-studio-cuddly-braces)~~
    * External link indicators
    * Syntax highlighting extras (line numbers, copy, etc)
    * ~~Link buttons~~
* ~~Fix/implement functionality or content for:~~
    * ~~host-based-ad-blocking - PHP snippet~~
    * ~~generative-art-google-logo - image captions~~
    * ~~the-importance-of-order - image resizing/linking (if necessary, maybe just restrict size unless explicitly linking higher res)~~
* ~~Other handy tags~~
    * ~~`<!-- more -->`~~ - works in summary pages and feed
    * ~~`<!--TOC-->`~~ - now [TOC]
* ~~Compile tags/cats~~
    * ~~Generate pages for tags - `/tag/tag-name`~~
    * ~~Generate pages for cats - `/category/category-name`~~
* ~~All posts pagination - reverse chrono~~
    * `/page/1/` redirect to `/` - .htaccess?
* Comment system iframe
* LESS?
* ~~Dark mode, light mode~~
    * selector
* Responsive design
* Process gallery sections using bs4 - keep JS minimal
* ~~Replicate existing site "close enough"~~
