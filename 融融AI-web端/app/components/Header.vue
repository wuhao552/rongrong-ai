<template>
  <header class="header">
    <section>
      <div class="current-time" v-if="store.timeData">
        <span class="time">{{ store.timeData.time.text }}</span>
        <span class="date">
          {{
            store.timeData.lunar.GanZhiYear +
            "年 " +
            store.timeData.lunar.text +
            " " +
            store.timeData.time.weekday
          }}
        </span>
      </div>
      <div class="current-time" v-else>
        <span class="time">时间获取中</span>
      </div>
      <div class="controls">
        <div class="button-group">
          <button v-if="showRefresh" @click="router.go(0)">
            <svg class="icon-refresh" viewBox="0 0 24 24">
              <path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c4.41 0 7.99-3.58 7.99-8 0-.53-.07-1.04-.2-1.54L13 14l6-6z"/>
            </svg>
            刷新页面
          </button>
          
        </div>
      </div>
      <div class="mobile">
        <button @click="showMenu = !showMenu">
          <svg class="icon-hamburger" viewBox="0 0 24 24">
            <path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/>
          </svg>
        </button>
        <div v-if="showMenu" class="dropdown-menu">
          <div class="time">
            <span>{{ store.timeData ? store.timeData.time.text : "时间获取失败" }}</span>
            <span class="date" v-if="store.timeData">
              {{
                store.timeData.lunar.GanZhiYear +
                "年 " +
                store.timeData.lunar.text +
                " " +
                store.timeData.time.weekday
              }}
            </span>
          </div>
          <hr />
          <button @click="router.go(0)">刷新页面</button>
          <button @click="store.setSiteTheme(store.siteTheme === 'light' ? 'dark' : 'light')">
            {{ store.siteTheme === "light" ? "深色模式" : "浅色模式" }}
          </button>
          <button @click="router.push('/setting')">全局设置</button>
        </div>
      </div>
    </section>
  </header>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from "vue";
import { mainStore } from "~/store";
import { useRouter } from "vue-router";
import { getCurrentTime } from "@/utils/getTime.js";

const router = useRouter();
const store = mainStore();
const timeInterval = ref(null);
const showRefresh = ref(false);
const showMenu = ref(false);

// 监听路由参数变化
watch(
  () => router.currentRoute.value,
  (val) => {
    const isHome = val.path === "/";
    showRefresh.value = isHome ? true : false;
  }
);

onMounted(() => {
  window.$timeInterval = timeInterval.value = setInterval(() => {
    store.timeData = getCurrentTime();
  }, 1000);
  showRefresh.value = router.currentRoute.value?.path === "/" ? true : false;
});

onBeforeUnmount(() => {
  clearInterval(timeInterval.value);
});
</script>

<style lang="scss" scoped>
.header {
  height: 118px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 24px 5vw;
  z-index: 2;
  top: 0;
  background-color: transparent;
  transition: all 0.3s;
  section {
    width: 100%;
    max-width: 1800px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    align-items: center;
    justify-content: space-between;
    .logo {
      display: flex;
      flex-direction: row;
      align-items: center;
      cursor: pointer;
      img {
        width: 50px;
        height: 50px;
        margin-right: 16px;
        transition: all 0.3s;
      }
      .name {
        display: flex;
        flex-direction: column;
        span {
          &:nth-of-type(1) {
            font-size: 20px;
            font-weight: bold;
            transition: all 0.3s;
          }
          &:nth-of-type(2) {
            font-size: 12px;
          }
        }
      }
    }
    .current-time {
      display: flex;
      flex-direction: column;
      align-items: center;
      .date {
        font-size: 12px;
      }
    }
    .controls {
      .button-group {
        display: flex;
        gap: 10px;
        button {
          background-color: transparent;
          border: none;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 5px;
          svg {
            width: 20px;
            height: 20px;
            fill: currentColor;
          }
        }
      }
    }
    .mobile {
      display: none;
      .dropdown-menu {
        position: absolute;
        top: 100%;
        right: 0;
        background-color: white;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        padding: 10px;
        border-radius: 5px;
        button {
          display: block;
          width: 100%;
          text-align: left;
          padding: 10px 0;
          border: none;
          background: none;
          cursor: pointer;
        }
        hr {
          border: none;
          border-top: 1px solid #ddd;
          margin: 10px 0;
        }
      }
    }
    @media (max-width: 768px) {
      display: flex;
      .logo {
        img {
          width: 40px;
          height: 40px;
        }
        .name {
          span {
            &:nth-of-type(1) {
              font-size: 18px;
            }
          }
        }
      }
      .current-time,
      .controls {
        display: none;
      }
      .mobile {
        display: block;
      }
    }
  }
}
</style>