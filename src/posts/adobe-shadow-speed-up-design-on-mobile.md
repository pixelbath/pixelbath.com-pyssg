---
title: "Adobe Shadow: Speed Up Design on Mobile"
date: 2012-03-13
categories: design
tags: adobe, android, browser, creative cloud, css, edge inspect, html, ios, shadow
---

<div class="image-caption alignright">

<img alt="Adobe Shadow" src="/images/sd-logo.png" />

Adobe Shadow, not to be confused with DJ Shadow.
</div>

[Lee Brimelow](http://www.leebrimelow.com/adobe-shadow-for-multi-screen-web-development/) (evangelist for Adobe) has just posted a link to a new product released in Adobe Labs called ~~Shadow~~ **Adobe Edge Inspect**. This is an application that sits both on your development machine, and as an app for Android or iOS devices (iPod Touch, iPhone, iPad), enabling you to quickly debug the rendering of websites.

Basically, once you are running Shadow on both your development machine and your mobile device(s), the app will then pair the devices. You then browse websites using your development machine, and your devices browse along with you. No touching, no turning on, and no fiddling with mobile browsers.

Remote inspection of pages is another pretty amazing feature of Shadow. In the same vein as Firebug and Chrome/Safari's Developer Tools, the DOM can be inspected and edited directly on the device from the development machine.

While this is all very cool, the one downside (yet somehow an upside from Adobe's point-of-view) is that each device is actually making separate requests to the server for each URL. While this does keep the navigation of pages consistent with how they would actually be browsed, I can't imagine this working very well for sites that rely heavily on POST requests.

For designers, it seems to be quite an elegant solution to the problem of testing multiple variations on a single site design.

~~Check it out at the <a href="#">Adobe Labs</a>.~~

Edit: This is now called "[Adobe Edge Inspect](http://html.adobe.com/edge/inspect/)" is now included with Creative Cloud subscriptions.