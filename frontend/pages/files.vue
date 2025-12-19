<template>
  <div>
    <div class="container mx-auto px-4 py-8">
      <div class="max-w-7xl mx-auto">
        <!-- 页面标题 -->
        <div class="text-center mb-8">
          <h1 class="text-4xl font-bold mb-4">文件管理</h1>
          <p class="text-gray-400 text-lg">管理您的所有加密和解密文件</p>
        </div>

        <!-- 文件统计卡片 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <UCard class="bg-gray-800 border-gray-700">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-gray-400 text-sm">已上传文件</p>
                <p class="text-3xl font-bold mt-1">{{ fileStats.uploaded }}</p>
              </div>
              <UIcon name="i-heroicons-cloud-arrow-up" class="text-4xl text-blue-500" />
            </div>
          </UCard>
          
          <UCard class="bg-gray-800 border-gray-700">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-gray-400 text-sm">已解密文件</p>
                <p class="text-3xl font-bold mt-1">{{ fileStats.decrypted }}</p>
              </div>
              <UIcon name="i-heroicons-lock-open" class="text-4xl text-green-500" />
            </div>
          </UCard>
          
          <UCard class="bg-gray-800 border-gray-700">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-gray-400 text-sm">存储空间</p>
                <p class="text-3xl font-bold mt-1">{{ fileStats.storage }}</p>
              </div>
              <UIcon name="i-heroicons-server" class="text-4xl text-purple-500" />
            </div>
          </UCard>
        </div>

        <!-- 文件操作区域 -->
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
          <div class="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
            <UButton color="primary" size="lg" @click="$router.push('/upload')">
              <UIcon name="i-heroicons-plus" class="mr-2" />
              上传新文件
            </UButton>
            
            <UButton color="gray" size="lg" variant="outline" @click="refreshFiles">
              <UIcon name="i-heroicons-arrow-path" class="mr-2" />
              刷新
            </UButton>
          </div>
          
          <div class="flex items-center gap-4 w-full sm:w-auto">
            <UInput
              v-model="searchQuery"
              placeholder="搜索文件..."
              icon="i-heroicons-magnifying-glass"
              size="lg"
              class="w-full sm:w-64"
            />
            
            <USelectMenu
              v-model="selectedFilter"
              :options="filterOptions"
              placeholder="筛选"
              size="lg"
              class="w-full sm:w-40"
            />
          </div>
        </div>

        <!-- 文件列表 -->
        <UCard class="bg-gray-800 border-gray-700">
          <template #header>
            <div class="flex items-center justify-between">
              <h2 class="text-xl font-semibold">文件列表</h2>
              <p class="text-sm text-gray-400">共 {{ filteredFiles.length }} 个文件</p>
            </div>
          </template>
          
          <div v-if="filteredFiles.length === 0" class="text-center py-12">
            <UIcon name="i-heroicons-folder-open" class="text-6xl text-gray-600 mb-4" />
            <p class="text-xl text-gray-400 mb-2">没有找到文件</p>
            <p class="text-gray-500 mb-6">上传您的第一个加密文件开始使用</p>
            <UButton color="primary" size="lg" @click="$router.push('/upload')">
              <UIcon name="i-heroicons-plus" class="mr-2" />
              上传文件
            </UButton>
          </div>
          
          <div v-else class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b border-gray-700">
                  <th class="text-left py-3 px-4">文件名</th>
                  <th class="text-left py-3 px-4">大小</th>
                  <th class="text-left py-3 px-4">状态</th>
                  <th class="text-left py-3 px-4">上传时间</th>
                  <th class="text-left py-3 px-4">操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="file in paginatedFiles" :key="file.id" class="border-b border-gray-700 hover:bg-gray-750">
                  <td class="py-3 px-4">
                    <div class="flex items-center">
                      <UIcon :name="getFileIcon(file.type)" class="text-xl mr-3" />
                      <div>
                        <p class="font-medium">{{ file.name }}</p>
                        <p class="text-sm text-gray-400">{{ file.type }}</p>
                      </div>
                    </div>
                  </td>
                  <td class="py-3 px-4">{{ file.size }}</td>
                  <td class="py-3 px-4">
                    <UBadge :color="getStatusColor(file.status)" variant="subtle">
                      {{ getStatusText(file.status) }}
                    </UBadge>
                  </td>
                  <td class="py-3 px-4">{{ formatDate(file.uploadTime) }}</td>
                  <td class="py-3 px-4">
                    <div class="flex gap-2">
                      <UButton
                        v-if="file.status === 'encrypted'"
                        color="primary"
                        size="sm"
                        variant="outline"
                        @click="decryptFile(file)"
                      >
                        <UIcon name="i-heroicons-lock-open" class="mr-1" />
                        解密
                      </UButton>
                      
                      <UButton
                        v-if="file.status === 'decrypted'"
                        color="green"
                        size="sm"
                        variant="outline"
                        @click="downloadFile(file)"
                      >
                        <UIcon name="i-heroicons-arrow-down-tray" class="mr-1" />
                        下载
                      </UButton>
                      
                      <UButton
                        color="red"
                        size="sm"
                        variant="outline"
                        @click="deleteFile(file)"
                      >
                        <UIcon name="i-heroicons-trash" class="mr-1" />
                        删除
                      </UButton>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <!-- 分页 -->
          <div v-if="filteredFiles.length > itemsPerPage" class="flex justify-center mt-6">
            <UPagination
              v-model="currentPage"
              :page-count="itemsPerPage"
              :total="filteredFiles.length"
              :max="5"
            />
          </div>
        </UCard>

        <!-- 文件详情模态框 -->
        <UModal v-model="isFileDetailsOpen" :ui="{ width: 'sm:max-w-2xl' }">
          <UCard class="bg-gray-800 border-gray-700">
            <template #header>
              <div class="flex items-center justify-between">
                <h2 class="text-xl font-semibold">文件详情</h2>
                <UButton color="gray" variant="ghost" icon="i-heroicons-x-mark-20-solid" @click="isFileDetailsOpen = false" />
              </div>
            </template>
            
            <div v-if="selectedFile" class="space-y-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p class="text-sm text-gray-400 mb-1">文件名</p>
                  <p class="font-medium">{{ selectedFile.name }}</p>
                </div>
                <div>
                  <p class="text-sm text-gray-400 mb-1">文件大小</p>
                  <p class="font-medium">{{ selectedFile.size }}</p>
                </div>
                <div>
                  <p class="text-sm text-gray-400 mb-1">文件类型</p>
                  <p class="font-medium">{{ selectedFile.type }}</p>
                </div>
                <div>
                  <p class="text-sm text-gray-400 mb-1">状态</p>
                  <UBadge :color="getStatusColor(selectedFile.status)" variant="subtle">
                    {{ getStatusText(selectedFile.status) }}
                  </UBadge>
                </div>
                <div>
                  <p class="text-sm text-gray-400 mb-1">上传时间</p>
                  <p class="font-medium">{{ formatDate(selectedFile.uploadTime) }}</p>
                </div>
                <div>
                  <p class="text-sm text-gray-400 mb-1">过期时间</p>
                  <p class="font-medium">{{ formatDate(selectedFile.expiryTime) }}</p>
                </div>
              </div>
              
              <div>
                <p class="text-sm text-gray-400 mb-1">文件描述</p>
                <p class="font-medium">{{ selectedFile.description || '无描述' }}</p>
              </div>
              
              <div class="flex gap-2 pt-4">
                <UButton
                  v-if="selectedFile.status === 'encrypted'"
                  color="primary"
                  @click="decryptFile(selectedFile)"
                >
                  <UIcon name="i-heroicons-lock-open" class="mr-2" />
                  解密文件
                </UButton>
                
                <UButton
                  v-if="selectedFile.status === 'decrypted'"
                  color="green"
                  @click="downloadFile(selectedFile)"
                >
                  <UIcon name="i-heroicons-arrow-down-tray" class="mr-2" />
                  下载文件
                </UButton>
                
                <UButton
                  color="red"
                  variant="outline"
                  @click="deleteFile(selectedFile)"
                >
                  <UIcon name="i-heroicons-trash" class="mr-2" />
                  删除文件
                </UButton>
              </div>
            </div>
          </UCard>
        </UModal>
      </div>
    </div>
  </div>
