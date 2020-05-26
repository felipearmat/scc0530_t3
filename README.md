# SCC0530 - Inteligência Artificial - Trabalho Prático (Labirinto)

## Resumo do Trabalho:

Trabalho Prático de Inteligência Artificial envolvendo a resolução de um labirinto através dos métodos de busca por profundidade, busca por largura, método best first, método de busca A e método hill climbing.

## O que vamos encontrar aqui?
- Várias pastas que configuram um projeto Django (app Web), o conteúdo principal está na pasta "base" que é o cerne do app.
- Uma pasta "vue" com uma app Vue.js que é, resumidamente, a interface do app WEB.
- As únicas coisas que realmente importam para este trabalho são o arquivo base/views.py (que possue a API, as funções de busca e a função de renderização da página principal) e o arquivo vue/src/templates/home.vue (que possui a interface, que desenha o mapa, faz as requisições de busca e mantém os vetores de resposta obtidos em cada requisição).

## Como executar (com Docker)?
- Instale o Docker: https://docs.docker.com/v17.12/install/
- Acesse a pasta do projeto e faça o build da Imagem (isso criará o contâiner do Docker - que é praticamente uma VM - com todos as dependências necessárias para se rodar o sistema):
```
docker build --build-arg PROJECT=scc0530_t3 -t scc0530_t3 .
```
- Ainda na pasta do projeto, execute o comando abaixo para iniciar a Imagem (esse comando iniciará o contâiner do projeto, mapeando a porta 8000 do seu pc com a porta 8000 da imagem, criando um diretório virtual para guardar os dados do BD e mapeando a pasta do projeto para a pasta webapps/scc0530_t3/scc0530_t3_app do contâiner):
```
# Comando para Windows
docker run -it --rm --name=scc0530_t3 -p 8000:8000 -v %cd%:/webapps/scc0530_t3/scc0530_t3_app scc0530_t3

# Comando para Unix
docker run -it --rm --net=host --name=scc0530_t3 -v `pwd`:/webapps/scc0530_t3/scc0530_t3_app scc0530_t3
```
- Acesse com seu navegador predileto o endereço localhost:8000

## Como executar (com Python)?
TODO
