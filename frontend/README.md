# 在线加密文件解密服务 - 前端部署说明

## 1. 项目概述

本项目是在线加密文件解密服务的前端部分，基于Nuxt.js 4开发，提供了用户友好的界面，支持文件上传、破解任务创建和查询等功能。

## 2. 技术栈

- 框架：Nuxt.js 4
- 语言：TypeScript
- UI组件库：Element Plus
- 样式框架：Tailwind CSS
- 状态管理：Pinia
- HTTP客户端：Axios

## 3. 环境要求

- Node.js：>= 18.0.0
- npm：>= 9.0.0

## 4. 安装依赖

1. 进入前端项目目录
```bash
cd frontend
```

2. 安装依赖
```bash
npm install
```

## 5. 开发环境运行

```bash
npm run dev
```

项目将在 http://localhost:3000 启动

## 6. 生产环境构建

```bash
# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

## 7. 部署方式

### 7.1 静态部署

```bash
# 生成静态文件
npm run generate
```

生成的静态文件将位于 `dist` 目录，可以部署到任何静态文件服务器，如Nginx、Apache、Vercel、Netlify等。

### 7.2 服务器部署

1. 构建生产版本
```bash
npm run build
```

2. 启动生产服务器
```bash
node .output/server/index.mjs
```

或者使用PM2进行进程管理：
```bash
npm install -g pm2
npm run build
pm2 start
```

## 8. 配置说明

### 8.1 环境变量

创建 `.env` 文件，配置以下环境变量：

```env
# API基础URL
API_BASE=http://localhost:8000/api

# 应用基础URL
BASE_URL=http://localhost:3000

# 开发模式
NODE_ENV=development
```

### 8.2 nuxt.config.ts 配置

主要配置项说明：

- `modules`：使用的Nuxt模块
- `css`：全局CSS文件
- `plugins`：插件配置
- `app.head`：页面头部配置
- `runtimeConfig`：运行时配置

## 9. 项目结构

```
frontend/
├── assets/        # 静态资源
├── components/    # Vue组件
├── composables/   # 组合式函数
├── layouts/       # 页面布局
├── pages/         # 页面组件
├── plugins/       # 插件
├── public/        # 公共资源
├── stores/        # Pinia状态管理
├── utils/         # 工具函数
├── app.config.ts  # 应用配置
├── nuxt.config.ts # Nuxt配置
├── package.json   # 项目依赖
└── tsconfig.json  # TypeScript配置
```

## 10. 常见问题

### 10.1 依赖安装失败

**问题**：`npm install` 失败

**解决方案**：
- 清理npm缓存：`npm cache clean --force`
- 删除 `node_modules` 和 `package-lock.json`，重新安装
- 使用镜像源：`npm install --registry=https://registry.npmmirror.com`

### 10.2 开发服务器启动失败

**问题**：`npm run dev` 启动失败

**解决方案**：
- 检查端口是否被占用
- 确保Node.js版本符合要求
- 检查环境变量配置

### 10.3 构建失败

**问题**：`npm run build` 或 `npm run generate` 失败

**解决方案**：
- 检查代码中是否有TypeScript错误
- 确保所有依赖版本兼容
- 检查配置文件是否正确

## 11. 联系方式

如有问题，请联系项目开发团队。
