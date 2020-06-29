---
layout: post
title: Elasticsearch como ferramenta de busca
subtitle: Entendendo como e porque utilizar o elasticsearch em um sistema de busca.
author: Raffael Tancman
date: 2020-06-30 08:51:00 -0300
background: '/img/posts/2020/06/elasticsearch-como-ferramenta-de-busca.jpg'
comments: true
shareBar: true
categories:
    - "information-retrieval"
---

Boa parte dos sistemas tem uma ferramenta de busca e a forma como a mesma é implementada pode variar. Faz sentido utilizar o banco de dados atual da aplicação e começar a aplicar algumas features de busca, mas isso pode ser um tiro no pé quando você quer de fato entregar o melhor documento dada uma determinada busca. Nesses casos, o elasticsearch é a ferramenta que vai trazer documentos relevantes para um resultado de busca. Vamos entender nesse artigo o que é essa ferramenta e executar os principais comandos do dia a dia. No final iremos subir um cluster no docker e ver a parte de monitoramento utilizando o kibana.


### O que é o elasticsearch?

É um sistema de busca distribuído baseado no Apache Lucene. A sua API Rest é simples e robusta. Além disso, é uma ferramenta completa, veloz e de escalabilidade distribuída. Foi lançado pela primeira vez em 2010 pela Elasticsearch e é uma ferramenta de alta confiabilidade e robustez. Muitas empresas utilizam essa ferramenta e já vi por lugares que passei diversas soluções sendo criadas com ele.

