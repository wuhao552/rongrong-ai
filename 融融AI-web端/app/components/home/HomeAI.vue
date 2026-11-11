<template>
  <UDashboardCard
    title="融融AI"
    description="你的智能投资助手"
    icon="i-heroicons-chart-bar-20-solid"
  >
  <keep-alive>
  
    <div class="home">
        <div class="home-right">
          <div class="right-version">
          </div>
          <div class="right-body" :class="messages.length === 0 ? 'nodata' : ''" ref="messageContainer">
            <div v-for="(message, index) in messages" class="main-message" :key="index"
                 :class="{'用户-message': message.sender === '用户', '融融AI-message': message.sender === '融融AI'}">
              <div v-if="message.sender === '融融AI'" class="融融AI-message" v-html="message.content"></div>
            </div>
          </div>
        </div>
      </div>
  
</keep-alive>
 </UDashboardCard>
</template>


<script setup>
import { ref, onMounted, nextTick } from 'vue';
import MarkdownIt from 'markdown-it';
import markdownItFootnote from 'markdown-it-footnote';
import markdownItTaskLists from 'markdown-it-task-lists';
import markdownItAbbr from 'markdown-it-abbr';
import markdownItContainer from 'markdown-it-container';
import hljs from 'highlight.js';
import markdownItHighlightjs from 'markdown-it-highlightjs';

const queryKeyword = ref('近期我国股市的总体趋势如何？');
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

  eventSource.value = new EventSource("http://127.0.0.1:5000/Getprompt?query="+keyword+
  "&prompt="+
  `你是智能投资助手融融AI,能够快速捕捉市场动态，为用户提供精准的市场分析。你的能力有:实时监测市场变化;提取关键数据和信息;结合趋势进行简要分析;以简洁明了的方式呈现结果;请结合最新数据;
  注意不用添加任何前缀，直接输出内容。
`
  +"&network="+1); 

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

function scrollToBottom() {
  const messageContainer = document.querySelector('.right-body');
  if (messageContainer) {
    messageContainer.scrollTop = messageContainer.scrollHeight;
  }
}

onMounted(() => {
  handleSearch(); // 页面加载时自动请求
});
</script>
