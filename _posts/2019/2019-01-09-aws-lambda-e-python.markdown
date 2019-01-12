---
layout: post
title: AWS Lambda + Python
subtitle: Como criar o setup de um projeto Python para rodar no AWS Lambda.
author: Raffael Tancman
date: 2019-01-09 12:10:00 -0200
background: '/img/posts/2019/01/aws-lambda-e-python.jpg'
comments: true
shareBar: true
categories:
    - "python"
    - "aws"
---


Vamos falar de AWS, vamos falar de lambdas e de python! Isso mesmo, nesse artigo vou começar uma série de posts sobre essas tecnologias.

A AWS é uma plataforma de serviços em cloud com as mais variadas funções. Neste artigo vamos abordar o [AWS Lambda](https://aws.amazon.com/lambda). O Lambda é um serviço que permite você rodar códigos sem ter a necessidade de ter uma máquina ligada o tempo todo. O lambda é executado através de gatilhos que são configurados no serviço. Atualmente podemos rodar códigos nas seguintes linguagens:

-   [Python](https://docs.aws.amazon.com/pt_br/lambda/latest/dg/python-programming-model.html)
-   [Java](https://docs.aws.amazon.com/pt_br/lambda/latest/dg/java-programming-model.html)
-   [Go](https://docs.aws.amazon.com/pt_br/lambda/latest/dg/go-programming-model.html)
-   [C#](https://docs.aws.amazon.com/pt_br/lambda/latest/dg/dotnet-programming-model.html)
-   [Ruby](https://docs.aws.amazon.com/pt_br/lambda/latest/dg/lambda-ruby.html)

Vamos utilizar o Python para exemplificar como podemos utilizar o lambda. Antes de começar a executar este serviço precisamos entender o contrato que serviço determinou para a sua utilização. Todo código a ser executado precisa estar dentro de uma função de inicialização que recebe 2 argumentos que são o event e o context. A estrutura da função fica nesse formato:

```python

def handler_name(event, context):  
...  
return some_value

```

- **event:** É o parâmetro principal. Neste argumento recebemos os dados envidados pelos serviços da AWS podendo conter dados de uma mensagem recebida no [SQS](https://aws.amazon.com/sqs) e até mesmo dados de um request repassado pelo [API Gateway](https://aws.amazon.com/api-gateway/).

- **context:** Neste recebemos um objeto LambdaContext. Temos neste objeto informações do contexto de invocação deste lambda como a quantidade de memória configurada até o ARN de quem invocou esta função. [Aqui temos uma explicação detalhada deste objeto.](https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html)

Caso você queira saber mais sobre essa estrutura do serviço de uma olhada [neste item da documentação do lambda.](https://docs.aws.amazon.com/pt_br/lambda/latest/dg/python-programming-model-handler-types.html)

Agora que já conhecemos a estrutura do lambda vamos criar uma função e para isso temos duas opções via console da AWS ou via terminal utilizando o [awscli](https://aws.amazon.com/cli/).

Vamos explorar o console da AWS primeiramente. Acessando o serviço vamos encontra esta tela inicial:  

![aws lambda tela inicial](/img/posts/2019/01/awslambda/1-aws-lambda-telainicial.gif)

Atualmente temos na tela de entrada do lambda um sandbox utilizando JS para brincar com o lambda e de fato rodar o seu primeiro “Hello World”. Mas vamos explorar a criação de uma nova função.

Na criação de uma função lambda temos opções para From Scratch, Blueprints e AWS Serveless Aplication Repository.

- **From Scratch:** É para criar funções do zero.

- **Blueprints:** São exemplos de funções para atividades recorrentes na AWS.

- **AWS Serveless Aplication Repository:** São exemplos de aplicações Serverless. Neste temos exemplos de arquiteturas utilizando os serviços da AWS e você consegue facilmente instalar e rodar.

Nosso foco aqui é mostrar a utilização do lambda From Scratch. Vamos criar uma função lambda com suporte a linguagem python na versão 3.7. O lambda precisa de uma role para execução e você pode criar [seguindo essa documentação](https://docs.aws.amazon.com/pt_br/lambda/latest/dg/intro-permission-model.html). Para o nosso exemplo vamos criar uma AWSLambdaBasicExecutionRole.
![aws lambda criando role](/img/posts/2019/01/awslambda/2-aws-lambda-criando-role.gif)

Lembrando que você também pode utilizar as templates disponíveis para o serviço que você vai ligar a sua função lambda.
![aws lambda criando role seguindo templates](/img/posts/2019/01/awslambda/3-aws-lambda-criando-role-seguindo-templates.gif)

Com a nossa role criada vamos ao que interessa e criar a nossa função lambda!
![aws lambda criando](/img/posts/2019/01/awslambda/4-aws-lambda-criando.gif)


Após a criação da função vamos cair na tela configuração da função. Aqui podemos escolher os serviços que vão ser os gatilhos para rodar o nosso lambda, podemos trocar o runtime para outras linguagens, setar variáveis de ambientes, quantidade de memória, tempo máximo de execução, escrever o nosso código em um editor web e colocar a nossa função para executar rodando testes. Fiz um video curto explicando esse console do lambda. Veja abaixo:

{% youtube "https://www.youtube.com/watch?v=Mr2XT_6HPSo" %}


Vamos de [awscli](https://aws.amazon.com/pt/cli/?nc1=h_ls), terminal!!! Como a maioria dos serviços da AWS temos uma interface de linha de comando. Para isso você vai precisar instalar essa ferramenta em sua máquina. O awscli é feito em Python <3 e por esse motivo vou utilizar o pip para a sua instalação. [Neste link você tem acesso a documentação da AWS explicando como instalar.](https://docs.aws.amazon.com/pt_br/cli/latest/userguide/cli-chap-install.html) Segue o comando para instalar usando o pip:

```bash

pip install awscli

#validando se o awscli foi instalado corretamente

aws --version

```

Com tudo instalado agora vamos precisar configurar a sua conta e para isso vamos rodar o seguinte comando:

```bash

aws configure

```

Após rodar esse comando vamos precisar colocar o seu AWS Access Key ID, AWS Secret Access Key, uma região default e o formato de output.

```bash

AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-west-2
Default output format [None]: json

```

[Nesse link você encontra a documentação completa e mais detalhes para realizar essa configuração.](https://docs.aws.amazon.com/pt_br/cli/latest/userguide/cli-chap-configure.html)


Com tudo configurado vamos dar uma olhada nos comandos do lambda rodando:

```bash

aws lambda help

```

![aws lambda cli help](/img/posts/2019/01/awslambda/5-aws-lambda-cli-help.gif)

No help temos todos os comandos disponíveis para configurar o serviço pelo terminal. Vamos focar nesse artigo nos seguintes comandos:

-   aws lambda create-function
-   aws lambda list-functions
-   aws lambda update-function-code
-   aws lambda invoke
-   aws lambda delete-function

aws lambda create-function
Como o nome já diz é função utilizada para criar uma função lambda. Vamos ao comando:

```bash

aws lambda create-function \
--region us-east-1 \
--handler main.handler \
--runtime python3.7 \
--function-name 'awscli-create-lambda' \
--zip-file fileb://./awsclicreatelambda.zip \
--role 'arn:aws:iam::032292203206:role/AWSLambdaBasicExecutionRole'

```

- **--zip-file:** No caso de subir um zip com menos de 10mb você deve usar o parametro --zip-file fileb://PATH_PARA_O_ZIP

- **--role:** Aqui precisamos pegar a [ARN](https://docs.aws.amazon.com/pt_br/general/latest/gr/aws-arns-and-namespaces.html) da role. Neste caso você consegue essa informação acessando a sessão de IAM e navegando até a role e clicando para ver os detalhes dela.

Este é o mínimo de argumentos que você precisa passar no modo cli para criar um lambda. Como pode perceber temos um arquivo .zip que neste exemplo tem o nome de awsclicreatelambda.zip . Exatamente precisamos zipar o nosso arquivo antes de subir nossa função para o lambda. Para zipar precisamos do arquivo que vai conter a nossa função python. Abaixo segue os dados que vamos usar neste exemplo.

Criando o arquivo main.py

```bash

echo -e "

def handler(event, context):
    return {
        'texto': 'hello world lambda usando awscli',
    }

" >> main.py

```

Zipando o arquivo main.py

```bash

zip -qr awsclicreatelambda.zip main.py

```

Agora que já temos o nosso zip vamos criar a nossa função via awscli.


```bash

aws lambda create-function \
--region us-east-1 \
--handler main.handler \
--runtime python3.7 \
--function-name 'awscli-create-lambda' \
--zip-file fileb://./awsclicreatelambda.zip \
--role 'PEGUE_SUA_ARN'

```

Se tudo ocorreu com sucesso você deve ter recebido uma resposta como essa e agora conseguimos visualizar o nosso lambda no console da aws.

```bash

{
  "FunctionName": "awscli-create-lambda",
  "FunctionArn": "arn:aws:lambda:us-east-1:XXXXXXXXX:function:awscli-create-lambda",
  "Runtime": "python3.7",
  "Role": "arn:aws:iam::XXXXXXXXXXX:role/AWSLambdaBasicExecutionRole",
  "Handler": "main.handler",
  "CodeSize": 254,
  "Description": "",
  "Timeout": 3,
  "MemorySize": 128,
  "LastModified": "2019-01-09T20:21:51.059+0000",
  "CodeSha256": "tpv2milsG+tB6qZWt4CPbtU4JxUXSxwK0aWsl0lbX6g=",
  "Version": "$LATEST",
  "TracingConfig": {
    "Mode": "PassThrough"
  },
  "RevisionId": "e2d3b109-1312-4eb9-80da-f8c710176541"
}

```

aws lambda list-functions
Vamos fazer um double check e listar as funções existentes na AWS.

```bash

aws lambda list-functions

```

Você deve receber uma lista com as configurações de cada lambda como essa aqui abaixo:

```bash

{
  "Functions": [
    {
      "FunctionName": "helloworld",
      "FunctionArn": "arn:aws:lambda:us-east-1:XXX:function:helloworld",
      "Runtime": "python3.7",
      "Role": "arn:aws:iam::XXXX:role/AWSLambdaBasicExecutionRole",
      "Handler": "lambda_function.lambda_handler",
      "CodeSize": 272,
      "Description": "",
      "Timeout": 3,
      "MemorySize": 128,
      "LastModified": "2019-01-08T23:32:13.046+0000",
      "CodeSha256": "Amrs9cH7J7bkB5kMuvxiVzodlZCSee1bcSZFN4KjNLs=",
      "Version": "$LATEST",
      "VpcConfig": {
        "SubnetIds": [],
        "SecurityGroupIds": [],
        "VpcId": ""
      },
      "Environment": {
        "Variables": {
          "TESTE": "LALA"
        }
      },
      "TracingConfig": {
        "Mode": "PassThrough"
      },
      "RevisionId": "863e4b1e-99cd-4cfc-8f8c-0644af4d5b38"
    },
    {
      "FunctionName": "awscli-create-lambda",
      "FunctionArn": "arn:aws:lambda:us-east-1:XXXXX:function:awscli-create-lambda",
      "Runtime": "python3.7",
      "Role": "arn:aws:iam::XXXXXXXX:role/AWSLambdaBasicExecutionRole",
      "Handler": "main.handler",
      "CodeSize": 254,
      "Description": "",
      "Timeout": 3,
      "MemorySize": 128,
      "LastModified": "2019-01-09T20:21:51.059+0000",
      "CodeSha256": "tpv2milsG+tB6qZWt4CPbtU4JxUXSxwK0aWsl0lbX6g=",
      "Version": "$LATEST",
      "TracingConfig": {
        "Mode": "PassThrough"
      },
      "RevisionId": "e2d3b109-1312-4eb9-80da-f8c710176541"
    }
  ]
}

```

aws lambda update-function-code
Para atualizar o codigo lambda basta rodar o seguinte comando:


```bash

aws lambda update-function-code \
--region us-east-1 \
--function-name 'awscli-create-lambda' \
--zip-file fileb://./awsclicreatelambda.zip

```

Este é o output esperado:

```bash

{
  "FunctionName": "awscli-create-lambda",
  "FunctionArn": "arn:aws:lambda:us-east-1:XXXX:function:awscli-create-lambda",
  "Runtime": "python3.7",
  "Role": "arn:aws:iam::XXXX:role/AWSLambdaBasicExecutionRole",
  "Handler": "main.handler",
  "CodeSize": 254,
  "Description": "",
  "Timeout": 3,
  "MemorySize": 128,
  "LastModified": "2019-01-09T20:41:49.473+0000",
  "CodeSha256": "tpv2milsG+tB6qZWt4CPbtU4JxUXSxwK0aWsl0lbX6g=",
  "Version": "$LATEST",
  "TracingConfig": {
    "Mode": "PassThrough"
  },
  "RevisionId": "2ae6d782-dde0-41d1-8227-db3bfa23d30f"
}

```

aws lambda invoke
Executando um lambda precisamos passar o nome da função, o paylod que neste caso tem que ser um json e passar um arquivo onde vai ser escrito a resposta dessa invocação.


```bash

aws lambda invoke \
--function-name 'awscli-create-lambda' \
--payload '{}' \
awsclicreatelambda.output

# para ver o resultado basta agora dar um cat no arquivo

cat awsclicreatelambda.output

```

aws lambda delete-function

Vamos remover este lambda recem criado rodando o comando delete-function. Este comando não tem output.

```bash

aws lambda delete-function \
--region us-east-1 \
--function-name 'awscli-create-lambda'

```

Para facilitar também criei este [gist no github](https://gist.github.com/rtancman/240e67545a4dbde5107cd1dd09df014b) com todos os comandos que executamos em sequência.

{% gist 240e67545a4dbde5107cd1dd09df014b %}

Neste post procurei mostrar o funcionamento básico do lambda e as diversas formas que podemos manipular as nossas funções que podem ser feitas via console da AWS ou utilizando o utilitário awscli. Fique ligado que nos próximos posts vou mostrar como podemos otimizar toda essa configuração utilizando o framework [apex](http://apex.run/). 

Veja como [organizar o ambiente de trabalho com apex.run e entenda as pegadinhas em utilizar Python no AWS Lambda.](/python/aws/organizando-aws-lambda-escrito-python.html) 

Comente sobre o que você achou desse post e me conte o você quer saber ou fazer utilizando Python e Lambdas.

Grande abraço!