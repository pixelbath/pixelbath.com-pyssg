---
title: "C#: Value does not fall within the expected range"
date: 2020-03-30
categories: programming
tags: csharp, quick tip
---

To save anybody from a fruitless internet search, the default message for ArgumentException is the phrase "Value does not fall within the expected range". This error may be returned from various sources, but in my case it was an explicit throw:

```c#
if (someInvalidValue)
{
throw new ArgumentException();
}
```

So if this error is bubbling up, it's an `ArgumentException`.