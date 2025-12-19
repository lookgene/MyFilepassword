<template>
  <header class="bg-gray-800 border-b border-gray-700 sticky top-0 z-50">
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <!-- Logo和品牌名称 -->
        <div class="flex items-center">
          <NuxtLink to="/" class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <UIcon name="i-heroicons-lock-closed" class="text-white text-xl" />
            </div>
            <span class="text-xl font-bold text-white">FilePassword</span>
          </NuxtLink>
        </div>

        <!-- 桌面端导航菜单 -->
        <nav class="hidden md:flex items-center space-x-1">
          <NuxtLink
            v-for="item in navigationItems"
            :key="item.name"
            :to="item.to"
            class="px-4 py-2 rounded-lg text-gray-300 hover:text-white hover:bg-gray-700 transition-colors duration-200 flex items-center space-x-2"
            :class="{ 'bg-gray-700 text-white': route.path === item.to }"
          >
            <UIcon :name="item.icon" class="text-lg" />
            <span>{{ item.name }}</span>
          </NuxtLink>
        </nav>

        <!-- 右侧操作区 -->
        <div class="flex items-center space-x-4">
          <!-- 通知按钮 -->
          <ClientOnly>
            <UButton color="gray" variant="ghost" size="sm" class="hidden sm:flex">
              <UIcon name="i-heroicons-bell" class="text-lg" />
            </UButton>
          </ClientOnly>

          <!-- 用户菜单 -->
          <ClientOnly>
            <UDropdown :items="userMenuItems" :popper="{ placement: 'bottom-end' }">
              <UButton color="gray" variant="ghost" class="flex items-center space-x-2">
                <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                  <UIcon name="i-heroicons-user" class="text-white text-sm" />
                </div>
                <UIcon name="i-heroicons-chevron-down" class="text-sm" />
              </UButton>
              
              <template #account="{ item }">
                <div class="text-left">
                  <p class="font-medium">已登录</p>
                  <p class="text-sm text-gray-400">user@example.com</p>
                </div>
              </template>
            </UDropdown>
          </ClientOnly>

          <!-- 移动端菜单按钮 -->
          <ClientOnly>
            <UButton
              color="gray"
              variant="ghost"
              size="sm"
              class="md:hidden"
              @click="toggleMobileMenu"
            >
              <UIcon :name="mobileMenuOpen ? 'i-heroicons-x-mark-20-solid' : 'i-heroicons-bars-3'" class="text-xl" />
            </UButton>
          </ClientOnly>
        </div>
      </div>

      <!-- 移动端导航菜单 -->
      <div v-if="mobileMenuOpen" class="md:hidden border-t border-gray-700 py-4">
        <nav class="flex flex-col space-y-2">
          <NuxtLink
            v-for="item in navigationItems"
            :key="item.name"
            :to="item.to"
            class="px-4 py-2 rounded-lg text-gray-300 hover:text-white hover:bg-gray-700 transition-colors duration-200 flex items-center space-x-2"
            :class="{ 'bg-gray-700 text-white': route.path === item.to }"
            @click="closeMobileMenu"
          >
            <UIcon :name="item.icon" class="text-lg" />
            <span>{{ item.name }}</span>
          </NuxtLink>
          
          <div class="border-t border-gray-700 pt-2 mt-2">
            <NuxtLink
              to="/settings"
              class="px-4 py-2 rounded-lg text-gray-300 hover:text-white hover:bg-gray-700 transition-colors duration-200 flex items-center space-x-2"
              @click="closeMobileMenu"
            >
              <UIcon name="i-heroicons-cog-6-tooth" class="text-lg" />
              <span>设置</span>
            </NuxtLink>
            
            <button
              class="w-full text-left px-4 py-2 rounded-lg text-gray-300 hover:text-white hover:bg-gray-700 transition-colors duration-200 flex items-center space-x-2"
              @click="logout"
            >
              <UIcon name="i-heroicons-arrow-right-on-rectangle" class="text-lg" />
              <span>退出登录</span>
            </button>
          </div>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup>
// 获取当前路由
const route = useRoute()

// 响应式数据
const mobileMenuOpen = ref(false)

// 导航菜单项
const navigationItems = [
  {
    name: '首页',
    to: '/',
    icon: 'i-heroicons-home'
  },
  {
    name: '上传文件',
    to: '/upload',
    icon: 'i-heroicons-cloud-arrow-up'
  },
  {
    name: '解密文件',
    to: '/decrypt',
    icon: 'i-heroicons-lock-open'
  },
  {
    name: '文件管理',
    to: '/files',
    icon: 'i-heroicons-folder'
  }
]

// 方法 - 退出登录
const logout = () => {
  // 实际应用中会调用API进行登出
  console.log('Logging out...')
  // 模拟登出后跳转到首页
  navigateTo('/')
}

// 用户菜单项
const userMenuItems = [
  [{
    label: '用户',
    slot: 'account',
    disabled: true
  }],
  [{
    label: '个人资料',
    icon: 'i-heroicons-user',
    click: () => navigateTo('/settings')
  }, {
    label: '设置',
    icon: 'i-heroicons-cog-6-tooth',
    click: () => navigateTo('/settings')
  }],
  [{
    label: '退出登录',
    icon: 'i-heroicons-arrow-right-on-rectangle',
    click: logout
  }]
]

// 方法 - 切换移动端菜单
const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

// 方法 - 关闭移动端菜单
const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}

// 监听路由变化，关闭移动端菜单
watch(() => useRoute().path, () => {
  closeMobileMenu()
})
</script>