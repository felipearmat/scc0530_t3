from django.views.generic.base import TemplateView

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import copy
import time
from typing import Callable, Optional
from random import sample # Retorna uma amostra da lista passada com os elementos ordenados aleatoriamente

######## Renderização da página/template ######################################
class HomeView(TemplateView):
    template_name = 'index.html'

######## Funções de Busca #####################################################
def obtem_vizinhos(matriz:list, ponto:list, visitados:list):
    i, j = ponto
    i_max = len(matriz) - 1
    j_max = len(matriz[i]) - 1
    resposta = []

    # Quadrado de cima
    if i > 0 and [i - 1, j] not in visitados and matriz[i - 1][j] != '-':
        resposta.append([i - 1, j])
    # Quadrado de baixo
    if i < i_max and [i + 1, j] not in visitados and matriz[i + 1][j] != '-':
        resposta.append([i + 1, j])
    # Quadrado da esquerda
    if j > 0 and [i, j - 1] not in visitados and matriz[i][j - 1] != '-':
        resposta.append([i, j - 1])
    # Quadrado da direita
    if j < j_max and [i, j + 1] not in visitados and matriz[i][j + 1] != '-':
        resposta.append([i, j + 1])

    # Retorna um vetor de pontos ordenado aleatóriamente
    return sample(resposta, len(resposta))

def distancia_pontos(ponto_a:list, ponto_b:list):
    xa, ya = ponto_a
    xb, yb = ponto_b
    return ((xa - xb) ** 2 + (ya - yb) ** 2) ** 0.5

def distancia_ponto_objetivos(ponto:list, objetivos:list):
    vetor_distancias = []
    for objetivo in objetivos:
        vetor_distancias.append(distancia_pontos(ponto, objetivo))
    return min(vetor_distancias)

# Para melhor clareza informamos os tipos na assinatura da função, fica mais
# claro também informarmos quais parâmetros são opcionais em sua chamada
def busca_profundidade(mapa:dict, visitados:Optional[list] = None):
    # OBS: Utilizamos o método iterativo de busca por este possívelmente
    # alocar uma quantidade menor de memória que o método recursivo
    # OBS2: Nunca se deve atribuir um valor opcional como uma lista ou objeto, pois isso cria
    # uma falha de segurança. Por isso atribuímos None e então checamos no código seu valor
    visitados = [] if not visitados else copy.deepcopy(visitados)
    caminho = []
    nos = sample(mapa['origem'], len(mapa['origem']))
    while nos:
        atual = nos.pop()
        caminho.append(atual)
        visitados.append(atual)
        vizinhos = obtem_vizinhos(mapa['matriz'], atual, visitados)
        if vizinhos:
            if len(vizinhos) > 1:
                for item in range(len(vizinhos) - 1):
                    caminho.append('decisao')
            for vizinho in vizinhos:
                if vizinho in mapa['objetivo']:
                    caminho.append(vizinho)
                    nos = []
                    break
                nos.append(vizinho)
        else:
            valor = None
            while caminho and valor != 'decisao':
                valor = caminho.pop()
    resposta = [list(filter(lambda x: x != 'decisao', caminho)), len(visitados)]
    return resposta

def busca_largura(mapa:dict):
    visitados = []
    caminho = []
    iniciais = sample(mapa['origem'], len(mapa['origem']))
    # Uma vez que podemos ter mais de um ponto inicial uma busca por
    # profundidade é executada para cada ponto inicial fornecido
    for inicial in iniciais:
        if inicial not in visitados:
            caminhos = [[inicial]]
            while caminhos:
                caminho_atual = list(caminhos.pop(0))
                atual = caminho_atual[-1]
                visitados.append(atual)
                if atual in mapa['objetivo']:
                    caminho = caminho_atual
                    break
                vizinhos = obtem_vizinhos(mapa['matriz'], atual, visitados)
                for vizinho in vizinhos:
                    novo_caminho = caminho_atual.copy()
                    novo_caminho.append(vizinho)
                    caminhos.append(novo_caminho)
        if caminho:
            break
    resposta = [caminho, len(visitados)]
    return resposta

