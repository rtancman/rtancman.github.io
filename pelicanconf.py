#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals


AUTHOR = u'Raffael Tancman'
AUTHOR_EMAIL = u'rtancman@gmail.com'
SITENAME = u'rtancman'
SITEURL = 'http://rtancman.github.io'
SITELOGO = 'http://s.gravatar.com/avatar/0115e99f9b12e4a630bcba1736967557?s=20'
SITELOGO_SIZE = '20px'
HIDE_SITENAME = True

GITHUB_URL = 'https://github.com/rtancman'
DISQUS_SITENAME = 'rtancman'

GOOGLE_ANALYTICS = ''
FACEBOOK_APPID = ''

TIMEZONE = 'America/Sao_Paulo'

PATH = 'content'

TIMEZONE = 'America/Sao_Paulo'

DEFAULT_LANG = u'pt'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (
    ('github', 'https://github.com/rtancman'),
    ('twitter', 'https://twitter.com/rtancman'),
    ('rss', 'feeds/all.atom.xml'),
)

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.8,
        'indexes': 0.5,
        'pages': 0.3
    },
    'changefreqs': {
        'articles': 'daily',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

# Plugins
PLUGIN_PATHS = [
    'pelican-plugins',
    # 'custom-plugins'
]

PLUGINS = [
    'gravatar',
    # 'pelican_alias', # para criar alias para artigos
    'sitemap',
    'pelican_youtube',  # funciona somente com arquivos rst
    'pelican_vimeo',  # funciona somente com arquivos rst
    'json_articles',
    'gzip_cache'  # deve ser o ultimo plugin
    # 'pdf', # funciona somente com arquivos rst

]

DEFAULT_PAGINATION = 10

# Theme
THEME = 'theme'

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# Geracao de PDF
# PDF_GENERATOR = True