<template>
  <footer class="bg-gray-800 border-t border-gray-700 mt-12">
    <div class="container mx-auto px-4 py-8">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <!-- 公司信息 -->
        <div class="space-y-4">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <UIcon name="i-heroicons-lock-closed" class="text-white text-xl" />
            </div>
            <span class="text-xl font-bold text-white">FilePassword</span>
          </div>
          <p class="text-gray-400 text-sm">
            安全的在线文件加密与解密服务，保护您的数据隐私。
          </p>
          <div class="flex space-x-4">
            <a href="#" class="text-gray-400 hover:text-white transition-colors">
              <UIcon name="i-heroicons-globe-alt" class="text-xl" />
            </a>
            <a href="#" class="text-gray-400 hover:text-white transition-colors">
              <UIcon name="i-simple-icons-twitter" class="text-xl" />
            </a>
            <a href="#" class="text-gray-400 hover:text-white transition-colors">
              <UIcon name="i-simple-icons-github" class="text-xl" />
            </a>
          </div>
        </div>

        <!-- 产品链接 -->
        <div class="space-y-4">
          <h3 class="text-lg font-semibold text-white">产品</h3>
          <ul class="space-y-2">
            <li>
              <NuxtLink to="/upload" class="text-gray-400 hover:text-white transition-colors">
                文件上传
              </NuxtLink>
            </li>
            <li>
              <NuxtLink to="/decrypt" class="text-gray-400 hover:text-white transition-colors">
                文件解密
              </NuxtLink>
            </li>
            <li>
              <NuxtLink to="/files" class="text-gray-400 hover:text-white transition-colors">
                文件管理
              </NuxtLink>
            </li>
            <li>
              <a href="#" class="text-gray-400 hover:text-white transition-colors">
                API文档
              </a>
            </li>
          </ul>
        </div>

        <!-- 资源链接 -->
        <div class="space-y-4">
          <h3 class="text-lg font-semibold text-white">资源</h3>
          <ul class="space-y-2">
            <li>
              <a href="#" class="text-gray-400 hover:text-white transition-colors">
                使用指南
              </a>
            </li>
            <li>
              <a href="#" class="text-gray-400 hover:text-white transition-colors">
                常见问题
              </a>
            </li>
            <li>
              <a href="#" class="text-gray-400 hover:text-white transition-colors">
                安全说明
              </a>
            </li>
            <li>
              <a href="#" class="text-gray-400 hover:text-white transition-colors">
                更新日志
              </a>
            </li>
          </ul>
        </div>

        <!-- 公司链接 -->
        <div class="space-y-4">
          <h3 class="text-lg font-semibold text-white">公司</h3>
          <ul class="space-y-2">
            <li>
              <a href="#" class="text-gray-400 hover:text-white transition-colors">
                关于我们
              </a>
            </li>
            <li>
              <a href="#" class="text-gray-400 hover:text-white transition-colors">
                联系我们
              </a>
            </li>
            <li>
              <a href="#" class="text-gray-400 hover:text-white transition-colors">
                隐私政策
              </a>
            </li>
            <li>
              <a href="#" class="text-gray-400 hover:text-white transition-colors">
                服务条款
              </a>
            </li>
          </ul>
        </div>
      </div>

      <!-- 版权信息 -->
      <div class="border-t border-gray-700 mt-8 pt-8 text-center">
        <p class="text-gray-400 text-sm">
          © {{ currentYear }} FilePassword. 保留所有权利。
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup>
// 当前年份
const currentYear = new Date().getFullYear()
</script>