---
layout: post
title: De Software Engineer para Search Ranking Engineer
subtitle: Introdução a conceitos de busca e o que um ranking engineer faz.
author: Raffael Tancman
date: 2020-06-29 17:55:00 -0300
background: '/img/posts/2020/06/de-software-engineer-para-search-ranking-engineer.jpg'
comments: true
shareBar: true
categories:
    - "information-retrieval"
---

Sempre trabalhei como desenvolvedor fullstack e me lembro como se fosse hoje quando recebi a minha primeira oportunidade na "A Resistência". Neste momento eu iniciava a minha jornada como profissional de tecnologia. Na maior parte das empresas em que trabalhei tive a oportunidade de trabalhar em diversas áreas sendo backend, frontend, dba e operações. Com isso, acabei adquirindo uma experiência em diversas áreas. Porém, nos últimos 4 anos passei a trabalhar como software engineer. A convite na minha atual empresa, troquei de time integrando o de busca.

Até então não tinha ideia de como tudo seria. Sobre busca, já havia trabalhado com uma das principais tecnologias utilizadas nas empresas que é o elasticsearch. Porém dessa vez foi bem diferente! Por onde passei, vi diversas implementações de elasticsearch. A maioria delas, utilizando o software no seu modo básico, que já é muito bom, seguindo o formato de software de prateleira e principalmente sem ter especialistas na área trabalhando junto com o time de desenvolvimento. Dessa vez seria diferente e foi aí que a mágica aconteceu!

Atualmente eu trabalho na Jusbrasil e por ela tive a imensa sorte de conhecer pessoas incríveis de Manaus, especificamente pesquisadores e estudantes da UFAM. Entrando nesse mundo descobri que busca vai muito além de uma simples implementação do elasticsearch existe toda uma ciência por trás que é chamada de RI ou Recuperação da Informação.

