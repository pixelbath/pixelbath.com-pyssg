
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

post_sources = pathlib.Path('.').glob('src/posts/*.md')
output_folder = './output'
output_static = output_folder + '/static'
output_images = output_folder + '/images'
webroot = '../..'

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

if not os.path.exists(output_folder):
    os.makedirs(output_folder)
if not os.path.exists(output_static):
    os.makedirs(output_static)
if not os.path.exists(output_images):
    os.makedirs(output_images)

def render_markdown(content: str) -> str:
    markdown_.reset()
    content = markdown_.convert(content)
    content = highlighting.highlight(content)
    return content

import pathlib

def render_page_folder(pages_path, output_folder):
    def process_file(source, relative_path):
        print(f"Processing page {source}")
        content = render_markdown(source.read_text())
        output_path = pathlib.Path(output_folder) / relative_path / f"{source.stem}/index.html"
        
        # ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        template = jinja_env.get_template('page.html')
        rendered = template.render(title='Title', description='', content=content)
        with output_path.open('w') as f:
            f.write(rendered)

    def traverse_folder(folder, relative_path=""):
        for item in folder.iterdir():
            if item.is_file() and item.suffix == '.md':
                process_file(item, relative_path)
            elif item.is_dir():
                traverse_folder(item, os.path.join(relative_path, item.name))

    base_folder = pathlib.Path(pages_path)
    traverse_folder(base_folder)

render_page_folder('src/pages/', './output/')

for source in post_sources:
    print(f"Processing post {source}")
    post = frontmatter.load(str(source))

    # set up post path
    # Path("{}/{}/".format(output_folder, source.stem)).mkdir(parents=True, exist_ok=True)
    content = render_markdown(post.content)

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