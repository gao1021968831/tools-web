import axios from 'axios'
import { ElMessage } from 'element-plus'
import { baseURL } from '../config'

const service = axios.create({
  baseURL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 响应拦截器
service.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    let message = '请求失败'
    if (error.response) {
      const { data } = error.response
      message = data.error || '服务器响应错误'
    } else if (error.request) {
      if (error.code === 'ECONNABORTED') {
        message = '请求超时，请重试'
      } else {
        message = '网络请求失败，请检查网络连接'
      }
    } else {
      message = error.message || '请求配置错误'
    }
    
    ElMessage.error(message)
    return Promise.reject(error)
  }
)

export default service 