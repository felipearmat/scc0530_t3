// Esse arquivo foi alterado para o formato CommonJS para ser utilizado tanto nos arquivos Vue quanto
// nos arquivos de teste, permitindo que a configuração do Vue seja a mesma nos dois ambientes
const axios = require('axios')
const BootstrapVue = require('bootstrap-vue')
const VueAxios = require('vue-axios')
const BaseVue = require('vue')
const BaseVueRouter = require('vue-router')

// Vue Router e Vue podem ser importados com .default ou não, dependendo de qual arquivo
// chama-lo, com isso temos que verificar se existe o .default e então fazer a atribuição correta
const VueRouter = BaseVueRouter.default ? BaseVueRouter.default : BaseVueRouter
const Vue = BaseVue.default ? BaseVue.default : BaseVue

if (window.NO_ROUTER !== 'True' && window.NO_ROUTER !== true) {
  Vue.use(VueRouter)
}

Vue.use(BootstrapVue)
Vue.use(VueAxios, axios)
Vue.config.productionTip = false

module.exports = Vue
