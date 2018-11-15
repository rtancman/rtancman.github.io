---
layout: post
title: Setup de maquina para devs
subtitle: Como automatizar o setup da sua máquina utilizando dotfile.
author: Raffael Tancman
date: 2018-11-14 19:21:00 -0300
background: '/img/posts/2018/11/setup-de-maquina-para-devs.png'
comments: true
shareBar: true
categories: 
    - "soudev"
    - "setup"
---


Realizar o setup e deixar a máquina do seu jeito é um trabalho bem legal de ser feito mas quando você precisa fazer a mesma coisa mais de 1x começa dar aquela “preguiça do bem” aquela que te faz pensar.

> Porque não automatizar este processo?

Seguindo nessa linha de facilitar a minha vida ao trocar de máquina resolvi criar o meu dotfiles. Ou seja dotfiles nesse contexto é um arquivo que facilita a instalação e configuração de suas ferramentas preferidas. Ou seja é pessoal mas você pode verificar o que os outros desenvolvedores estão usando e se inspirar e testar essas ferramentas no seu dia a dia. Neste link do github [https://dotfiles.github.io/](https://dotfiles.github.io/) você tem alguns exemplos.

Para criar esta configuração você pode usar qualquer tipo de linguagem ou ferramentas para escrever este script. No meu caso eu acabei escolhendo [Shell script](https://en.wikipedia.org/wiki/Shell_script) utilizando o interpretador bash. Shell script é uma linguagem de script usada em vários sistemas operacionais, com diferentes dialetos, dependendo do interpretador de comandos utilizado. Um exemplo de interpretador de comandos é o bash, usado na grande maioria das distribuições GNU/Linux.

Este scritp esta no [meu github](https://github.com/rtancman) no repositório [https://github.com/rtancman/dotfiles](https://github.com/rtancman/dotfiles). No meu dotfiles você irá encontrar scripts para sistemas Debians Like, Fedora e OSX. Atualmente o meu SO preferido é o fedora e por este motivo ele é o mais atualizado no meu projeto. Caso você precise de uma configuração específica para o seu SO, pode se inspirar neste projeto e em outros para criar o seu dotfiles. Sinta-se a vontade também para forkar e me ajudar a manter essas configurações atualizadas PRs são sempre bem vindos.

No meu dotfiles você vai encontrar as seguintes ferramentas:

**Aplicações**
- meetfranz
- chrome
- Slack
- Skype
- drawio
- OBS Project Studio
- Postman
- GnuCash
- GIMP
- Linphone

**Editores**
- vim + tmux, gvim e vim-bootstrap
- sublimetext3
- atom
- vscode
- pycharm
- Android Studio

**Linguagens**
- ruby com rvm
- python com pyenv
- js com nvm
- go com goenv
- Java
- php


**Bancos**
- sqlite
- postgresql, pgadmin
- mysql, workbench
- mongodb
- robomongo
- redis

**Clientes**
- heroku
- apex

**Tools**
- docker
- docker-compose
- flatpak
- jq
- direnv
- tmux
- teamviewer
- zeal
- filezilla
- vlc
- ngrok
- git-flow
- git-flow-completion
- git
- svn
- mercurial


Para utilizar o meu dotfiles basta seguir as seguintes instruções:

1.  Clonar o repositório  
2.  Rodar no seu SO

```bash
$ git clone git@github.com:rtancman/dotfiles.git

# Run MacOSX
$ bash main.sh -u YOUR_LOCAL_USER

# Run linux
$ sudo bash main.sh -u YOUR_LOCAL_USER
```

Grande Abraço

