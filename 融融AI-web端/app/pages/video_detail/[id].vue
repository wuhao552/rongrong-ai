<template>
  <div class="video-detail-page max-w-6xl mx-auto p-4 sm:p-6 lg:p-8">
    <!-- 标题 -->
    <h1 class="text-3xl font-bold text-gray-900 mb-4">{{ video.title }}</h1>

    <!-- 视频和AI总结区域 -->
    <div class="grid grid-cols-1 md:grid-cols-[7fr_3fr] gap-4 md:gap-6">
      <!-- 视频 -->
      <div class="left-section relative rounded-lg overflow-hidden shadow-md mb-4 md:mb-0">
        <iframe
          :src="video.realUrl"
          allowfullscreen
          frameborder="0"
          class="w-full aspect-[16/9] min-h-[300px] md:min-h-[400px] lg:min-h-[500px]"
        ></iframe>
      </div>

      <!-- AI总结 -->
      <div class="right-section space-y-4">
        <h2 class="text-2xl font-semibold text-gray-800">AI总结</h2>
        <div class="right-body h-[450px] overflow-y-auto" :class="messages.length === 0 ? 'nodata' : ''" ref="messageContainer">
          <div
            v-for="(message, index) in messages"
            class="main-message"
            :key="index"
            :class="{'用户-message': message.sender === '用户', '融融AI-message': message.sender === '融融AI'}"
          >
            <div v-if="message.sender === '融融AI'" class="融融AI-message" v-html="message.content"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 视频描述 -->

    <p v-html="video.description" class="text-gray-700 mt-6"></p>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useFetch } from '#app'
import { useRoute } from '#app'
import MarkdownIt from 'markdown-it'
import markdownItFootnote from 'markdown-it-footnote'
import markdownItTaskLists from 'markdown-it-task-lists'
import markdownItAbbr from 'markdown-it-abbr'
import markdownItContainer from 'markdown-it-container'
import hljs from 'highlight.js'
import markdownItHighlightjs from 'markdown-it-highlightjs'

// 获取动态路由中的 ID
const route = useRoute()
const id = route.params.id

// 定义响应式变量
const video = ref({})
const messages = ref([])
const queryKeyword = ref('近期我国股市的总体趋势如何？');
const loading = ref(false)
const eventSource = ref(null)
const videoUrl = ref(null)
// 初始化Markdown解析器
const md = new MarkdownIt()
  .use(markdownItFootnote)
  .use(markdownItTaskLists, { enabled: true })
  .use(markdownItAbbr)
  .use(markdownItContainer, 'warning')
  .use(markdownItHighlightjs, { hljs })

// 加载视频数据
async function fetchVideoData() {
  const { data } = await useFetch(`http://127.0.0.1:9090/media/video/${id}`, {
    server: false,
    key: `/media/video/${id}`,
  })
  if (data.value && data.value.code === 200) {
    video.value = data.value.data
    videoUrl.value = data.value.data.videoUrl
    console.log("111"+videoUrl.value)
  }
}

// 搜索处理函数
function handleSearch() {
  if (loading.value) return

  const keyword = queryKeyword.value
  loading.value = true

  messages.value.push({ content: keyword, sender: '用户' })

  nextTick(() => {
    scrollToBottom()
  })

  eventSource.value = new EventSource(
    `http://127.0.0.1:5000/bilibili_video?url=`+`${videoUrl.value}`
  )

  eventSource.value.onmessage = (event) => {
    const dataObject = JSON.parse(event.data)

    if (dataObject.message === 'done') {
      eventSource.value.close()
      loading.value = false
    } else {
      const lastMessage = messages.value[messages.value.length - 1]
      if (lastMessage.sender === '融融AI') {
        lastMessage.orgcontent += dataObject.message
        lastMessage.orgcontent = lastMessage.orgcontent.replace(/\*\*\s*([^*]*?)\s*(:\s*)?\*\*/g, '**$1$2**')
        lastMessage.content = md.render(lastMessage.orgcontent)
      }
      scrollToBottom()
    }
  }

  messages.value.push({ orgcontent: '', content: '', sender: '融融AI' })
  queryKeyword.value = ''

  eventSource.value.onerror = (error) => {
    console.error('EventSource failed:', error)
    eventSource.value.close()
  }
}

function scrollToBottom() {
  const messageContainer = document.querySelector('.right-body')
  if (messageContainer) {
    messageContainer.scrollTop = messageContainer.scrollHeight
  }
}

// 在挂载时执行的逻辑
onMounted(async () => {
  await fetchVideoData() // 加载视频数据
  handleSearch() // 页面加载时自动请求
})
</script>