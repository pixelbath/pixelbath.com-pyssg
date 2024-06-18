---
title: "The Importance of Order"
date: 2019-03-30
categories: miscellany, open source software
tags: blender, command line
---

The order of things is important; even moreso when those things are command line arguments.

<img alt="the venerable Blender default cube" class="aligncenter" src="../images/default-cube-render.png">

After spending way too long (~30 minutes) trying to figure out why my background Blender renders were producing default cubes when that is clearly not what is in the scene, I finally looked at the console output and understood.

`blender --background --python script.py myfile.blend`

What this command does is tells Blender, "Load into memory as a background process and run script.py (which changes some settings and starts a render). _Then_ load myfile.blend." Once the file is loaded, background Blender exits.

In the proper order:

`blender myfile.blend --background --python script.py`
