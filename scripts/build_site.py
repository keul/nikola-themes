#!/usr/bin/env python

"""Inspect themes, create a JSON describing all the data."""

from __future__ import unicode_literals, print_function
import codecs
import glob
import json
import os

import colorama

from nikola import utils

import pygments
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

MINIMUM_VERSION_SUPPORTED = 6
MAXIMUM_VERSION_SUPPORTED = 7
ALL_VERSIONS = list(range(MINIMUM_VERSION_SUPPORTED, MAXIMUM_VERSION_SUPPORTED + 1))

def error(msg):
    print(colorama.Fore.RED + "ERROR:" + msg)

def theme_list():
    return sorted(['base', 'base-jinja', 'bootstrap', 'bootstrap-jinja', 'bootstrap3', 'bootstrap3-jinja'] + [theme.split('/')[-1] for theme in glob.glob("v{0}/*".format(MAXIMUM_VERSION_SUPPORTED))])

def build_site():
    data = {}
    for theme in theme_list():
        data[theme] = get_data(theme)

    data['__meta__'] = {'allver': ALL_VERSIONS}
    with open(os.path.join('output', 'theme_data.js'), 'wb+') as outf:
        outf.write("var data = " + json.dumps(data, indent=4, ensure_ascii=True, sort_keys=True))

def get_data(theme):
    data = {}
    data['chain'] = utils.get_theme_chain(theme, 'v7')
    data['name'] = theme
    readme = utils.get_asset_path('README.md', data['chain'], _themes_dir='v7')
    conf_sample = utils.get_asset_path('conf.py.sample', data['chain'], _themes_dir='v7')
    if readme:
        data['readme'] = codecs.open(readme, 'r', 'utf8').read()
    else:
        data['readme'] = 'No README.md file available.'

    if conf_sample:
        data['confpy'] = pygments.highlight(
            codecs.open(conf_sample, 'r', 'utf8').read(),
            PythonLexer(), HtmlFormatter(cssclass='code'))
    else:
        data['confpy'] = None

    data['bootswatch'] = ('bootstrap' in data['chain'] or
        'bootstrap-jinja' in data['chain'] or
        'bootstrap3-jinja' in data['chain'] or
        'bootstrap3' in data['chain']) and \
        'bootstrap3-gradients' not in data['chain']
    data['engine'] = utils.get_template_engine(data['chain'], 'v7')
    data['chain'] = data['chain'][::-1]

    data['allver'] = []
    for v in ALL_VERSIONS:
        if glob.glob('v{0}/*'.format(v)):
            data['allver'].append(v)

    return data

if __name__ == "__main__":
    colorama.init()
    print("Building theme_data.js")
    build_site()
