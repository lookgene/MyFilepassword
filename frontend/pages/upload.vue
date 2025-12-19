<template>
  <div>

    <!-- Main Content -->
    <main class="pt-32 pb-24 px-4 sm:px-6 lg:px-8">
      <div class="max-w-4xl mx-auto">
        <!-- 页面标题 -->
        <div class="text-center mb-16">
          <UBadge variant="secondary" class="bg-blue-500/20 text-blue-400 px-4 py-2 rounded-full text-sm font-medium border border-blue-500/30 mb-4">
            文件解密
          </UBadge>
          <h2 class="text-[clamp(1.5rem,3vw,2.5rem)] font-bold text-white mb-4">上传加密文件</h2>
          <p class="text-lg text-gray-400 max-w-2xl mx-auto">
            选择您需要解密的文件，填写相关信息，我们将尽快为您解密
          </p>
        </div>
        
        <!-- 表单卡片 -->
        <UCard class="border border-gray-700 bg-gray-800/50 rounded-2xl overflow-hidden">
          <template #content>
            <div class="p-8">
              <form @submit.prevent="handleSubmit" class="space-y-8">
                <!-- 文件上传 -->
                <div class="space-y-3">
                  <label class="block text-sm font-medium text-white">
                    选择文件 <span class="text-red-400">*</span>
                  </label>
                  <div class="flex flex-col space-y-3">
                    <div class="relative group">
                      <input
                        type="file"
                        id="file-upload"
                        ref="fileInput"
                        @change="handleFileChange"
                        accept=".zip,.rar,.7z,.pdf,.doc,.docx,.xls,.xlsx"
                        class="absolute inset-0 opacity-0 cursor-pointer z-10"
                      >
                      <div class="border-2 border-dashed border-gray-600 rounded-xl p-8 text-center hover:border-blue-500 transition-colors duration-300 bg-gray-800/30">
                        <div class="text-4xl mb-4 text-gray-400">📁</div>
                        <h3 class="text-lg font-semibold text-white mb-1">
                          {{ selectedFileName ? '已选择文件' : '点击或拖拽文件到此处' }}
                        </h3>
                        <p class="text-sm text-gray-400 mb-4">
                          {{ selectedFileName ? selectedFileName : '支持ZIP、RAR、7Z、PDF、Word、Excel文件' }}
                        </p>
                        <UButton 
                          type="button" 
                          variant="outline" 
                          size="sm"
                          class="border-blue-500 text-blue-400 hover:bg-blue-500/10"
                          @click="fileInput?.click()"
                        >
                          <template #default>
                            {{ selectedFileName ? '更换文件' : '选择文件' }}
                          </template>
                        </UButton>
                      </div>
                    </div>
                    <p class="text-xs text-gray-400">
                      单个文件最大100MB，文件将被安全处理并在解密完成后删除
                    </p>
                  </div>
                </div>

                <!-- 破解类型 -->
                <div class="space-y-3">
                  <label class="block text-sm font-medium text-white">
                    破解类型 <span class="text-red-400">*</span>
                  </label>
                  <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <label 
                      v-for="type in crackTypes" 
                      :key="type.value"
                      class="relative border-2 border-gray-700 rounded-xl p-5 cursor-pointer hover:border-blue-500 transition-all duration-300 hover:shadow-sm bg-gray-800/30"
                      :class="{ 'border-blue-500 bg-blue-500/10': uploadForm.crackType === type.value }"
                    >
                      <input 
                        type="radio" 
                        v-model="uploadForm.crackType" 
                        :value="type.value" 
                        class="absolute top-4 right-4 h-4 w-4 text-blue-500 focus:ring-blue-500 border-gray-600"
                      >
                      <div class="flex flex-col space-y-2">
                        <div class="text-lg font-semibold text-white">{{ type.name }}</div>
                        <div class="text-sm text-gray-400">{{ type.description }}</div>
                        <div class="text-sm font-medium text-blue-400 mt-1">{{ type.price }}</div>
                      </div>
                    </label>
                  </div>
                </div>

                <!-- 邮箱地址 -->
                <div class="space-y-3">
                  <label class="block text-sm font-medium text-white">
                    邮箱地址 <span class="text-red-400">*</span>
                  </label>
                  <UInput
                    v-model="uploadForm.email"
                    placeholder="请输入邮箱地址，用于接收破解结果"
                    type="email"
                    class="w-full"
                    :rules="{ required: '请输入邮箱地址', email: '请输入有效的邮箱地址' }"
                  >
                    <template #left>
                      <span class="text-gray-400">📧</span>
                    </template>
                  </UInput>
                </div>

                <!-- 提交按钮 -->
                <div>
                  <UButton 
                    type="submit" 
                    variant="primary" 
                    class="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 px-8 py-6 rounded-full w-full sm:w-auto"
                    :disabled="isSubmitting"
                  >
                    <template #default>
                      <span>{{ isSubmitting ? '提交中...' : '提交任务' }}</span>
                    </template>
                  </UButton>
                </div>
              </form>
            </div>
          </template>
        </UCard>
      </div>
    </main>

    <!-- 成功提示 -->
    <UModal v-model="dialogVisible" class="backdrop-blur-sm">
      <template #content>
        <div class="sm:max-w-md w-full bg-gray-800 border border-gray-700 rounded-xl">
          <div class="text-center py-6">
            <div class="bg-green-500/20 rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-6">
              <div class="text-4xl text-green-400">✅</div>
            </div>
            <h3 class="text-xl font-bold text-white mb-3">任务提交成功！</h3>
            <p class="text-gray-400 mb-6">
              我们将在完成后通过邮箱通知您。请保持邮箱畅通。
            </p>
            <div class="bg-gray-900/50 border border-gray-700 rounded-lg overflow-hidden mb-6 p-4">
              <div class="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <div class="text-gray-400">任务ID</div>
                  <div class="font-semibold text-white">{{ taskId }}</div>
                </div>
                <div>
                  <div class="text-gray-400">邮箱</div>
                  <div class="font-semibold text-white">{{ uploadForm.email }}</div>
                </div>
              </div>
            </div>
            <UButton 
              variant="primary" 
              @click="dialogVisible = false"
              class="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 w-full"
            >
              <template #default>
                <span>确定</span>
              </template>
            </UButton>
          </div>
        </div>
      </template>
    </UModal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