def algoritmo_bf(mapa:dict, funcao_custo:Callable[[dict], float]):
    # O algoritmo de busca A é um caso especial do best-first, por isso utilizamos uma função comum para os
    # dois algoritmos
    caminho = []
    visitados = []
    rotas = []
    for origem in mapa['origem']:
        rotas.append({'distancia': distancia_ponto_objetivos(origem, mapa['objetivo']),
                      'caminho': [origem]})
    while rotas:
        rotas.sort(key = funcao_custo)
        rota_atual = dict(rotas.pop(0))
        atual = rota_atual.get('caminho')[-1]
        visitados.append(atual)
        if atual in mapa['objetivo']:
            caminho = rota_atual.get('caminho')
            break
        vizinhos = obtem_vizinhos(mapa['matriz'], atual, visitados)
        for vizinho in vizinhos:
            # Como rota possui um vetor de vetores que não queremos alterar, precisamos
            # efetuar um deepcopy para manter a imutabilidade do vetor caminho.
            nova_rota = copy.deepcopy(rota_atual)
            nova_rota['caminho'].append(vizinho)
            nova_rota['distancia'] = distancia_ponto_objetivos(vizinho, mapa['objetivo'])
            rotas.append(nova_rota)
    resposta = [caminho, len(visitados)]
    return resposta

def best_first(mapa:dict):
    # Como o enunciado de exercício faz com que todos os pontos do mapa possuam
    # o mesmo custo de travessia, vamos utilizar como critério de custo a menor
    # distância euclidiana entre o ponto analisado e os possíveis pontos objetivo
    def funcao_custo(rota:dict):
        # Função best-first: f(n) = g(n) + 0
        return rota.get('distancia')

    return algoritmo_bf(mapa, funcao_custo)

def busca_a(mapa:dict):
    # O algoritmo de busca A é um algoritmo best-first com uma função de custo que
    # leva em conta a minimização do custo total do caminho do nó início até o nó fim.
    def funcao_custo(rota:dict):
        # Função busca A*: f(n) = g(n) + h(n)
        return rota.get('distancia') + len(rota.get('caminho'))

    return algoritmo_bf(mapa, funcao_custo)

def hill_climbing_aux(vetor_inicial:list, mapa:dict, total_visitados:int):
    # Começamos fazendo uma cópia do vetor inicial para evitar alterá-lo (Mutabilidade sucks!)
    caminho = vetor_inicial.copy()
    # Fazemos uma cópia da origem do mapa para evitar alterá-la posteriormente
    mapa_local = {'origem': mapa['origem'].copy(),
                  'matriz': mapa['matriz'],
                  'objetivo': mapa['objetivo']}
    # Fazemos o "for" com relação ao índices do vetor caminho, já que este terá
    # seus itens modificados ao longo do algoritmo. Utilizando apenas os índices
    # estaremos sempre na posição esperada, não importando os itens do vetor.
    for index in range(len(caminho) - 1):
        atual = caminho[index]
        proximo = caminho[index + 1]
        # Pegamos o iten atual do caminho e o próximo item
        # Verificamos se o próximo ponto é o objetivo (caso de parada do algoritmo)
        if proximo in mapa_local['objetivo']:
            break
        # Assumimos que o melhor caminho é o próximo obtido e verificamos se isso é verdade
        melhor = proximo
        vizinhos = obtem_vizinhos(mapa_local['matriz'], atual, caminho)
        dist_proximo = distancia_ponto_objetivos(proximo, mapa_local['objetivo'])
        for vizinho in vizinhos:
            dist_vizinho = distancia_ponto_objetivos(vizinho, mapa_local['objetivo'])
            # Se a distância do vizinho for menor que a do melhor ponto, substituímos
            melhor = vizinho if dist_vizinho <= dist_proximo else melhor
        # Se algum dos vizinhos for melhor que o ponto inicial
        if melhor != proximo:
            # Guardamos o caminho até esse ponto
            caminho_ate_aqui = caminho[:(index + 1)]
            # Alteramos a origem do mapa para ser o melhor ponto encontrado
            mapa_local['origem'] = [melhor]
            # Recalculamos o caminho partindo do ponto que consideramos melhor
            novo_caminho, visitados = busca_profundidade(mapa_local, caminho_ate_aqui)
            total_visitados += visitados
            # Se um novo caminho for obtido, fazemos a comparação de tamanhos
            if novo_caminho:
                novo_caminho = caminho_ate_aqui + novo_caminho
                # Se o tamanho do novo caminho for menor que
                # o tamanho do caminho atual, fazemos a troca
                caminho = novo_caminho if len(novo_caminho) < len(caminho) else caminho
    return [caminho, total_visitados]

