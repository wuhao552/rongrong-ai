<template>
  <UCard
  :header-class="{ p: '4', 'border-b': '1', 'border-color': 'gray-200' }"
  :body-class="{ p: '0 4' }"
  :footer-class="{ p: '4', 'border-t': '1', 'border-color': 'gray-200' }"
  :id="`hot-list-${hotData.name}`"
  class="hot-list "
>
    <template #header>
      <UDivider class="title" :class="{ 'justify-between': true }">
        <div class="name">
          <UAvatar
            class="ico"
            :src="`/logo/${hotData.name}.png`"
            :alt-src="`/ico/icon_error.png`"
          />
          <USpan class="name-text">{{ hotData.label }}</USpan>
        </div>
        <USpan v-if="hotListData?.type" class="subtitle" :class="{ 'text-gray-500': true }">
          {{ hotListData.type }}
        </USpan>
        <USkeleton v-else width="60px" class="rounded-md" />
      </UDivider>
    </template>
    <UScrollArea class="news-list" ref="scrollbarRef">
      <Transition name="fade" mode="out-in" class="fixed-height-card">
        <div v-if="loadingError" class="error">
          <UResult
            size="sm"
            status="error"
            title="哎呀，加载失败了"
            description="生活总会遇到不如意的事情"
            style="mt-10"
          />
          <UButton
            size="sm"
            variant="ghost"
            color="gray"
            class="rounded-full"
            @click.stop="getHotListsData(hotData.name)"
          >
            <template #icon>
              <UIcon :name="Refresh" />
            </template>
            重试
          </UButton>
        </div>
        <div v-else-if="!hotListData || listLoading" class="loading">
          <USkeleton text class="rounded-md" :repeat="10" height="20px" />
        </div>
        <div v-else class="lists" :id="hotData.name + 'Lists'">
          <div
            class="item"
            v-for="(item, index) in hotListData.data.slice(0, 15)"
            :key="item"
          >
            <USpan
              class="num"
              :class="[
                index === 0 ? 'one' : index === 1 ? 'two' : index === 2 ? 'three' : '',
                'text-gray-700'
              ]"
            >
              {{ index + 1 }}
            </USpan>
            <USpan
              :class="['text', { 'text-lg': store.listFontSize > 16 }]"
              @click.stop="jumpLink(item)"
            >
              {{ item.title }}
            </USpan>
          </div>
        </div>
      </Transition>
    </UScrollArea>
    <template #footer>
      <Transition name="fade" mode="out-in">
        <div v-if="!hotListData" class="loading">
          <USkeleton text class="rounded-md" />
        </div>
        <div v-else class="message">
          <USpan class="time" :class="{ 'text-gray-500': true }" v-if="updateTime">
            {{ updateTime }}
          </USpan>
          <USpan class="time" :class="{ 'text-red-500': true }" v-else> 获取失败 </USpan>
          
        </div>
      </Transition>
    </template>
  </UCard>
</template>

<script setup>
import { Refresh, More } from "@icon-park/vue-next";
import { getHotLists } from "@/api";
import { formatTime } from "@/utils/getTime";
import { mainStore } from "~/store";
import { useRouter } from "vue-router";

const router = useRouter();
const store = mainStore();
const props = defineProps({
  // 热榜数据
  hotData: {
    type: Object,
    default: {},
  },
});

// 更新时间
const updateTime = ref(null);

// 刷新按钮数据
const lastClickTime = ref(
  localStorage.getItem(`${props.hotData.name}Btn`) || 0
);

// 热榜数据
const hotListData = ref(null);
const scrollbarRef = ref(null);
const listLoading = ref(false);
const loadingError = ref(false);

// 获取热榜数据
const getHotListsData = async (name, isNew = false) => {
  try {
    // hotListData.value = null;
    loadingError.value = false;
    const item = store.newsArr.find((item) => item.name == name);
    const result = await getHotLists(item.name, isNew, item.params);
    // console.log(result);
    if (result.code === 200) {
      listLoading.value = false;
      hotListData.value = result;
      // 滚动至顶部
      if (scrollbarRef.value) {
        scrollbarRef.value.scrollTo({ position: "top", behavior: "smooth" });
      }
    } else {
      loadingError.value = true;
      $message.error(result.title + result.message);
    }
  } catch (error) {
    loadingError.value = true;
    $message.error("热榜加载失败，请重试");
  }
};