// 设置页面标题和元数据
useHead({
  title: '上传文件 - CrackSecure - 专业密码破解服务',
  meta: [
    { name: 'description', content: '上传您的加密文件，选择破解方案，我们将快速为您破解密码。支持ZIP、RAR、7Z、PDF等多种文件格式。' },
    { name: 'keywords', content: '文件上传,密码破解,在线解密,ZIP解密,RAR解密,7Z解密,PDF解密' }
  ]
})

// 表单数据
const uploadForm = reactive({
  email: '',
  crackType: 'simple' as 'simple' | 'regular' | 'professional'
})

// 破解类型选项
const crackTypes = [
  {
    value: 'simple',
    name: '简单密码',
    description: '6位纯数字密码',
    price: '免费'
  },
  {
    value: 'regular',
    name: '常规任务',
    description: '字母、数字、符号组合',
    price: '按文件大小收费'
  },
  {
    value: 'professional',
    name: '专业破解',
    description: '高级加密算法',
    price: '定制价格'
  }
]

// 文件相关
const fileInput = ref<HTMLInputElement | null>(null)
const selectedFile = ref<File | null>(null)
const selectedFileName = ref('')

// 提交状态
const isSubmitting = ref(false)

// 对话框状态
const dialogVisible = ref(false)
const taskId = ref('')

// 文件选择处理
const handleFileChange = (event: Event) => {
  const input = event.target as HTMLInputElement
  if (input.files && input.files.length > 0) {
    const file = input.files[0]
    
    // 验证文件大小
    const isLt100M = file.size / 1024 / 1024 < 100
    if (!isLt100M) {
      alert('文件大小不能超过100MB')
      input.value = '' // 清空文件选择
      return
    }
    
    selectedFile.value = file
    selectedFileName.value = file.name
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!selectedFile.value) {
    alert('请选择要上传的文件')
    return
  }

  if (!uploadForm.email) {
    alert('请输入邮箱地址')
    return
  }

  isSubmitting.value = true

  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // 生成任务ID
    taskId.value = 'TASK-' + Math.random().toString(36).substr(2, 9).toUpperCase()
    dialogVisible.value = true

    // 重置表单
    if (fileInput.value) {
      fileInput.value.value = ''
    }
    selectedFile.value = null
    selectedFileName.value = ''
    uploadForm.email = ''
    uploadForm.crackType = 'simple'
  } catch (error) {
    console.error('提交失败:', error)
    alert('任务提交失败，请稍后重试')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
/* 自定义过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>