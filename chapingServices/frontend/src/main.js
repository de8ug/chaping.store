// for dev -->start
// import './plugins/element.js'
// import ElementUI from 'element-ui';
// Vue.use(ElementUI) 

// import VCharts from 'v-charts' 
// Vue.use(VCharts) 
// import VeLine from 'v-charts/lib/line.common'
// Vue.component(VeLine.name, VeLine)

// for dev end <--

// for pro
import Vue from 'vue'
import router from './router'
import store from './store'
import axios from "axios";
import App from './App.vue'
Vue.config.productionTip = true
axios.defaults.baseURL = 'http://192.168.1.7:8888'  // in docker net

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
