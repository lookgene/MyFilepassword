<template>
  <div>
    <div class="container mx-auto px-4 py-8">
      <div class="max-w-4xl mx-auto">
        <!-- 页面标题 -->
        <div class="text-center mb-12">
          <h1 class="text-4xl font-bold mb-4">文件解密</h1>
          <p class="text-gray-400 text-lg">输入解密密钥，获取您的文件内容</p>
        </div>

        <!-- 文件信息卡片 -->
        <UCard class="mb-8 bg-gray-800 border-gray-700">
          <template #header>
            <div class="flex items-center justify-between">
              <h2 class="text-xl font-semibold">文件信息</h2>
              <UBadge color="blue" variant="subtle">已加密</UBadge>
            </div>
          </template>
          
          <div class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p class="text-sm text-gray-400 mb-1">文件名</p>
                <p class="font-medium">{{ fileName || 'example_document.pdf' }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-400 mb-1">文件大小</p>
                <p class="font-medium">{{ fileSize || '2.4 MB' }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-400 mb-1">上传时间</p>
                <p class="font-medium">{{ uploadTime || '2023-11-15 14:30' }}</p>
              </div>
              <div>
                <p class="text-sm text-gray-400 mb-1">加密算法</p>
                <p class="font-medium">{{ encryptionType || 'AES-256' }}</p>
              </div>
            </div>
          </div>
        </UCard>

        <!-- 解密表单 -->
        <UCard class="mb-8 bg-gray-800 border-gray-700">
          <template #header>
            <h2 class="text-xl font-semibold">输入解密密钥</h2>
          </template>
          
          <UForm :state="form" @submit="onSubmit" class="space-y-6">
            <UFormGroup label="解密密钥" name="key" required>
              <UInput
                v-model="form.key"
                type="password"
                placeholder="请输入您的解密密钥"
                icon="i-heroicons-key"
                size="lg"
                :loading="isProcessing"
              />
              <template #help>
                请输入您在加密文件时设置的密钥
              </template>
            </UFormGroup>

            <div class="flex flex-col sm:flex-row gap-4">
              <UButton
                type="submit"
                color="primary"
                size="lg"
                :loading="isProcessing"
                :disabled="!form.key"
                class="flex-1"
              >
                <template v-if="isProcessing">
                  解密中...
                </template>
                <template v-else>
                  <UIcon name="i-heroicons-lock-open" class="mr-2" />
                  解密文件
                </template>
              </UButton>
              
              <UButton
                color="gray"
                size="lg"
                variant="outline"
                :disabled="isProcessing"
                @click="resetForm"
              >
                重置
              </UButton>
            </div>
          </UForm>
        </UCard>

        <!-- 解密结果 -->
        <UCard v-if="decryptionResult" class="bg-gray-800 border-gray-700">
          <template #header>
            <div class="flex items-center justify-between">
              <h2 class="text-xl font-semibold">解密结果</h2>
              <UBadge :color="decryptionResult.success ? 'green' : 'red'" variant="subtle">
                {{ decryptionResult.success ? '成功' : '失败' }}
              </UBadge>
            </div>
          </template>
          
          <div v-if="decryptionResult.success" class="space-y-4">
            <UAlert color="green" icon="i-heroicons-check-circle" title="解密成功">
              <template #description>
                您的文件已成功解密，可以查看或下载内容。
              </template>
            </UAlert>
            
            <div class="flex flex-col sm:flex-row gap-4">
              <UButton color="primary" size="lg" class="flex-1">
                <UIcon name="i-heroicons-eye" class="mr-2" />
                查看内容
              </UButton>
              
              <UButton color="green" size="lg" class="flex-1">
                <UIcon name="i-heroicons-arrow-down-tray" class="mr-2" />
                下载文件
              </UButton>
            </div>
            
            <!-- 文件预览区域 -->
            <div class="mt-6 p-4 bg-gray-700 rounded-lg">
              <h3 class="text-lg font-medium mb-3">文件预览</h3>
              <div class="bg-gray-900 p-4 rounded border border-gray-600 max-h-96 overflow-auto">
                <pre class="text-sm text-gray-300">{{ decryptionResult.content || '文件内容预览将显示在这里...' }}</pre>
              </div>
            </div>
          </div>
          
          <div v-else class="space-y-4">
            <UAlert color="red" icon="i-heroicons-exclamation-triangle" title="解密失败">
              <template #description>
                {{ decryptionResult.message || '提供的解密密钥不正确，请检查后重试。' }}
              </template>
            </UAlert>
            
            <UButton color="primary" size="lg" @click="resetForm">
              重新尝试
            </UButton>
          </div>
        </UCard>

        <!-- 安全提示 -->
        <UCard class="mt-8 bg-gray-800 border-gray-700">
          <template #header>
            <h2 class="text-xl font-semibold">安全提示</h2>
          </template>
          
          <div class="space-y-3">
            <div class="flex items-start">
              <UIcon name="i-heroicons-shield-check" class="text-green-500 mt-0.5 mr-3 flex-shrink-0" />
              <p class="text-sm text-gray-300">您的密钥仅在本地处理，不会发送到服务器</p>
            </div>
            <div class="flex items-start">
              <UIcon name="i-heroicons-lock-closed" class="text-green-500 mt-0.5 mr-3 flex-shrink-0" />
              <p class="text-sm text-gray-300">解密完成后，请及时下载并安全保存您的文件</p>
            </div>
            <div class="flex items-start">
              <UIcon name="i-heroicons-clock" class="text-green-500 mt-0.5 mr-3 flex-shrink-0" />
              <p class="text-sm text-gray-300">解密后的文件将在服务器上保留24小时，之后将被自动删除</p>
            </div>
          </div>
        </UCard>
      </div>
    </div>
  </div>
</template>

<script setup>
// 页面元数据
definePageMeta({
  title: '文件解密',
  description: '输入解密密钥，获取您的文件内容'
})

// 响应式数据
const form = reactive({
  key: ''
})

const isProcessing = ref(false)
const decryptionResult = ref(null)

// 模拟文件信息
const fileName = ref('example_document.pdf')
const fileSize = ref('2.4 MB')
const uploadTime = ref('2023-11-15 14:30')
const encryptionType = ref('AES-256')

// 表单提交处理
const onSubmit = async () => {
  isProcessing.value = true
  
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // 模拟解密结果（实际应用中这里会调用后端API）
    const isSuccess = form.key === 'correctkey' || Math.random() > 0.3 // 70%成功率用于演示
    
    if (isSuccess) {
      decryptionResult.value = {
        success: true,
        content: `这是解密后的文件内容示例。

文件标题: 机密文档
创建日期: 2023-11-10
作者: 系统管理员

正文内容:
这是一个加密文件系统的示例文档。该系统使用AES-256加密算法保护您的文件安全。

主要功能:
1. 文件上传与加密
2. 安全密钥管理
3. 在线解密与预览
4. 安全文件下载

技术特点:
- 端到端加密
- 客户端密钥处理
- 安全传输协议
- 自动文件清理

感谢您使用我们的安全文件加密服务！`
      }
    } else {
      decryptionResult.value = {
        success: false,
        message: '提供的解密密钥不正确，请检查后重试。'
      }
    }
  } catch (error) {
    decryptionResult.value = {
      success: false,
      message: '解密过程中发生错误，请稍后重试。'
    }
  } finally {
    isProcessing.value = false
  }
}

// 重置表单
const resetForm = () => {
  form.key = ''
  decryptionResult.value = null
}

// 获取路由参数（如果有）
const route = useRoute()
onMounted(() => {
  // 如果从上传页面跳转过来，可能会有文件ID参数
  if (route.query.fileId) {
    // 实际应用中会根据fileId获取文件信息
    console.log('File ID from query:', route.query.fileId)
  }
})
</script>