Um dos motivos da sua velocidade é o [índice invertido](https://en.wikipedia.org/wiki/Inverted_index). Que é projetado para permitir buscas de texto completo muito rápidas. Um índice invertido lista cada palavra exclusiva que apareça em qualquer documento e identifica todos os documentos em que cada palavra aparece. [Nesta sessão da documentação](https://www.elastic.co/guide/en/elasticsearch/reference/current/documents-indices.html) do elasticsearch temos mais detalhes de porque ele é rápido e como essa distribuição acontece.

Agora focando na relevância dos documentos retornados no resultado, elasticsearch utiliza algoritmos de similaridade para criar um score único e com esse valor ele ordena os resultados dos mais relevantes para os menos relevantes baseado em uma query feita pelo usuário. Por default a partir da versão 7, utiliza o [BM25](https://en.wikipedia.org/wiki/Okapi_BM25) que é uma função de ranking para calcular quão importante cada documento. Além do BM25 existem outros algoritmos e você pode ver nessa sessão da documentação ["Similarity module"](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-similarity.html) mas o atual da conta recado é um dos melhores algoritmos de ranking.

Recomendo a leitura da documentação da ferramenta para maior entendimento de como as coisa funcionam por debaixo dos panos e principalmente para entender como funciona a análise de textos que você pode acessar aqui nessa sessão de ["Text analysis"](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis.html#analysis) . Vamos entender na prática como podemos interagir com essa ferramenta e quão simples e subir um cluster.


### Rodando o elasticsearch localmente

O elasticsearch como é uma solução construída em Java, você basicamente precisa baixar o mesmo e rodar localmente. Eu recomendo sempre utilizar os gerenciadores de pacotes do seu SO para realizar essa instalação. Mas para esse artigo vamos utilizar o docker e docker-compose para facilitar todo o setup. Então vamos entender o que vamos instalar que serão as seguintes ferramentas:

- Elasticsearch: Que é o sistema de busca.
- Kibana: É o cliente para gerenciar o elasticsearch além de ter ferramentas de monitoramento e um cliente rico para rodar queries no elastic.

Vamos a configuração do arquivo docker-compose.yml:

```yaml
version: '2.2'
services:
  es:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.8.0
    container_name: es
    environment:
      - node.name=es
      - cluster.name=es-docker-cluster
      - discovery.seed_hosts=es
      - cluster.initial_master_nodes=es
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - es_data:/usr/share/elasticsearch/data
    ports:
      - 9200:9200
    networks:
      - elastic

  kibana:
    image: docker.elastic.co/kibana/kibana:7.8.0
    container_name: kibana
    ports:
      - 5601:5601
    environment:
      ELASTICSEARCH_URL: http://es:9200
      ELASTICSEARCH_HOSTS: http://es:9200
    networks:
      - elastic

volumes:
  es_data:
    driver: local

networks:
  elastic:
    driver: bridge
```

Essa configuração foi feita com base na documentação do elasticsearch ["Running the Elastic Stack on Docker"](https://www.elastic.co/guide/en/elastic-stack-get-started/current/get-started-docker.html) e simplifiquei por hora para a gente entender como as coisas funcionam. Agora podemos executar o comando docker-compose up.
```bash
docker-compose up -d
```

Agora com a aplicação rodando podemos acessar o kibana pela url [http://localhost:5601/](http://localhost:5601/). Pode ser que demore um pouquinho para subir e você pode conferir se tudo está funcionando verificando se os containers estão de pé. Para isso basta executar:

```bash
# containers que estão rodando
$ docker ps
CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES
011da05e9bd2 docker.elastic.co/elasticsearch/elasticsearch:7.8.0 "/tini -- /usr/local..." 4 hours ago Up 4 hours 0.0.0.0:9200->9200/tcp, 9300/tcp es01
961846fb5ae6 docker.elastic.co/kibana/kibana:7.8.0 "/usr/local/bin/dumb..." 4 hours ago Up 4 hours 0.0.0.0:5601->5601/tcp kib01

# para ver os logs
$ docker logs es01
$ docker logs kib01

# checando o servico elasticsearch
$ curl -X GET "localhost:9200/_cat/indices?v&pretty"
health status index uuid pri rep docs.count docs.deleted store.size pri.store.size
green open .kibana-event-log-7.8.0-000001 7fJFAISuQRaEqZcWLBH7oA 1 0 3 0 15.5kb 15.5kb
green open .apm-custom-link BijrW0OUQOOw7RSGJcz9HA 1 0 0 0 208b 208b
green open .kibana_task_manager_1 FvG7WnppQ6WioFlyQTF17Q 1 0 5 0 14.1kb 14.1kb
green open .apm-agent-configuration Qh9Ye6CgSMu_aIrulqZFsQ 1 0 0 0 208b 208b
green open .kibana_1 kd3OSBtlSGyjKCIze8VVvQ 1 0 26 6 63kb 63kb

$ curl -X GET "localhost:9200/_cat/nodes?v&pretty"
ip heap.percent ram.percent cpu load_1m load_5m load_15m node.role master name
172.21.0.3 20 96 5 0.85 1.52 1.08 dilmrt * 'es01'
```

Agora que verificamos que esta tudo está rodando normalmente vamos explorar o elasticsearch pelo kibana.


### Executando comandos do elasticsearch

Vamos explorar o elasticsearch realizando operações. Com o kibana aberto vamos acessar o Console web dele para rodar as operações.

<iframe width="100%" height="315" src="https://www.youtube.com/embed/jA83LpR-gmo" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Caso você não tenha encontrado o console basta acessar a url [http://0.0.0.0:5601/app/kibana#/dev_tools/console](http://0.0.0.0:5601/app/kibana#/dev_tools/console) ou então rodar os comandos diretamente pelo seu terminal utilizando o curl. Nestes exemplos vou disponibilizar as 2 formas. Vamos acessar a API do elasticsearch:


#### API Cat -  [cat indices API](https://www.elastic.co/guide/en/elasticsearch/reference/current/cat-indices.html#cat-indices)

#### Lista os indices que temos dispóniveis
Podemos acessar os outros recursos na sessão da documentação [cat APIs](https://www.elastic.co/guide/en/elasticsearch/reference/current/cat.html).

```bash
# chamada no kibana

GET /_cat/indices

# curl para rodar no terminal
$ curl -XGET "http://localhost:9200/_cat/indices"
```

Provavelmente você deve ter tido o seguinte resultado:
```bash
green open .kibana-event-log-7.8.0-000001 7fJFAISuQRaEqZcWLBH7oA 1 0 4 0 20.6kb 20.6kb
green open .apm-custom-link BijrW0OUQOOw7RSGJcz9HA 1 0 0 0 208b 208b
green open .kibana_task_manager_1 FvG7WnppQ6WioFlyQTF17Q 1 0 5 0 14.1kb 14.1kb
green open .apm-agent-configuration Qh9Ye6CgSMu_aIrulqZFsQ 1 0 0 0 208b 208b
green open .kibana_1 kd3OSBtlSGyjKCIze8VVvQ 1 0 38 4 77.2kb 77.2kb
```
Estes são os índices que o kibana cria. Agora vamos criar um índice e trabalhar em cima dele.

### Trabalhando com indices

#### Criando um índice ["Create index API"](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html)

Vamos dar uma olhada em como podemos criar index.

```bash
# chamada no kibana
PUT /meu_primeiro_index

# curl para rodar no terminal
curl -XPUT "http://localhost:9200/meu_primeiro_index"
```

Dessa forma criamos um índice sem nenhum atributo. Os índices são responsáveis por armazenar os nosso documentos e nele podemos usar diversos tipos que você pode ver os suportados nessa sessão da documentação ["Field datatypes"](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html). Agora vamos criar um índice com alguns campos.

```bash
# chamada no kibana
PUT /filmes
{
  "mappings": {
    "properties": {
      "nome": {
        "type": "text"
      },
      "descricao": {
        "type": "text"
      },
      "nota": {
        "type": "float"
      },
      "classificao": {
        "type": "text"
      },
      "data_lancamento": {
        "type": "date"
      }
    }
  }
}


# curl para rodar no terminal
curl -XPUT "http://localhost:9200/filmes" -H 'Content-Type: application/json' -d'{  "mappings": {    "properties": {      "nome": {        "type": "text"      },      "descricao": {        "type": "text"      },      "nota": {        "type": "float"      },      "classificao": {        "type": "text"      },      "data_lancamento": {        "type": "date"      }    }  }}'
```

Após a sua criação podemos visualizar a sua estrutura da seguinte forma:

```bash
# chamada no kibana
GET /filmes/_mapping
GET /filmes/_settings


# curl para rodar no terminal
curl -XGET "http://localhost:9200/filmes/_mapping"
curl -XGET "http://localhost:9200/filmes/_settings"
```

- [Mapping](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html) : Descreve as propriedades de um documento que vai ser inserido em um índice.
- [Settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules.html#index-modules): Descreve as configurações de um índice. Aqui são configurados um recurso muito interessante que são os [analyzers, tokenizers, token filters and character filters.](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis.html)


### Manipulando documentos ["Document APIs"](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs.html)

Nesta parte vamos entender como inserir, editar, ler e remover documentos dos indices. Vamos lá!

#### Criando documentos ["Index API"](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-index_.html):

```bash
# chamada no kibana
POST /filmes/_doc/
{
  "nome": "Matrix",
  "descricao": "Melhor filme ever!",
  "classificao": "livre",
  "nota": 10,
  "data_lancamento": "1999-05-21T14:12:12"
}


# curl para rodar no terminal
curl -XPOST "http://localhost:9200/filmes/_doc/" -H 'Content-Type: application/json' -d'{  "nome": "Matrix",  "descricao": "Melhor filme ever!",  "classificao": "livre",  "nota": 10,  "data_lancamento": "1999-05-21T14:12:12"}'
```

#### Editando documentos ["Update API"](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-update.html):

```bash
# chamada no kibana
POST filmes/_update/-DEY_XIBblRt4Ct0995B
{
  "doc": {
    "classificao": "Não recomendado para menores de doze anos"
  }
}


# curl para rodar no terminal
curl -XPOST "http://localhost:9200/filmes/_update/-DEY_XIBblRt4Ct0995B" -H 'Content-Type: application/json' -d'{  "doc": {    "classificao": "Não recomendado para menores de doze anos"  }}'
```

#### Lendo documentos ["Get API"](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-get.html):

```bash
# chamada no kibana
GET filmes/_doc/-DEY_XIBblRt4Ct0995B

# curl para rodar no terminal
curl -XGET "http://localhost:9200/filmes/_doc/-DEY_XIBblRt4Ct0995B"
```

#### Removendo documentos ["Delete API"](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-delete.html):

```bash
# chamada no kibana
DELETE filmes/_doc/-DEY_XIBblRt4Ct0995B

# curl para rodar no terminal
curl -XDELETE "http://localhost:9200/filmes/_doc/-DEY_XIBblRt4Ct0995B"
```

### Realizando buscas

Vamos entender como fazer queries no elasticsearch. Para isso vamos continuar explorando o nosso índice recém criado de filmes. Vamos popular o mesmo com alguns filmes utilizando o ["Bulk API"](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html) para inserir vários documentos na mesma requisição.

```bash
POST /filmes/_bulk
{"index":{}}
{"nome":"Matrix","descricao":"Melhor filme ever!","classificao":"Não recomendado para menores de doze anos","nota":10,"data_lancamento":"1999-05-21T14:12:12"}
{"index":{}}
{"nome":"Matrix Reloaded","descricao":"Melhor filme ever!!!!","classificao":"Não recomendado para menores de doze anos","nota":8.5,"data_lancamento":"2003-05-15T11:30:00"}
{"index":{}}
{"nome":"Matrix Revolutions","descricao":"Melhor filme ever!!!!","classificao":"Não recomendado para menores de doze anos","nota":8.9,"data_lancamento":"2003-11-05T11:30:00"}
{"index":{}}
{"nome":"Matrix 4","descricao":"Melhor filme ever!!!!","classificao":"Não recomendado para menores de doze anos","nota":0,"data_lancamento":"2022-04-01T11:30:00"}



# curl para rodar no terminal
curl -XPOST "http://localhost:9200/filmes/_bulk" -H 'Content-Type: application/json' -d'{"index":{}}{"nome":"Matrix","descricao":"Melhor filme ever!","classificao":"Não recomendado para menores de doze anos","nota":10,"data_lancamento":"1999-05-21T14:12:12"}{"index":{}}{"nome":"Matrix Reloaded","descricao":"Melhor filme ever!!!!","classificao":"Não recomendado para menores de doze anos","nota":8.5,"data_lancamento":"2003-05-15T11:30:00"}{"index":{}}{"nome":"Matrix Revolutions","descricao":"Melhor filme ever!!!!","classificao":"Não recomendado para menores de doze anos","nota":8.9,"data_lancamento":"2003-11-05T11:30:00"}{"index":{}}{"nome":"Matrix 4","descricao":"Melhor filme ever!!!!","classificao":"Não recomendado para menores de doze anos","nota":0,"data_lancamento":"2022-04-01T11:30:00"}'
```

Com o nosso índice populado vamos realizar algumas queries utilizando a ["Search API"](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html):

```bash
# chamada no kibana
GET /filmes/_search

GET filmes/_search
{
  "query": {
    "match": {
      "nome": "Matrix"
    }
  }
}

GET filmes/_search
{
  "query": {
    "match": {
      "nome": "Matrix"
    }
  }
}


GET /filmes/_search
{
  "query": {
    "range": {
      "nota": {
        "gte": 2,
        "lte": 9
      }
    }
  }
}


# curl para rodar no terminal
curl -XGET "http://localhost:9200/filmes/_search"

curl -XGET "http://localhost:9200/filmes/_search" -H 'Content-Type: application/json' -d'{  "query": {    "match": {      "nome": "Matrix"    }  }}'

curl -XGET "http://localhost:9200/filmes/_search" -H 'Content-Type: application/json' -d'{  "query": {    "range": {      "nota": {        "gte": 2,        "lte": 9      }    }  }}'
```

Acima utilizamos queries com o [match](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html) e [range](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-range-query.html). São queries simples mas analisando a documentação você pode incrementar esses filtros conforme a sua necessidade.

Se você chegou até aqui PARABÉNS!!! Você agora já sabe criar documentos e pesquisar os mesmos. Vamos seguir nosso artigo transformando agora nosso elasticsearch em cluster com mais nodes.

###  Criando um cluster elasticsearch

Vamos seguir utilizando o docker mas a configuração continua sendo a mesma e você basicamente precisa incluir essas propriedades no arquivo de configuração do elasticsearch que geralmente fica no /usr/share/elasticsearch/config/elasticsearch.yml ou você pode criar variáveis de ambientes seguindo o nome das chaves utilizadas. São elas:

-   [cluster.name](https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster.name.html)
-   [discovery.seed_hosts](https://www.elastic.co/guide/en/elasticsearch/reference/current/discovery-settings.html#unicast.hosts)
-   [cluster.initial_master_nodes](https://www.elastic.co/guide/en/elasticsearch/reference/current/discovery-settings.html#initial_master_nodes)

Com isso agora vamos alterar o nosso docker-compose.yml para os seguintes valores:

```yaml
version: '2.2'
services:
  es01:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.8.0
    container_name: es01
    environment:
      - node.name=es01
      - cluster.name=es-docker-cluster
      - discovery.seed_hosts=es02
      - cluster.initial_master_nodes=es01
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms256m -Xmx256m"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - data01:/usr/share/elasticsearch/data
    ports:
      - 9200:9200
    networks:
      - elastic

  es02:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.8.0
    container_name: es02
    environment:
      - node.name=es02
      - cluster.name=es-docker-cluster
      - discovery.seed_hosts=es01
      - cluster.initial_master_nodes=es01
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms256m -Xmx256m"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - data02:/usr/share/elasticsearch/data
    ports:
      - 9201:9200
    networks:
      - elastic

  kib01:
    image: docker.elastic.co/kibana/kibana:7.8.0
    container_name: kib01
    ports:
      - 5601:5601
    environment:
      XPACK_APM_SERVICEMAPENABLED: 'false'
      ELASTICSEARCH_URL: http://es01:9200
      ELASTICSEARCH_HOSTS: http://es01:9200
    networks:
      - elastic

volumes:
  data01:
    driver: local
  data02:
    driver: local

networks:
  elastic:
    driver: bridge
```

Em seguida vamos rodar o comando do docker-compose para recriar os containers:

```bash
docker-compose up -d
```

Agora precisamos aguardar os containers subirem com sucesso. Em alguns casos caso você tenha uma máquina com poucos recursos recomendo alterar a configuração no docker-compose.yml `ES_JAVA_OPTS=-Xms256m -Xmx256m` devido a problemas de recursos em sua máquina local mesmo.

Caso os containers estejam rodando normalmente, agora vou te mostrar abaixo a parte de monitoramento do kibana para agente acessar o nosso cluster e verificar se tudo está rodando corretamente. Vamos lá!

<iframe width="100%" height="315" src="https://www.youtube.com/embed/3ljxqJ3pEcw" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


### Resumindo

Neste post vimos o que é o elasticsearch e como ele funciona. Subimos um elastic local utilizando docker e docker-compose e nos conectamos ao kibana para executar as queries. Além disso também vimos como configurar um cluster localmente para testes e visualizamos no kibana a área de monitoramento em geral.

Nos próximos posts vamos construir um serviço de busca utilizando a linguagem de programação Go. Também iremos evoluir o nosso índice "filmes" aplicando boas práticas para um sistema de busca com o elasticsearch.

Grande Abraço!
