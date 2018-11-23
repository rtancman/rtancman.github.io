---
layout: post
title: Dia a dia de um dev remoto
subtitle: Contando a minha experiência em trabalhar remoto.
author: Raffael Tancman
date: 2018-11-24 12:10:00 -0200
background: '/img/posts/2018/11/dia-a-dia-de-um-dev-remoto.jpg'
comments: true
shareBar: true
categories:
    - "soudev"
---


Nossa você trabalha de casa? É essa pergunta cada vez mais vem se tornando comum no universo dos devs. Trabalho remoto hoje ao meu ver é essencial para facilitar a correria do dia a dia. Acordar, tomar aquele café e sentar na frente do pc e começar a trabalhar é maravilhoso! Nesse post não vou contar os prós e contras dessa forma de trabalho mas sim vou contar um pouco do meu dia a dia e das ferramentas que utilizo.

Atualmente trabalho remoto para a [Resultados Digitais](https://resultadosdigitais.com.br/). O time no qual eu trabalho tem todo um esquema que facilita e integra as pessoas que não estão presentes no mesmo local físico. Estamos sempre num ciclo de aprendizado testando processos e ferramentas para melhorar toda a nossa comunicação.

## Comunicação

Esse é um dos pontos mais importantes. Toda comunicação fica centralizada em um canal do time no Slack ou seja abusamos da comunicação assíncrona. Para não perder nenhuma informação é muito importante ter tudo documentado para quem não esteja presente naquele momento tenha o entendimento do que está acontecendo posteriormente.

No caso de uma reunião, procuramos sempre que possível agendar no Google Calendar ou quando precisamos ser mais ágeis iniciamos uma thread no canal. A reunião é feita em uma sala virtual onde toda a conversa vai para um doc que em seguida é compartilhado com o time.

Passamos a utilizar uma ferramenta chamada [Sococo](https://www.sococo.com/). É uma ferramenta de comunicação que simula o ambiente da sua empresa virtualmente. Basicamente ele segue o modelo de salas que temos em um escritório físico facilitando a visualização de onde está cada integrante do time. Além disso ele tem algumas formas de imitar ambiente físico onde você pode bater na porta de uma sala para participar de uma reunião por exemplo que esteja acontecendo. Você já entra na sala e vê o que os participantes estão fazendo podendo iteragir com eles normalmente como no dia a dia como acontece numa sala física. Abaixo uma imagem de como é a ferramenta.

![Sococo](/img/posts/2018/11/sococo.jpg)

Eu trabalhei antes sem o Sococo e posso te afirmar que me sinto muito mais integrado com o time. O simples fato de simular o dia a dia físico em um software remoto muda a experiência do trabalho remoto fazendo com que todos se sintam mais próximos uns dos outros. Não deixamos de usar Slack. Pode parecer estranho, mas minha experiência no dia a dia é que os dois se complementam cada um com o seu devido valor.

Também utilizamos o [Trello](https://trello.com) onde todo trabalho em andamento fica visível por lá criando um modelo mental compartilhado entre o time para saber o que cada um está fazendo naquele momento.

## Pair programing

Nosso time utiliza muito dessa ferramenta e vou te dizer É FANTÁSTICO e muito valioso para o produto. O foco não aqui não é explicar o que é essa ferramenta mas sim como trabalhamos com ela de maneira remota. Todo nosso desenvolvimento é feito em par. Seja ele na parte de entendimento, planejamento da solução a ser desenvolvida ou no desenvolvimento propriamente dito.

Na parte de análise de solução, geralmente abrimos um doc no Google Drive e vamos discutindo e desenhando juntos a solução. Nesse momento juntamos os envolvidos em uma sala do Sococo onde além de debater compartilhamos a tela um do outro para mostrar alguma ideia. Procuramos seguir uma dinâmica de como se estivessemos um ao lado do outro rabiscando em uma folha de papel, mostrando sites com algum conteúdo ou documento para auxiliar no processo. Após o trabalho estar finalizado ainda contamos com a revisão de outros membros do time para seguir em diante. Nesse momento passamos para a fase de mão na massa ou seja coding!

No pair programing como o XP manda, sempre temos piloto e copiloto. Quem está pilotando normalmente compartilha a sua tela e vamos discutindo e escrevendo juntos o código para resolver o problema. Essa parte não estava sendo muito dinâmica devido ao fato de não ter uma forma fácil e rápida para rotacionar o piloto e copiloto. O trabalho se torna muito cansativo principalmente para quem esta de copiloto. Algumas vezes o compartilhamento de telas trava e algumas coisas ficam dificil de se ler.

Para resolver este problema começamos a testar ferramentas que compartilham a IDE e o terminal de trabalho. As que vem se mostrando interessantes para se trabalhar são a [VS Live Share](https://marketplace.visualstudio.com/items?itemName=MS-vsliveshare.vsliveshare-pack) que é um plugin para o VSCode e o tmux para compartilhar a sessão de um terminal usando o [tmate](https://tmate.io/). Muitas pessoas do time usam o Vim + tmux como ferramenta de trabalho e o tmate ajuda muito nesse contexto. Essas duas práticas vem ajudando muito no dinamismo do pair programing remoto onde todos conseguem manipular o mesmo código e ter acesso ao terminal. Com isso rodar os testes e realizar o commit de maneira remota ficou muito mais simples e dinâmico igual ao que fazemos no dia a dia quando estamos um do lado do outro trabalhando na mesma máquina.

## Dicas

Trabalhar remoto é uma realidade! Cada vez mais acredito nessa prática e diversas empresas tem adotado essa opção para melhorar a qualidade de vida do profissional, diminuir os custos de ter um espaço físico e principalmente contratar profissionais.

Ferramentas que utilizo no dia a dia que podem te ajudar a se organizar são elas:

-   [Github](https://github.com)
-   [Trello](https://trello.com)
-   [Vim](https://www.vim.org/), [Tmux](https://en.wikipedia.org/wiki/Tmux) e [Tmate](https://tmate.io/)
-   [VSCode](https://code.visualstudio.com/) e [VS Live Share](https://marketplace.visualstudio.com/items?itemName=MS-vsliveshare.vsliveshare-pack)
-   [Sococo](https://www.sococo.com/)
-   [Slack](https://slack.com/)
-   [Google Drive](https://www.google.com/drive/)
-   [Google Calendar](https://www.google.com/calendar)

Recomendo também MUITO a leitura desses posts que focam em boas práticas para facilitar o seu dia a dia remoto:

-   [O Guia do Trabalho Remoto — segundo especialistas](https://medium.com/rd-shipit/o-guia-do-trabalho-remoto-segundo-especialistas-55cbff2e111b)
-   [6 dicas para ser mais produtivo no home office](http://shipit.resultadosdigitais.com.br/blog/6-dicas-para-ser-mais-produtivo-no-home-office/)


Grande abraço!
