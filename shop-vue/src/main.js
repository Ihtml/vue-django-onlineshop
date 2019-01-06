import mock from '../mock/mock.js'
import $ from 'jquery'
import Vue from 'vue'
import './styles/common.scss';

import router from './router';

//全局加载resource拦截器
import './axios/';
import Axios from 'axios';
Vue.prototype.$http = Axios

import App from './App';

new Vue({
    el:'#app',
    router,
    store,
    template:'<App/>',
    components:{App}
})
