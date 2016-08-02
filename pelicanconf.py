#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from slugify import slugify

AUTHOR = u'Raffael Tancman'
AUTHOR_EMAIL = u'rtancman@gmail.com'
AUTHOR_PHONE = u'(21) 98352-4442'
AUTHOR_ADDRESS = u'Vargem Grande<br>Rio de Janeiro'
AUTHOR_MAPS = u'https://www.google.com.br/maps/place/R.+Manhua%C3%A7u+-+Vargem+Grande,+Rio+de+Janeiro+-+RJ/@-22.9810134,-43.4972055,17z/data=!3m1!4b1!4m5!3m4!1s0x9be7906db9a8c3:0x50b9b9d955b5aff2!8m2!3d-22.9810134!4d-43.4950168?hl=pt-br'
AUTHOR_MAPS_EMBED = u'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3673.163528563044!2d-43.49720548503303!3d-22.9810133849741!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x9be7906db9a8c3%3A0x50b9b9d955b5aff2!2sR.+Manhua%C3%A7u+-+Vargem+Grande%2C+Rio+de+Janeiro+-+RJ!5e0!3m2!1spt-BR!2sbr!4v1469383607808"'

SITENAME = u'rtancman'
SITEURL = 'http://rtancman.com.br/'
SITELOGO = 'http://s.gravatar.com/avatar/0115e99f9b12e4a630bcba1736967557?s=20'
FAVICON = '/images/common/favicon.png'
SITELOGO_SIZE = '20px'
HIDE_SITENAME = False

GITHUB_URL = u'https://github.com/rtancman'
TWITTER_URL = u'https://twitter.com/rtancman'
FACEBOOK_URL = u'https://facebook.com/rtancman'
LINKEDIN_URL = u'https://www.linkedin.com/in/rtancman'
DISQUS_SITENAME = u'rtancman'
ADDTHIS_PROFILE = u'rtancman'

BANNER_TITLE = u'rtancman'
BANNER_SUBTITLE = u'Software Developer'
BANNER_IMG = u'/theme/images/common/banner.jpg'
BANNER_LINK = u'#about'
DEFAULT_BANNER_LINK = u'#rtc-content'
BANNER_LINK_LABEL = u'Saiba Mais'
DEFAULT_BANNER_LINK_LABEL = u'Ir para o conteúdo'
BANNER_LOGO = 'http://s.gravatar.com/avatar/0115e99f9b12e4a630bcba1736967557?s=50'

ABOUT_ME = 'Olá sou Raffael Tancman, carioca, desenvolvedor poliglota. Trabalho com web desde 2008 e atualmente estou no M4U. Sou gamer e apaixonado por LOL. Além disso gosto de pegar ondas sempre que possível.'
ABOUT_ME_RECOMENDS = True
ABOUT_ME_RECOMENDS_LIST = [
    [
        {'person': 'Rodrigo de Castro', 'text': 'Raffael é um profissional excelente com quem tive o prazer de trabalhar por mais de um ano. É alguem que sempre corre atrás de soluções viáveis para os problemas, executando de maneira limpa e eficiente. Qualquer obstáculo em seu caminho era motivo para estudar mais e tornar seu trabalho ainda melhor, resolvendo a situação. Suas qualidades pessoais aumentam mais ainda suas qualidades de trabalho em grupo, sempre disponível para ajudar outros membros da equipe e ainda outras áreas da empresa com bom humor. Trabalharia com ele novamente com toda a certeza.'},
        {'person': 'Hugo Leonardo Costa e Silva', 'text': 'Tive uma excelente oportunidade de conhecer e trabalhar ao lado do Raffael Tancman. Um profissional incrivél, super enganjado e que sabe trabalhar em equipe. Várias vezes passamos por grandes desafios discutindo e implementando soluções fruto dessas discussões. Raffael sempre esteve disposto a ajudar tanto técnicamente quanto pessoalmente. Uma pessoa que hoje tenho o prazer de ter também em meus circulo de amigos. É com uma enorme segurança que recomendo e sempre vou recomendar o Raffael para qualquer projeto a qual participe.'},
    ],
    [
        {'person': 'Delermando Santos Miranda', 'text': 'Tanc é profissional excepcional com um perfil inovador e autocrítico e com uma incrível capacidade de motivar a todos e uma grande disposição para compartilhar seus conhecimentos. Um profissional que vive por aprender e buscar novos desafios, e que ainda irá crescer muito mais, tive o imenso prazer de trabalhar com ele. Pessoa a qual eu devo muito do profissional que sou hoje.'},
        {'person': 'Eduardo Luz', 'text': 'Trabalhei com Raffael durante 4 anos onde pude observar o empenho para entrega do resultado esperado pelo product owner e cliente final. Um ponto forte pessoal é sua capacidade de comunicação formal ou informal com a equipe. Na parte técnica se destaca sempre a busca pela melhor solucão que atenda as necessidades de cada projeto, visando menor custo de desenvolvimento e maior flexibilidade para implementação e manutenção. Realizamos muitos projetos interessantes neste período e com certeza trabalharia com ele novamente.'},
    ],
    [
        {'person': 'Luiz Gustavo Felício', 'text': 'Recomendo o Raffael por ser um profissional com amplo conhecimento em programação, dedicado e está sempre em busca de aperfeiçoamento e crescimento em sua carreira.'},
    ]
]

GOOGLE_ANALYTICS = ''
FACEBOOK_APPID = ''
GOOGLE_TAGMANAGER = 'GTM-RZN9'

# Articles
DISPLAY_ARTICLE_INFO_ON_INDEX = True
DISQUS_DISPLAY_COUNTS = True

# Caregories
CATEGORY_BANNER_IMG = u'/images/categories/odesafio10anos.jpg'
CATEGORY_BANNER_SUBTITLE = u'Veja todos os posts desta categoria.'

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
    # 'json_articles',
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


def makeimgbanner(category=''):
    return '/images/categories/' + slugify(str(category)) + '.jpg'


JINJA_FILTERS = {'imgbanner':makeimgbanner}