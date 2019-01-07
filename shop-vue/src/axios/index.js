import axios from 'axios'
import store from '../store/store'

// 添加请求拦截器
axios.interceptors.request.use(
    // 在发送请求之前
    config => {
        // 判断是否存在token，如果存在的话，则每个http header都加上token
        if (store.state.userInfo.token) { 
            config.headers.Authorization = `JWT ${store.state.userInfo.token}`
        }
        return config
    },
    err => {
        return Promise.reject(err)
    }
)

// http response 拦截器
axios.interceptors.response.use(
    undefined,
    // 请求错误时做些事
    error => {
      let res = error.response
      switch (res.status) {
        case 401:
          // 返回 401 清除token信息并跳转到登录页面
          // store.commit(types.LOGOUT)
          console.log('未登录')
          // router.replace({
          //   path: '/app/login',
          //   query: {redirect: router.currentRoute.fullPath}
          // })
        case 403:
          console.log('您没有该操作权限')
          // alert('您没有该操作权限')
        case 500:
          console.log('服务器错误')
          // alert('服务器错误')
      }
      return Promise.reject(error.response.data)   // 返回接口返回的错误信息
  });