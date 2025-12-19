<template>
  <div>

    <!-- Hero区域 -->
    <section class="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto">
        <div class="text-center space-y-8">
          <div class="space-y-4">
            <UBadge variant="secondary" class="bg-blue-500/20 text-blue-400 px-4 py-2 rounded-full text-sm font-medium border border-blue-500/30">
              🔒 专业级密码破解服务
            </UBadge>
            
            <h2 class="text-[clamp(2.5rem,5vw,4rem)] font-bold leading-tight bg-gradient-to-r from-white via-blue-100 to-purple-200 bg-clip-text text-transparent">
              安全、快速的密码破解服务
            </h2>
            
            <p class="text-xl text-gray-400 max-w-3xl mx-auto leading-relaxed">
              支持ZIP、RAR、PDF等50+格式，成功率高达95%
            </p>
          </div>
          
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <UButton 
              size="lg" 
              class="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 px-8 py-6 rounded-full text-lg font-semibold shadow-2xl hover:shadow-blue-500/25 transition-all duration-300"
              @click="$router.push('/upload')"
            >
              <template #default>
                <div class="flex items-center space-x-2">
                  <span>🚀</span>
                  <span>免费试用</span>
                </div>
              </template>
            </UButton>
            <UButton 
              variant="secondary" 
              size="lg" 
              class="px-8 py-6 rounded-full text-lg font-semibold border-2 border-gray-600 hover:border-gray-500 hover:bg-gray-800"
              @click="scrollToPricing"
            >
              <template #default>
                <div class="flex items-center space-x-2">
                  <span>💰</span>
                  <span>查看定价</span>
                </div>
              </template>
            </UButton>
          </div>
          
          <!-- 统计数据 -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16 max-w-4xl mx-auto">
            <div class="text-center space-y-2">
              <div class="text-4xl font-bold text-blue-400">10,000+</div>
              <div class="text-gray-400">已破解文件</div>
            </div>
            <div class="text-center space-y-2">
              <div class="text-4xl font-bold text-green-400">99.9%</div>
              <div class="text-gray-400">正常运行时间</div>
            </div>
            <div class="text-center space-y-2">
              <div class="text-4xl font-bold text-purple-400">256位</div>
              <div class="text-gray-400">加密保护</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 三步流程展示 -->
    <section class="py-20 px-4 sm:px-6 lg:px-8 bg-gray-800/50">
      <div class="max-w-7xl mx-auto">
        <div class="text-center mb-16">
          <h3 class="text-[clamp(2rem,4vw,3rem)] font-bold text-white mb-4">简单三步，轻松解密</h3>
          <p class="text-lg text-gray-400">无需专业知识，任何人都能轻松使用</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- 第一步 -->
          <UCard class="border border-gray-700 bg-gray-800/50 rounded-2xl overflow-hidden hover:bg-gray-800 transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl">
            <template #content>
              <div class="p-8 text-center space-y-6">
                <div class="w-16 h-16 bg-gradient-to-r from-blue-500 to-blue-600 rounded-full flex items-center justify-center mx-auto shadow-lg">
                  <span class="text-3xl">☁️</span>
                </div>
                <div class="space-y-3">
                  <h4 class="text-2xl font-bold text-white">上传文件</h4>
                  <p class="text-gray-400 leading-relaxed">
                    只需将您的加密文件拖拽到我们的安全上传区域，支持批量上传多个文件。
                  </p>
                </div>
                <div class="flex justify-center">
                  <UBadge variant="secondary" class="bg-blue-500/20 text-blue-400 border border-blue-500/30">
                    第1步
                  </UBadge>
                </div>
              </div>
            </template>
          </UCard>
          
          <!-- 第二步 -->
          <UCard class="border border-gray-700 bg-gray-800/50 rounded-2xl overflow-hidden hover:bg-gray-800 transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl">
            <template #content>
              <div class="p-8 text-center space-y-6">
                <div class="w-16 h-16 bg-gradient-to-r from-purple-500 to-purple-600 rounded-full flex items-center justify-center mx-auto shadow-lg">
                  <span class="text-3xl">⚙️</span>
                </div>
                <div class="space-y-3">
                  <h4 class="text-2xl font-bold text-white">选择方案</h4>
                  <p class="text-gray-400 leading-relaxed">
                    根据文件类型和密码复杂度选择最适合的破解方案，我们提供多种价格选项。
                  </p>
                </div>
                <div class="flex justify-center">
                  <UBadge variant="secondary" class="bg-purple-500/20 text-purple-400 border border-purple-500/30">
                    第2步
                  </UBadge>
                </div>
              </div>
            </template>
          </UCard>
          
          <!-- 第三步 -->
          <UCard class="border border-gray-700 bg-gray-800/50 rounded-2xl overflow-hidden hover:bg-gray-800 transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl">
            <template #content>
              <div class="p-8 text-center space-y-6">
                <div class="w-16 h-16 bg-gradient-to-r from-green-500 to-green-600 rounded-full flex items-center justify-center mx-auto shadow-lg">
                  <span class="text-3xl">🔑</span>
                </div>
                <div class="space-y-3">
                  <h4 class="text-2xl font-bold text-white">获取密码</h4>
                  <p class="text-gray-400 leading-relaxed">
                    我们的AI算法快速分析并破解密码，成功后立即将密码发送给您。
                  </p>
                </div>
                <div class="flex justify-center">
                  <UBadge variant="secondary" class="bg-green-500/20 text-green-400 border border-green-500/30">
                    第3步
                  </UBadge>
                </div>
              </div>
            </template>
          </UCard>
        </div>
      </div>
    </section>

    <!-- 支持的格式展示 -->
    <section class="py-20 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto">
        <div class="text-center mb-16">
          <h3 class="text-[clamp(2rem,4vw,3rem)] font-bold text-white mb-4">支持多种文件格式</h3>
          <p class="text-lg text-gray-400">我们支持50+种主流文件格式的密码破解</p>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-6">
          <UCard 
            v-for="format in supportedFormats" 
            :key="format.name"
            class="border border-gray-700 bg-gray-800/30 rounded-xl overflow-hidden hover:bg-gray-800 transition-all duration-300 hover:border-blue-500/50 hover:shadow-lg hover:shadow-blue-500/10"
          >
            <template #content>
              <div class="p-6 text-center space-y-3">
                <div class="text-4xl mb-2">{{ format.icon }}</div>
                <div class="text-sm font-semibold text-white">{{ format.name }}</div>
                <div class="text-xs text-gray-400">{{ format.description }}</div>
              </div>
            </template>
          </UCard>
        </div>
      </div>
    </section>

    <!-- 方案对比表格 -->
    <section id="pricing" class="py-20 px-4 sm:px-6 lg:px-8 bg-gray-800/30">
      <div class="max-w-7xl mx-auto">
        <div class="text-center mb-16">
          <h3 class="text-[clamp(2rem,4vw,3rem)] font-bold text-white mb-4">选择适合您的方案</h3>
          <p class="text-lg text-gray-400">灵活的定价，满足不同需求</p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <!-- 基础版 -->
          <UCard class="border border-gray-700 bg-gray-800/50 rounded-2xl overflow-hidden hover:border-blue-500/30 transition-all duration-300">
            <template #content>
              <div class="p-8 text-center space-y-6">
                <h4 class="text-2xl font-bold text-white">基础版</h4>
                <div class="text-4xl font-bold text-blue-400">¥9.9</div>
                <p class="text-gray-400">适合个人用户</p>
                <ul class="space-y-3 text-left">
                  <li class="flex items-center space-x-2">
                    <span class="text-green-400">✓</span>
                    <span class="text-gray-300">支持3个文件</span>
                  </li>
                  <li class="flex items-center space-x-2">
                    <span class="text-green-400">✓</span>
                    <span class="text-gray-300">最大100MB</span>
                  </li>
                  <li class="flex items-center space-x-2">
                    <span class="text-green-400">✓</span>
                    <span class="text-gray-300">标准破解速度</span>
                  </li>
                  <li class="flex items-center space-x-2">
                    <span class="text-gray-500">✗</span>
                    <span class="text-gray-500">优先处理</span>
                  </li>
                </ul>
                <UButton variant="outline" class="w-full border-blue-500 text-blue-400 hover:bg-blue-500/10">
                  选择基础版
                </UButton>
              </div>
            </template>
          </UCard>
          
          <!-- 专业版 -->
          <UCard class="border-2 border-blue-500 bg-gray-800/50 rounded-2xl overflow-hidden relative transform scale-105 transition-all duration-300">
            <template #content>
              <div class="absolute top-0 right-0 bg-blue-500 text-white text-xs px-3 py-1 rounded-bl-lg rounded-tr-2xl">
                推荐
              </div>
              <div class="p-8 text-center space-y-6">
                <h4 class="text-2xl font-bold text-white">专业版</h4>
                <div class="text-4xl font-bold text-blue-400">¥29.9</div>
                <p class="text-gray-400">适合专业用户</p>
                <ul class="space-y-3 text-left">
                  <li class="flex items-center space-x-2">
                    <span class="text-green-400">✓</span>
                    <span class="text-gray-300">支持15个文件</span>
                  </li>
                  <li class="flex items-center space-x-2">
                    <span class="text-green-400">✓</span>
                    <span class="text-gray-300">最大500MB</span>
                  </li>
                  <li class="flex items-center space-x-2">
                    <span class="text-green-400">✓</span>
                    <span class="text-gray-300">高速破解</span>
                  </li>
                  <li class="flex items-center space-x-2">
                    <span class="text-green-400">✓</span>
                    <span class="text-gray-300">优先处理</span>
                  </li>
                </ul>
                <UButton class="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                  选择专业版
                </UButton>
              </div>
            </template>
          </UCard>
          
          <!-- 企业版 -->
          <UCard class="border border-gray-700 bg-gray-800/50 rounded-2xl overflow-hidden hover:border-blue-500/30 transition-all duration-300">
            <template #content>
              <div class="p-8 text-center space-y-6">
                <h4 class="text-2xl font-bold text-white">企业版</h4>
                <div class="text-4xl font-bold text-blue-400">¥99.9</div>
                <p class="text-gray-400">适合企业用户</p>
                <ul class="space-y-3 text-left">
                  <li class="flex items-center space-x-2">
                    <span class="text-green-400">✓</span>
                    <span class="text-gray-300">无限文件</span>
                  </li>
                  <li class="flex items-center space-x-2">
                    <span class="text-green-400">✓</span>
                    <span class="text-gray-300">最大2GB</span>
                  </li>
                  <li class="flex items-center space-x-2">
                    <span class="text-green-400">✓</span>
                    <span class="text-gray-300">极速破解</span>
                  </li>
                  <li class="flex items-center space-x-2">
                    <span class="text-green-400">✓</span>
                    <span class="text-gray-300">API接口</span>
                  </li>
                </ul>
                <UButton variant="outline" class="w-full border-blue-500 text-blue-400 hover:bg-blue-500/10">
                  选择企业版
                </UButton>
              </div>
            </template>
          </UCard>
        </div>
      </div>
    </section>

    <!-- FAQ部分 -->
    <section class="py-20 px-4 sm:px-6 lg:px-8">
      <div class="max-w-4xl mx-auto">
        <div class="text-center mb-16">
          <h3 class="text-[clamp(2rem,4vw,3rem)] font-bold text-white mb-4">常见问题</h3>
          <p class="text-lg text-gray-400">解答您的疑问</p>
        </div>
        
        <div class="space-y-4">
          <UAccordion multiple :items="[
            {
              label: '破解成功率有多高？',
              content: '我们的破解成功率高达95%，对于常见的密码模式，成功率甚至更高。对于复杂密码，我们也会尝试多种高级算法。'
            },
            {
              label: '需要多长时间才能破解？',
              content: '破解时间取决于密码复杂度和文件大小。简单密码通常在几分钟内完成，复杂密码可能需要几小时。我们会实时显示进度。'
            },
            {
              label: '我的文件安全吗？',
              content: '我们采用银行级加密技术保护您的文件，所有文件在传输和存储过程中都经过加密处理，破解完成后会立即删除。'
            },
            {
              label: '支持哪些文件格式？',
              content: '我们支持50+种主流文件格式，包括ZIP、RAR、7Z、PDF、Office文档、加密磁盘镜像等。完整列表请查看文档。'
            },
            {
              label: '如果破解失败怎么办？',
              content: '如果破解失败，我们将全额退款。我们也会提供失败原因分析，帮助您了解文件加密情况。'
            }
          ]" />
        </div>
      </div>
    </section>

    <!-- 再次行动召唤 -->
    <section class="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-blue-900/30 to-purple-900/30">
      <div class="max-w-4xl mx-auto text-center space-y-8">
        <h3 class="text-[clamp(2rem,4vw,3rem)] font-bold text-white">
          准备好解密您的文件了吗？
        </h3>
        <p class="text-xl text-gray-300">
          立即开始，几分钟内即可恢复您的重要文件
        </p>
        <UButton 
          size="lg" 
          class="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 px-8 py-6 rounded-full text-lg font-semibold shadow-2xl hover:shadow-blue-500/25 transition-all duration-300"
          @click="$router.push('/upload')"
        >
          <template #default>
            <div class="flex items-center space-x-2">
              <span>🚀</span>
              <span>立即开始</span>
            </div>
          </template>
        </UButton>
      </div>
    </section>
  </div>
