
import os
import pathlib
import datetime
import markdown
import markdown.extensions.fenced_code
import frontmatter
import jinja2
import highlighting
from shutil import copy, copytree, rmtree
import pathlib
from pathlib import Path
from pprint import pprint
from bs4 import BeautifulSoup
import re

RESET  = '\033[0m'
BOLD   = '\033[1m'
DIM    = '\033[2m'
CYAN   = '\033[36m'
GREEN  = '\033[32m'
YELLOW = '\033[33m'
MAGENTA= '\033[35m'
WHITE  = '\033[97m'
RED    = '\033[31m'

def print_header():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    bar = '─' * 45
    print(f"\n{CYAN}{bar}{RESET}")
    print(f"{BOLD}{WHITE}  make a pixelbath  {DIM}•{RESET}{BOLD}{WHITE}  {now}{RESET}")
    print(f"{CYAN}{bar}{RESET}\n")

print_header()

output_folder = './output'
output_static = output_folder + '/static'
output_images = output_folder + '/images'
webroot = ''
posts_per_page = 6
posts_per_feed = 10
theme = 'pixel'

markdown_ = markdown.Markdown(
    extensions=[
        "toc",
        "tables",
        "abbr",
        "fenced_code",
        "extra",
        "pymdownx.tilde",
    ]
)

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader([f'templates/{theme}', 'templates/base']),
)
jinja_env.globals['now'] = datetime.datetime.now()

categories = []
tags = []
posts_by_date = {}
posts_by_tag = {}
posts_by_category = {}

# delete and re-create output folders
try:
    rmtree(output_folder, ignore_errors=True)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, mode=0o777)
    if not os.path.exists(output_static):
        os.makedirs(output_static, mode=0o777)
    if not os.path.exists(output_images):
        os.makedirs(output_images, mode=0o777)
except OSError as e:
    print(f"Error clearing folder {output_folder}: {e.strerror}")
    exit()

def render_markdown(content: str) -> str:
    if content.startswith('#draft'):
        return None

    markdown_.reset()
    content = markdown_.convert(content)
    content = content.replace('<!-- more -->', '<span id="more"></span>')
    content = highlighting.highlight(content)
    content = render_keybuttons(content)
    content = render_filelinks(content)
    content = render_emoji(content)

    # TODO: make this configurable
    content = content.replace('../../images', f"{webroot}/images")
    content = content.replace('../images', f"{webroot}/images")
    content = content.replace('../static', f"{webroot}/static")

    # update image captions
    soup = BeautifulSoup(content, features='lxml')
    captions = soup.find_all('div', {'class': 'image-caption'})
    for caption in captions:
        # print(f"  Caption: {caption}")
        caption_text = ''
        # for those situations where there is 
        for caption_seg in caption.contents[1:]:
            caption_text += str(caption_seg)
        
        if len(caption_text) > 1:
            content = content.replace(caption_text, f"<p class=\"caption-text\">{caption_text.strip()}</p>")
    
    # TODO: update gallery layouts
    return content

def key_upper_repl(match):
    return '<span class="key-button">' + match.group(1).upper() + '</span>'

def render_keybuttons(content: str) -> str:
    content = re.sub(r'\[ cmd \]', '<span class="key-button"><span class="unicode">⌘</span></span>', content, flags=re.IGNORECASE)
    content = re.sub(r'\[ ctrl \]', '<span class="key-button">Ctrl</span>', content, flags=re.IGNORECASE)
    content = re.sub(r'\[ alt \]', '<span class="key-button">Alt</span>', content, flags=re.IGNORECASE)
    content = re.sub(r'\[ shift \]', '<span class="key-button"><span class="unicode">⇧</span> Shift</span>', content, flags=re.IGNORECASE)
    content = re.sub(r'\[ option \]', '<span class="key-button"><span class="unicode">⌥</span> Option</span>', content, flags=re.IGNORECASE)
    content = re.sub(r'\[ (.) \]', key_upper_repl, content, flags=re.IGNORECASE)
    return content

def render_filelinks(content: str) -> str:
    # only match downloads/ with a file extension
    def filelink_repl(match):
        href = match.group(1)
        text = match.group(2)
        ext = href.rsplit('.', 1)[-1].lower()
        return f'<a class="button-std file-icon icon-{ext}" href="{href}">{text}</a>'
    return re.sub(r'href="([^"]*downloads/[^"]+\.[^/"<>]{1,10})">(.*?)</a>', filelink_repl, content)

