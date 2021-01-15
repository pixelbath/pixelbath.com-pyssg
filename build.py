import os
import pathlib
import cmarkgfm
from cmarkgfm.cmark import Options as cmarkgfmOptions
import frontmatter
import jinja2
import highlighting

import pixelbathdark

sources = pathlib.Path('.').glob('src/*.md')
output_folder = './output'
output_static = output_folder + '/static'
output_images = output_folder + '/images'

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
)

if not os.path.exists(output_folder):
    os.makedirs(output_folder)
if not os.path.exists(output_static):
    os.makedirs(output_static)
if not os.path.exists(output_images):
    os.makedirs(output_images)

for source in sources:
    post = frontmatter.load(str(source))
    content = cmarkgfm.markdown_to_html_with_extensions(
        post.content,
        extensions=['table', 'autolink'],
        options=cmarkgfmOptions.CMARK_OPT_UNSAFE
    )
    # highlight here
    content = highlighting.highlight(content)

    # addtl pre-parsing of html
    post['stem'] = source.stem
    path = pathlib.Path("{}/{}.html".format(output_folder, post['stem']))
    template = jinja_env.get_template('post.html')
    rendered = template.render(post=post, content=content)
    
    path.write_text(rendered)

    # write syntax highlighting stylesheet
    css = highlighting.get_style_css('native')
    pathlib.Path("{}/static/pygments.css".format(output_folder)).write_text(css)