</template>

<script setup>
// 支持的文件格式
const supportedFormats = [
  { name: 'ZIP', icon: '📦', description: '压缩文件' },
  { name: 'RAR', icon: '🗜️', description: '压缩文件' },
  { name: '7Z', icon: '📁', description: '压缩文件' },
  { name: 'PDF', icon: '📄', description: '文档' },
  { name: 'Word', icon: '📝', description: '文档' },
  { name: 'Excel', icon: '📊', description: '表格' },
  { name: 'PowerPoint', icon: '📽️', description: '演示文稿' },
  { name: '图片', icon: '🖼️', description: '加密图片' },
  { name: '视频', icon: '🎬', description: '加密视频' },
  { name: '音频', icon: '🎵', description: '加密音频' },
  { name: '磁盘镜像', icon: '💿', description: '加密镜像' },
  { name: '数据库', icon: '🗄️', description: '加密数据库' },
  { name: '邮件', icon: '📧', description: '加密邮件' }
]

// 滚动到定价区域
const scrollToPricing = () => {
  const element = document.getElementById('pricing')
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}

// 设置页面标题和元数据
useHead({
  title: '在线加密文件解密服务 - 专业、安全、高效的密码破解方案',
  meta: [
    { name: 'description', content: '专业的在线加密文件解密服务，支持ZIP、RAR、7Z、PDF等多种格式，提供快速、安全的密码破解方案，几分钟内即可恢复您的重要文件。' },
    { name: 'keywords', content: '文件解密,密码破解,在线解密,ZIP解密,RAR解密,7Z解密,PDF解密,加密文件解密' }
  ]
})
</script>