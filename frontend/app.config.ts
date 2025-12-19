export default defineAppConfig({
  title: '在线加密文件解密服务',
  description: '专业的在线加密文件解密服务，支持多种文件格式，提供快速、安全的密码破解方案',
  baseURL: process.env.BASE_URL || 'http://localhost:3000',
  apiBase: process.env.API_BASE || 'http://localhost:8000/api'
})