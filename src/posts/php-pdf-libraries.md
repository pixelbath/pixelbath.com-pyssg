---
title: "PHP PDF Libraries"
date: 2015-04-01
categories: programming
tags: pdf, php
---


<div class="image-caption alignright">

<img alt="PDFs are easy! Like riding a...oh." src="/images/pdf-bike-crash.jpg" />

PDFs are easy! Like riding a...oh.
</div>

I wanted to do something I figured would be relatively simple. After all, we're doing it in .Net with a third-party library: Create a PDF with text from a database with vector graphics incorporated in the page. Turns out, it's pretty easy if you want a paid solution; numerous libraries exist for PHP that are non-free. If you insist on going free-only though, be warned: here be dragons (maybe).

Since this was a low-priority project (read as: for fun), I needed something that's free, preferably open source. I tried four of the top PHP PDF libraries, excluding libraries that are part of a larger framework (i.e. Zend Framework has fairly robust PDF functionality, from what I've read).

Skip to the bottom if you're not interested in a per-product breakdown.

## FPDF

I've used [FPDF](http://www.fpdf.org/) in the past. My invoice generator that I wrote over 5 years ago actually uses FPDF. The only problem is, that's around when the FPDF project was last updated, which means that all the things that bugged me in 2010 are still a problem.

For starters, the API is a bit messy. I mean, it's easy to get started, and if you want to just knock out a quick document that also happens to be a PDF, then great. This library is probably for you.

Embedding fonts, for me, was an exercise in frustration. FPDF needs a `.php` file containing glyph information for FPDF, and a `.z` file that contains the gzipped font. It doesn't always work, and there's no documentation explaining the errors. One issue that kept popping up was the failure to generate the `.z` file, which I ended up working around and creating myself.

More to the point of my immediate need, though: FPDF only supports JPEG, PNG, and GIF (if GD is installed). It's important for this project that the PDF contain only vector artwork, so that was a no-go from the start.

## TCPDF

[TCPDF](http://www.tcpdf.org/), on the other hand, does support vector graphics in the form of SVG, EPS, and even raw Illustrator (.ai) files. EPS and SVG import worked equally well, and the API is a bit cleaner than FPDF.

All fonts are imported via the `addTTFfont()` method, which is also used for OpenType or Type 1 fonts. After permissions were set up, there was no large issue importing the fonts, aside from TCPDF appearing to discard any hinting or kerning information. The documentation claims to allow for kerning, but the "tracking/kerning" demo actually only shows tracking and stretching. When I used an imported font, the kerning went completely random and I had no way to correct it. Seems to work fine with system fonts, though.

Since I needed vector-only artwork and a specific non-system font, TCPDF is out too.

On a marginally-related note, SourceForge is terrible. Please don't host code there.

## dompdf

I read that dompdf (name is lowercase; not just me being lazy) was good at converting HTML to PDFs with styling and background images (which requires GD installed) intact. I will admit, this worked surprisingly well in practice. The library includes an administration panel that allows direct font loading and conversion. This also worked well and I had no issues with it. Fonts seem to use their built-in kerning and tracking and came out looking clean.

The only problem I had with dompdf was that it has no support for vector image formats, even SVG. I hoped SVG support might be coming, since it's just more XML and is supported by most modern browsers as a valid image format.

If this project didn't absolutely require that there be vector-only artwork (it's for a print project), I'd drop everything else and use dompdf in a second. HTML and CSS is a hell of a lot easier to work with than PHP classes written by someone else.

## FPDI

So what if, I thought, I could use TCPDF to import the artwork to a "template" PDF (or just create the template myself), and use dompdf to create a text-only PDF, then merge the elements?

Enter [FPDI](http://www.setasign.com/products/fpdi/about/). It's a library made to work with existing PDF files. In the included examples, it even claims to work with TCPDF, but I found it to be less than clear about how this was working. There was some mention of templates, but I honestly couldn't figure out the whole thing.

It requires FPDF, but also claims to be able to use TCPDF instead? I don't know. I was unable to find any way to merge to pages into the same page, but plenty of examples of PDF concatenation (not what I want). Perhaps I missed something, but it seemed fairly opaque to me. Exit FPDI.

## Screw It


<div class="alignright">
<img alt="'Automating' comes from the roots 'auto-' meaning 'self-', and 'mating', meaning 'screwing'." src="/images/xkcd-automation.png" />
</div>

 In the end, I copped out and avoided the PDF generation entirely. Starting from an SVG exported from Illustrator, I'm stepping through the textual fields with DOMDocument and replacing the text before it's sent to the browser. The output is saved directly to the client's disk as an SVG file. When that SVG file is dragged into Illustrator, it's good to go. Illustrator includes glyph information with the SVG for its own use, so fonts are already set up and correct. I can then just save the file as a PDF with no modifications.

Sure, it's not the 100% automated plan I had in the beginning, but this still saves me at least 20 minutes each time I have to do this process. So, a win at least.

## Conclusions

The free offerings for PHP->PDF libraries kind of suck in their own unique ways. I found [dompdf](https://github.com/dompdf/dompdf) to be the slickest of all of them, for sure, but it has some limitations. I'd heard good things about the [PDF tool in Zend Framework](http://framework.zend.com/manual/1.12/en/zend.pdf.html), but I don't use Zend so haven't tried it.

[mPDF](https://mpdf.github.io/) is similar to dompdf in that it converts HTML (including CSS3) to PDF. The examples were ugly, but showed an impressive array of features. I didn't end up trying it out, but it looks decent.

If you're able to use a non-free solution, I can easily recommend [PDFLib](http://www.pdflib.com/products/pdflib-family/prices-licensing/), but it's not cheap ($1150 for a server license). I've used this in the past with different programming languages and found it to be solid. Since it's a mature product, there are hundreds of real-world examples of developers using it in actual projects.