def render_emoji(content: str) -> str:
    mapping = [
        (' :))',' 😆'),
        (' :)',' 🙂'),
        (' ;)',' 😉'),
        (' :D',' 😁'),
        (' :(',' 🙁'),
        (' :|',' 😐'),
        (' :/',' 😕'),
        (' :P',' 😛'),
        (' ;P',' 😜'),
        (':melt:','🫠'),
        (':heart:','❤️'),
    ]
    for k, v in mapping:
        content = content.replace(k, v)
    return content

# build all non-blog pages using the folder layout in pages_path
def process_page_folder(pages_path: str, output_folder: str) -> None:
    def process_file(source, relative_path):
        raw = source.read_text()
        content = render_markdown(raw)
        if content is None:
            return

        title = next(
            (line.lstrip('#').strip() for line in raw.splitlines() if line.startswith('#')),
            source.stem
        )

        output_path = pathlib.Path(output_folder) / relative_path / f"{source.stem}/index.html"
        if source.stem.endswith('index'):
            output_path = pathlib.Path(output_folder) / relative_path / f"index.html"

        print(f"  {GREEN}{source}{RESET} {DIM}-> {output_path}{RESET}")

        # ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        template = jinja_env.get_template('page.html')
        rendered = template.render(title=title, description='', content=content)
        with output_path.open('w', encoding='utf-8') as f:
            f.write(rendered)

    def traverse_folder(folder, relative_path=""):
        for item in folder.iterdir():
            if item.is_file() and item.suffix == '.md':
                process_file(item, relative_path)
            elif item.is_dir():
                traverse_folder(item, os.path.join(relative_path, item.name))

    print(f"{CYAN}pages{RESET}")
    base_folder = pathlib.Path(pages_path)
    traverse_folder(base_folder)

