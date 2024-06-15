---
title: "ROM Checksums and Headers"
date: 2019-08-05
categories: programming
tags: nex, nes
---

Lately I've been futzing around with classic game ROMs a bit more. Since nearly day one of Nesticle hitting the Internet, I've been obsessed with emulation of classic computer systems. I love playing old video games, and I love learning more about the internals of the systems I cut my teeth on back in the day.

But this post isn't about nostalgia; it's about organizing games, specifically ROM files. While I'm fairly certain I've got several discs (and old HDDs) filled with variously-complete ROM sets for various platforms, these were mostly collected from newsgroups _waaay_ back in the day and as a result have a wide variety of headers, possible trainers, and intros. Nowadays, even the Internet Archive maintains full sets of "no-intro" ROMs donated by people who stayed in the scene far longer than I did.

If you intend to organize such a non-trivial amount of games, you're gonna need some ROM utilities. The most well-known of these are clrmamepro, RomCenter, and RomVault. I'm sure there are others, but these are the big players. I'm not really going to speak about their various strengths/weaknesses, as that's a little outside the scope of this post.

What I actually want to discuss is how checksums are calculated using the "datfiles" provided by the No-Intro site's users. I had a hard time finding this information initially, so I'm putting it here for anyone else. Also, if I'm wrong, I'd love to be called out and told what I'm doing wrong.

I'm using the following:

* [No Intro NES ROM set](https://archive.org/details/no-intro-nintendo-nintendo-entertainment-system-20170618)
* [Dat-o-Matic Fulltitle NES datfile](https://datomatic.no-intro.org/index.php?page=download)
* [clrmamepro iNES header config](http://datomatic.no-intro.org/stuff/header_nes.zip) (not linked from anywhere I could see on the No-Intro site)

I only found the clrmamepro iNES header config far later than the rest of this info. This specific file is fairly sparse, and only has the following:

```xml
<detector>
<name>No-Intro NES Dat iNES Header Skipper</name>
<author>Yakushi~Kabuto</author>
<version>20070321</version>
<rule start_offset="10">
<data offset="0" value="4E4553"/>
</rule>
</detector>
```

Basically, take this to mean we're starting at offset `0x10` and reading to EOF (NES files aren't larger than `0x4e4553` bytes). Once I did this, my CRC32 checks started working. I'd normally stop there, but it looks like my MD5 and SHA-1 hashes are wrong. Adding the entire file back in fixes this, so…I'm not really sure why we're bothering to trim the header for only one check.

To sum up:

* **CRC32**:  `0x10` through EOF
* **MD5**:  entire file
* **SHA-1**: entire file
