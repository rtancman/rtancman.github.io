---
layout: post
title: Organizando AWS Lambda escrito em Python
subtitle: Arrumando o ambiente de trabalho com apex.run e explicando as pegadinhas em utilizar Python no AWS Lambda.
author: Raffael Tancman
date: 2019-01-11 20:55:00 -0200
background: '/img/posts/2019/01/organizando-aws-lambda-escrito-python.jpg'
comments: true
shareBar: true
categories:
    - "python"
    - "aws"
---


Continuando a série de posts relacionados ao AWS Lambda. Caso você tenha lido o primeiro post ou não conheça este serviço da Amazon, recomendo a leitura do artigo [AWS Lambda + Python - Como criar o setup de um projeto Python para rodar no AWS Lambda.](/python/aws/aws-lambda-e-python.html)

No meu primeiro contato com o lambda não procurei nenhum framework para organizar o trabalho e apaixonado por [Make](https://en.wikipedia.org/wiki/Make_(software)) acabei caindo de cabeça automatizando praticamente todos os comandos do [awscli lambda](https://docs.aws.amazon.com/cli/latest/reference/lambda/index.html). Isso no início foi bem legal e importante para entender bem o serviço e os comandos, mas depois de um tempo, com a complexidade de alguns projetos se tornou algo difícil de se manter. Além disso, por mais simples que o Make seja existem pessoas que não gostam de utilizar essa ferramenta por incrível que pareça. Neste caso, construímos uma API para uma empresa toda utilizando lambdas. Este foi o meu primeiro projeto. Meu time definiu a arquitetura, configuração e o processo de deploy.

## Apex

Conheci essa ferramenta através de um amigo após ter criado um “framework em Make” para gerenciar as ações do lambda. Após alguns testes, entendi o potencial do framework e a sua simplicidade para organizar e gerenciar funções no AWS Lambda. Sem sombras de dúvidas entender os comandos facilitaram o entendimento do [apex](http://apex.run/).

O apex propõe uma estrutura de diretórios para se trabalhar com o lambda. Também foi pensada em uma forma de deployar o seu lambda para ambientes diferentes como staging e production por exemplo. Além disso, a ferramenta simplifica a forma de realizar atualizações e deploys no seu lambda criando arquivos de configurações. Com ele fica simples versionar o projeto. Agora vamos ao que interessa vamos conhecer a ferramenta e depois em seguida vou detalhar os principais comandos. Segue abaixo o vídeo de apresentação do apex:

{% youtube "https://www.youtube.com/watch?v=PvvlCvfljz0" %}

Agora que conhecemos o apex, vamos aos principais comandos que executamos no video que são eles:

-   apex init
-   apex deploy
-   apex list

### apex init

Cria a Role na AWS com a configuração mínima de execução do lambda e uma estrutura inicial para se trabalhar com lambdas seguindo este formato:

```bash

├── functions
│ └── hello
│   └── index.js
└── project.json

```

Os comandos deploy e list os nomes são sugestivos e fazem o deploy criando ou atualizando o lambda existente e o outro lista todos os lambdas criados.

Para facilitar o setup de cada linguagem suportada no apex, temos um link na documentação com vários [exemplos de caso de uso que você pode ver clicando neste link.](https://github.com/apex/apex/tree/master/_examples)

Agora que já temos ideia do que é o apex e como ele funciona, vamos ver como instalar outros pacotes Pythons no nosso lambda.

## Utilizando pacotes

Sim meus amigos, o lambda suporta instalação de outras bibliotecas em nosso código. Basicamente precisamos instalar as dependências no mesmo diretório onde a nossa função lambda foi criada, zipar todo o conteúdo e subir em seguida para o lambda.

Em outras linguagens como Ruby e JS, as dependências normalmente ficam na raiz do projeto no mesmo nível de diretório onde se encontram os arquivos Gemfile ou Package.json. No Python ao instalar dependências para um projeto precisamos criar uma [virtualenv](https://docs.python.org/3/library/venv.html). E agora como fazer? Então amigos ao invés de rodar o pip instal -r requirements.txt vamos precisar mais um argumento o -t. Esta opção permite a gente passar o caminho onde vão ser criados os arquivos de dependências do nosso projeto. Exemplo:

```bash

pip install -r requirements.txt -t CAMINHO_PARA_CRIAR_ARQUIVOS_DEPENDENCIAS

```

Logo basta colocar esse caminho para ser o mesmo onde esta no nosso arquivo main.py que é a nossa função lambda e em seguida zipar e subir tudo como fazemos normalmente. Vejamos o seguinte exemplo para utilizar a lib [requests](http://docs.python-requests.org/en/master/) do Python.

```bash

#criando o arquivo main.py
echo -e "
import requests


def handle(event, context):
    r = requests.get('https://api.github.com/events')
    return {
        'texto': r.text,
    }

" >> main.py

#criando o requirements.txt
echo -e "requests" >> requirements.txt

#instalando as dependencias para o lambda
pip install -r requirements.txt -t .

# zipando
zip -qr hellorequests.zip .

# criar a nossa função via awscli.
aws lambda create-function \
  --region us-east-1 \
  --handler main.handle \
  --runtime python3.7 \
  --function-name 'hellorequests' \
  --zip-file fileb://./hellorequests.zip \
  --role 'PEGUE_SUA_ARN'

```

Pronto tendo feito isso temos o nosso lambda sendo executado incluindo o requests como dependências. Dessa maneira você pode instalar qualquer biblioteca na sua função lambda. [Aqui neste link você tem a documentação da AWS explicando em detalhes esse processo.](https://docs.aws.amazon.com/pt_br/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html)

Um grande ponto de atenção ao utilizar dependências com linguagens dinâmicas, é que a algumas bibliotecas feitas em Python fazem [wrapper](https://en.wikipedia.org/wiki/Wrapper_function) para funções escritas em C e outras funções do SO. Ou seja, o lambda roda em cima de uma [Amazon Linux AMI](https://aws.amazon.com/pt/amazon-linux-ami/) com isso podemos ter problemas de compatibilidades ao instalar bibliotecas. É nessa hora que o [docker](https://www.docker.com/) entra para nos ajudar! Ou seja, o ideal para não sofrer com esse tipo de problema e realizar a instalação em um [container que tenha o Amazon Linux AMI](https://docs.aws.amazon.com/pt_br/AmazonECR/latest/userguide/amazon_linux_container_image.html). Acessando o [hub docker](https://hub.docker.com/) temos acesso a essa imagem que você pode encontrar também por este link [https://hub.docker.com/_/amazonlinux/](https://hub.docker.com/_/amazonlinux/).

Agora com esse detalhe em mente vamos realizar a nossa instalação utilizando o docker com a imagem da AWS. Vamos fazer os seguintes passos:

1.  Criar o nosso Dockerfile com as configurações necessários para o Python
2.  Rodar o container para instalar as dependências
3.  Subir o nosso lambda

Para isso eu criei um gist para mostrar você incluir no seu projeto Python 3.7.

{% gist 4ce09756dd3ffe465ca6000f23496af5 %}

Agora basta criar os arquivos com base no gist e rodar os seguintes comandos:

```bash

make lambda.docker.build lambda.docker.pkgcreate

# zipando

zip -qr hellorequests.zip .

# criar a nossa função via awscli.

aws lambda create-function \
  --region us-east-1 \
  --handler main.handle \
  --runtime python3.7 \
  --function-name 'hellorequests' \
  --zip-file fileb://./hellorequests.zip \
  --role 'PEGUE_SUA_ARN'

```

Com isso você tem um ambiente mais “seguro” para instalar as suas dependências. Vale ainda dar uma olhada no projeto [lambda-ci](https://github.com/lambci/docker-lambda) que tem uma variedade de imagens prontas para instalar os seus lambdas. Você ainda pode encontrar mais alguns problemas como algumas bibliotecas específicas e caso isso aconteça comente nesse post que eu vou procurar te ajudar ;)

Resumindo mostrei o funcionamento básico do apex, como instalar as dependencias e ficar atento com os possíveis problemas de incompatibilidade de bibliotecas. Nos próximos posts vou mostrar casos reais de utilização do AWS Lambda criando uma api e consumido tarefas em background utilizando SQS e Kinesis.

Comente sobre o que você achou desse post e me conte o você quer saber ou fazer utilizando Python e Lambdas.

Grande abraço!