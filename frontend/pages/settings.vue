<template>
  <div>
    <div class="container mx-auto px-4 py-8">
      <div class="max-w-4xl mx-auto">
        <!-- 页面标题 -->
        <div class="text-center mb-8">
          <h1 class="text-4xl font-bold mb-4">用户设置</h1>
          <p class="text-gray-400 text-lg">管理您的账户信息和偏好设置</p>
        </div>

        <!-- 设置选项卡 -->
        <UTabs v-model="activeTab" :items="tabItems" class="mb-8">
          <template #profile="{ item }">
            <UCard class="bg-gray-800 border-gray-700">
              <template #header>
                <h2 class="text-xl font-semibold">个人资料</h2>
              </template>
              
              <UForm :state="profileForm" @submit="updateProfile" class="space-y-6">
                <div class="flex flex-col sm:flex-row gap-6">
                  <!-- 头像上传 -->
                  <div class="flex flex-col items-center">
                    <div class="relative mb-4">
                      <div 
                        class="w-24 h-24 rounded-full border-4 border-gray-700 bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center"
                      >
                        <UIcon name="i-heroicons-user" class="text-white text-4xl" />
                      </div>
                      <UButton
                        color="primary"
                        size="sm"
                        class="absolute bottom-0 right-0 rounded-full p-2"
                        @click="triggerAvatarUpload"
                      >
                        <UIcon name="i-heroicons-camera" />
                      </UButton>
                      <input
                        ref="avatarInput"
                        type="file"
                        accept="image/*"
                        class="hidden"
                        @change="handleAvatarChange"
                      >
                    </div>
                    <p class="text-sm text-gray-400 text-center">点击相机图标更换头像</p>
                  </div>
                  
                  <!-- 基本信息表单 -->
                  <div class="flex-1 space-y-4">
                    <UFormGroup label="用户名" name="username">
                      <UInput
                        v-model="profileForm.username"
                        placeholder="请输入用户名"
                        icon="i-heroicons-user"
                      />
                    </UFormGroup>
                    
                    <UFormGroup label="电子邮箱" name="email">
                      <UInput
                        v-model="profileForm.email"
                        type="email"
                        placeholder="请输入电子邮箱"
                        icon="i-heroicons-envelope"
                      />
                    </UFormGroup>
                    
                    <UFormGroup label="手机号码" name="phone">
                      <UInput
                        v-model="profileForm.phone"
                        placeholder="请输入手机号码"
                        icon="i-heroicons-device-phone-mobile"
                      />
                    </UFormGroup>
                  </div>
                </div>
                
                <UFormGroup label="个人简介" name="bio">
                  <UTextarea
                    v-model="profileForm.bio"
                    placeholder="请输入个人简介"
                    :rows="4"
                  />
                </UFormGroup>
                
                <div class="flex justify-end">
                  <UButton type="submit" color="primary" :loading="isUpdating">
                    保存更改
                  </UButton>
                </div>
              </UForm>
            </UCard>
          </template>
          
          <template #security="{ item }">
            <UCard class="bg-gray-800 border-gray-700">
              <template #header>
                <h2 class="text-xl font-semibold">安全设置</h2>
              </template>
              
              <div class="space-y-6">
                <!-- 修改密码 -->
                <div>
                  <h3 class="text-lg font-medium mb-4">修改密码</h3>
                  <UForm :state="passwordForm" @submit="updatePassword" class="space-y-4">
                    <UFormGroup label="当前密码" name="currentPassword">
                      <UInput
                        v-model="passwordForm.currentPassword"
                        type="password"
                        placeholder="请输入当前密码"
                        icon="i-heroicons-lock-closed"
                      />
                    </UFormGroup>
                    
                    <UFormGroup label="新密码" name="newPassword">
                      <UInput
                        v-model="passwordForm.newPassword"
                        type="password"
                        placeholder="请输入新密码"
                        icon="i-heroicons-lock-closed"
                      />
                    </UFormGroup>
                    
                    <UFormGroup label="确认新密码" name="confirmPassword">
                      <UInput
                        v-model="passwordForm.confirmPassword"
                        type="password"
                        placeholder="请再次输入新密码"
                        icon="i-heroicons-lock-closed"
                      />
                    </UFormGroup>
                    
                    <div class="flex justify-end">
                      <UButton type="submit" color="primary" :loading="isUpdatingPassword">
                        更新密码
                      </UButton>
                    </div>
                  </UForm>
                </div>
                
                <!-- 双因素认证 -->
                <div class="border-t border-gray-700 pt-6">
                  <h3 class="text-lg font-medium mb-4">双因素认证</h3>
                  <div class="flex items-center justify-between">
                    <div>
                      <p class="font-medium">启用双因素认证</p>
                      <p class="text-sm text-gray-400">为您的账户添加额外的安全保护</p>
                    </div>
                    <UToggle v-model="twoFactorEnabled" @change="toggleTwoFactor" />
                  </div>
                </div>
                
                <!-- 登录活动 -->
                <div class="border-t border-gray-700 pt-6">
                  <h3 class="text-lg font-medium mb-4">最近登录活动</h3>
                  <div class="space-y-3">
                    <div v-for="activity in loginActivities" :key="activity.id" class="flex items-center justify-between p-3 bg-gray-700 rounded-lg">
                      <div class="flex items-center">
                        <UIcon :name="getDeviceIcon(activity.device)" class="text-xl mr-3" />
                        <div>
                          <p class="font-medium">{{ activity.device }}</p>
                          <p class="text-sm text-gray-400">{{ activity.location }} · {{ formatDate(activity.time) }}</p>
                        </div>
                      </div>
                      <UBadge :color="activity.current ? 'green' : 'gray'" variant="subtle">
                        {{ activity.current ? '当前会话' : '历史会话' }}
                      </UBadge>
                    </div>
                  </div>
                </div>
              </div>
            </UCard>
          </template>
          
          <template #preferences="{ item }">
            <UCard class="bg-gray-800 border-gray-700">
              <template #header>
                <h2 class="text-xl font-semibold">偏好设置</h2>
              </template>
              
              <div class="space-y-6">
                <!-- 通知设置 -->
                <div>
                  <h3 class="text-lg font-medium mb-4">通知设置</h3>
                  <div class="space-y-4">
                    <div class="flex items-center justify-between">
                      <div>
                        <p class="font-medium">邮件通知</p>
                        <p class="text-sm text-gray-400">接收有关文件上传和解密的通知</p>
                      </div>
                      <UToggle v-model="preferences.emailNotifications" />
                    </div>
                    
                    <div class="flex items-center justify-between">
                      <div>
                        <p class="font-medium">浏览器通知</p>
                        <p class="text-sm text-gray-400">在浏览器中接收实时通知</p>
                      </div>
                      <UToggle v-model="preferences.browserNotifications" />
                    </div>
                    
                    <div class="flex items-center justify-between">
                      <div>
                        <p class="font-medium">文件过期提醒</p>
                        <p class="text-sm text-gray-400">在文件即将过期前发送提醒</p>
                      </div>
                      <UToggle v-model="preferences.expiryReminders" />
                    </div>
                  </div>
                </div>
                
                <!-- 界面设置 -->
                <div class="border-t border-gray-700 pt-6">
                  <h3 class="text-lg font-medium mb-4">界面设置</h3>
                  <div class="space-y-4">
                    <UFormGroup label="语言" name="language">
                      <USelectMenu
                        v-model="preferences.language"
                        :options="languageOptions"
                        placeholder="选择语言"
                      />
                    </UFormGroup>
                    
                    <UFormGroup label="时区" name="timezone">
                      <USelectMenu
                        v-model="preferences.timezone"
                        :options="timezoneOptions"
                        placeholder="选择时区"
                      />
                    </UFormGroup>
                    
                    <div class="flex items-center justify-between">
                      <div>
                        <p class="font-medium">深色模式</p>
                        <p class="text-sm text-gray-400">使用深色主题界面</p>
                      </div>
                      <UToggle v-model="preferences.darkMode" />
                    </div>
                  </div>
                </div>
                
                <!-- 文件设置 -->
                <div class="border-t border-gray-700 pt-6">
                  <h3 class="text-lg font-medium mb-4">文件设置</h3>
                  <div class="space-y-4">
                    <UFormGroup label="默认文件过期时间" name="defaultExpiry">
                      <USelectMenu
                        v-model="preferences.defaultExpiry"
                        :options="expiryOptions"
                        placeholder="选择默认过期时间"
                      />
                    </UFormGroup>
                    
                    <UFormGroup label="文件下载格式" name="downloadFormat">
                      <USelectMenu
                        v-model="preferences.downloadFormat"
                        :options="downloadFormatOptions"
                        placeholder="选择默认下载格式"
                      />
                    </UFormGroup>
                    
                    <div class="flex items-center justify-between">
                      <div>
                        <p class="font-medium">自动解密</p>
                        <p class="text-sm text-gray-400">上传后自动尝试解密文件</p>
                      </div>
                      <UToggle v-model="preferences.autoDecrypt" />
                    </div>
                  </div>
                </div>
                
                <div class="flex justify-end pt-4">
                  <UButton color="primary" @click="savePreferences" :loading="isSavingPreferences">
                    保存偏好设置
                  </UButton>
                </div>
              </div>
            </UCard>
          </template>
        </UTabs>
      </div>
    </div>
  </div>
