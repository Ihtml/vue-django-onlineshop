import mock from '../mock/mock.js'
import $ from 'jquery'
import Vue from 'vue'
import './styles/common.scss'
import './styles/fonts/iconfont.css'
import router from './router';
import store from './store/store'

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
