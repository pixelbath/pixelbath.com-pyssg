---
title: "Building a Static Site Generator"
date: 2026-05-02
categories: programming
tags: python, ssg, web, markdown
---

It's been a while since I posted... well, really _anything_ on my site. I don't know that I could give a single reason (I have considered the possibility I might be lazy, but discarded that idea); the problem is the sum of a number of reasons, some of which I'll lay at the feet of WordPress.

<!-- more -->

## WordPress
Don't get me wrong; WordPress does what it does fairly well, even when it's a shopping plugin or complete-site-design theme. I worked on plugins and themes for years in my freelance work; if something's not built-in (and a lot _is_), there's likely a dozen plugins for it, and you can easily pay someone to make it for you if there aren't. That being said, there were (probably still are) a _lot_ of third-party themes and plugins with security holes large enough to drive a truck through. Which is not an indictment of WordPress, per se, but made me wary of adding things in without vetting them first.

Around the time I stopped working with it as often, WordPress changed over to their "blocks" interface. My preference is to do most of my typing in plain text, then format it as needed. It reduces friction. For a while, I could change a setting through my custom theme's `functions.php`, but after a while felt like I was just fighting the platform. Really though, the fact that it was just _forced_ on me as a default was galling. I was also helping my wife set up a WordPress site with the Divi theme, and like many of its contemporaries, was an "all-in-one" theme that had its own page builder and content editors. These did not play well with the new WordPress changes, everything exploded in complexity, and that site was scrapped for other reasons, but still left a sour taste in my mouth.

So my own blog languished, and time passed. The idea behind static site generators isn't really new; I've seen people generate .html files from a folder of text files, but the ecosystem had just started to explode and I could see a lot of value in serving static content, which is what I was already doing with WordPress and a caching plugin that served static .html files behind the scenes. Which also felt...wasteful. I'm spinning up an entire PHP framework on every visit just to shunt to static HTML anyway. Every time I'd log in, WordPress would tell me about 10 new spam comments, a couple broken links, and release notes for the changes it made to itself. All that felt like maintaining a container for content instead of the content itself.

## Static site generators?

Fast-forward nearly a decade, and there's an entire landscape of fancy static site generators out there. Markdown is now everywhere, and I use it all the time: readme files, Visual Studio Code's preview panel, GitHub-flavored Markdown... a simple text format that encompasses about 90% of what I use HTML formatting for. So I started trying out various candidates in the site generator landscape.

I'd heard good things about **Hugo**; many posts on Hacker News about people converting their site to it and immediately being freed of the CMS grind. It bills itself as "the world's fastest framework for building sites." Since it's written in Go, that may be true for the build step, but looking through the documentation, it's clear this is a CMS wearing a different hat. For a basic post, you have "archetypes" which are basically FrontMatter + Markdown. Ok, that's fine. But now you can have _different_ archetypes with template to inform authors of _how_ new files should be written using that archetype. Ok, that's...less fine, but I don't _have_ to use the advanced features, right? So then we start getting into templates, and it's using Go templates, which...ok, time to learn a new template format, I guess. But it can also connect to data sources? And everything's managed using its own CLI? It's clear Hugo is far more than I will ever want or need.

What about **Jekyll**? Honestly, this seemed like it would work really well: while it also has its own CLI, everything looks very lightweight, Liquid is another templating language but looks similar enough to Jinja and Twig. But it's written in Ruby. Which means I have to install Ruby and dependencies. No shade to Ruby, but it's not an ecosystem I'm even remotely interested in, so it'll forever be a black box to me. Next choice, I suppose.

The name **Gatsby** was also floating around quite a bit at this time, so I checked that out. The documentation starts out almost immediately discussing GraphQL (uh oh), but it's optional at least. Even without GraphQL, though, it's already talking about data sources, hydration, and things I'm used to seeing in React. Oh, it _is_ using React. Next.