</template>

<script setup>
// 页面元数据
definePageMeta({
  title: '用户设置',
  description: '管理您的账户信息和偏好设置'
})

// 响应式数据
const activeTab = ref(0)
const isUpdating = ref(false)
const isUpdatingPassword = ref(false)
const isSavingPreferences = ref(false)
const twoFactorEnabled = ref(false)
const avatarInput = ref(null)

// 选项卡项目
const tabItems = [
  { key: 'profile', label: '个人资料' },
  { key: 'security', label: '安全设置' },
  { key: 'preferences', label: '偏好设置' }
]

// 个人资料表单
const profileForm = reactive({
  username: 'demo_user',
  email: 'user@example.com',
  phone: '+86 138 0000 0000',
  bio: '这是一个示例用户简介。',
  avatar: ''
})

// 密码表单
const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 偏好设置
const preferences = reactive({
  emailNotifications: true,
  browserNotifications: false,
  expiryReminders: true,
  language: 'zh-CN',
  timezone: 'Asia/Shanghai',
  darkMode: true,
  defaultExpiry: '24h',
  downloadFormat: 'original',
  autoDecrypt: false
})

// 选项数据
const languageOptions = [
  { label: '简体中文', value: 'zh-CN' },
  { label: 'English', value: 'en-US' },
  { label: '繁體中文', value: 'zh-TW' }
]

