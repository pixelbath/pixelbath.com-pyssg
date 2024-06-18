
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

sources = pathlib.Path('.').glob('src/posts/*.md')
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

for source in sources:
    print(f"Processing {source}")
    post = frontmatter.load(str(source))

    # set up post path
    # Path("{}/{}/".format(output_folder, source.stem)).mkdir(parents=True, exist_ok=True)
    content = render_markdown(post.content)

    # addtl pre-parsing of html
    post['stem'] = source.stem
    path = pathlib.Path("{}/{}/index.html".format(output_folder, post['stem']))
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
    
    path.write_text(rendered, encoding="utf-8")

    # write syntax highlighting stylesheet
    css = highlighting.get_style_css('native')
    pathlib.Path("{}/static/pygments.css".format(output_folder)).write_text(css)

    # copy over static stylesheet
    copy('./templates/style.css', "{}/static/".format(output_folder))

    # copy static folders that need to be in the output
    copytree('./src/images', "{}/images".format(output_folder), dirs_exist_ok=True)