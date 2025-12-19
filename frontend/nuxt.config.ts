export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },
  modules: [
    '@nuxt/ui',
    '@nuxtjs/tailwindcss',
  ],
  ui: {
    // 禁用Google Fonts自动获取，使用系统字体
    fonts: false
  },
  tailwindcss: {
    cssPath: '~/assets/css/tailwind.css',
    configPath: 'tailwind.config.js',
    exposeConfig: false,
    viewer: true,
  },
  app: {
    head: {
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
      title: '在线加密文件解密服务 - 专业、安全、高效的密码破解方案',
      meta: [
        { name: 'description', content: '专业的在线加密文件解密服务，支持ZIP、RAR、7Z、PDF等多种格式，提供快速、安全的密码破解方案，几分钟内即可恢复您的重要文件。' },
        { name: 'keywords', content: '文件解密,密码破解,在线解密,ZIP解密,RAR解密,7Z解密,PDF解密,加密文件解密' },
        { name: 'author', content: '在线加密文件解密服务' },
        { name: 'robots', content: 'index, follow' },
        { name: 'googlebot', content: 'index, follow' },
        { name: 'og:type', content: 'website' },
        { name: 'og:title', content: '在线加密文件解密服务 - 专业、安全、高效的密码破解方案' },
        { name: 'og:description', content: '专业的在线加密文件解密服务，支持ZIP、RAR、7Z、PDF等多种格式，提供快速、安全的密码破解方案。' },
        { name: 'og:url', content: 'https://www.decryptservice.com/' },
        { name: 'og:site_name', content: '在线加密文件解密服务' },
        { name: 'twitter:card', content: 'summary_large_image' },
        { name: 'twitter:title', content: '在线加密文件解密服务 - 专业、安全、高效的密码破解方案' },
        { name: 'twitter:description', content: '专业的在线加密文件解密服务，支持多种文件格式，提供快速、安全的密码破解方案。' }
      ],
      link: [
        { rel: 'canonical', href: 'https://www.decryptservice.com/' },
        { rel: 'sitemap', href: 'https://www.decryptservice.com/sitemap.xml' }
      ]
    }
  },
  // SEO相关配置
  robots: {
    rules: {
      UserAgent: '*',
      Allow: '/',
      Disallow: '/admin/'
    }
  },
  // 结构化数据配置
  schema: {
    Article: {
      '@id': 'https://www.decryptservice.com/#article',
      name: '在线加密文件解密服务',
      author: {
        '@type': 'Organization',
        name: '在线加密文件解密服务'
      },
      publisher: {
        '@type': 'Organization',
        name: '在线加密文件解密服务'
      },
      datePublished: '2024-01-01',
      dateModified: '2024-01-01',
      description: '专业的在线加密文件解密服务，支持多种文件格式，提供快速、安全的密码破解方案。'
    }
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE || 'http://localhost:8000/api',
      siteUrl: process.env.SITE_URL || 'https://www.decryptservice.com'
    }
  }
})