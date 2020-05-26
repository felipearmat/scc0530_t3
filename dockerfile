# Começamos com uma imagem do Debian 10
FROM debian:10

LABEL maintainer="SCC0530 - Inteligência Artificial"

ENV TZ America/Sao_Paulo

# Setup do ambiente (atualiza o SO, acerta o timezone e instala nginx, node e uwsgi).
RUN echo $TZ > /etc/timezone \
 && rm /etc/localtime \
 && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
 && apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y --no-install-recommends locales acl libcurl4-gnutls-dev ntp htop python3-pip ipython3 nginx npm \
 supervisor apt-transport-https software-properties-common gnupg gnutls-dev build-essential curl libpq-dev gettext-base
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install -y nodejs \
 && apt-get clean

# Adicionando repositorio de segurança
RUN add-apt-repository "deb http://security.debian.org/debian-security buster/updates main contrib non-free"

# Adicionando repositório do python para bionic
RUN add-apt-repository "deb http://ppa.launchpad.net/deadsnakes/ppa/ubuntu bionic main" \
 && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys BA6932366A755776

# Instalando Python e uwsgi
RUN apt-get update \
 && apt-get install -y python3.7 python3.7-dev python3-setuptools \
 && pip3 install uwsgi

######################################################

# Instalando dependências do Python
COPY ./setup/requirements.txt /opt/requirements.txt
RUN pip3 install --no-cache-dir -r /opt/requirements.txt

# Variáveis de ambiente que configuram o watcher "chokidar" do
# node.js, para evitar problemas com o docker rodando no Windows
ENV CHOKIDAR_USEPOLLING 1
ENV CHOKIDAR_INTERVAL 1000

# ARG precisa ter um valor default
ARG PROJECT="PROJETO_BASE"

# Variáveis de Ambiente
ENV PROJECT=$PROJECT
ENV APP_FOLDER ${PROJECT}_app
ENV DJANGO_APP_PATH /webapps/${PROJECT}/${APP_FOLDER}

# Arquivos do Django
COPY ./base       ${DJANGO_APP_PATH}/base
COPY ./config     ${DJANGO_APP_PATH}/config
COPY ./templates  ${DJANGO_APP_PATH}/templates
COPY ./vue        ${DJANGO_APP_PATH}/vue
COPY ./manage.py  ${DJANGO_APP_PATH}/manage.py

# Pré-instalando dependencias do Vue
RUN cd ${DJANGO_APP_PATH}/vue \
 && npm install

# Gerando arquivos estáticos do Django
RUN cd ${DJANGO_APP_PATH}/ \
 && python3 manage.py collectstatic --noinput

# Removendo excessos (node_modules)
RUN rm -rf ${DJANGO_APP_PATH}/vue/node_modules

# Copiando script para execução do container
COPY ./setup/run.sh /opt/run.sh

EXPOSE 8000

WORKDIR /opt

# Comando padrão para execução do container
CMD ["/opt/run.sh"]