// 获取最新数据
const getNewData = () => {
  const now = Date.now();
  if (now - lastClickTime.value > 60000) {
    // 点击事件
    listLoading.value = true;
    getHotListsData(props.hotData.name, true);
    // 更新最后一次点击时间
    lastClickTime.value = now;
    localStorage.setItem(`${props.hotData.name}Btn`, now);
  } else {
    // 不执行点击事件
    $message.info("请稍后再刷新");
  }
};

// 链接跳转
const jumpLink = (data) => {
  if (!data.url || !data.mobileUrl) return $message.error("链接不存在");
  const url = window.innerWidth > 680 ? data.url : data.mobileUrl;
  if (store.linkOpenType === "open") {
    window.open(url, "_blank");
  } else if (store.linkOpenType === "href") {
    window.location.href = url;
  }
};

// 前往全部列表
const toList = () => {
  if (props.hotData.name) {
    router.push({
      path: "/list",
      query: {
        type: props.hotData.name,
      },
    });
  } else {
    $message.error("数据出错，请重试");
  }
};

// 判断列表是否显示
const checkListShow = () => {
  const typeName = props.hotData.name;
  const listId = "hot-list-" + typeName;
  const listDom = document.getElementById(listId);
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        console.log(`👀 ${typeName} 可见，开始加载`);
        getHotListsData(props.hotData.name);
        observer.unobserve(entry.target);
      }
    });
  });
  observer.observe(listDom);
};

// 实时改变更新时间
watch(
  () => store.timeData,
  () => {
    if (hotListData.value) {
      updateTime.value = formatTime(hotListData.value.updateTime);
    }
  }
);

onMounted(() => {
  checkListShow();
});
</script>

<style lang="scss" scoped>
.fixed-height-card {
  height: 500px; /* 设置你想要的高度 */
  overflow: auto; /* 添加滚动条 */
}
/* 隐藏滚动条的方法（适用于现代浏览器） */
.fixed-height-card::-webkit-scrollbar {
  display: none; /* 隐藏滚动条 */
}
.hot-list {
  border-radius: 12px;
  transition: all 0.3s;
  cursor: pointer;
  .title {
    display: flex;
    align-items: center;
    font-size: 16px;
    height: 26px;
    .name {
      display: flex;
      align-items: center;
      
    }

    .subtitle {
      margin-left: auto;
      font-size: 12px;
    }
  }

  .message {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    font-size: 12px;
    height: 24px;

    .time {
      padding: 0 6px;
    }
  }

  :deep(.news-list) {
    height: 300px;

    .n-scrollbar-rail {
      right: 0;
    }

    .error {
      display: flex;
      flex-direction: column;
      align-items: center;
      .n-button {
        margin-top: 12px;
      }
    }

    .loading {
      display: flex;
      flex-direction: column;
      height: 300px;
      justify-content: space-between;
    }
  }

  .lists {
    padding-right: 6px;

    .item {
      display: flex;
      align-items: center;
      margin-bottom: 6px;
      padding-bottom: 2px;
      min-height: 30px;
      border-radius: 8px;
      transition: all 0.3s;
      cursor: pointer;

      &:nth-last-of-type(1) {
        margin-bottom: 0;
      }

      .num {
        width: 24px;
        height: 24px;
        min-width: 24px;
        margin-right: 8px;
        font-size: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: var(--n-border-color);
        border-radius: 8px;
        transition: all 0.3s;

        &:hover {
          background-color: var(--n-close-color-hover);
        }

        &.one {
          background-color: #ea444d;
          color: #fff;
        }

        &.two {
          background-color: #ed702d;
          color: #fff;
        }

        &.three {
          background-color: #eead3f;
          color: #fff;
        }
      }

      .text {
        position: relative;
        display: inline-block;
        width: 100%;
        transition: all 0.3s;

        @media (min-width: 768px) {
          &:hover {
            transform: translateX(4px);

            &::after {
              width: 90%;
            }
          }
        }

        @media (max-width: 768px) {
          &:active {
            color: #ea444d;
          }
        }

        &::after {
          content: "";
          width: 0;
          height: 2px;
          max-height: 2px;
          background-color: var(--n-close-color-pressed);
          position: absolute;
          left: 0;
          bottom: -2px;
          border-radius: 8px;
          transition: all 0.3s;
        }
      }
    }
  }

  :deep(.n-card-header) {
    .loading {
      height: 26px;
    }
  }

  :deep(.n-card__footer) {
    .loading {
      height: 24px;
    }
  }
}
</style>
