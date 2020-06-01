<template>
  <div class="main container-fluid pb-4">
    <h1 class="text-center">
      SCC0530 - Inteligência Artificial
    </h1>
    <h2 class="text-center">
      Trabalho Prático (Labirinto)
    </h2>
    <h3>Alunos:</h3>
    <ul class="mb-4">
      <li>Felipe Araujo Matos NUSP: 5968691</li>
      <li>Leandro Sena Silva NUSP: 9293060</li>
      <li>William Zaniboni Silva NUSP: 10309159</li>
    </ul>
    <app-fieldfile
      id="arquivo_mapa"
      ref="arquivo_mapa"
      v-model="arquivoMapa"
      :url="urlArquivo"
      label="Arquivo com mapa a ser analisado (apenas .txt)"
      accept=".txt"
      @resolved="trataPostMapa($event)"
    />
    <b-button
      id="arquivo_mapa_post"
      size="sm"
      variant="info"
      :disabled="!arquivoMapa"
      class="pr-3 pl-3 pt-2 pb-2 ml-3"
      @click.prevent.stop="uploadArquivo()"
    >
      Enviar Arquivo
    </b-button>
    <app-fieldmessage
      id="erros"
      v-model="erros"
      variant="danger"
      class="mt-3 mb-2"
    />
    <template v-if="mapa.matriz && mapa.matriz.length > 0">
      <hr class="divisor">
      <div class="row">
        <div class="col-md-6 mt-4">
          <div
            v-for="(item, chave) in solucao"
            :key="item.id"
            class="row"
          >
            <div class="col-6 text-right">
              <app-post
                :id="'botao_' + chave"
                :url="urlBusca"
                :value="mapa"
                :parameters="{ metodo: chave }"
                class="pr-3 pl-3 pt-2 pb-2 mt-4 mb-2"
                variant="info"
                size="sm"
                @resolved="trataPostSolucao($event)"
              >
                {{ chave }}
              </app-post>
              <!-- <br>
              <app-post
                :id="'botao_' + chave"
                :url="urlBusca"
                :value="mapa"
                :parameters="{ metodo: chave, vezes: 100 }"
                class="pr-3 pl-3 pt-2 pb-2 mt-2 mb-4"
                variant="info"
                size="sm"
                @resolved="trataPostSolucao($event)"
              >
                {{ chave + ' * 100' }}
              </app-post> -->
            </div>
            <div class="col-6">
              <table
                v-if="item.vetor && item.vetor.length > 0"
                style="height: 100%;"
              >
                <tbody>
                  <tr>
                    <td class="align-middle pt-2 pb-2">
                      <b-form-checkbox
                        :id="'checkbox_' + chave"
                        v-model="item.mostrar"
                      >
                        Mostrar caminho
                      </b-form-checkbox>
                      <span>Tamanho do caminho: {{ item.vetor.length }}</span>
                      <br>
                      <span>Tempo (ms): {{ item.tempos[item.tempos.length - 1] }}</span>
                      <br>
                      <span>Nº de testes: {{ item.visitados.length }}</span>
                      <br>
                      <span>Média dos caminhos: {{ mediaVetor(item.caminhos) }}</span>
                      <br>
                      <span>Média dos tempos (ms): {{ mediaVetor(item.tempos) }}</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        <div class="col-md-6 mt-4">
          <div class="d-flex justify-content-center">
            <b-table
              :items="mapa.matriz"
              :style="`width: ${mapa.matriz[0].length * 15 + 2}px;
                       height: ${mapa.matriz.length * 15 + 34}px;`"
              class="border border-dark"
              theadClass="d-none"
              small
              responsive
            >
              <template v-slot:cell()="data">
                <div :class="defineClasse(data.value, data.index, data.field.label)">
                  <span :title="`[${data.index}, ${data.field.label}]`">
                    {{ data.value }}
                  </span>
                </div>
              </template>
            </b-table>
          </div>
        </div>
      </div>
    </template>
    <div v-else>
      Nenhum mapa para exibir
    </div>
  </div>
</template>

<script>
import { globalVars } from '@/main.js'
import fieldFile from '@/campos/fieldFile.vue'
import post from '@/componentes/post.vue'
import fieldMessage from '@/campos/fieldMessage.vue'
export default {
  components: {
    'app-post': post,
    'app-fieldfile': fieldFile,
    'app-fieldmessage': fieldMessage
  },
  data: function () {
    return {
      urlArquivo: globalVars.API_ARQUIVO,
      urlBusca: globalVars.API_BUSCA,
      arquivoMapa: '',
      mapa: {},
      solucao: {
        busca_profundidade: {
          mostrar: false,
          vetor: [],
          caminhos: [],
          visitados: [],
          tempos: []
        },
        busca_largura: {
          mostrar: false,
          vetor: [],
          caminhos: [],
          visitados: [],
          tempos: []
        },
        best_first: {
          mostrar: false,
          vetor: [],
          caminhos: [],
          visitados: [],
          tempos: []
        },
        busca_a: {
          mostrar: false,
          vetor: [],
          caminhos: [],
          visitados: [],
          tempos: []
        },
        hill_climbing: {
          mostrar: false,
          vetor: [],
          caminhos: [],
          visitados: [],
          tempos: []
        }
      },
      erros: []
    }
  },
  methods: {
    defineClasse (valor, linha, coluna) {
      var _resp = ''
      var _vetor = [linha, Number(coluna)]
      switch (valor) {
        case '*': _resp += 'bg-white '; break
        case '#': _resp += 'bg-primary '; break
        case '$': _resp += 'bg-danger '; break
        case '-': _resp += 'bg-dark '; break
      }
      for (const [key, value] of Object.entries(this.solucao)) {
        // Colocamos value.mostrar no if para evitar percorrer o vetor caso o caminho não deva ser exibido
        var contemVetor = value.mostrar && value.vetor.some(item => {
          return item[0] === _vetor[0] && item[1] === _vetor[1]
        })
        if (value.mostrar && contemVetor) {
          _resp += `${key} `
        }
      }
      return _resp
    },
    limpaCampos () {
      this.mapa = {}
      this.solucao = {
        busca_profundidade: {
          mostrar: false,
          vetor: [],
          caminhos: [],
          visitados: [],
          tempos: []
        },
        busca_largura: {
          mostrar: false,
          vetor: [],
          caminhos: [],
          visitados: [],
          tempos: []
        },
        best_first: {
          mostrar: false,
          vetor: [],
          caminhos: [],
          visitados: [],
          tempos: []
        },
        busca_a: {
          mostrar: false,
          vetor: [],
          caminhos: [],
          visitados: [],
          tempos: []
        },
        hill_climbing: {
          mostrar: false,
          vetor: [],
          caminhos: [],
          visitados: [],
          tempos: []
        }
      }
      this.erros = []
    },
    uploadArquivo () {
      if (this.$refs.arquivo_mapa) {
        this.$refs.arquivo_mapa.uploadArquivo()
      }
    },
    trataPostMapa (response) {
      this.limpaCampos()
      var _resp = response.data
      if (_resp && _resp.erros) {
        this.erros = _resp.erros
      } else if (_resp && _resp.resposta && _resp.resposta.mapa) {
        this.mapa = _resp.resposta.mapa
      } else {
        this.errosGravame = ['Ocorreu um erro desconhecido. Atualize a página!']
      }
    },
    trataPostSolucao (response) {
      this.erros = []
      var _resp = response.data
      if (_resp && _resp.erros) {
        this.erros = _resp.erros
      } else if (_resp && _resp.resposta && _resp.resposta.tipo) {
        var _resposta = _resp.resposta
        this.solucao[_resposta.tipo].vetor = _resposta.vetor
        var tempoFormatado = Number(Number(_resposta.tempo).toFixed(6))
        this.solucao[_resposta.tipo].tempos.push(tempoFormatado)
        this.solucao[_resposta.tipo].caminhos.push(_resposta.vetor.length)
        this.solucao[_resposta.tipo].visitados.push(_resposta.visitados)
      } else {
        this.errosGravame = ['Ocorreu um erro desconhecido. Atualize a página!']
      }
    },
    mediaVetor (vetor) {
      var soma = vetor.reduce((soma, item) => {
        soma += item
        return soma
      }, 0)
      var qnt = vetor.length
      return (soma / qnt).toFixed(2)
    }
  }
}
</script>

<style lang="scss" scoped>
  >>> {
    .divisor {
      height: 10px;
      border: 0;
      box-shadow: 0 10px 10px -10px #8c8b8b inset;
    }
    .table-sm {
      th, td {
        padding: 0;
        margin: 0;
      }
    }
    .table {
      th, td {
        width: 15px;
        height: 15px;
        padding: 0;
        margin: 0;
        border-top: 0;
        line-height: 1;
        text-align: center;
      }
    }
    table {
      border-spacing: 0;
    }
    div {
      .busca_profundidade {
        background-color: #222299 !important
      }
      .busca_largura {
        background-color: #229922 !important
      }
      .best_first {
        background-color: #992222 !important
      }
      .busca_a {
        background-color: #6666DD !important
      }
      .hill_climbing {
        background-color: #DD6666 !important
      }
    }
  }
</style>
