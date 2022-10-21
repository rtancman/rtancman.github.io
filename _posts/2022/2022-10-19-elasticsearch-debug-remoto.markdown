---
layout: post
title: Elasticsearch Debug Remoto
subtitle: Realizando um debug remoto no Elasticsearch com o IntelliJ IDEA e VSCode
author: Raffael Tancman
date: 2022-10-19 06:00:00 -0300
background: '/img/posts/2022/10/elasticsearch-debug-remoto.png'
comments: true
shareBar: true
categories:
    - "elasticsearch"
---

Quem nunca precisou realizar um debug? Essa ferramenta é muito importante para ajudar a entender sistemas e comportamentos inesperados, vulgo bugs! 

Trazendo para o mundo da JVM e Elastic, a um tempinho acabei contribuindo para um plugin do elasticsearch, o [elasticsearch-learning-to-rank](https://github.com/o19s/elasticsearch-learning-to-rank), precisei debugar remotamente para entender como as coisas estavam funcionando e acabei encontrando um bug e solucionando em seguida. Neste momento não cheguei a documentar o processo. Recentemente um amigo de trabalho perguntou em como poderia investigar um possível problema de concorrência nos analyzers do elasticsearch e acabei sugerindo o remote debug. 

Após esse papo resolvi escrever esse post em PT-BR para documentar esse processo.

## Configurando o ambiente de trabalho
Meus amores pelo [sdkman](https://sdkman.io/) já foram expressados em outros posts do meu blog e por isso no universo JVM recomendo para gerenciar as diversas versões de java, scala, sbt e por aê vai. Neste caso vamos usar o JDK 17. 

```bash
# instalando o sdkman
curl -s "https://get.sdkman.io" | bash


# instalando versões da jdk que precisamos para compilar o elastic
sdk install 17.0.2-open
sdk use java 17.0.2-open
```

## Baixando & Compilando o projeto

Vamos utilizar como base a versão 8.4.3 e o git para clonar o projeto e ir para a branch dessa versão.

```bash
mkdir elasticsearch-debug 
cd elasticsearch-debug
git clone git@github.com:elastic/elasticsearch.git
cd elasticsearch
git checkout 8.4
```

Compilando...

```bash
./gradlew localDistro
```

Se tudo deu certo você deverá ver essa mensagem:

```bash
> Task :localDistro
Elasticsearch distribution installed to ~/elasticsearch-debug/elasticsearch/build/distribution/local/elasticsearch-8.4.3-SNAPSHOT

BUILD SUCCESSFUL in 9m
456 actionable tasks: 456 executed
```

## Debugando!

Tenho 2 formas para debugar o elastic que são:
- [Debug via gradlew](#debug-via-gradlew)
- [Debug via Docker + JAVA_OPTIONS](#debug-via-docker--java_options)

Eu particularmente gosto de utilizar uma IDE para interagir com o a aplicação em modo debug. Nesse post eu vou demonstrar como podemos fazer nas IDEs abaixo:
- [IntelliJ IDEA](#debug-no-intellij-idea)
- [VSCode](#debug-no-vscode)

### Debug via gradlew

Quando não preciso instalar um plugin de terceiros no elastic gosto de executar na forma mais convencional que é rodando a aplicação em modo debug na JVM.
```bash
./gradlew run --debug-jvm
```

Após rodar este comando o projeto do elastic vai ficar executando localmente com a opção de debug habilitada. Basta agora dar um `Attach to Process` em sua IDE de preferência. Nesse post vou demonstrar como rodar com o [IntelliJ](#debug-no-intellij-idea) e no VSCode.

### Debug via Docker + JAVA_OPTIONS

Aqui vamos subir o elastic utilizando o docker mas passando umas variaveis para habilitar o modo debug. Por praticidade eu acabei criando um docker-compose.yml com o seguinte conteúdo:
```yaml
version: '2.2'
services:
  es:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.4.3
    container_name: es-remote-debug-8-4-3
    environment:
      - node.name=es-remote-debug-8-4-3
      - cluster.name=es-docker-cluster
      - discovery.seed_hosts=es-remote-debug-8-4-3
      - xpack.security.enabled=false
      - cluster.initial_master_nodes=es-remote-debug-8-4-3
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5007 -Xms512m -Xmx512m"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - es_data:/usr/share/elasticsearch/data
    ports:
      - 9200:9200
      - 5007:5007
    networks:
      - elastic

  kibana:
    image: docker.elastic.co/kibana/kibana:8.4.3
    container_name: kibana
    ports:
      - 5601:5601
    environment:
      ELASTICSEARCH_URL: http://es-remote-debug-8-4-3:9200
      ELASTICSEARCH_HOSTS: http://es-remote-debug-8-4-3:9200
    networks:
      - elastic

volumes:
  es_data:
    driver: local

networks:
  elastic:
    driver: bridge
```

Após criar o arquivo `docker-compose.yml`, vamos rodar o comando para subir os containers:
```bash
docker-compose up -d
```

Pronto! O elastic vai ficar executando localmente com a opção de debug habilitada. Basta agora dar um `Attach to Process` em sua IDE de preferência.

### Debug no IntelliJ IDEA

Vamos configurar o projeto do elastic para abrir no IntelliJ.

```bash
./gradlew idea
```

Após essa execução basta [importar o projeto para o IntelliJ](https://www.jetbrains.com/help/idea/import-project-or-module-wizard.html#import-project). Após a importação vamos executar novamente:

```bash
./gradlew run --debug-jvm

# ou rodando com o Docker + JAVA_OPTIONS
docker-compose up -d
```

Agora é ir no menu `Run > Debug > Debug Elasticsearch`. Se tudo deu certo seu console de debug no IntelliJ vai ter a seguinte menssagem:

```bash
Connected to the target VM, address: 'localhost:5007', transport: 'socket'
```

Para testar se tudo esta funcionando, vamos colocar um breakpoint no arquivo `server/src/main/java/org/elasticsearch/rest/RestController.java` na função abaixo:
```java
    @Override
    public void dispatchRequest(RestRequest request, RestChannel channel, ThreadContext threadContext) {
        // COLOCAR BREAKPOINT NESSA LINHA ABAIXO!!!
        threadContext.addResponseHeader(ELASTIC_PRODUCT_HTTP_HEADER, ELASTIC_PRODUCT_HTTP_HEADER_VALUE);
        try {
            tryAllHandlers(request, channel, threadContext);
        } catch (Exception e) {
            try {
                channel.sendResponse(new RestResponse(channel, e));
            } catch (Exception inner) {
                inner.addSuppressed(e);
                logger.error(() -> "failed to send failure response for uri [" + request.uri() + "]", inner);
            }
        }
    }
```
Segue o link do arquivo no repositório do github [RestController](https://github.com/elastic/elasticsearch/blob/8.4/server/src/main/java/org/elasticsearch/rest/RestController.java#L308)

Executamos um curl de teste para a API de `_search` e sua IDE deve saltar na tela com o debug travado nessa linha para seguir navegando!
```bash
curl -u elastic:password localhost:9200/_search
```
### Debug no VSCode

Basta abrir o projeto no VSCode utilizando o comando no seu terminal:
```bash
cd elasticsearch-debug/elasticsearch
code .
```

Vamos criar o arquivo de configuração para dar um `Attach to Process` via VSCode.
```bash
mkdir .vscode/
touch .vscode/launch.json
```

Agora edite o arquivo `.vscode/launch.json` incluindo o conteudo abaixo:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "java",
            "name": "Elastic Debug Remote",
            "request": "attach",
            "hostName": "localhost",
            "port": 5007
        }
    ]
}
```

Abra uma aba do terminal indo menu `Terminal > New Terminal` e vamos rodar novamente o comando run do gradlew:
```bash
./gradlew run --debug-jvm

# ou rodando com o Docker + JAVA_OPTIONS
docker-compose up -d
```

Com o projeto rodando, vamos no menu `Run > Start Debugging > Elastic Debug Remote`.

Vamos colocar um breakpoint no arquivo `server/src/main/java/org/elasticsearch/rest/RestController.java` na função abaixo:
```java
    @Override
    public void dispatchRequest(RestRequest request, RestChannel channel, ThreadContext threadContext) {
        // COLOCAR BREAKPOINT NESSA LINHA ABAIXO!!!
        threadContext.addResponseHeader(ELASTIC_PRODUCT_HTTP_HEADER, ELASTIC_PRODUCT_HTTP_HEADER_VALUE);
        try {
            tryAllHandlers(request, channel, threadContext);
        } catch (Exception e) {
            try {
                channel.sendResponse(new RestResponse(channel, e));
            } catch (Exception inner) {
                inner.addSuppressed(e);
                logger.error(() -> "failed to send failure response for uri [" + request.uri() + "]", inner);
            }
        }
    }
```
Segue o link do arquivo no repositório do github [RestController](https://github.com/elastic/elasticsearch/blob/8.4/server/src/main/java/org/elasticsearch/rest/RestController.java#L308)

Executamos um curl de teste para a API de `_search` e sua IDE deve saltar na tela com o debug travado nessa linha para seguir navegando!
```bash
curl -u elastic:password localhost:9200/_search
```

## Conclusão
Debugar sempre é o meu último recurso! É um processo demorado! Prefira sempre documentar a sua aplicação utilizando testes unitários! Para mim esses sim expressam a funcionalidade do sistema e tem mais chances de estarem atualizados (rs...). Porém debugar salva vidas em alguns casos.

Se você chegou até aqui parabéns! Agora é brincar de debugar o projeto do elastic para entender tudo no detalhe e assim poder encontrar bugs e ajudar a manter.

Referências:
- [How to Debug Elasticsearch Source Code in IntelliJ IDEA](https://www.elastic.co/blog/how-to-debug-elasticsearch-source-code-in-intellij-idea)
- [jconwell Gist - Remotly Debug ElasticSearch in IntelliJ](https://gist.github.com/jconwell/1af41535c5ecd2f4a9dd)
- [Development Environment Set-up for a Custom Elasticsearch Plugin](https://ocampor.medium.com/development-environment-set-up-for-a-custom-elasticsearch-plugin-266c0df6bbdd)
- [Install Elasticsearch with Docker](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#docker)
