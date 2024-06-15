---
title: ".htaccess Snippets"
date: 2009-05-29
categories: programming
tags: 301, apache, hotlinking, htaccess, redirect, rewritecond, rewriterule
---

Here are some .htaccess snippets I've had to use, and if you run your own site, blog, or some other third thing, you might find them useful.

**Moved from one URL to another:** My old blog url used to be verbose.pixelbath.com, and before that was pixelbath.com/verbose. Setting aside the notion that this blog moves around too much, the following snippet…

```apacheconf
RewriteEngine on
RewriteCond %{HTTP_HOST} ^verbose [NC]
RewriteRule ^(.*)$ https://www.pixelbath.com/blog/ [R=301,L]
```

…redirects any host name containing ‘verbose' will be redirected to the main blog URL. Useful because many sites had me linked to the old blog, and I didn't want to break their links too badly. Nothing fancy, so please note that this does not transfer url parameters. It only redirects requests with the single word ‘verbose' to the main blog URL.

**Using a single file to handle all URL requests:** If you've used almost any PHP <acronym title="Content Management System">CMS</acronym> or <acronym title="Model-View-Controller">MVC</acronym> framework such as CodeIgniter or CakePHP, you've probably used something like this for “search friendly URLs”:

```apacheconf
RewriteEngine On
RewriteBase /blog/
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule (.+) /blog/index.php L
```

What this does is start from the `/blog/` folder, and handle any requests under that. The first RewriteCond sets our rule to not apply to any physical files matching the request, and the second does the same for physical directories.

Once it passes the two conditions (a request in `/blog/` that is not a physical file or directory), it goes to the `RewriteRule`, which simply takes all matching requests and redirect them internally to `/blog/index.php`. This is not a browser redirect, so the user will still see the URL the way they found it, something like `http://example.com/blog/archive/foo`. I use this technique on the comics pages by parsing the URL segments into comic and page requests.

**Stop image and/or content hotlinking:** Some netizens are either not savvy with the way the Internet works, or don't give a crap because idiocy prefers the low-hanging fruit. Either way, I've actually got a few snippets for this purpose.

```apacheconf
RewriteEngine On
RewriteCond %{HTTP_REFERER} !^http://(.+\.)?myspace.com [NC,OR]
RewriteCond %{HTTP_REFERER} !^http://(.+\.)?blogspot.com [NC]
RewriteRule ^.*$ http://www.yourdomain.com/ [R,L]
```

The preceding snippet will block specific websites and their subdomains from hotlinking from your site, but will allow any other site not specified in your `.htaccess` file to do so. If you'd prefer to stick another image in place of the hotlinked one, this is easily done:

```apacheconf
RewriteEngine On
RewriteCond %{HTTP_REFERER} !^http://(.+\.)?yourdomain\.com/ [NC]
RewriteCond %{HTTP_REFERER} !^$
RewriteRule .*\.(jpe?g|gif|bmp|png)$ /images/horrifying-image.jpg L
```

This one will take any request with a referer not originating from your domain, or blank referers (because some users do legitimately blank their referer string), and redirect them to an image elsewhere on your site. This will work “inline” and display whichever image you specify on outside sites.

If you'd prefer to be plain and simple though, you can just set HTTP code 403 (Forbidden) on any image for any of the rewrites in this section. Simply replace the `RewriteRule` of each with:

```apacheconf
RewriteRule .*\.(jpe?g|gif|bmp|png)$ - F
```

Which simply sets any request for any image to 403 (Forbidden). Obviously, it should be used in conjunction with `RewriteCond`s.