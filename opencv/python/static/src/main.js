import Vue from 'vue'
import axios from 'axios'
import App from './App.vue'
import router from './router'

import VueMeta from 'vue-meta'

Vue.use(VueMeta)

axios.defaults.baseURL = 'http://0.0.0.0:5000';
axios.defaults.withCredentials = true;
axios.defaults.debug = true;
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

new Vue({
  router,
  render: function (h) { return h(App) }
}).$mount('#app')