const timezoneOptions = [
  { label: '北京时间 (GMT+8)', value: 'Asia/Shanghai' },
  { label: '东京时间 (GMT+9)', value: 'Asia/Tokyo' },
  { label: '纽约时间 (GMT-5)', value: 'America/New_York' },
  { label: '伦敦时间 (GMT+0)', value: 'Europe/London' }
]

const expiryOptions = [
  { label: '6小时', value: '6h' },
  { label: '12小时', value: '12h' },
  { label: '24小时', value: '24h' },
  { label: '3天', value: '3d' },
  { label: '7天', value: '7d' }
]

const downloadFormatOptions = [
  { label: '原始格式', value: 'original' },
  { label: 'PDF', value: 'pdf' },
  { label: 'ZIP压缩包', value: 'zip' }
]

// 登录活动数据
const loginActivities = ref([
  {
    id: 1,
    device: 'Windows PC - Chrome',
    location: '北京市',
    time: new Date(),
    current: true
  },
  {
    id: 2,
    device: 'iPhone - Safari',
    location: '上海市',
    time: new Date(Date.now() - 86400000), // 1天前
    current: false
  },
  {
    id: 3,
    device: 'MacBook - Safari',
    location: '深圳市',
    time: new Date(Date.now() - 172800000), // 2天前
    current: false
  }
])

// 方法 - 触发头像上传
const triggerAvatarUpload = () => {
  avatarInput.value.click()
}

// 方法 - 处理头像更改
const handleAvatarChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    // 实际应用中会上传文件到服务器
    const reader = new FileReader()
    reader.onload = (e) => {
      profileForm.avatar = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

// 方法 - 更新个人资料
const updateProfile = async () => {
  isUpdating.value = true
  
  try {
    // 实际应用中会调用API更新用户资料
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 显示成功通知
    useToast().add({
      title: '成功',
      description: '个人资料已更新',
      color: 'green'
    })
  } catch (error) {
    // 显示错误通知
    useToast().add({
      title: '错误',
      description: '更新个人资料失败',
      color: 'red'
    })
  } finally {
    isUpdating.value = false
  }
}

// 方法 - 更新密码
const updatePassword = async () => {
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    useToast().add({
      title: '错误',
      description: '两次输入的密码不一致',
      color: 'red'
    })
    return
  }
  
  isUpdatingPassword.value = true
  
  try {
    // 实际应用中会调用API更新密码
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 显示成功通知
    useToast().add({
      title: '成功',
      description: '密码已更新',
      color: 'green'
    })
    
    // 清空表单
    passwordForm.currentPassword = ''
    passwordForm.newPassword = ''
    passwordForm.confirmPassword = ''
  } catch (error) {
    // 显示错误通知
    useToast().add({
      title: '错误',
      description: '更新密码失败',
      color: 'red'
    })
  } finally {
    isUpdatingPassword.value = false
  }
}

// 方法 - 切换双因素认证
const toggleTwoFactor = () => {
  // 实际应用中会调用API切换双因素认证状态
  console.log('Two-factor authentication toggled:', twoFactorEnabled.value)
}

// 方法 - 保存偏好设置
const savePreferences = async () => {
  isSavingPreferences.value = true
  
  try {
    // 实际应用中会调用API保存偏好设置
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 显示成功通知
    useToast().add({
      title: '成功',
      description: '偏好设置已保存',
      color: 'green'
    })
  } catch (error) {
    // 显示错误通知
    useToast().add({
      title: '错误',
      description: '保存偏好设置失败',
      color: 'red'
    })
  } finally {
    isSavingPreferences.value = false
  }
}

// 方法 - 获取设备图标
const getDeviceIcon = (device) => {
  if (device.includes('Windows') || device.includes('PC')) return 'i-heroicons-computer-desktop'
  if (device.includes('iPhone') || device.includes('Android')) return 'i-heroicons-device-phone-mobile'
  if (device.includes('Mac') || device.includes('MacBook')) return 'i-heroicons-computer-desktop'
  return 'i-heroicons-device-phone-mobile'
}

// 方法 - 格式化日期
const formatDate = (date) => {
  return new Intl.DateTimeFormat('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}
</script>