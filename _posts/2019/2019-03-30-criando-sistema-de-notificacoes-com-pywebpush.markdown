---
layout: post
title: Criando um sistema de notificações com  pywebpush
subtitle: Vamos utilizar o pywebpush para criar uma API de notificações simples.
author: Raffael Tancman
date: 2019-03-30 17:55:00 -0300
background: '/img/posts/2019/03/criando-sistema-de-notificacoes-com-pywebpush.jpg'
comments: true
shareBar: true
categories:
    - "python"
---

Esses dias um amigo veio me perguntar no GruPy Blumenau em como criar um sistema de notificações e acabei passando meio que o caminho das pedras que poderia utilizar o [Firebase](https://firebase.google.com/) ou utilizar o [notification API](https://developer.mozilla.org/en-US/docs/Web/API/notification) para isso. Como eu nunca tinha desenvolvido um sistema para esse caso resolvi então criar um post sobre este tema.

## Web Push Notifications

Existe um padrão para realizar esse tipo de operação na web que é o [Push API](https://developer.mozilla.org/en-US/docs/Web/API/Push_API).

![Push API](/img/posts/2019/03/Push_API.jpg)

Basicamente o que acontece é o seguinte:

1. O cliente solicita permissão ao navegador para receber notificações
2. O navegador gera uma credencial de acesso e o cliente passa esses dados para o servidor
3. O servidor manda uma notificação com as credenciais para o serviço
4. O serviço notifica os navegadores

Todo este processo utiliza o [Web Push Protocol](https://tools.ietf.org/html/draft-ietf-webpush-protocol-12). Este protocolo descreve como toda essa comunicação deve ser feita e com isso temos um padrão para enviar notificações para os navegadores. O projeto [web-push-libs](https://github.com/web-push-libs) tem implementações desse protocolo para diversas linguagens. Neste post vamos utilizar a implementação feita para Python que é o [pywebpush](https://github.com/web-push-libs/pywebpush).

## Sistema de Notifição

Vamos criar uma API e um site. Todo o código esta disponível no repositorio [flask-pywebpush](https://github.com/rtancman/flask-pywebpush). Além disso apaixonado por Makefile como sou criei todos os comandos que iremos executar nele para saber mais acesse o [arquivo e veja os comandos na íntegra](https://github.com/rtancman/flask-pywebpush/blob/master/Makefile).

### API de notificação
Na nossa API vamos utilizar flask, redis e pywebpush para desenvolver nossa aplicação.

A API armazenará as informações de assinatura dos usuários e distribuirá a chave pública VAPID. VAPID é o curto prazo para Identificação Voluntária do Servidor de Aplicativos, a chave pública gerada será usada através do aplicativo cliente.

Gerando as chaves:

```bash

make generate.vapid

```
OBS: Estou usando como base **linux** e o **openssl**. Portanto para gerar essas chaves você precisa ter o openssl instalado em sua máquina.

Após rodar o comando vamos ter gerado os seguintes arquivos no diretório **flaskwebpush/certs** no projeto:

- private_key.txt
- public_key.txt
- vapid_private.pem
- vapid_public.pem

Nosso backend terá as seguintes rotas:

- /api/subscribe
- /api/notify
- /api/unsubscribe

### /api/subscribe

Responsável por inscrever o cliente para receber notificações do nosso site. Esta rota atende aos verbos:

GET - Responsável por retornar a chave pública a ser utilizada no cliente que é o nosso site
POST - Responsável por inscrever o cliente. Aqui recebemos o endereço e as credenciais de acesso para realizar o push de notificação.

Segue o código:

```python

@api.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if request.method == "GET":
      return jsonify({'public_key': VAPID_PUBLIC_KEY})
    print(request.json)
    subscription_info = {
      'endpoint': request.json.get('endpoint'),
      'keys': request.json.get('keys'),
      'expiration_time': request.json.get('expirationTime'),
    }
    webpush_key = str(uuid.uuid4())
    redis_webpush.set('webpush:subscription:info:{}'.format(webpush_key), json.dumps(subscription_info))
    redis_webpush.sadd('webpush:subscriptions', webpush_key)
    return jsonify({'id': webpush_key})

```

### /api/notify

Responsável em realizar o push dessa notificação aos clientes inscritos no nosso site. Esta recebe um POST com os dados da mensagem que queremos enviar aos clientes. Segue o código:

```python

@api.route('/notify', methods=['POST'])
def notify():
    from pywebpush import webpush, WebPushException
    count = 0
    sub_webpush_key = 'webpush:subscription:info:{}'
    message_data = {
      'title': request.json.get('title'),
      'body': request.json.get('body'),
      'url': request.json.get('url'),
    }
    for key in redis_webpush.smembers('webpush:subscriptions'):
        try:
            sub_key = sub_webpush_key.format(key.decode())
            sub_val = redis_webpush.get(sub_key)
            if sub_val:
              webpush(
                  subscription_info=json.loads(sub_val),
                  data=json.dumps(message_data),
                  vapid_private_key=VAPID_PRIVATE_KEY,
                  vapid_claims=VAPID_CLAIMS
              )
              count += 1
        except WebPushException as e:
            print(e)
    return "{} notification(s) sent".format(count)

```

### /api/unsubscribe

Responsável por descadastrar o cliente que não quer mais receber notificações do nosso site. Recebe um POST com o identificador do cliente para remover. Segue o código:

```python

@api.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    webpush_key = request.json.get('client_uuid')
    if not webpush_key:
      return jsonify({'message': 'client_uuid is required'}), 400
             redis_webpush.delete('webpush:subscription:info:{}'.format(webpush_key))
    redis_webpush.srem('webpush:subscriptions', webpush_key)
    return jsonify({'message': 'unsubscribed'})

```

Agora que conhecemos a nossa API vamos rodar o nosso projeto:

```bash

git clone git@github.com:rtancman/flask-pywebpush.git

cd flask-pywebpush

python3 -m venv .venv

make setup setup.web

# levando o redis com docker
make run.redis

# rodando a api
make run.api

# rodando o site web
run.web

```

Com a nossa aplicação rodando, abra no seu navegador o endereço [http://127.0.0.1:8080](http://127.0.0.1:8080). Neste link temos o nosso site que foi baseado no projeto [GoogleChromeLabs/web-push-codelab](https://github.com/GoogleChromeLabs/web-push-codelab).

Vamos realizar a ação para se inscrever:

![Clicando para receber notificações](/img/posts/2019/03/notificacoes-clicar-para-receber.gif)

Após clicar no button, vamos ver as credenciais de acesso que são enviadas ao nosso servidor. Após este processo, agora vamos enviar a nossa mensagem pelo servidor e para isso vamos utilizar o curl para fazer o post:

```bash

curl -X POST \
  http://127.0.0.1:5000/api/notify \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '{
	"title": "Minha notificação!",
	"url": "http://localhost:8080/",
	"body": "O corpo da minha notificação com a menssagem."
}'

```

Após realizar este comando você irá receber uma notificação como abaixo:

![Recebendo notificações](/img/posts/2019/03/notificacoes-recebendo-notificacao.gif)

Com isso fechamos por aqui nosso sistema simples de notificação. Para testar a API diretamente do postman basta importar o arquivo [flaskwebpush.postman_collection.json](https://github.com/rtancman/flask-pywebpush/flaskwebpush.postman_collection.json).

Para se aprofundar mais no assunto recomendo a leitura desses links:

- [https://developers.google.com/web/fundamentals/push-notifications/](https://developers.google.com/web/fundamentals/push-notifications/)
- [https://developer.mozilla.org/en-US/docs/Web/API/Push_API](https://developer.mozilla.org/en-US/docs/Web/API/Push_API)
- [https://serviceworke.rs/web-push.html](https://serviceworke.rs/web-push.html)

Grande abraço!