</template>

<script setup>
// 页面元数据
definePageMeta({
  title: '文件管理',
  description: '管理您的所有加密和解密文件'
})

// 响应式数据
const searchQuery = ref('')
const selectedFilter = ref('all')
const currentPage = ref(1)
const itemsPerPage = 10
const isFileDetailsOpen = ref(false)
const selectedFile = ref(null)

// 文件统计数据
const fileStats = ref({
  uploaded: 12,
  decrypted: 8,
  storage: '125 MB'
})

// 筛选选项
const filterOptions = [
  { label: '全部文件', value: 'all' },
  { label: '已加密', value: 'encrypted' },
  { label: '已解密', value: 'decrypted' }
]

// 模拟文件数据
const files = ref([
  {
    id: 1,
    name: '财务报表.pdf',
    type: 'application/pdf',
    size: '2.4 MB',
    status: 'encrypted',
    uploadTime: new Date('2023-11-15T14:30:00'),
    expiryTime: new Date('2023-11-16T14:30:00'),
    description: '2023年第三季度财务报表'
  },
  {
    id: 2,
    name: '项目计划.docx',
    type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    size: '1.8 MB',
    status: 'decrypted',
    uploadTime: new Date('2023-11-14T10:15:00'),
    expiryTime: new Date('2023-11-15T10:15:00'),
    description: '新产品开发项目计划'
  },
  {
    id: 3,
    name: '客户数据.xlsx',
    type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    size: '3.2 MB',
    status: 'encrypted',
    uploadTime: new Date('2023-11-13T16:45:00'),
    expiryTime: new Date('2023-11-14T16:45:00'),
    description: '客户联系信息和购买历史'
  },
  {
    id: 4,
    name: '产品图片.zip',
    type: 'application/zip',
    size: '15.6 MB',
    status: 'decrypted',
    uploadTime: new Date('2023-11-12T09:30:00'),
    expiryTime: new Date('2023-11-13T09:30:00'),
    description: '新产品宣传图片集合'
  },
  {
    id: 5,
    name: '会议记录.txt',
    type: 'text/plain',
    size: '125 KB',
    status: 'encrypted',
    uploadTime: new Date('2023-11-11T13:20:00'),
    expiryTime: new Date('2023-11-12T13:20:00'),
    description: '团队周会会议记录'
  }
])

