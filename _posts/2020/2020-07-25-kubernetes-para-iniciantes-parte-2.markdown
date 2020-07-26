---
layout: post
title: Kubernetes para iniciantes - Parte 2
subtitle: Aplicando Secrets, Configmap e Volumes no k8s.
author: Raffael Tancman
date: 2020-07-25 08:51:00 -0300
background: '/img/posts/2020/06/kubernetes-para-iniciantes.jpg'
comments: true
shareBar: true
categories:
    - "kubernetes"
---


Este artigo é a continuação do nosso wordpress rodando no k8s. Caso você não tenha acessado a primeira parte, [clique aqui](https://www.rtancman.com.br/kubernetes/kubernetes-para-iniciantes.html) para entender o que é k8s, quais são seus principais comandos e como subir um wordpress.

Neste artigo vamos evoluir o nosso projeto do wordpress aplicando Secrets, Configmap e Volumes. Vamos iniciar alterando o nosso Deployment para utilizar o Configmap e Secrets.

### Configmap e Secrets na prática

No nosso manifesto atual estamos incluindo as variáveis de ambiente todas no manifesto. Isso não é errado, mas quando se trata de configurações que podem ser compartilhadas entre outros pods o ideal é a gente centralizar essas informações em um manifesto em si. O Configmap vai nos ajudar nesse sentido. Vamos criar o nosso e aplicar essa alteração no Deployment.

Crie o arquivo wp-configmap.yaml com o seguinte conteúdo abaixo:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: meu-blog-escalavel-configmap
data:
  WORDPRESS_DB_HOST: "mariadb-service"
  WORDPRESS_DB_PORT: "3306"
  WORDPRESS_DB_NAME: "wp-k8s"
```

Agora podemos rodar o apply e verificar se tudo esta funcionando.

```bash
kubectl apply -f wp-configmap.yaml
kubectl get configmap

# resultado
NAME DATA AGE
meu-blog-escalavel-configmap 2 11m

# rodando o describe
kubectl describe configmap meu-blog-escalavel-configmap
```

Vamos aplicar essas variáveis no nosso deployment e para isso existem diversas formas de aplicar essa configuração e recomendo a leitura da [documentação aqui](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/#use-configmap-defined-environment-variables-in-pod-commands). Altere o arquivo wp-deployment.yaml com o seguinte conteúdo abaixo:

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
        - name: WORDPRESS_DB_USER
          value: wp-user
        - name: WORDPRESS_DB_PASSWORD
          value: q1w2e3r4
        - name: WORDPRESS_DB_HOST
          valueFrom:
            configMapKeyRef:
              name: meu-blog-escalavel-configmap
              key: WORDPRESS_DB_HOST
        - name: WORDPRESS_DB_PORT
          valueFrom:
            configMapKeyRef:
              name: meu-blog-escalavel-configmap
              key: WORDPRESS_DB_PORT
        - name: WORDPRESS_DB_NAME
          valueFrom:
            configMapKeyRef:
              name: meu-blog-escalavel-configmap
              key: WORDPRESS_DB_NAME
        ports:
        - containerPort: 80
```

Iremos agora alterar o Deployment do nosso banco mariaDB. Altere o arquivo wp-mariadb.yaml com o seguinte conteúdo abaixo:

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
          valueFrom:
            configMapKeyRef:
              name: meu-blog-escalavel-configmap
              key: WORDPRESS_DB_NAME
        ports:
        - containerPort: 3306
          name: mariadb-wp
```

Agora basta aplicar as alterações. Vamos lá!

```bash
kubectl apply -f wp-deployment.yaml
kubectl apply -f wp-mariadb.yaml
```

Pronto! Agora toda vez que alterar o valor do ConfigMap essas variáveis vão ser aplicadas nos nossos deployments. Ainda precisamos acertar as credenciais de acesso e para isso vamos utilizar o [Secret](https://kubernetes.io/docs/concepts/configuration/secret/).

Antes de criar o arquivo vamos precisar colocar os valores de login e senha do banco em base64 encode.

```bash
echo -n  "adminroot" | base64
#resultado
YWRtaW5yb290

echo -n  "wp-user" | base64
#resultado
d3AtdXNlcg==

echo -n  "q1w2e3r4" | base64
#resultado
cTF3MmUzcjQ=
```

Agora é criar o nosso manifesto e para isso vamos criar o arquivo wp-secrets.yaml com o seguinte conteúdo abaixo:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: meu-blog-escalavel-secrets
type: Opaque
data:
  mariadb_username: d3AtdXNlcg==
  mariadb_password: cTF3MmUzcjQ=
  mariadb_root_password: YWRtaW5yb290
```

Vamos aplicar e verificar as configurações.

```bash
kubectl apply -f wp-secrets.yaml
kubectl get secrets meu-blog-escalavel-secrets
#resultado
NAME TYPE DATA AGE
meu-blog-escalavel-secrets Opaque 3 9s

kubectl describe secrets meu-blog-escalavel-secrets
```

Após subir essa configuração, vamos aplicar os secrets em nossos deployments. Altere o arquivo wp-deployment.yaml com o seguinte conteúdo abaixo:

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
        - name: WORDPRESS_DB_USER
          valueFrom:
            secretKeyRef:
              name: meu-blog-escalavel-secrets
              key: mariadb_username
        - name: WORDPRESS_DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: meu-blog-escalavel-secrets
              key: mariadb_password
        - name: WORDPRESS_DB_HOST
          valueFrom:
            configMapKeyRef:
              name: meu-blog-escalavel-configmap
              key: WORDPRESS_DB_HOST
        - name: WORDPRESS_DB_PORT
          valueFrom:
            configMapKeyRef:
              name: meu-blog-escalavel-configmap
              key: WORDPRESS_DB_PORT
        - name: WORDPRESS_DB_NAME
          valueFrom:
            configMapKeyRef:
              name: meu-blog-escalavel-configmap
              key: WORDPRESS_DB_NAME
        ports:
        - containerPort: 80
```

E precisamos alterar o arquivo wp-mariadb.yaml com o seguinte conteúdo abaixo:

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
        - name: MYSQL_USER
          valueFrom:
            secretKeyRef:
              name: meu-blog-escalavel-secrets
              key: mariadb_username
        - name: MYSQL_PASSWORD
          valueFrom:
            secretKeyRef:
              name: meu-blog-escalavel-secrets
              key: mariadb_password
        - name: MYSQL_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: meu-blog-escalavel-secrets
              key: mariadb_root_password
        - name: MYSQL_DATABASE
          valueFrom:
            configMapKeyRef:
              name: meu-blog-escalavel-configmap
              key: WORDPRESS_DB_NAME
        ports:
        - containerPort: 3306
          name: mariadb-wp
```

Com os manifestos alterados vamos aplicar essa nova configuração.

```bash
kubectl apply -f wp-deployment.yaml
kubectl apply -f wp-mariadb.yaml
```

Pronto! Nossos deployments agora estão configurados utilizando ConfigMap e Secrets. Com isso aplicamos boas práticas em nosso manifesto. Agora vamos aplicar o PersistentVolume e fazer com que a nossa base do mariaDB não seja destruida a cada restart dos pods.


## Persistent Volume

Diferentemente dos outros deployments, como este é um banco de dados e não queremos perder as suas informações a cada restart do pod, vamos criar um volume. E para isso vamos alterar o nosso manifesto para incluir a configuração de volumes. Aqui utilizamos o tipo [PersistentVolume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistent-volumes) e [PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims).

Crie o arquivo wp-mariadb-pv.yaml com o seguinte conteúdo abaixo:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: mariadb-pv-volume
  labels:
    type: local
spec:
  capacity:
    storage: 20Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data"
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mariadb-pv-claim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 20Gi
```

Neste aquivo acima estamos criando 2 objetos no k8s que são PersistentVolume e o PersistentVolumeClaim. O k8s permite essa formatação incluindo o delimitador --- defindo onde termina o manifesto. Agora vamos aplicar o nosso volume no Deployment do mariadb.

Alterar o arquivo wp-mariadb.yaml com o seguinte conteúdo abaixo:

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
        - name: MYSQL_USER
          valueFrom:
            secretKeyRef:
              name: meu-blog-escalavel-secrets
              key: mariadb_username
        - name: MYSQL_PASSWORD
          valueFrom:
            secretKeyRef:
              name: meu-blog-escalavel-secrets
              key: mariadb_password
        - name: MYSQL_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: meu-blog-escalavel-secrets
              key: mariadb_root_password
        - name: MYSQL_DATABASE
          valueFrom:
            configMapKeyRef:
              name: meu-blog-escalavel-configmap
              key: WORDPRESS_DB_NAME
        ports:
        - containerPort: 3306
          name: mariadb-wp
        volumeMounts:
        - name: mariadb-persistent-storage
          mountPath: /var/lib/mysql
      volumes:
      - name: mariadb-persistent-storage
        persistentVolumeClaim:
          claimName: mariadb-pv-claim
```

Com isso, vamos executar os comandos de apply.

```bash
kubectl apply -f wp-mariadb-pv.yaml
kubectl apply -f wp-mariadb.yaml

# verificando os nossos volumes
kubectl get pvc mariadb-pv-claim
kubectl get pv mariadb-pv-volume
```

Pronto! Com isso agora podemos restart o nosso deployment sem problemas que a nossa base de dados não vai ser mais removida devido ao volume que criamos. Ainda sim podemos melhor esse manifesto do mariadb. Nesses casos que precisamos de um volume para manter a consistência dos nossos deployments o ideal é utilizar o objeto [StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/). Vamos as alterações em nosso manifesto.

Vamos criar um novo arquivo wp-mariadb-statefullsets.yaml com o seguinte conteúdo abaixo:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mariadb-wp
spec:
  selector:
    matchLabels:
      app: mariadb-wp
  serviceName: mariadb-service
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
        - name: MYSQL_USER
          valueFrom:
            secretKeyRef:
              name: meu-blog-escalavel-secrets
              key: mariadb_username
        - name: MYSQL_PASSWORD
          valueFrom:
            secretKeyRef:
              name: meu-blog-escalavel-secrets
              key: mariadb_password
        - name: MYSQL_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: meu-blog-escalavel-secrets
              key: mariadb_root_password
        - name: MYSQL_DATABASE
          valueFrom:
            configMapKeyRef:
              name: meu-blog-escalavel-configmap
              key: WORDPRESS_DB_NAME
        ports:
        - containerPort: 3306
          name: mariadb-wp
        volumeMounts:
        - name: mariadb-persistent-storage
          mountPath: /var/lib/mysql
  volumeClaimTemplates:
    - metadata:
        name: mariadb-persistent-storage
      spec:
        accessModes: [ "ReadWriteOnce" ]
        resources:
          requests:
            storage: 20Gi
```

Com essa configuração volumeClaimTemplates toda vez que você subir um novo statefullset ou der um scale nesse objeto, o k8s vai criar um novo volume seguindo a especificação do manifesto. Agora vamos executar os comandos.

```bash
# vamos apagar as configurações passadas
kubectl delete deployments mariadb-wp
kubectl delete pvc mariadb-pv-claim
kubectl delete pv mariadb-pv-volume

kubectl apply -f wp-mariadb-statefullsets.yaml
# verificando os nossos volumes
kubectl get pvc mariadb-pv-claim
kubectl get pv mariadb-pv-volume
```

Pronto agora temos o nosso mariadb como statefullset! Mais uma vez parabéns se você chegou até aqui e podemos dizer que o básico sobre Secrets, ConfigMap e Volumes no k8s você acabou de aprender. Leia a documentação e faça os tutoriais no site do k8s para continuar praticando. Todo este código esta no github no repositorio [rtancman/k8s-examples](https://github.com/rtancman/k8s-examples).


Grande abraço!
