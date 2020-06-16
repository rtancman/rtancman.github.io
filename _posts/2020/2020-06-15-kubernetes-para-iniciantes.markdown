---
layout: post
title: Kubernetes para iniciantes
subtitle: Meu diário de bordo contando como foi a minha primeira experiência com Kubernetes.
author: Raffael Tancman
date: 2020-06-15 17:55:00 -0300
background: '/img/posts/2020/06/kubernetes-para-iniciantes.jpg'
comments: true
shareBar: true
categories:
    - "kubernetes"
---

Me lembro como se fosse hoje quando comecei a virtualizar o meu ambiente de desenvolvimento. Antes rodava tudo em uma VM do VirtualBox montando o diretório do meu projeto na VM. Com o passar dos tempos acabei conhecendo o [Vagrant](https://www.vagrantup.com/) e mais a frente o [Docker](https://www.docker.com/) que foi amor à primeira vista! Desde então passei a gerenciar meu ambiente de desenvolvimento com docker-compose.

Participei de um movimento de migrar aplicações que rodam no heroku para o Google Cloud utilizando o serviço Kubernetes Engine o GKE. Nesse projeto eu trabalhei bem superficialmente com k8s, apelido do kubernetes. Atualmente venho trabalhando diariamente com essa ferramenta e neste artigo vou contar como foi todo o meu aprendizado e sintetizar os principais casos do dia a dia.

### O que é o Kubernetes?

É um gerenciador de containers onde utilizamos uma sintaxe declarativa para criar nossos serviços na cloud. O kubernetes veio nessa era de containers para facilitar todas as operações e boas práticas que temos hoje disponíveis em cloud para deployar suas aplicações. Com isso foi sendo construído um ecossistema em volta dessa tecnologia com muitos serviços e plugins tais como recursos de monitoração, autoscale, blue-green deployments, service discovery e muitos outros disponíveis pela comunidade.


### Como ele funciona?

<img alt="k8s arquitetura" src="/img/posts/2020/06/k8s-arquitetura.png" style="max-width: 992px;width: 100%;" />
Fonte: kubernetes.io

De forma resumidamente o k8s é uma aplicação em Go que se comunica através de uma API. O Docker não consegue gerenciar containers de maneira remota e é aí que o k8s passa a fazer sentido. Essa arquitetura acima foi retirada do site oficial do kubernetes e pode ser acessada [aqui](https://kubernetes.io/docs/concepts/overview/components/) onde temos a documentação que detalha esse processo por inteiro. Mas para vocês entenderem de uma forma geral, temos 2 nodes onde em 1 temos rodando a API do k8s com todo os seus componentes como etcd que é o banco de chave valor onde ficam salvas todas as configurações e no segundo node temos o kubelet que é o cliente responsável em se comunicar com a API do k8s e aplicar as alterações nos containers que rodam em cada máquina.


O objetivo desse artigo é ser um guia prático de como você pode executar os serviços em ambiente local ou até mesmo em cloud, não vou entrar em detalhes de como funciona todos os componentes do kubernetes. Para isso você pode e deve ler a documentação para entender como essa ferramenta irá te ajudar no dia a dia. [Neste link você confere a documentação do Kubernetes que é bem completa e repleta de exemplos.](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

Agora precisamos instalar o nosso ambiente de trabalho que basicamente vai precisar do Docker, Kubernetes e algumas outras aplicações para deployar o nosso sistema.

### Instalação:

Vamos precisar instalar o [kubectl](http://kubernetes.io/docs/tasks/tools/install-kubectl/) e o [minikube](http://github.com/kubernetes/minikube#installation) para quem tem linux. No  mac, o próprio docker já tem um suporte para subir um cluster k8s. Caso você esteja rodando no mac, segue um tutorial de como levantar um cluster local [nesse link aqui](https://xebia.com/blog/running-kubernetes-locally-docker-mac-os-x/).

-   Kubectl: É o CLI para iteragir com o cluster k8s.
-   Minikube: Simula em uma VM o funcionamento de um cluster k8s em ambiente local.

Para você já sair executando os comandos do kubectl recomendo esses playgrounds:
-   [Katacoda](https://www.katacoda.com/courses/kubernetes/playground)
-   [Play with Kubernetes](https://labs.play-with-k8s.com/)


Agora que já temos um um cluster rodando, vamos iniciar dar uma explorada nos principais comandos do k8s que vamos utilizar durante o desenvolvimento.

O k8s permite que você gerencie diversos clusters e por isso e sempre bom ver os que estão configurados com o comando `kubectl config get-contexts`. Exemplo:

```bash
$ kubectl config get-contexts
CURRENT NAME CLUSTER AUTHINFO NAMESPACE

docker-desktop docker-desktop docker-desktop

* docker-for-desktop docker-desktop docker-desktop
```

Para selecionar um contexto você roda o seguinte comando:

```bash
$ kubectl config use-context docker-for-desktop
```

Esses passos são importantes principalmente se você já tem acesso a um cluster k8s na sua máquina para não criar nada em cluster que já exista ;)

### K8S em prática com um pod simples

Vamos subir agora um Pod com o Wordpress baseado em uma imagem do Docker que está disponível no [hub docker do wordpress](https://hub.docker.com/_/wordpress/) para testar alguns dos comandos do k8s. Não se preocupe com o arquivo abaixo vamos entender ele melhor mais a frente ;)

Crie o arquivo wp-dumb.yaml com o seguinte conteudo abaixo:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: meu-blog
  labels:
    app: wordpress
spec:
  containers:
  - name: meu-blog-wp-1
    image: wordpress:php7.2-fpm
    ports:
    - containerPort: 9000
```

Agora vamos subir o nosso primeiro Pod! Para isso vamos rodar o seguinte comando:

```bash
$ kubectl apply -f wp-dumb.yaml
```

Acima vimos o nosso primeiro comando o kubectl apply como vocês já viram, ele é responsável em aplicar alterações feita no arquivo wp-dumb.yaml. Após ele aplicar essa alteração o k8s se encarrega em subir um Pod com a configuração descrita no manifesto do aquivo wp-dumb.yaml. Agora podemos rodar outros comandos para visualizar como esta este Pod recem criado.

Para listar todos os pods rodando vamos executar o [kubectl get](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#get):

```bash
$ kubectl get pods

#resultado

NAME READY STATUS RESTARTS AGE

meu-blog 1/1 Running 0 59s
```

O comando get diz como está o nosso Pod em nosso cluster. Veja em detalhes:

-   NAME: é o nome do Pod. E este nome é ÚNICO.
-   READY: diz que o nosso Pod está rodando / pronto.
-   STATUS: é o status atual de execução
-   RESTARTS: quantidade de restarts que o pod teve
-   AGE: A quanto tempo ele foi criado

[Aqui na documentação do k8s](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#get) você tem todos os exemplos dos comandos a serem executados. Mas vamos falar dos que mais rodamos no dia a dia.

```bash
# para buscar um pod por nome
$ kubectl get pods meu-blog

# para buscar um pod por label
$ kubectl get pods -l app=wordpress

# para retornar em outro formato de output
$ kubectl get pods -l app=wordpress -o yaml
$ kubectl get pods -l app=wordpress -o json
```

Também podemos acessar esse Pod rodando o [kubectl exec](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#exec):

```bash
$ kubectl exec -it meu-blog bash
root@meu-blog:/var/www/html#
```

Descrição desse Pod rodando o [kubectl describe](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#describe):

```bash
$ kubectl describe pods -l app=wordpress
$ kubectl describe pods meu-blog
```

Copiando arquivos para o container ou do container para a sua máquina com o comando cp rodando o [kubectl cp](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#cp):

```bash
# criando um arquivo qualquer
$ echo "lala" > arquivo-lala.txt

# copiando um arquivo para o container
$ kubectl cp arquivo-lala.txt meu-blog:/var/www/html

# copiando um arquivo do container para sua maquina
$ kubectl cp meu-blog:/var/www/html/arquivo-lala.txt arquivo-lele.txt
```

Verificando CPU e Memoria com o comando top rodando o [kubectl top](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#top):

```bash
$ kubectl top pods -l app=wordpress
$ kubectl top pods meu-blog
```

Remover um Pod rodando o [kubectl delete](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#delete):

```bash
$ kubectl delete pods -l app=wordpress
$ kubectl delete pods meu-blog
```

Se você chegou até aqui MEUS PARABÉNS você conseguiu subir um pod e principalmente executar uns dos comandos que mais utilizamos no dia a dia! Na documentação oficial, temos uma parte muito interessante com os "macetes" para servir como um guia quando você não se lembrar exatamente como é cada comando do k8s que é o [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/).



### K8S em prática subindo um wordpress completo

Nosso aplicação que irá rodar no kubernetes vai ser um wordpress um dos principais cms do mundo. Teremos a seguinte arquitetura:

<img alt="wordpress no k8s arquitetura" src="/img/posts/2020/06/wp-k8s.jpg" style="max-width: 992px;width: 100%;" />

No exemplo anterior a gente utilizou o objeto Pod que é o objeto mais genérico do k8s. [Aqui na documentação você tem todos os detalhes](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/). Agora nesse exemplo vamos utilizar o [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) para criar um Pod mais inteligente dizendo em seu manifesto a quantidade de réplicas que devem sempre executar em nosso cluster. Isso mesmo, o k8s com base no manifesto vai gerenciar a execução desse pod podendo remover e recriar o mesmo caso alguma coisa de errado aconteça. Vamos a esse manifesto:

Crie o arquivo wp-deployment.yaml com o seguinte conteúdo abaixo:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: meu-blog-escalavel
  labels:
    app: wordpress-escalavel
spec:
  replicas: 3
  selector:
    matchLabels:
      app: wordpress-escalavel
  template:
    metadata:
      labels:
        app: wordpress-escalavel
    spec:
      containers:
      - name: wordpress
        image: wordpress:5.4.2-php7.2-apache
        ports:
        - containerPort: 80
```

Agora vamos subir o nosso primeiro deployment!

```bash
$ kubectl apply -f wp-deployment.yaml
```

Sim temos 3 pods em execução vamos olhar rodando o comando get:

```bash
$ kubectl get pods -l app=wordpress-escalavel
NAME READY STATUS RESTARTS AGE
meu-blog-escalavel-69f498dc5b-25zb7 1/1 Running 0 19s
meu-blog-escalavel-69f498dc5b-7dx4z 1/1 Running 0 19s
meu-blog-escalavel-69f498dc5b-zbtvs 1/1 Running 0 19s
```

Agora vamos brincar com o k8s vamos deletar o um dos Pods criados e ficar dando o get para ver o que esta irá acontecer.

```bash
$ kubectl delete pod meu-blog-escalavel-69f498dc5b-c7hvd
pod "meu-blog-escalavel-69f498dc5b-c7hvd" deleted

$ kubectl get pods -l app=wordpress-escalavel
NAME READY STATUS RESTARTS AGE
meu-blog-escalavel-69f498dc5b-7dx4z 1/1 Running 0 4m33s
meu-blog-escalavel-69f498dc5b-c7hvd 0/1 Terminating 0 36s
meu-blog-escalavel-69f498dc5b-jb424 1/1 Running 0 6s
meu-blog-escalavel-69f498dc5b-zbtvs 1/1 Running 0 4m33s
```

Caso algum pode seja deletado o k8s sobe outro o mais rápido possível e mantém sempre o que está configurado no manifesto do arquivo wp-deployment.yaml. Agora vamos explorar novos comandos que os deployments tem que é o [kubectl scale](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#scale).

```bash
$ kubectl scale deployment meu-blog-escalavel --replicas=5

$ kubectl get pods -l app=wordpress-escalavel

NAME READY STATUS RESTARTS AGE
meu-blog-escalavel-69f498dc5b-66bbr 1/1 Running 0 7s
meu-blog-escalavel-69f498dc5b-7dx4z 1/1 Running 0 22h
meu-blog-escalavel-69f498dc5b-jb424 1/1 Running 0 22h
meu-blog-escalavel-69f498dc5b-x57f8 1/1 Running 0 7s
meu-blog-escalavel-69f498dc5b-zbtvs 1/1 Running 0 22h
```

Pronto nosso sistema do wordpress está escalável podendo subir ou diminuir réplicas. Agora falta a gente configurar o nosso load balancer, que no caso do k8s será o [Service](https://kubernetes.io/docs/concepts/services-networking/service/). Este é responsável em localizar o nosso deployment e expor o serviço do mesmo através de um endereço tendo o funcionamento comparado ao de um load balancer distribuindo a carga. Vamos a esse manifesto:

Crie o arquivo wp-service.yaml com o seguinte conteúdo abaixo:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: meu-blog-escalavel-service
spec:
  type: LoadBalancer
  selector:
    app: wordpress-escalavel
  ports:
    - protocol: TCP
      port: 8080
      targetPort: 80
```

Agora vamos subir o nosso primeiro service!

```bash
$ kubectl apply -f wp-service.yaml
```

Para visualizar o nosso service executando rodamos o comando get mas agora incluindo o tipo service. Sim o k8s segue um padrão e trocando o kind você lista somente os pods de um tipo específico.

```bash
$ kubectl get service

NAME TYPE CLUSTER-IP EXTERNAL-IP PORT(S) AGE
meu-blog-escalavel-service ClusterIP 10.102.166.220 localhost 8080/TCP 7m57s
```

Agora todos os nossos deployments ficam acessíveis através do service recém criado que consegue localizar os pods por conta da configuração de selector que utiliza o label aplicado a um pod para localizar para onde a requisição deve chegar. Agora basta chamar localhost:8080 que vamos bater no service e o mesmo redireciona o tráfego para os nossos deployments como um load balancer. Agora que já temos o nosso LB e wordpress de pé precisamos subir o nosso banco de dados. Vamos a esse manifesto:

Crie o arquivo wp-mariadb.yaml com o seguinte conteúdo abaixo:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mariadb-wp
spec:
  selector:
    matchLabels:
      app: mariadb-wp
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: mariadb-wp
    spec:
      containers:
      - name: mariadb-wp
        image: rtancman/mariadb-local
        imagePullPolicy: "Always"
        env:
        - name: MYSQL_ROOT_PASSWORD
          value: adminroot
        - name: MYSQL_USER
          value: wp-user
        - name: MYSQL_PASSWORD
          value: q1w2e3r4
        - name: MYSQL_DATABASE
          value: wp-k8s
        ports:
        - containerPort: 3306
          name: mariadb-wp
```

Com isso agora como já sabemos, falta criar o nosso service e vamos lá! Crie o arquivo wp-mariadb-service.yaml com o seguinte conteúdo abaixo:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: mariadb-service
spec:
  type: LoadBalancer
  selector:
    app: mariadb-wp
  ports:
    - protocol: TCP
      port: 3306
      targetPort: 3306
```

Agora vamos dar apply em todos os manifestos recém criados:

```yaml
$ kubectl apply -f wp-mariadb.yaml
$ kubectl apply -f wp-mariadb-service.yaml
```
Agora temos o nosso banco rodando! Com isso vamos alterar o nosso manifesto do wp-deployment.yaml para incluir as variáveis de ambiente que tem o acesso ao banco de dados.

Altere o arquivo wp-deployment.yaml com o seguinte conteúdo abaixo:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: meu-blog-escalavel
  labels:
    app: wordpress-escalavel
spec:
  replicas: 3
  selector:
    matchLabels:
      app: wordpress-escalavel
  template:
    metadata:
      labels:
        app: wordpress-escalavel
    spec:
      containers:
      - name: wordpress
        image: wordpress:5.4.2-php7.2-apache
        env:
        - name: WORDPRESS_DB_HOST
          value: mariadb-service
        - name: WORDPRESS_DB_USER
          value: wp-user
        - name: WORDPRESS_DB_PASSWORD
          value: q1w2e3r4
        - name: WORDPRESS_DB_NAME
          value: wp-k8s
        ports:
        - containerPort: 80
```

MEUS PARABÉNS! Você acabou de configurar a nossa arquitetura proposta no exemplo e tudo esta deve estar rodando normalmente se você acessar o [http://localhost:8080/](http://localhost:8080/) deve cair na página de configuração do wordpress e seguindo os passos você terá o mesmo rodando no seu cluster k8s \o/.

Kubernetes é uma ferramenta com muitos plugins e serviços e irei fazer um novo post melhorando essa nossa arquitetura utilizando outros objetos do k8s como o [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/), [Configmap](https://kubernetes.io/docs/concepts/configuration/configmap/), [PersistentVolume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistent-volumes) e [PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims).

Referências:
-   [https://kubernetes.io/docs/concepts/](https://kubernetes.io/docs/concepts/)
-   [https://kubernetes.io/docs/tutorials/stateful-application/mysql-wordpress-persistent-volume/](https://kubernetes.io/docs/tutorials/stateful-application/mysql-wordpress-persistent-volume/)
-   [https://xebia.com/blog/running-kubernetes-locally-docker-mac-os-x/](https://xebia.com/blog/running-kubernetes-locally-docker-mac-os-x/)
-   [https://medium.com/containers-101/local-kubernetes-for-mac-minikube-vs-docker-desktop-f2789b3cad3a](https://medium.com/containers-101/local-kubernetes-for-mac-minikube-vs-docker-desktop-f2789b3cad3a)

Grande abraço xD