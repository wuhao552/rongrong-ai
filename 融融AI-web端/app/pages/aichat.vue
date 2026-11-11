<template>
  <UDashboardPage>
    <UDashboardPanel grow>
      <keep-alive>
      <div class="home">
    <div class="home-right">
      <div class="right-version">
        <div class="llm-chat-demo">
          <span class="chat-demo">融融AI</span>
        </div>
      </div>
      <div class="right-body" :class="messages.length === 0 ? 'nodata' : ''" ref="messageContainer">
        <div v-for="(message, index) in messages" class="main-message" :key="index"
             :class="{'用户-message': message.sender === '用户', '融融AI-message': message.sender === '融融AI'}">
          <!-- 显示用户标识和图片 -->
          <div class="message-sender"
               :class="{'用户-message': message.sender === '用户', '融融AI-message': message.sender === '融融AI'}">
            <span class="message-sender-name"
                  :class="message.sender === '用户' ? '用户-color' : '融融AI-color'">{{ message.sender }}:</span>
          </div>
          <div v-if="message.sender === '用户'" class="用户-message">{{ message.content }}</div>
          <div v-else class="融融AI-message" v-html="message.content"></div>
        </div>
      </div>
      <div class="right-input" @keyup.enter="handleSearch">
        <!-- 输入框 -->
        <el-input v-model="queryKeyword" placeholder="给融融AI发送消息" class="input"></el-input>
        <!-- 查询按钮 -->
        <el-button v-if="!loading" type="primary" @click="handleSearch">
          <img  class="up-load" src="@/assets/上传.png">
        </el-button>
        <el-button v-if="loading" type="primary" @click="closeEventSource">
          <img  class="up-load" src="@/assets/等待.png" >
        </el-button>
      </div>
      <div class="sec-notice">服务生成的所有内容均由人工智能模型生成，其生成内容的准确性和完整性无法保证</div>
    </div>
  </div>
</keep-alive>
    </UDashboardPanel>
  </UDashboardPage>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import MarkdownIt from 'markdown-it';
import markdownItFootnote from 'markdown-it-footnote';
import markdownItTaskLists from 'markdown-it-task-lists';
import markdownItAbbr from 'markdown-it-abbr';
import markdownItContainer from 'markdown-it-container';
import hljs from 'highlight.js';
import markdownItHighlightjs from 'markdown-it-highlightjs';

const queryKeyword = ref('');
const messages = ref([]);
const loading = ref(false);
const eventSource = ref(null);

const md = new MarkdownIt()
  .use(markdownItFootnote)
  .use(markdownItTaskLists, { enabled: true })
  .use(markdownItAbbr)
  .use(markdownItContainer, 'warning')
  .use(markdownItHighlightjs, { hljs });

function handleSearch() {
  if (loading.value) {
    return;
  }

  const keyword = queryKeyword.value;
  loading.value = true;

  messages.value.push({ content: keyword, sender: '用户' });

  nextTick(() => {
    scrollToBottom();
  });

  eventSource.value = new EventSource("http://127.0.0.1:5000/llm/ask_finance?question="+keyword);

  eventSource.value.onmessage = (event) => {
    const dataObject = JSON.parse(event.data);

    if (dataObject.message === 'done') {
      eventSource.value.close();
      loading.value = false;
    } else {
      const lastMessage = messages.value[messages.value.length - 1];
      if (lastMessage.sender === '融融AI') {
        lastMessage.orgcontent += dataObject.message;
        lastMessage.orgcontent = lastMessage.orgcontent.replace(/\*\*\s*([^*]*?)\s*(:\s*)?\*\*/g, '**$1$2**');
        lastMessage.content = md.render(lastMessage.orgcontent);
      }
      scrollToBottom();
    }
  };

  messages.value.push({ orgcontent: '', content: '', sender: '融融AI' });
  queryKeyword.value = '';
  eventSource.value.onerror = (error) => {
    console.error('EventSource failed:', error);
    eventSource.value.close();
  };
}

function closeEventSource() {
  loading.value = false;
  if (eventSource.value) {
    eventSource.value.close();
  }
}

function scrollToBottom() {
  const messageContainer = document.querySelector('.right-body');
  if (messageContainer) {
    messageContainer.scrollTop = messageContainer.scrollHeight;
  }
}

onUnmounted(() => {
  if (eventSource.value) {
    eventSource.value.close();
  }
});
</script>

<style scoped>
.home {
  height: 100%;
  display: flex;
}

.home-right {
  width: 100%;
}

.right-version {
  /* //width: 60%; */
  margin: auto;
  /* //background-color: #F9FFD8; */
  height: 5%;
  display: flex;
  justify-content: start;
  align-items: center;
  border-radius: 15px;
  margin-bottom: 12px;
}

.version {
  color: rgb(155, 155, 155);
}

.llm-chat-demo {
  width: 58%;
  margin: auto;
  /* //margin-left: 20px;
  //font-family: "黑体", "SimHei", sans-serif; */
  font-family: Söhne, ui-sans-serif, system;
  font-variation-settings: normal;
  font-weight: 550;
  font-size: 18px;
  cursor: pointer;
  color-scheme: light;
}

.chat-demo {
  opacity: 0.65; /* 设置透明度为 0.7，您可以根据需要调整这个值 */
}

.right-body {
  height: 85%;
  overflow-y: auto;
}

.main-message {
  margin: auto;
  width: 58%;
  justify-content: center;
}

.message-sender-name {
  margin-left: 10px;
  /* font-family: "黑体", "SimHei", sans-serif; */
  font-family: Söhne, ui-sans-serif, system;
  font-weight: 550;
  font-size: 18px;
}

.right-input {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 6.5%;

  position: relative;
}

.sec-notice {
  height: 3.5%;
  font-size: 12px;
  font-family: Söhne, ui-sans-serif;
  color: rgb(155, 155, 155);
  display: flex;
  justify-content: center;
}

.input {
  width: 58%;
  margin-right: 5px;
}


:deep(.el-button) {
  padding: 5px 6px;
}

:deep(.el-input__inner) {
  height: 52px;
}

:deep(.el-button--primary) {
  position: relative;
  right: 48px;
  background-color: rgba(180, 180, 180, 0.3) !important;
  color: black !important;
  border-color: rgba(180, 180, 180, 0.3) !important;
}

.用户-message {
  text-align: left;
  padding: 5px;
  margin-bottom: 5px;
  border-radius: 15px;

}

.融融AI-message {
  text-align: left;
  padding: 5px;
  margin-bottom: 5px;
}

:deep(.融融AI-message pre .hljs) {
  border-radius: 10px !important; /* 圆角 */
  background-color: #FAF7F7; /* 例子中的背景色 */
}

/* 设置滚动条的样式 */
::-webkit-scrollbar {
  width: 6px; /* 设置滚动条宽度 */
}

/* 设置滚动条轨道的样式 */
::-webkit-scrollbar-track {
  background: #f1f1f1; /* 设置滚动条轨道的背景色 */
}

/* 设置滚动条滑块的样式 */
::-webkit-scrollbar-thumb {
  background: #888; /* 设置滚动条滑块的背景色 */
  border-radius: 3px; /* 设置滚动条滑块的圆角 */
}

/* 鼠标悬停时滚动条滑块的样式 */
::-webkit-scrollbar-thumb:hover {
  background: #555; /* 设置鼠标悬停时滚动条滑块的背景色 */
}
</style>
