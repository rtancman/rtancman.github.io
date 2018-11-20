---
layout: post
title: Configurar VSCode para JavaScript
subtitle: Lista de plugins para trabalhar no Visual Studio Code.
author: Raffael Tancman
date: 2018-11-19 19:21:00 -0300
background: '/img/posts/2018/11/configurando-vscode-para-javascript-blur.jpg'
comments: true
shareBar: true
categories: 
    - "javascript"
---


[VSCode](https://code.visualstudio.com) é um editor de texto free desenvolvido pela [Microsoft](https://github.com/Microsoft). Neste editor podemos instalar e desenvolver diversos plugins para facilitar o desenvolvimento de sistemas em diversas linguagens. Atualmente eu utilizo o VSCode para trabalhar com [JavaScript](https://developer.mozilla.org/bm/docs/Web/JavaScript). Vale dar uma olhada nesse tópico [JavaScript in Visual Studio Code](https://code.visualstudio.com/docs/languages/javascript) onde temos diversas dicas de como melhorar o seu editor para trabalhar com JS.

No meu [dotfiles](https://github.com/rtancman/dotfiles) eu guardo essa [lista de plugins](https://github.com/rtancman/dotfiles/blob/master/sh/common/vscode/extensions) e neste artigo vou detalhar melhor o que cada um deles faz. Vamos a minha lista de plugins:

-   nathanchapman.JavaScriptSnippets
-   oderwat.indent-rainbow
-   CoenraadS.bracket-pair-colorizer
-   EQuimper.react-native-react-redux
-   TimonVS.ReactSnippetsStandard
-   wayou.vscode-todo-highlight
-   minhthai.vscode-todo-parser
-   wix.vscode-import-cost
-   humao.rest-client
-   formulahendry.auto-close-tag
-   formulahendry.auto-rename-tag
-   eamodio.gitlens
-   alefragnani.project-manager
-   emmanuelbeziat.vscode-great-icons
-   SirTori.indenticator
-   wakatime 
-   Orta.vscode-jest
-   msjsdiag.debugger-for-chrome
-   MS-vsliveshare.vsliveshare
-   cssho.vscode-svgviewer


Segue o resumo do que cada um desses plugins e veja como eles podem facilitar o seu dia a dia.

### JavaScript Snippets

Plugin: [https://marketplace.visualstudio.com/items?itemName=nathanchapman.JavaScriptSnippets](https://marketplace.visualstudio.com/items?itemName=nathanchapman.JavaScriptSnippets)

Como nome sugere, são trechos de códigos utilizados no Visual Studio para agilizar o desenvolvimento de código.

### Indent-Rainbow  

Plugin: [https://marketplace.visualstudio.com/items?itemName=oderwat.indent-rainbow](https://marketplace.visualstudio.com/items?itemName=oderwat.indent-rainbow)

![Indent-Rainbow](/img/posts/2018/11/vscode/vscode-indent-rainbow.png)

Uma extensão simples para tornar a indentação do seu código mais legível criando linhas com cores para cada nível.

### Bracket Pair Colorizer

Plugin: [https://marketplace.visualstudio.com/items?itemName=CoenraadS.bracket-pair-colorizer](https://marketplace.visualstudio.com/items?itemName=CoenraadS.bracket-pair-colorizer)

![Bracket Pair Colorizer](/img/posts/2018/11/vscode/vscode-coenraads-bracket-pair-colorizer.png)

Essa extensão permite que os colchetes correspondentes sejam identificados com cores. O usuário pode definir quais caracteres corresponder e quais cores usar.

### React-Native/React/Redux snippets for es6/es7 version Standard

Plugin: [https://marketplace.visualstudio.com/items?itemName=EQuimper.react-native-react-redux-snippets-for-es6-es7-version-standard](https://marketplace.visualstudio.com/items?itemName=EQuimper.react-native-react-redux-snippets-for-es6-es7-version-standard)

Mais um snippet mas focado em React, React Native, Redux e padrões do ES6/ES7.

### TODO Highlight

Plugin: [https://marketplace.visualstudio.com/items?itemName=wayou.vscode-todo-highlight](https://marketplace.visualstudio.com/items?itemName=wayou.vscode-todo-highlight)

![TODO Highlight](/img/posts/2018/11/vscode/vscode-TODOHighlight.png)

Para dar um highlight em algumas marcações dos comentários como TODO, FIXME e outras anotações em seu código.

### TODO Parser

Plugin: [https://marketplace.visualstudio.com/items?itemName=minhthai.vscode-todo-parser](https://marketplace.visualstudio.com/items?itemName=minhthai.vscode-todo-parser)

![TODO Parser](/img/posts/2018/11/vscode/demo_vscode1.2_todo_parser.gif){:width="992px"}

Analisa todos os TODO marcados em seu código.

### Import Cost

Plugin: [https://marketplace.visualstudio.com/items?itemName=wix.vscode-import-cost](https://marketplace.visualstudio.com/items?itemName=wix.vscode-import-cost)

![Import Cost](/img/posts/2018/11/vscode/import-cost.gif)

Exibe o tamanho dos módulos que você está importando para o seu código em JS.

### REST Client

Plugin: [https://marketplace.visualstudio.com/items?itemName=humao.rest-client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)

Faça requests direto do VSCode e veja as respostas de cada requisição.

### Auto Close Tag

Plugin: [https://marketplace.visualstudio.com/items?itemName=formulahendry.auto-close-tag](https://marketplace.visualstudio.com/items?itemName=formulahendry.auto-close-tag)

![Auto Close Tag](/img/posts/2018/11/vscode/auto_close_tags_usage.gif){:width="992px"}

### Auto Rename Tag

Plugin: [https://marketplace.visualstudio.com/items?itemName=formulahendry.auto-rename-tag](https://marketplace.visualstudio.com/items?itemName=formulahendry.auto-rename-tag)

![Auto Rename Tag](/img/posts/2018/11/vscode/auto_rename_tag_usage.gif){:width="992px"}

### GitLens

Plugin: [https://github.com/eamodio/vscode-gitlens](https://github.com/eamodio/vscode-gitlens)

![GitLens](/img/posts/2018/11/vscode/gitlens-preview.gif)

Este é um dos meus prediletos! Facilita muito a utilização do git principalmente para fazer diffs e analisar o histórico.

### Project Manager

Plugin: [https://marketplace.visualstudio.com/items?itemName=alefragnani.project-manager](https://marketplace.visualstudio.com/items?itemName=alefragnani.project-manager)

Gerencia projetos no VSCode.

### VSCode Great Icons

Plugin: [https://marketplace.visualstudio.com/items?itemName=emmanuelbeziat.vscode-great-icons](https://marketplace.visualstudio.com/items?itemName=emmanuelbeziat.vscode-great-icons)

![VSCode Great Icons](/img/posts/2018/11/vscode/vscode-great-icons.jpg){:width="992px"}

Pacote de icones para o VSCode.

### Indenticator

Plugin: [https://marketplace.visualstudio.com/items?itemName=SirTori.indenticator](https://marketplace.visualstudio.com/items?itemName=SirTori.indenticator)

![Indenticator](/img/posts/2018/11/vscode/SirTori_indenticatordemo.gif)

Facilita a visualização do bloco de código que está identado.

### WakaTime

Plugin: [https://marketplace.visualstudio.com/items?itemName=WakaTime.vscode-wakatime](https://marketplace.visualstudio.com/items?itemName=WakaTime.vscode-wakatime)

Gera métricas e reports automaticamente conforme você for programando no VSCode.

### Jest

Plugin: [https://marketplace.visualstudio.com/items?itemName=Orta.vscode-jest](https://marketplace.visualstudio.com/items?itemName=Orta.vscode-jest)

![Jest](/img/posts/2018/11/vscode/vscode-jest.gif)

Complemento para Jest no VSCode, com linter, autocompletes e status do test que você esta escrevendo.

### Debugger for Chrome

Plugin: [https://marketplace.visualstudio.com/items?itemName=msjsdiag.debugger-for-chrome](https://marketplace.visualstudio.com/items?itemName=msjsdiag.debugger-for-chrome)

Debugger no VSCode como acontece no console do Chrome. Você precisa instalar o [Chrome DevTools Protocol](https://chromedevtools.github.io/debugger-protocol-viewer/) no seu Chrome. Além disso você precisa realizar uma configuração no seu VSCode. Neste caso eu tenho um [exemplo aqui](https://github.com/rtancman/reactnd-project-cms/blob/master/.vscode/launch.json). Abaixo segue o passo a passo:

```bash

#entrar no diretorio do seu projeto

mkdir .vscode/

cd .vscode

echo -e '{

"version": "0.2.0",

"configurations": [

{

"name": "Debug CRA Tests",

"type": "node",

"request": "launch",

"runtimeExecutable": "${workspaceRoot}/node_modules/.bin/react-scripts",

"args": [

"test",

"--runInBand",

"--no-cache",

"--env=jsdom"

],

"cwd": "${workspaceRoot}",

"protocol": "inspector",

"console": "integratedTerminal",

"internalConsoleOptions": "neverOpen"

},

{

"name": "Chrome Attach",

"type": "chrome",

"request": "attach",

"port": 9222,

"url": "http://localhost:3000"

}

]

}' > launch.json

```

### VS Live Share

Plugin: [https://marketplace.visualstudio.com/items?itemName=MS-vsliveshare.vsliveshare](https://marketplace.visualstudio.com/items?itemName=MS-vsliveshare.vsliveshare)

Muito útil para fazer [pair programing](https://en.wikipedia.org/wiki/Pair_programming) remoto!!!! Ele compartilha a sessão do seu projeto no VSCode dando acesso ao código em si e ao terminal.

### SVG Viewer

Plugin: [https://marketplace.visualstudio.com/items?itemName=cssho.vscode-svgviewer](https://marketplace.visualstudio.com/items?itemName=cssho.vscode-svgviewer)

![SVG Viewer](/img/posts/2018/11/vscode/cssho.vscode-svgviewerfrom_context.gif)


Renderizar o arquivo .svg como se fosse uma imagem.


Atualmente são estes os plugins que eu estou utilizando.
Grande abraço!