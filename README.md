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

Full post will be linked with a "Read more" button. Clicking it leads to an anchor where the tag was placed.

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
- `:heart:` -> ❤️

## TODO

* Doodads
    * External link indicators
    * Syntax highlighting extras (line numbers, copy, etc)
* Comment system?
* ~~Dark mode, light mode~~
    * selector
