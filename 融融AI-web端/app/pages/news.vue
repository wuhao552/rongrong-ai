<template>
  <UDashboardPage>
    <UDashboardPanel grow>
      <Header :class="headerShow ? 'show' : null" />
  <main>
    
    <!-- Home Page Content -->
    <div class="mt-1">
    <div class="home">
      <div v-if="store.newsArr[0] && store.newsArr.filter((item) => item.show)[0]" class="grid-container">
        <div
          class="news-card"
          v-for="(item, index) in store.newsArr.filter((item) => item.show)"
          :key="item"
          :style="{ animationDelay: index / 10 + 0.2 + 's' }"
        >
          <HotList :hotData="item" />
        </div>
      </div>
    </div>
    </div>
    <Footer />
  </main>
 
    </UDashboardPanel>
    </UDashboardPage>
  
</template>

<script setup>
import { mainStore } from "~/store";
import Header from "@/components/Header.vue";
import HotList from "@/components/HotList.vue";
import Footer from "@/components/Footer.vue";
const store = mainStore();

// 顶栏显隐
const headerShow = ref(false);

onMounted(() => {
  store.checkNewsUpdate();
  // 写入默认
  nextTick(() => {
    if (store.newsArr.length === 0) {
      store.newsArr = store.defaultNewsArr;
    }
  });
});

// 重置功能
const reset = () => {
  $dialog.warning({
    title: "重置站点",
    content:
      "确认重置站点？你的自定义数据将会恢复为默认状态！（当设置页面能正常进入并显示时请不要执行此操作！）",
    positiveText: "重置",
    negativeText: "取消",
    onPositiveClick: () => {
      if ($timeInterval) clearInterval($timeInterval);
      localStorage.clear();
      location.reload();
    },
  });
};
</script>

<style lang="scss" scoped>
/* app.vue 的样式 */
.home {
  .grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 24px;
  }
  .news-card {
    opacity: 0;
    transform: translateY(20px);
    animation-timing-function: cubic-bezier(0.42, 0, 0.58, 1);
    animation: cardShow 0.3s forwards ease-in-out;
  }
  .tip {
    font-size: 22px;
  }
}

// 出现动画
@keyframes cardShow {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

main {
  padding: 0 5vw;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  min-height: calc(100vh - 238px);
  overflow-y: auto; /* 添加垂直滚动条 */
}
/* 隐藏滚动条的方法（适用于现代浏览器） */
main::-webkit-scrollbar {
  display: none; /* 隐藏滚动条 */
}
</style>