---
layout: post
title: Elasticsearch & Spark
subtitle: Ingestão de dados no Elasticsearch com Spark
author: Raffael Tancman
date: 2022-08-17 06:00:00 -0300
background: '/img/posts/2022/08/elasticsearch-spark-ingestao-de-dados.jpg'
comments: true
shareBar: true
categories:
    - "elasticsearch"
---

Recentemente me deparei com o problema de ter que processar um arquivão (muito comum no dia a dia) e fazer algumas operações. Logo em seguida, salvar o resultado em um indice do elasticsearch. Nesses casos eu recorro sempre ao [Apache Spark](https://spark.apache.org/) e pensei será que não existe algum cliente para colocar isso de maneira otimizada no elastic? E como sempre o google me respondeu temos sim e se chama [elasticsearch-hadoop](https://github.com/elastic/elasticsearch-hadoop). Olhando a [Doc](https://www.elastic.co/guide/en/elasticsearch/hadoop/current/spark.html#spark-sql-write), fui testar na prática e em alguns casos tive uns comportamentos inesperados, principalmente utilizando [Dataframes](https://spark.apache.org/docs/latest/sql-programming-guide.html). 

O Spark tem uma API muito boa para lidar com leitura e escrita de Dataframes, ou seja quero usar dessa forma! Googlando um pouquinho mais acabei encontrando na [documentação do Databricks](https://docs.databricks.com/data/data-sources/elasticsearch.html) a forma "certa" de ser fazer. Hoje vou compartilhar com vocês este aprendizado, vamos lá! 

## Configurando o ambiente de trabalho

Quando trabalho no universo JVM recomendo utilizar o [sdkman](https://sdkman.io/) para gerenciar as diversas versões de java, scala, sbt e por aê vai. 

```bash
# instalando o sdkman
curl -s "https://get.sdkman.io" | bash


# instalando versões da jdk, scala, sbt
sdk install 8.0.275.hs-adpt
sdk use java 8.0.275.hs-adpt

sdk install scala 2.12.16
sdk use scala 2.12.16

sdk install sbt 1.7.1
sdk use sbt 1.7.1
```

## Compilando o projeto

Com o ambiente pronto, agora vamos criar o nosso projeto, e eu recomendo utilizar o comando [sbt new ALGUMA_TEMPLATE_QUALQUER](https://www.scala-sbt.org/1.x/docs/sbt-new-and-Templates.html).

```bash
sbt new scala/scala-seed.g8
```

Agora que temos a estrutura do projeto criada, vamos compilar para saber se tudo esta ok!

```bash
sbt compile
sbt run
```

Se tudo deu certo iremos visualizar o seguinte output:

```bash
$ sbt run
[info] welcome to sbt 1.7.1 (Oracle Corporation Java 17.0.2)
[info] loading global plugins from /Users/MEU_USUARIO/.sbt/1.0/plugins
[info] loading project definition from /Users/MEU_USUARIO/elasticsearch-spark/project
[info] loading settings for project root from build.sbt ...
[info] set current project to lala (in build file:/Users/MEU_USUARIO/elasticsearch-spark/)
[info] running example.Hello
hello
```

## Criando o nosso pacote, método main e adicionando as dependências

Agora vamos criar os nossos exemplos em scala.

```bash
mkdir project
mkdir -p src/main/scala/br/com/rtancman/
touch src/main/scala/br/com/rtancman/ElasticsearchSpark.scala
touch project/plugins.sbt
touch docker-compose.yml
```

Edite o arquivo `src/main/scala/br/com/rtancman/ElasticsearchSpark.scala` com o conteudo abaixo:

```scala
package br.com.rtancman

import org.apache.spark.sql.{SparkSession, Row}
import org.apache.spark.sql.types.{StringType, StructField, StructType}
import org.apache.spark.sql.functions._
import scala.collection.JavaConversions._

object ElasticsearchSpark {
  def main(args: Array[String]) {
    val spark = SparkSession
      .builder()
      .appName("elasticsearch-spark-example-1")
      .master("local[*]")
      .config("es.nodes", "localhost")
      .config("es.port", "9200")
      .getOrCreate()

    import spark.implicits._

    val schemaMovie = StructType(
      Array(
        StructField("title", StringType,true),
        StructField("type", StringType,true)
      )
    )
    val rowMovie= Seq(Row("Matrix", "movie"), Row("John Wick", "movie"))

    val df = spark.createDataFrame(rowMovie, schemaMovie)

    df.write
      .format("org.elasticsearch.spark.sql")
      .option("es.resource", "elasticsearch-spark-small-movies")
      .option("es.write.operation", "upsert")
      .option("es.index.auto.create", "true")
      .option("es.nodes.wan.only", "true")
      .option("es.mapping.id", "id")
      .option("es.spark.dataframe.write.null", "true")
      .save()

    spark.close()
  }
}
```

Vamos incluir as dependências. Para isto vamos precisar editar 3 arquivos `project/Dependencies.scala`, `build.sbt` e `project/plugins.sbt` com o conteúdo abaixo:

Arquivo `project/Dependencies.scala`:
```scala
import sbt._

object Dependencies {
  lazy val scalaTest = "org.scalatest" %% "scalatest" % "3.2.11"
  lazy val spark = "org.apache.spark" %% "spark-core" % "3.2.2"
  lazy val sparkSql = "org.apache.spark" %% "spark-sql" % "3.2.2"
  lazy val elasticSpark =
    "org.elasticsearch" % "elasticsearch-spark-30_2.12" % "8.3.3"
}

object ExcludeDependencies {
  lazy val sparkCore2_11 = "org.apache.spark" % "spark-core_2.11"
  lazy val sparkSQL2_11 = "org.apache.spark" % "spark-sql_2.11"
  lazy val sparkYarn2_11 = "org.apache.spark" % "spark-yarn_2.11"
  lazy val sparkStreaming2_11 = "org.apache.spark" % "spark-streaming_2.11"
}
```

Arquivo `build.sbt`:
```scala
import Dependencies._
import ExcludeDependencies._

ThisBuild / scalaVersion := "2.12.16"
ThisBuild / version := "1.0.0"
ThisBuild / organization := "br.com.rtancman"
ThisBuild / organizationName := "rtancman"
ThisBuild / assembly / assemblyMergeStrategy := {
  case PathList("META-INF", _*) => MergeStrategy.discard
  case "application.conf"       => MergeStrategy.concat
  case "reference.conf"         => MergeStrategy.concat
  case _                        => MergeStrategy.first
}

lazy val root = (project in file("."))
  .settings(
    name := "rtancman-elastic-spark-examples",
    libraryDependencies ++= Seq(
      scalaTest % Test,
      elasticSpark,
      spark,
      sparkSql
    ),
    excludeDependencies ++= Seq(
      sparkCore2_11,
      sparkSQL2_11,
      sparkYarn2_11,
      sparkStreaming2_11
    )
  )
```

Arquivo `project/plugins.sbt`:

```scala
addSbtPlugin("com.eed3si9n" % "sbt-assembly" % "1.2.0")
```

Vamos testar se tudo esta ok rodando `sbt compile`. Devemos ter o seguinte resultado:
```bash
[success] Total time: 4 s, completed Aug 17, 2022, 4:44:51 PM
```

## Instalando o spark e elasticsearch

Para executar este programa precisamos de um cluster spark e do elasticsearch. Começando com o setup do spark:

```bash
wget https://archive.apache.org/dist/spark/spark-3.2.2/spark-3.2.2-bin-hadoop2.7.tgz
tar x spark-3.2.2-bin-hadoop2.7.tgz
export SPARK_HOME=`pwd`/spark-3.2.2-bin-hadoop2.7
export PATH=$PATH:$SPARK_HOME:$SPARK_HOME/bin:$SPARK_HOME/sbin
# test
spark-shell
```

Para o elasticsearch, vamos subir com o docker-compose. Edite o arquivo `docker-compose.yml` com o conteúdo abaixo:

```bash
version: '3'
services:
  elasticsearch:
    image: us.gcr.io/jusbrasil-155317/jusbrasil/scooby-tenx-elastic-iteration-test-base:8.3.3
    container_name: elasticsearch_spark
    ports:
      - "9200:9200"
      - "9300:9300"
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    networks:
      - elasticsearch_spark

  kibana:
    image: docker.elastic.co/kibana/kibana:8.3.3
    ports:
      - "5601:5601"
    environment:
      ELASTICSEARCH_URL: http://elasticsearch_spark:9200
      ELASTICSEARCH_HOSTS: http://elasticsearch_spark:9200
    networks:
      - elasticsearch_spark

volumes:
  es_data:
    driver: local

networks:
  elasticsearch_spark:
    driver: bridge
```

## Executando o programa

Para rodar este spark job, vamos subir o elastic, compilar o nosso projeto gerando um .jar e rodar o comando spark-submit. 

```bash
docker-compose up -d

sbt assembly

spark-submit \
  --class br.com.rtancman.ElasticsearchSpark \
  target/scala-2.12/rtancman-elastic-spark-examples-assembly-1.0.0.jar
```

## Verificando no kibana os valores indexados

Nosso docker-compose tem uma imagem do kibana e podemos acessar a url [http://localhost:5601/app/dev_tools](http://localhost:5601/app/dev_tools) para realizar queries no elasticsearch. 

```http
GET /_cat/indices

GET /elasticsearch-spark-small-movies/_search
```

Se tudo correu conforme o esperado o seu resultado deve ser:
```json
{
  "took": 1,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "elasticsearch-spark-small-movies",
        "_id": "2",
        "_score": 1,
        "_source": {
          "id": "2",
          "title": "John Wick",
          "type": "movie"
        }
      },
      {
        "_index": "elasticsearch-spark-small-movies",
        "_id": "1",
        "_score": 1,
        "_source": {
          "id": "1",
          "title": "Matrix",
          "type": "movie"
        }
      }
    ]
  }
}
```

## Conclusão

Spark e Elasticsearch são duas ferramentas poderosas e neste artigo busquei detalhar como podemos trabalhar com elas em conjunto para gerar valor no nosso dia a dia.

Referências:
- [ElasticSearch - Data ingestion Doc by Databrics](https://docs.databricks.com/data/data-sources/elasticsearch.html)
- [Elastic - Apache Spark Support](https://www.elastic.co/guide/en/elasticsearch/hadoop/current/spark.html)
- [Writing a Spark Dataframe to an Elasticsearch Index](https://docs.databricks.com/data/data-sources/elasticsearch.html)