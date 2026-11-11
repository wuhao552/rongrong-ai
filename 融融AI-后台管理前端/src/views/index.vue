<template>
  <div class="app-container home">
    <div class="home">
      <el-scrollbar style="height: calc(100vh - 190px)" wrap-style="overflow-x:hidden;">
    
      
      <!-- 显示对话历史 -->
      <div v-for="(message, index) in messages" :key="index" :class="['message', { 'user-message': message.isUser, 'ai-message': !message.isUser }]" class="message-wrap">
        <div class="message-content" v-html="message.text.replace(/\n/g, '<br>')">
      </div>
      
    </div>
    <div v-if="loading" class="message ai-message message-wrap">
          <div class="message-content">
            <div>
                <div class="sk-chase">
                    <div class="sk-chase-dot"></div>
                    <div class="sk-chase-dot"></div>
                    <div class="sk-chase-dot"></div>
                    <div class="sk-chase-dot"></div>
                    <div class="sk-chase-dot"></div>
                    <div class="sk-chase-dot"></div>
                </div>
            </div>
          </div>
      </div>
  </el-scrollbar>
    
    <!-- 输入框和发送按钮 -->
     <div class="right-input">
      <el-input placeholder="请输入消息..." v-model="inputMessage" @keyup.enter="sendMessage" class="input">
        </el-input>
      <el-button type="primary" @click="sendMessage">
        <img  class="up-load" src="@/assets/上传.png">
      </el-button>
    </div>
    
    </div>
  </div>
    
</template>

<script>
import axios from 'axios';

export default {
  name: "Index",
  data() {
    return {
      inputMessage: '', // 用户输入的消息
      messages: [
      { text: '你好！👋🏻我是融融AI的技术助手，有关后台数据库的任何问题，都欢迎向我咨询。期待与你沟通！', isUser: false, timestamp: new Date().toISOString() },
      ] // 对话历史记录
    };
  },
  filters: {
    formatTime(timestamp) {
      const date = new Date(timestamp);
      return `${date.getHours()}:${date.getMinutes()}`
    }
  },
  methods: {
    sendMessage() {
      
      
      if (this.inputMessage.trim() === '') return;
      
      this.messages.push({
        text: this.inputMessage,
        isUser: true
      });

      this.loading = true; // 开始加载

      axios.get('http://127.0.0.1:5000/llm/sql', {
        params: {
          query: this.inputMessage
        }
      })
      .then(response => {
        const answer = response.data; // 假设后端返回的是文本答案
        this.messages.push({
          text: answer,
          isUser: false
        });
        this.loading = false
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        this.loading = false; // 结束加载
      });

      this.inputMessage = ''; // 清空输入框
    }
  }
};
</script>

<style scoped lang="scss">
.home {
  font-family: "open sans", "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: 16px;
  color: #1c1c1c;
  overflow-x: hidden;

  .user-message {
    text-align: right;
    margin-bottom: 10px;
  }
  .input {
  width: 58%;
  margin-right: 5px;
}
.right-input {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 6.5%;

  position: relative;
}
.message {
  display: flex;
  margin-bottom: 10px;
}

.user-message {
  justify-content: flex-end;
}

.ai-message {
  justify-content: flex-start;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 10px;
  background-color: #f5f5f5;
}

.user-avatar {
  margin-right: 0;
  margin-left: 10px;
}

.message-content {
  padding: 12px;
  border-radius: 4px;
  max-width: 70%;
  white-space: pre-wrap;
}

.user-message .message-content {
  background-color: #f5f5f5;
  color: rgb(0, 0, 0);
}

.ai-message .message-content {
  background-color: #f5f5f5;
  color: black;
}

.timestamp {
  font-size: 12px;
  color: #999;
}
::v-deep .el-button {
  padding: 5px 6px;
}

::v-deep .el-input__inner {
  height: 52px;
  border-radius: 15px;
  border: 1px solid #DCDFE6;
}

::v-deep .el-button--primary {
  position: relative;
  right: 3.5%;
  background-color: rgba(180, 180, 180, 0.3) !important;
  color: black !important;
  border-color: rgba(180, 180, 180, 0.3) !important;
}
.loading-message {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 10px;
  background-color: #eee;
  color: #666;
}
.sk-chase {
	  width: 20px;
	  height: 20px;
	  position: relative;
	  animation: sk-chase 2.5s infinite linear both;
	}
	
	.sk-chase-dot {
	  width: 100%;
	  height: 100%;
	  position: absolute;
	  left: 0;
	  top: 0; 
	  animation: sk-chase-dot 2.0s infinite ease-in-out both; 
	}
	
	.sk-chase-dot:before {
	  content: '';
	  display: block;
	  width: 25%;
	  height: 25%;
	  background-color: #11A983;
	  border-radius: 100%;
	  animation: sk-chase-dot-before 2.0s infinite ease-in-out both; 
	}
	
	.sk-chase-dot:nth-child(1) { animation-delay: -1.1s; }
	.sk-chase-dot:nth-child(2) { animation-delay: -1.0s; }
	.sk-chase-dot:nth-child(3) { animation-delay: -0.9s; }
	.sk-chase-dot:nth-child(4) { animation-delay: -0.8s; }
	.sk-chase-dot:nth-child(5) { animation-delay: -0.7s; }
	.sk-chase-dot:nth-child(6) { animation-delay: -0.6s; }
	.sk-chase-dot:nth-child(1):before { animation-delay: -1.1s; }
	.sk-chase-dot:nth-child(2):before { animation-delay: -1.0s; }
	.sk-chase-dot:nth-child(3):before { animation-delay: -0.9s; }
	.sk-chase-dot:nth-child(4):before { animation-delay: -0.8s; }
	.sk-chase-dot:nth-child(5):before { animation-delay: -0.7s; }
	.sk-chase-dot:nth-child(6):before { animation-delay: -0.6s; }
	
	@keyframes sk-chase {
	  100% { transform: rotate(360deg); } 
	}
	
	@keyframes sk-chase-dot {
	  80%, 100% { transform: rotate(360deg); } 
	}
	
	@keyframes sk-chase-dot-before {
	  50% {
	    transform: scale(0.4); 
	  } 100%, 0% {
	    transform: scale(1.0); 
	  } 
	}

}
</style>