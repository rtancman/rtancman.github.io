---
layout: post
title: Vim e tmux
subtitle: Minha configuração de trabalho.
author: Raffael Tancman
date: 2018-11-23 19:28:00 -0200
background: '/img/posts/2018/11/vim-e-tmux-minha-configuracao.jpg'
comments: true
shareBar: true
categories:
    - "soudev"
---


Sempre programando com outras ferramentas de fato resolvi dar uma chance ao [Vim](https://en.wikipedia.org/wiki/Vim_(text_editor)). Com os plugins ele vira uma baita de uma ferramenta para se trabalhar. Sobre o [tmux](https://en.wikipedia.org/wiki/Tmux) foi um caso de amor e ódio. Comecei acompanhar os amigos aqui do time quando estávamos “pareando” e resolvi de fato testar no dia a dia.

## Vim

Wiki: [https://en.wikipedia.org/wiki/Vim_(text_editor)](https://en.wikipedia.org/wiki/Vim_(text_editor))

É um editor de texto clonado a partir do [Vi](https://pt.wikipedia.org/wiki/Vi) que pode ser utilizado tanto no terminal ou como uma aplicação gráfica como no gvim além de ser um software livre de código aberto.

Para aprender sobre o vim recomendo os seguintes sites:

-   [https://thoughtbot.com/upcase/vim](https://thoughtbot.com/upcase/vim)

-   [https://vim-adventures.com/](https://vim-adventures.com/)

A parte que eu gosto desse editor a sua simplicidade, leveza e o além de facilmente rodar a minha configuração em um servidor ou em outra máquina. Outro ponto favorável é sua gama de plugins. Neste site [vim awesome](https://vimawesome.com/) você consegue buscar e encontrar plugins. Esta parte pode se tornar um pouco trabalhosa e por este motivo eu comecei configurando o meu Vim com base no projeto [vim-bootstrap](https://vim-bootstrap.com/). Este projeto facilita a configuração sugerindo plugins ideias a várias linguagem de programação.

Toda sua configuração do vim fica em um arquivo na sua home que é o ~/.vimrc . [Aqui](https://github.com/rtancman/dotfiles/blob/master/sh/common/vim-bootstrap/main.sh) eu acabei automatizando esse processo de instalação do vim-bootsrap onde ele gera essas configurações e salva no .vimrc na home da sua máquina. Além desse arquivo eu crio mais 2 arquivos que são os ~/.vimrc.local e o ~/.vimrc.local.bundles . Eu gerei estes arquivos para facilitar a alteração de algumas configurações além do vim-bootstrap sem correr o risco de um sobrescrever o outro.

Conteúdo do meu ~/.vimrc.local
Neste arquivo eu coloco outras configurações para o meu vim além das que existem no ~/.vimrc.

```
" Config
" set relativenumber
set nrformats+=alpha
let g:NERDTreeMapOpenInTabSilent = 'T'

" Ruby Syntastic
set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*
let g:syntastic_check_on_open = 0
let g:syntastic_check_on_wq = 1
let g:syntastic_ruby_checkers = ['rubocop', 'reek']
let g:vimrubocop_config = '.rubocop.yml'
let g:reek_on_loading = 0

" Remove Trailing Whitespace
nnoremap <silent> <F5> :let _s=@/ <Bar> :%s/\s\+$//e <Bar> :let @/=_s <Bar> :nohl <Bar> :unlet _s <CR>

" vim-javascript
augroup vimrc-javascript
autocmd!
autocmd FileType javascript,javascript.jsx set tabstop=2|set shiftwidth=2|set expandtab softtabstop=2
augroup END

" Vim autoresize
autocmd VimResized * :wincmd =
" zoom a vim pane, <C-w>= to re-balance
nnoremap <leader>- :wincmd _<cr>:wincmd \|<cr>
nnoremap <leader>= :wincmd =<cr>
```

Conteúdo do meu ~/.vimrc.local.bundles
Neste arquivo eu inclou outros plugins além das que existem no ~/.vimrc.
```
" Plugins
Plug 'wakatime/vim-wakatime'
Plug 'ngmy/vim-rubocop'
Plug 'rainerborene/vim-reek'
Plug 'terryma/vim-multiple-cursors'
Plug 'mxw/vim-jsx'
" Plug 'w0rp/ale'
Plug 'christoomey/vim-tmux-navigator'
```

## Tmux

É um multiplexador de terminais para sistemas Unix like. Ou seja conseguimos abrir vários terminais no mesmo terminal. Além disso, conseguimos “salvar” o estado atual de cada sessão aberta no terminal e retomar de onde paramos. No nosso dia a dia abrimos varios terminais para executar diversas ações e é ae que o tmux entra para facilitar a sua vida. Ele se torna uma ferramenta muito poderosa usada em conjunto com o Vim.

Para aprender sobre o tmux recomendo os seguintes sites:

-   [https://thoughtbot.com/upcase/tmux](https://thoughtbot.com/upcase/tmux)

-   [https://gist.github.com/henrik/1967800](https://gist.github.com/henrik/1967800)

-   [https://lukaszwrobel.pl/blog/tmux-tutorial-split-terminal-windows-easily/](https://lukaszwrobel.pl/blog/tmux-tutorial-split-terminal-windows-easily/)

Como o vim ele suporta diversas configurações e isso que faz ele ficar bem produtivo no seu dia a dia. Abaixo eu estou compartilhando as minhas que acabei adotando após finalizar o curso da Upcase.

Conteúdo do meu ~/.tmux.conf
```
unbind C-b
set -g prefix C-s
set -g base-index 1
set -g renumber-windows on
bind-key -r C-s send-prefix
bind-key r source-file ~/.tmux.conf \; display-message "~/.tmux.conf reloaded"
set-option -g default-terminal "screen-256color"
set-option -g status-keys "emacs"
#set-option -g status-bg '#666666'
#set-option -g status-fg '#aaaaaa'
set-option -g status-left-length 50
set-option -g status-right " #(date '+%a, %b %d - %I:%M') "
bind-key - split-window -v -c '#{pane_current_path}'
bind-key \ split-window -h -c '#{pane_current_path}'

# Fine adjustment (1 or 2 cursor cells per bump)
bind -n S-Left resize-pane -L 2
bind -n S-Right resize-pane -R 2
bind -n S-Down resize-pane -D 1
bind -n S-Up resize-pane -U 1

# Coarse adjustment (5 or 10 cursor cells per bump)
bind -n C-Left resize-pane -L 10
bind -n C-Right resize-pane -R 10
bind -n C-Down resize-pane -D 5
bind -n C-Up resize-pane -U 5
bind c new-window -c "#{pane_current_path}"
bind-key b break-pane -d
bind-key C-j choose-tree

# Use vim keybindings in copy mode
setw -g mode-keys vi

# Setup 'v' to begin selection as in Vim
bind-key -T copy-mode-vi v send-keys -X begin-selection
bind -T copy-mode-vi y send-keys -X copy-pipe-and-cancel 'xclip -in -selection clipboard'

# Smart pane switching with awareness of Vim splits.
# See: https://github.com/christoomey/vim-tmux-navigator
is_vim='echo "#{pane_current_command}" | grep -iqE "(^|\/)g?(view|n?vim?)(diff)?$"'
bind -n C-h if-shell "$is_vim" "send-keys C-h" "select-pane -L"
bind -n C-j if-shell "$is_vim" "send-keys C-j" "select-pane -D"
bind -n C-k if-shell "$is_vim" "send-keys C-k" "select-pane -U"
#bind -n C-l if-shell "$is_vim" "send-keys C-l" "select-pane -R"
bind -n C-\ if-shell "$is_vim" "send-keys C-\\" "select-pane -l"

# Quickly view system & process info in htop
bind-key h split-window -h "htop"

# Quickly edit todo list
bind-key t split-window -h "vim ~/todo.md"

# Prompted join-pane
bind-key j command-prompt -p "join pane from: " "join-pane -h -s '%%'"

# Easily swap a pane (targeted by pane number) with the current pane
bind-key s display-panes\; command-prompt -p "pane #: " "swap-pane -t '%%'"

# Breaking Out Sessions
bind-key C-b send-keys 'tat && exit' 'C-m'
```

Neste post eu trouxe essas duas ferramentas que me ajudam bastante no meu dia a dia caso você tenha alguma configuração legal para o tmux ou vim compartilhe nos comentários.

Grande abraço!
