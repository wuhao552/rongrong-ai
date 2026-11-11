<template>
  <div class="container mx-auto p-4">

    <!-- 加载状态 -->
    <div v-if="loading" class="flex items-center justify-center h-64">
      <p class="text-gray-600">正在加载...</p>
    </div>

    <!-- 智能体列表 -->
    <ul v-else-if="agents && agents.length" class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
      <li v-for="agent in agents" :key="agent.agentId" class="bg-white rounded-lg shadow-lg overflow-hidden transition-transform transform hover:scale-105 duration-300">
        <NuxtLink :to="{
          path: `/agent_detail/${encodeURIComponent(agent.agentId)}`,
          query: {
            configInfo: encodeURIComponent(agent.configInfo),
            name: encodeURIComponent(agent.name)
          }
        }" class="block">
          <div class="relative">
            <img :src="agent.icon" :alt="agent.name" class="w-24 h-24 rounded-full mx-auto mt-4 border-2 border-indigo-500" />
            <div class="absolute inset-x-0 bottom-0 bg-gradient-to-t from-gray-900 to-transparent opacity-75"></div>
          </div>
          <div class="p-4 text-center">
            <h2 class="text-xl font-semibold mb-2">{{ agent.name }}</h2>
            <p class="text-sm text-gray-500">{{ new Date(agent.creationTime).toLocaleDateString() }}</p>
          </div>
        </NuxtLink>
      </li>

      <!-- 新增智能体按钮 -->
      <li class="add-agent bg-white rounded-lg overflow-hidden flex items-center justify-center cursor-pointer" @click="toggleAddAgentForm">
        <span class="text-4xl">+</span>
      </li>
    </ul>

    <!-- 没有智能体或错误信息 -->
    <p v-else class="text-center text-red-500 mt-8">
      {{ error ? '加载智能体失败，请稍后再试。' : '没有找到任何智能体。' }}
    </p>

    <!-- 添加智能体的表单 -->
    <div v-if="showAddAgentForm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-10">
      <div class="bg-white p-6 rounded-lg w-96 max-w-md">
        <h2 class="text-xl font-bold mb-4 text-center">添加新智能体</h2>
        <form @submit.prevent="addAgent">
          <div class="mb-4">
            <label for="name" class="block text-sm font-medium text-gray-700">名称</label>
            <input v-model="newAgent.name" id="name" type="text" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
          </div>
          <div class="mb-4">
            <label for="icon" class="block text-sm font-medium text-gray-700">图标URL</label>
            <input v-model="newAgent.icon" id="icon" type="text" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
          </div>
          <div class="mb-4">
            <label for="introduction" class="block text-sm font-medium text-gray-700">简介</label>
            <textarea v-model="newAgent.introduction" id="introduction" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"></textarea>
          </div>
          <div class="mb-4">
            <label for="configInfo" class="block text-sm font-medium text-gray-700">提示词内容</label>
            <textarea v-model="newAgent.configInfo" id="configInfo" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"></textarea>
          </div>
          <button type="submit" class="w-full bg-blue-500 text-white py-2 px-4 rounded-md shadow-sm hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">确认</button>
        </form>
        <button @click="toggleAddAgentForm" class="mt-4 w-full bg-gray-500 text-white py-2 px-4 rounded-md shadow-sm hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500">取消</button>
        
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useFetch } from '#app'

const agents = ref([])
const loading = ref(true)
const error = ref(null)
const showAddAgentForm = ref(false)
const newAgent = ref({
  name: '',
  icon: '',
  introduction: '',
  configInfo: ''
})

onMounted(async () => {
  try {
    const { data } = await useFetch('http://127.0.0.1:9090/llm/agents/list', {
      method: 'GET',
      key: '/llm/agents/list', // 使用缓存键
    })

    if (data.value && data.value.code === 200) {
      agents.value = data.value.rows
    }
  } catch (err) {
    error.value = err
  } finally {
    loading.value = false
  }
})

// 切换显示/隐藏添加智能体的表单
const toggleAddAgentForm = () => {
  showAddAgentForm.value = !showAddAgentForm.value
}

// 提交新增智能体
const addAgent = async () => {
  try {
    const response = await fetch('http://127.0.0.1:9090/llm/agents', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        ...newAgent.value,
        network: 1,
        userId: 1
      })
    })

    if (response.ok) {
      // 如果请求成功，刷新智能体列表
      await loadAgents()
      toggleAddAgentForm() // 关闭表单
      // 清空表单数据
      Object.assign(newAgent.value, {
        name: '',
        icon: '',
        introduction: '',
        configInfo: ''
      })
    } else {
      console.error('Failed to add the agent.')
    }
  } catch (err) {
    console.error('Error:', err)
  }
}

// 加载智能体列表
const loadAgents = async () => {
  try {
    loading.value = true
    const { data } = await useFetch('http://127.0.0.1:9090/llm/agents/list', {
      method: 'GET',
      key: '/llm/agents/list', // 使用缓存键
    })

    if (data.value && data.value.code === 200) {
      agents.value = data.value.rows
    }
  } catch (err) {
    error.value = err
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.add-agent {
  /* 确保新增智能体按钮的大小与其它列表项一致 */
  height: 100%;
  min-height: 100%; /* 对于某些浏览器可能需要 */
  padding: 1rem; /* 根据其他项目的内边距进行调整 */
}

.add-agent span {
  /* 加号的颜色，可以根据设计需求调整 */
  color: #000; /* 黑色 */
  /* 调整加号的大小，根据需要调整 */
  font-size: 140px; /* 例如：3rem 或者 48px */
  line-height: 1; /* 确保加号垂直居中 */
  /* 如果需要，可以设置一个过渡效果 */
  transition: font-size 0.3s ease;
}

/* 当鼠标悬停时，可以放大加号 */
.add-agent:hover span {
  font-size: 150px; /* 或者更大的尺寸 */
}
</style>