# build all blog posts using frontmatter to structure backward-compatible permalinks
# also updates cumulative variables posts_by_date, posts_by_tag, posts_by_cat, post_tags, and post_cats for later use
def slugify(name: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', name.strip().lower()).strip('-')

def process_post_folder(posts_path: str, output_folder: str) -> None:
    post_sources = pathlib.Path(posts_path).glob('*.md')
    global posts_by_date, posts_by_tag, posts_by_category

    print(f"{CYAN}posts{RESET}")
    for source in post_sources:
        post = frontmatter.load(str(source))

        missing = [f for f in ('date', 'tags', 'categories') if not post.get(f)]
        if missing:
            print(f"  {RED}SKIP {source.name}: missing {', '.join(missing)}{RESET}")
            continue

        # build tag and category lists with slugs for linking
        post_tags = [{'name': t.strip(), 'slug': slugify(t)} for t in post['tags'].split(',') if t.strip()]
        post_cats = [{'name': c.strip(), 'slug': slugify(c)} for c in post['categories'].split(',') if c.strip()]
        post['tags_list'] = post_tags
        post['categories_list'] = post_cats

        content = render_markdown(post.content)

        # set up paths and render content to template
        post['stem'] = source.stem
        post['permalink'] = f"/{post['date'].strftime('%Y/%m')}/{post['stem']}/"
        post['summary'] = render_markdown(get_post_summary(post.content))
        output_path = pathlib.Path(output_folder) / post['date'].strftime('%Y/%m') / post['stem'] / 'index.html'

        posts_by_date[post['date']] = post

        # accumulate posts per tag and category
        for tag in post_tags:
            posts_by_tag.setdefault(tag['slug'], {'name': tag['name'], 'posts': {}})
            posts_by_tag[tag['slug']]['posts'][post['date']] = post
        for cat in post_cats:
            posts_by_category.setdefault(cat['slug'], {'name': cat['name'], 'posts': {}})
            posts_by_category[cat['slug']]['posts'][post['date']] = post

        print(f"  {GREEN}{post['title']}{RESET} {DIM}-> {output_path}{RESET}")
        template = jinja_env.get_template('post.html')
        rendered = template.render(post=post, content=content)

        # ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")

    # convert unsorted dict to a sorted dict because...python
    new_posts_by_date = {}
    for post_date in sorted(posts_by_date.keys(), reverse=True):
        new_posts_by_date[post_date] = posts_by_date[post_date]

    posts_by_date = new_posts_by_date

def get_post_summary(content: str) -> str:
    summary_index = content.find('<!-- more -->')
    if summary_index != -1:
        return content[:summary_index]
    else:
        return content

def markdown_heirarchy_down(in_content:str) -> str:
    out_content = in_content.replace('####', '#####')
    out_content = in_content.replace('###', '####')
    out_content = in_content.replace('##', '###')
    out_content = in_content.replace('#', '##')
    return out_content


# take a list of posts and generate pages of them
def process_pagination(base_path: str, posts: list, page_title: str = 'Posts') -> None:
    if base_path == '.':
        print(f"  {DIM}paginate {base_path}{RESET}")

    global posts_per_page
    total_posts = len(posts)
    total_pages = max(1, (total_posts - 1) // posts_per_page + 1)

    # resolve the base URL prefix for pagination links
    base_url = '/' if base_path == '.' else f'/{base_path}/'

    for page_number in range(1, total_pages + 1):
        start_index = (page_number - 1) * posts_per_page
        end_index = min(start_index + posts_per_page, total_posts)

        page_posts = []
        for key in list(posts.keys())[start_index:end_index]:
            post = posts[key]
            post['truncated'] = '<!-- more -->' in post.content
            post.content = render_markdown(get_post_summary(markdown_heirarchy_down(post.content)))
            page_posts.append(post)

        if page_number == 1:
            output_path = pathlib.Path(output_folder) / base_path / 'index.html'
            prev_url = None
        else:
            output_path = pathlib.Path(output_folder) / base_path / 'page' / str(page_number) / 'index.html'
            prev_url = base_url if page_number == 2 else f'{base_url}page/{page_number - 1}/'

        next_url = f'{base_url}page/{page_number + 1}/' if page_number < total_pages else None

        if base_path == '.':
            print(f"    {DIM}write {output_path}{RESET}")
        template = jinja_env.get_template('posts.html')
        rendered = template.render(
            posts=page_posts,
            page_title=page_title,
            page_number=page_number,
            total_pages=total_pages,
            prev_url=prev_url,
            next_url=next_url,
        )

        # ensure path exists, and write file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")

process_page_folder('src/pages/', output_folder)

process_post_folder('src/posts/', output_folder)

# pagination
print(f"{CYAN}pagination{RESET}  {DIM}{len(posts_by_date)} posts{RESET}")
process_pagination('.', posts_by_date)

# category/tag archive pages
print(f"{CYAN}categories{RESET}  {DIM}({len(posts_by_category)}){RESET}")
for slug, data in posts_by_category.items():
    print(f"  {MAGENTA}{data['name']}{RESET}: {YELLOW}{len(data['posts'])}{RESET}")
    process_pagination(f'category/{slug}', data['posts'], page_title=f"Category: {data['name']}")

print(f"{CYAN}tags{RESET}  {DIM}({len(posts_by_tag)}){RESET}")
for slug, data in posts_by_tag.items():
    print(f"  {MAGENTA}{data['name']}{RESET}: {YELLOW}{len(data['posts'])}{RESET}")
    process_pagination(f'tag/{slug}', data['posts'], page_title=f"Tag: {data['name']}")

# syntax highlighting stylesheet
css = highlighting.get_style_css('native')
pathlib.Path("{}/static/pygments.css".format(output_folder)).write_text(css)

# copy theme stylesheet; base stylesheet fallback
css_path = next(
    p for p in [f'./templates/{theme}/style.css', './templates/base/style.css']
    if os.path.exists(p)
)
copy(css_path, "{}/static/".format(output_folder))

# copy optional theme scripts
for script in ['gallery.js']:
    script_path = f'./templates/{theme}/{script}'
    if os.path.exists(script_path):
        copy(script_path, "{}/static/".format(output_folder))

# copy static folders that need to be in the output
copytree('./src/images', "{}/images".format(output_folder), dirs_exist_ok=True)

copy('./src/assets/favicon.png', output_folder)
copy('./src/.htaccess', output_folder)

# RSS
print(f"{CYAN}rss.xml{RESET}  {DIM}{len(posts_by_date)} posts{RESET}")
template = jinja_env.get_template('rss.xml')
rendered = template.render(posts=posts_by_date, last_updated=datetime.datetime.now(datetime.UTC))
output_path = pathlib.Path(output_folder) / 'feed.xml'
output_path.write_text(rendered, encoding="utf-8")

# debug stuff
# print (f"Posts by date: {posts_by_date}")
# print (f"Posts by tag: {posts_by_tag}")
# print (f"All categories: {categories}")
# print (f"All tags: {tags}")
