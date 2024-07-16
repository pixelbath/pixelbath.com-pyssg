
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

post_sources = pathlib.Path('.').glob('src/posts/*.md')
output_folder = './output'
output_static = output_folder + '/static'
output_images = output_folder + '/images'
webroot = ''

markdown_ = markdown.Markdown(
    extensions=[
        "toc",
        "tables",
        "abbr",
        "fenced_code",
    ]
)

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
)

# delete and re-create output folders
try:
    pathlib.Path(output_folder).unlink(missing_ok=True)
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
    markdown_.reset()
    content = markdown_.convert(content)
    content = highlighting.highlight(content)
    return content

def render_keybuttons(content: str) -> str:
    content = re.sub(r'\[ cmd \]', '<span class="key-button"><span class="unicode">⌘</span>', content, flags=re.IGNORECASE)
    content = re.sub(r'\[ ctrl \]', '<span class="key-button">Ctrl</span>', content, flags=re.IGNORECASE)
    content = re.sub(r'\[ alt \]', '<span class="key-button">Alt</span>', content, flags=re.IGNORECASE)
    content = re.sub(r'\[ shift \]', '<span class="key-button"><span class="unicode">⇧</span> Shift</span>', content, flags=re.IGNORECASE)
    content = re.sub(r'\[ option \]', '<span class="key-button"><span class="unicode">⌥</span> Option</span>', content, flags=re.IGNORECASE)
    content = re.sub(r'\[ (.) \]', r'<span class="key-button">\1</span>', content, flags=re.IGNORECASE)
    return content

def render_emoji(content: str) -> str:
    mapping = [
        (':))','😆'),
        (':)','🙂'),
        (';)','😉'),
        (':D','😁'),
        (':(','🙁'),
        (':|','😐'),
        (':/','😕'),
        (':P','😛'),
        (';P','😜'),
        (':melt:','🫠'),
    ]
    for k, v in mapping:
        content = content.replace(k, v)
    return content

import pathlib

def render_page_folder(pages_path, output_folder):
    def process_file(source, relative_path):
        print(f"Processing page {source}")
        content = render_markdown(source.read_text())
        content = render_keybuttons(content)
        content = render_emoji(content)
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

render_page_folder('src/pages/', output_folder)

for source in post_sources:
    print(f"Processing post {source}")
    post = frontmatter.load(str(source))

    # set up post path
    # Path("{}/{}/".format(output_folder, source.stem)).mkdir(parents=True, exist_ok=True)
    content = render_markdown(post.content)
    content = render_keybuttons(content)

    # set up paths and render content to template
    post['stem'] = source.stem
    output_path = pathlib.Path(output_folder) / post['date'].strftime('%Y/%m') / post['stem'] / 'index.html'
    template = jinja_env.get_template('post.html')
    rendered = template.render(post=post, content=content)

    # TODO: make this configurable
    rendered = rendered.replace('../images', f"{webroot}/images")
    rendered = rendered.replace('../static', f"{webroot}/static")

    # update image captions
    soup = BeautifulSoup(rendered, features='lxml')
    captions = soup.find_all('div', {'class': 'image-caption'})
    for caption in captions:
        rendered = rendered.replace(caption.text.strip(), f"<p class=\"caption-text\">{caption.text.strip()}</p>")
        # print(caption.text.strip())
    
    # ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")

    # write syntax highlighting stylesheet
    css = highlighting.get_style_css('native')
    pathlib.Path("{}/static/pygments.css".format(output_folder)).write_text(css)

    # copy over static stylesheet
    copy('./templates/style.css', "{}/static/".format(output_folder))

    # copy static folders that need to be in the output
    copytree('./src/images', "{}/images".format(output_folder), dirs_exist_ok=True)