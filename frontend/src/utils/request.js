import axios from 'axios'
import { ElMessage } from 'element-plus'
import config from '../config'

const service = axios.create({
  baseURL: config.baseURL,
  timeout: 5000
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    return config
  },
  error => {
    console.log(error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    const res = response.data
    if (res.error) {
      ElMessage.error(res.error)
      return Promise.reject(new Error(res.error))
    }
    return res
  },
  error => {
    console.log('err' + error)
    ElMessage.error(error.response?.data?.error || '请求失败')
    return Promise.reject(error)
  }
)

export default service 