def hill_climbing(mapa:dict):
    # O método hill_climbing é um método iterativo que pode ser implementado de várias formas, para este
    # trabalho sa implementação seguirá da seguinte forma:
    # - Obtém-se uma solução inicial utilizando a busca em profundidade
    # - Analisa-se a solução em cada ponto de decisão, se houver um ponto onde outro caminho tem potencial
    #   para de ser uma solução melhor tenta se criar um novo caminho a partir deste ponto
    # - Se for criado um novo caminho, comparamos esta nova solução com a solução anterior, se a nova
    #   solução for melhor descartamos a antiga, caso contrário descartamos a nova. Se nenhum caminho
    #   foi gerado, mantemos a solução atual
    # - Seguimos avaliando o caminho até o próximo ponto de decisão e repetimos o segundo passo, se não
    #   houver mais nenhum ponto de decisão, terminamos o algoritmo
    vetor_inicial, visitados = busca_profundidade(mapa)
    return hill_climbing_aux(vetor_inicial, mapa, visitados)

######## API que faz o parse do arquivo #######################################
class APIMapaArquivo(APIView):
    def post(self, request, *args, **kwargs):
        if not (request.FILES and request.FILES.get('file', None)):
           return Response(
                {'erros': ['É necessário enviar um \'arquivo\'.']},
                status=status.HTTP_400_BAD_REQUEST)
        arquivo = request.FILES['file']
        valores = list(map(lambda x: x.decode("utf-8"), arquivo.read().splitlines()))
        # Precisamos realmente olhar o tamanho do arquivo? Faremos isso apenas
        # para garantir que obtivemos os dados de uma matriz do tamanho informado
        linhas, colunas = list(map(int, valores[0].split()))
        # Cuidado, mutabilidade!!! Retirando a primeira linha de valores
        valores.pop(0)
        matriz = [['' for j in range(colunas)] for i in range(linhas)]
        mapa = {'origem': [], 'objetivo': [], 'matriz': matriz}
        # TODO: Validar se temos pelo menos uma origem e um objetivo?
        for i in range(linhas):
            for j in range(colunas):
                _val = str(valores[i][j])
                if _val == '#':
                    mapa['origem'].append([i, j])
                elif _val == '$':
                    mapa['objetivo'].append([i, j])
                mapa['matriz'][i][j] = str(valores[i][j])

        return Response({'resposta': {'mapa': mapa}}, status=status.HTTP_200_OK)

######## API que executa o método de busca e retorna o resultado ##############
class APIBuscaMapa(APIView):
    def post(self, request, *args, **kwargs):

        if 'metodo' not in request.query_params:
            return Response(
                {'erros': ['Informe um método a ser utilizado.']},
                status=status.HTTP_400_BAD_REQUEST)

        _metodo = request.query_params.get('metodo', '').strip()
        if _metodo not in ['busca_profundidade', 'busca_largura', 'best_first',
                           'busca_a', 'hill_climbing']:
            return Response(
                {'erros': [f'Valor inválido para o parâmetro \'metodo\': {_metodo}.']},
                status=status.HTTP_400_BAD_REQUEST)

        mapa = request.data
        if not mapa or not isinstance(mapa, dict):
            return Response(
                {'erros': ['Não foi encontrado um dicionario na request.']},
                status=status.HTTP_400_BAD_REQUEST)
        if not mapa.get('matriz'):
            return Response(
                {'erros': ['Não foi encontrada uma matriz no dicionário da request.']},
                status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(mapa.get('matriz'), list):
            return Response(
                {'erros': ['A matriz no dicionário da request deve ser um vetor.']},
                status=status.HTTP_400_BAD_REQUEST)
        if not mapa.get('origem'):
            return Response(
                {'erros': ['Não foi encontrada uma origem no dicionário da request.']},
                status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(mapa.get('origem'), list):
            return Response(
                {'erros': ['A origem no dicionário da request deve ser um vetor.']},
                status=status.HTTP_400_BAD_REQUEST)
        if not mapa.get('objetivo'):
            return Response(
                {'erros': ['Não foi encontrado um objetivo no dicionário da request.']},
                status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(mapa.get('objetivo'), list):
            return Response(
                {'erros': ['O objetivo no dicionário da request deve ser um vetor.']},
                status=status.HTTP_400_BAD_REQUEST)

        vetor = []
        funcoes = {'busca_profundidade': busca_profundidade,
                   'busca_largura': busca_largura,
                   'best_first': best_first,
                   'busca_a': busca_a,
                   'hill_climbing': hill_climbing}

        # * 1000 converte os segundos em milisegundos
        inicio = time.monotonic() * 1000
        vetor, visitados = funcoes.get(_metodo)(mapa)
        tempo = time.monotonic() * 1000 - inicio

        return Response({'resposta': {'tipo':_metodo,
                                      'vetor': vetor,
                                      'visitados': visitados,
                                      'tempo': tempo}},
                        status=status.HTTP_200_OK)
