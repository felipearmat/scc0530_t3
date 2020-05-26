#!/bin/bash
echo "Rodando a versão de desenvolvimento..."

cd $DJANGO_APP_PATH
echo "Instalando Dependencias do Vue..."
cd "$DJANGO_APP_PATH/vue"
npm install
echo "Iniciando app no modo watch.."
npm start &
echo "Atualizando Banco de Dados..."
cd $DJANGO_APP_PATH
python3 manage.py makemigrations
python3 manage.py migrate
echo "Iniciando Servidor..."
python3 manage.py runserver 0.0.0.0:8000
