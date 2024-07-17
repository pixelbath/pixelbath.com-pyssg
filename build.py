
import os
import pathlib
import markdown
import markdown.extensions.fenced_code
import frontmatter
import jinja2
import highlighting
from shutil import copy, copytree
from pathlib import Path
# import pixelbathdark
from pprint import pprint
from bs4 import BeautifulSoup
import re

output_folder = './output'
output_static = output_folder + '/static'
output_images = output_folder + '/images'
webroot = ''
posts_per_page = 6
posts_per_feed = 10

markdown_ = markdown.Markdown(
    extensions=[
        "toc",
        "tables",
        "abbr",
        "fenced_code",
        "extra",
    ]
)

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
)

categories = []
tags = []
posts_by_date = {}
posts_by_tag = {}
posts_by_category = {}

# delete and re-create output folders
try:
    # pathlib.Path(output_folder).unlink(missing_ok=True)
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
    content = highlighting.highlight(content)
    content = render_keybuttons(content)
    content = render_emoji(content)

    # TODO: make this configurable
    content = content.replace('../../images', f"{webroot}/images")
    content = content.replace('../images', f"{webroot}/images")
    content = content.replace('../static', f"{webroot}/static")

    # update image captions
    soup = BeautifulSoup(content, features='lxml')
    captions = soup.find_all('div', {'class': 'image-caption'})
    for caption in captions:
        caption_text = ''
        for caption_seg in caption.contents[1:]:
            caption_text += str(caption_seg)
        content = content.replace(caption_text, f"<p class=\"caption-text\">{caption_text.strip()}</p>")
    
    # TODO: update gallery layouts
    return content

def key_upper_repl(match):
    return '<span class="key-button">' + match.group(1).upper() + '</span>'

def render_keybuttons(content: str) -> str:
    content = re.sub(r'\[ cmd \]', '<span class="key-button"><span class="unicode">⌘</span>', content, flags=re.IGNORECASE)
    content = re.sub(r'\[ ctrl \]', '<span class="key-button">Ctrl</span>', content, flags=re.IGNORECASE)
    content = re.sub(r'\[ alt \]', '<span class="key-button">Alt</span>', content, flags=re.IGNORECASE)
    content = re.sub(r'\[ shift \]', '<span class="key-button"><span class="unicode">⇧</span> Shift</span>', content, flags=re.IGNORECASE)
    content = re.sub(r'\[ option \]', '<span class="key-button"><span class="unicode">⌥</span> Option</span>', content, flags=re.IGNORECASE)
    content = re.sub(r'\[ (.) \]', key_upper_repl, content, flags=re.IGNORECASE)
    return content

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
    ]
    for k, v in mapping:
        content = content.replace(k, v)
    return content

import pathlib

# build all non-blog pages using the folder layout in pages_path
def process_page_folder(pages_path: str, output_folder: str) -> None:
    def process_file(source, relative_path):
        # print(f"Processing page {source}")
        content = render_markdown(source.read_text())
        if content is None:
            return

        output_path = pathlib.Path(output_folder) / relative_path / f"{source.stem}/index.html"
        if source.stem.endswith('index'):
            output_path = pathlib.Path(output_folder) / relative_path / f"index.html"
        
        # ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        template = jinja_env.get_template('page.html')
        rendered = template.render(title='Title', description='', content=content)
        with output_path.open('w', encoding='utf-8') as f:
            f.write(rendered)

    def traverse_folder(folder, relative_path=""):
        for item in folder.iterdir():
            if item.is_file() and item.suffix == '.md':
                process_file(item, relative_path)
            elif item.is_dir():
                traverse_folder(item, os.path.join(relative_path, item.name))

    base_folder = pathlib.Path(pages_path)
    traverse_folder(base_folder)

# build all blog posts using frontmatter to structure backward-compatible permalinks
# also updates cumulative variables posts_by_date, posts_by_tag, posts_by_cat, post_tags, and post_cats for later use.
def process_post_folder(posts_path: str, output_folder: str) -> None:
    post_sources = pathlib.Path(posts_path).glob('*.md')

    for source in post_sources:
        post = frontmatter.load(str(source))
        posts_by_date[post['date']] = post

        post_tags = [x.strip() for x in post['tags'].split(',')]
        # tags = set().union(tags, post_tags)

        post_cats = [x.strip() for x in post['categories'].split(',')]
        # categories = set().union(categories, post_cats)

        content = render_markdown(post.content)
        # set up paths and render content to template
        post['stem'] = source.stem
        output_path = pathlib.Path(output_folder) / post['date'].strftime('%Y/%m') / post['stem'] / 'index.html'
        template = jinja_env.get_template('post.html')
        rendered = template.render(post=post, content=content)

        # ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered, encoding="utf-8")


# def render_post_summary(post: frontmatter.Post) -> str:
#     return None

# Create website Pages.
process_page_folder('src/pages/', output_folder)

# Create website Posts.
process_post_folder('src/posts/', output_folder)

# start pagination and re-sort everything by reverse chrono
page_counter = 1
page_number = 1
posts_by_date = sorted(posts_by_date.items(), reverse=True)
# print(posts_by_date)
# for post_date, post in posts_by_date:
#     output_path = pathlib.Path(output_folder) / 'page' / page_number / 'index.html'
#     print(output_path)


# write syntax highlighting stylesheet
css = highlighting.get_style_css('native')
pathlib.Path("{}/static/pygments.css".format(output_folder)).write_text(css)

# copy over static stylesheet
copy('./templates/style.css', "{}/static/".format(output_folder))

# copy static folders that need to be in the output
copytree('./src/images', "{}/images".format(output_folder), dirs_exist_ok=True)

# Generate RSS
# template = jinja_env.get_template('rss.xml')
# rendered = template.render(post=post, content=content)

# debug stuff
# print (f"Posts by date: {posts_by_date}")
# print (f"Posts by tag: {posts_by_tag}")
# print (f"All categories: {categories}")
# print (f"All tags: {tags}")
