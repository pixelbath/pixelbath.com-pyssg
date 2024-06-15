---
title: "Host-Based Ad Blocking"
date: 2009-01-23
categories: programming
tags: ad block, apache, hosts, rewritecond, rewriterule
---

To block ads on the web, we need to catch requests to a particular ad server and send them to our local server. We do this by adding an entry to the [hosts file](https://en.wikipedia.org/wiki/Hosts_file). The hosts file on a computer system gives the system information about where to find a computer on the network by mapping hostnames to IP addresses. For our purposes, we will be taking advantage of this by routing requests to ad servers from webpages to our personal system.

These steps will require that you have Apache HTTP server (or IIS with ISAPI_rewrite, something that can rewrite URLs) running on your local machine (or on a system with low latency, possibly on your network).

<!-- more -->
First, we will need to edit the hosts file, and add an entry in the form `127.0.0.1 ad.example.com`. If you are running Windows, examples should already be present in the hosts file. On Windows systems, this file can be found in `%WINDOWS%\\system32\\drivers\\etc\\hosts`, on Linux systems in `/etc/hosts`, and in OSX 10.2 and later in `/private/etc/hosts`.

So how do we get the hostname of an ad server? We can do this several ways, but you have to work for it just a little bit (I know, AdBlock makes it so easy). Since I am a web developer, I usually have the Firebug extension running (now using Firefox's native developer tools), so I just click "Inspect" and the element is highlighted in the source code, usually with the URL of the server right there for me.

If you don't have or don't need Firebug, you can go the "view source" route. I have found the easiest way using this method is to search for some adjacent text you see in the rendered page, and look around for included Javascript files or hotlinked images. Most of the time the ad is easy to see. For included Javascript files that build the ad image, just block the whole server, and they won't be able to render the ad, making the image server irrelevant. Often, ad servers will use several host names, requiring multiple entries in the hosts file.

If you're using Firefox or Internet Explorer, you can usually right-click an image and select Properties to get information about an image's location. Chrome seems to not want to give you that information easily, and selecting "Inspect Element" usually gives me mixed results, and a Webkit inspector that is surprisingly shoddy and works about three quarters of the time for me.

Once we've created the entry in the hosts file, we can test by closing all browser windows to force a reload of the file, then opening the ad server URL. If it goes to our local server instead of the ad server, we've successfully blocked the ad server across the entire operating system. Since we're handling a bunch of HTTP requests anyway, why not do something with them?

I created a page that shows the word "Blocked" and the hostname instead of the Apache 404 error page, but I don't want it displayed as my 404 URL for everything. I tried this, and it was problematic. I forget why.

To get our page handling all these misdirected requests, we'll use some basic URL rewriting. You may need to adjust the example to suit your development environment, as this will take over all requests to your local server. This is the .htaccess file I have on my development machine's DocumentRoot:

```apacheconf
RewriteEngine on

RewriteCond %{HTTP_HOST} !^localhost* [NC]
RewriteRule (.+) index.php L
```

The `RewriteCond` takes any request that is not for localhost and sends it to the `RewriteRule`, which directs all requests to `index.php`:

Blocked

I styled my block page in a nice light blue, so it shows up unobtrusively in ad-blocked pages. At the same time, you can easily see which items have been blocked. Since it replaces content that would otherwise be served from elsewhere, it doesn't break page layout.

The advantage to blocking ads this way is that since I have my hosts file in a list of shortcuts, I can open it up, add an entry for an ad server, and close it. Since it is then blocked at the operating system level, any browser run from that system will respect the block.

That's it! Happy ad-free surfing!