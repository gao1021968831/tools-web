// 开发环境配置
const dev = {
  baseURL: '/api'
}

// 生产环境配置
const prod = {
  baseURL: '/api'
}

export default {
  ...(process.env.NODE_ENV === 'production' ? prod : dev)
} 