Falando sobre busca em si eu primeiramente imaginava ser um grande banco de dados onde rodamos um select paginado. Porém isso está longe de ser um sistema de busca e é aí que RI começa a fazer sentido. Imaginem vocês retornar milhares de resultados sem relevância para a busca que usuário está fazendo, qual seria a percepção do mesmo pelo sistema? Não é atoa que gostamos do google, porque geralmente ele traz bons resultados para os termos que buscamos e RI é a ciência por trás disso. Recomendo MUITO o [curso de RI na UFAM do prof. Dr. Edleno Silva de Moura](https://www.youtube.com/watch?v=skDZcsOWq7U&list=PLgMem-KiO8qHUcI8D7gyhqH2gv0TPzhzR) para entenderem do assunto..


### Entendendo o que um sistema de RI deve fazer...

Confesso a vocês que quando entrei no time me senti um extraterrestre! Eram tantos termos e algoritmos específicos que levou um tempinho para digerir todo esse novo conhecimento. Para isso contei com a ajuda dos meus amigos de time e principalmente pelo curso que comentei acima.


Primeiramente procurei entender do básico e o principal fato que surgiu foi Precisão X Revocação. Ou seja quando buscamos algo queremos que o documento mais relevante esteja nas primeiras posições. Isso é precisão e quanto maior os cliques nas primeiras posições temos uma boa métrica para dizer o quão preciso o nosso sistema de busca é. Entretanto, nem sempre o melhor resultado está na primeira posição e gostaríamos que os outros resultados em sequência fossem tão bons ou melhores que os primeiros. Logo quando trazemos mais documentos relevantes nos resultados de busca, estamos melhorando a revocação do nosso sistema.

Quando aprendi esse conceito imaginei nossa simples é trazer os documentos relevantes nas primeiras posições sempre. Mas como medimos se isso está acontecendo e que unidade de medida deveríamos utilizar?


### Métricas de qualidade

Falamos de Precisão X Revocação e para os resultados em geral podemos utilizar algumas métricas tais como MRR e NDCG.

MRR ou [Mean reciprocal rank](https://en.wikipedia.org/wiki/Mean_reciprocal_rank), é uma fórmula estatística para dizer o quão preciso o seu sistema de busca é. Mas como eu calculo essa informação? Precisamos registrar da lista de resultado qual é o resultado clicado e a sua posição se foi o primeiro ou último por exemplo. Tendo essa informação registrada rodamos uma fórmula para saber quão preciso o nosso sistema está.

NDCG ou [Normalized Discounted cumulative gain](https://en.wikipedia.org/wiki/Discounted_cumulative_gain#Normalized_DCG) é uma métrica de normalização que é uma métrica que vai apontar a qualidade geral do seu sistema de busca. Ela leva em consideração precisão e revocação mas além disso, ela introduz a nota de documento e faz um desconto progressivo com base na sua posição.

Além dessas existem outras métricas e para ter um entendimento melhor recomendo a leitura do livro ["Recuperação de Informação: Conceitos e Tecnologia das Máquinas de Busca"](https://books.google.com.br/books?id=YWk3AgAAQBAJ&printsec=frontcover&hl=pt-BR&source=gbs_ge_summary_r&cad=0#v=onepage&q&f=false) dos autores Berthier Ribeiro Neto e Ricardo Baeza Yates. Estou lendo este livro que é uma referência na literatura para um entendimento geral de RI e foi recomendado pelo meu time.


### Como geramos as métricas?

Para isso precisamos coletar os eventos em nosso sistema de busca. Vocês devem conhecer o Google Analytics e caso você utilize essa ferramenta, pode ser uma boa usar os eventos para registrar essas informações. Muito cuidado com o Analytics porque no modo free ele exibe somente uma amostragem dos dados e isso não pode ser uma boa escolha. Agora caso você tenha acesso a todas as informações com o 360 é uma ferramenta que pode te ajudar e muito até porque com o 360 você consegue exportar todos os dados para uma tabela no bigtable por exemplo. Caso contrário a sugestão é ter de alguma forma todos as informações de busca registradas. Os eventos que precisamos registrar inicialmente são o usuário clicou no resultado da posição X e qual termo ele procurou somado com os resultados que você exibiu. Como vimos acima nas métricas, precisamos dessas informações mapeadas para criar-las e ir acompanhando as mesmas.


### Search Ranking Engineer

Agora que vocês entenderam o que deve ser um sistema de busca e como podemos medir a sua qualidade vamos ver qual é o papel de um Ranking Engineer. Na minha concepção é um engenheiro focado em melhorar o ranking de busca utilizando algoritmos, teorias e MUITOS testes para trazer o maior número de documentos relevantes nas primeiras posições do seu sistema.

Essa profissão é de muito estudo, pesquisa e testes principalmente. Porque eu diria que não existe uma fórmula única e tudo depende muito do domínio da sua empresa. Além disso, cada usuário realiza a busca de uma forma peculiar em um sistema de busca e por este motivo precisamos da sua utilização e de um acompanhamento das métricas para saber se de fato alteração na forma como exibimos os resultados vem melhorando ou piorando em média.


### Resumo

Esta é uma área mais científica e necessita de muita pesquisa e estudos. As tecnologias em geral são praticamente as mesmas que utilizamos como desenvolvedores em si porém os algoritmos são mais complexos e você aqui vai ver que suas aulas na faculdade de estrutura de dados vão valer cada segundo em sua vida nessa profissão.

Nos próximos posts vou falar sobre o elasticsearch. Vamos ver porquê e como devemos usar o mesmo para construir um sistema de busca. Falo dessa ferramenta por ser uma solução de mercado que vai ser o primeiro passo para muitas empresas melhorarem o seu sistema de busca.

Este post é uma introdução no assunto de RI e provavelmente na medida do possível irei continuar postando outros conteúdos relacionados sobre o que estou estudando no momento.


[VEJA O POST: Elasticsearch como ferramenta de busca
](/information-retrieval/elasticsearch-como-ferramenta-de-busca.html)

Grande abraço!
