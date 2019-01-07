import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

//公共部分
import app from '../views/app/app'

import store from '../store/store'

const router = new Router({
    routes: [{
        path: '/app',
        component: app
,    }]
})

export default router
