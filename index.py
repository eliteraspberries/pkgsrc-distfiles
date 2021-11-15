import configparser
import os
import string
import sys


exclude = (
    '.git',
    'index.cfg',
    'index.html',
    'index.html.in',
    'index.py',
    'Makefile',
)


def find(dir):
    for entry in os.scandir(dir):
        if entry.name not in exclude:
            if os.path.isfile(entry.path):
                yield entry.path
            elif os.path.isdir(entry.path):
                for path in find(entry.path):
                    yield path
            else:
                pass


config = configparser.ConfigParser()
config.read('index.cfg')

with open('index.html.in', 'rt') as f:
    template = string.Template(f.read())

top = os.path.dirname(os.path.realpath(__file__))
files = [os.path.relpath(x, top) for x in find(top)]

body = '<ul>\n'
for x in files:
    body += '<li><a href="{}">{}</a></li>\n'.format(
        config['DEFAULT']['url'] + x,
        x,
    )
body += '</ul>\n'

html = template.safe_substitute(dict(
    **config['DEFAULT'],
    **{'body': body},
))
sys.stdout.write(html)