// 计算属性 - 筛选后的文件
const filteredFiles = computed(() => {
  let result = files.value
  
  // 按状态筛选
  if (selectedFilter.value !== 'all') {
    result = result.filter(file => file.status === selectedFilter.value)
  }
  
  // 按搜索关键词筛选
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(file => 
      file.name.toLowerCase().includes(query) || 
      file.type.toLowerCase().includes(query) ||
      (file.description && file.description.toLowerCase().includes(query))
    )
  }
  
  return result
})

// 计算属性 - 分页后的文件
const paginatedFiles = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredFiles.value.slice(start, end)
})

// 方法 - 获取文件图标
const getFileIcon = (type) => {
  if (type.includes('pdf')) return 'i-heroicons-document-text'
  if (type.includes('word') || type.includes('document')) return 'i-heroicons-document'
  if (type.includes('excel') || type.includes('spreadsheet')) return 'i-heroicons-chart-bar'
  if (type.includes('image')) return 'i-heroicons-photo'
  if (type.includes('zip') || type.includes('compressed')) return 'i-heroicons-archive-box'
  if (type.includes('text')) return 'i-heroicons-document-text'
  return 'i-heroicons-document'
}

// 方法 - 获取状态颜色
const getStatusColor = (status) => {
  return status === 'encrypted' ? 'blue' : status === 'decrypted' ? 'green' : 'gray'
}

// 方法 - 获取状态文本
const getStatusText = (status) => {
  return status === 'encrypted' ? '已加密' : status === 'decrypted' ? '已解密' : '未知'
}

// 方法 - 格式化日期
const formatDate = (date) => {
  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

// 方法 - 刷新文件列表
const refreshFiles = () => {
  // 实际应用中会调用API获取最新文件列表
  console.log('Refreshing files...')
}

// 方法 - 解密文件
const decryptFile = (file) => {
  // 跳转到解密页面
  $router.push({ path: '/decrypt', query: { fileId: file.id } })
}

// 方法 - 下载文件
const downloadFile = (file) => {
  // 实际应用中会调用API下载文件
  console.log('Downloading file:', file.name)
  // 模拟下载
  const link = document.createElement('a')
  link.href = '#'
  link.download = file.name
  link.click()
}

// 方法 - 删除文件
const deleteFile = (file) => {
  // 实际应用中会调用API删除文件
  console.log('Deleting file:', file.name)
  // 模拟删除
  const index = files.value.findIndex(f => f.id === file.id)
  if (index !== -1) {
    files.value.splice(index, 1)
  }
}

// 监听搜索查询变化，重置分页
watch([searchQuery, selectedFilter], () => {
  currentPage.value = 1
})
</script>