Ok, how about **Eleventy**? Documentation starts with "Eleventy requires a way to run JavaScript on your computer and we recommend Node.js." Hmm, not a deal breaker since I usually have Node installed somewhere. Builds clean, works well enough and is fast; I'm thinking we have a contender here! One of the things I wanted to do was replicate some of the plugins I'd built for my WordPress blog: emoji conversion from text smileys (think classic `:-)`-type stuff), "key buttons" for tutorials (so Ctrl+A could look like [ Ctrl ]+[ A ]), and support for table-of-contents shortcodes so I could place them wherever I want. For Eleventy, that meant either finding or writing plugins. In JS. I'm a frequent _user_ of Node scripts, but not so much a _developer_ of Node scripts. It quickly became clear that I'd be fighting this ecosystem too, and I kinda gave up on the idea of using someone else's site generator unless I just went with barebones output.

## D-I-Why
One day, browsing Hacker News, I came across a link to Thea Flowers' blog post _[A Small Static Site Generator](https://blog.thea.codes/a-small-static-site-generator/)_ and thought "well, this is basically _it_!" It's compact and easy to digest (less than 150 lines), does syntax highlighting, folder layout is sensible... with a few additions, I could make use of this. Her story was close to mine as well: trying to escape some other CMS, wanting to own your own code, and all that fun stuff.

I cloned her repository and moved a few things around, then coded in my various enhancements. While I stuck with a lot of her initial choices: `python-frontmatter`, `jinja2`, and `pathlib`, that's where my path started to diverge from hers. She used her own GitHub-flavored Markdown plugin to parse Markdown, but I found that I needed to pre-process mine to do some of the janky stuff I wanted to add, like the emoji substitution and "key buttons", so I went with the more-extensible `markdown` package. I also wanted to largely replicate the permalink structure that has been sitting on my site for _decades_ (yes, my site is that old), so that meant tags, categories, pagination, permalink generation, and a concept of posts versus pages. Surely it shouldn't take too long, right?

<div class="image-caption alignright">
<img alt="'Automating' comes from the roots 'auto-' meaning 'self-', and 'mating', meaning 'screwing'." src="/images/xkcd-automation.png" />

<p>"File xkcd-automation.png already exists. Overwrite?": Apparently this is not the first time I've used this joke.</p>

</div>

The big stuff I wanted: image galleries with custom lightbox, dark and light themes, and responsive. I also wanted to trim up the content (far too much "old man shouts at cloud" posts, mostly about Adobe), so knew I'd be using redirects and status codes.

I exported my posts from WordPress and cleaned them up in Markdown, doing my best to ensure I could still use `alignright` and similar layout selectors. Maybe I'll ditch these in the future, but they work well enough for now. I made some changes to Thea's templates to make it look more like my existing WordPress site, but with a focus on responsiveness and accessibility. At some point, I decided to stick a parallax starfield in the background that follows scrolling.

By this point, the script has grown to a not-as-lean-just-under-400-lines, but I'm now happy with it. Markdown documents turn into pages; Markdown with Frontmatter turns into posts, with any tags and categories automatically generating taxonomy; I've got syntax highlighting; I can inject free-form HTML wherever I want. Also ended up adding colors to the output, because that's how "keeping things minimal" works, right?

All of this leads to a far lower level of friction when it comes to writing: I write Markdown all the time, I don't mind tossing HTML where Markdown falls short, and I can generally fire-and-forget when it comes to deployment. Knowing what I know now, If I were to choose someone else's system, I'd probably go with Eleventy.

## Links

This page is rendered with the framework described above. It might not be your bag, but it just goes to show someone else's idea might be the necessary seed to build your own thing. You can find it on [GitHub](https://github.com/pixelbath/pixelbath.com-pyssg).

Other site generators:

- [Hugo](https://gohugo.io/)
- [Jekyll](https://jekyllrb.com/)
- [Gatsby](https://www.gatsbyjs.com/)
- [Eleventy](https://www.11ty.dev/)
