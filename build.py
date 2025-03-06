import os
import shutil
from jinja2 import Environment, FileSystemLoader

def build_site():
    # Create build directory
    if os.path.exists('build'):
        shutil.rmtree('build')
    os.makedirs('build')

    # Copy static files
    shutil.copytree('static', 'build/static', dirs_exist_ok=True)

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))

    # Render index.html
    template = env.get_template('index.html')
    rendered = template.render()
    
    with open('build/index.html', 'w') as f:
        f.write(rendered)

    # Copy other necessary files
    shutil.copy('_headers', 'build/_headers')
    shutil.copy('_redirects', 'build/_redirects')

if __name__ == '__main__':
    build_site()
