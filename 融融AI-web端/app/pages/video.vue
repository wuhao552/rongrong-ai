<template>
  <div class="container mx-auto p-4">

    <!-- 加载状态 -->
    <div v-if="loading" class="text-center mt-8">
      <p class="text-gray-600">正在加载...</p>
    </div>
    
    <!-- 视频列表 -->
    <ul v-else-if="videos && videos.length" class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <li v-for="video in videos" :key="video.id" class="bg-white rounded-lg shadow-lg overflow-hidden transition-transform transform hover:scale-105 duration-300">
        <NuxtLink :to="`/video_detail/${video.id}`" class="block">
          <img :src="video.imageUrl" :alt="video.title" class="w-full h-48 object-cover" referrerpolicy="no-referrer"/>
          <div class="p-4">
            <h2 class="text-xl font-semibold mb-2">{{ video.title }}</h2>
            <p v-html="video.description" class="text-sm text-gray-500"></p>
          </div>
        </NuxtLink>
      </li>
    </ul>

    <!-- 没有视频或错误信息 -->
    <p v-else class="text-center text-red-500 mt-8">
      {{ error ? '加载视频失败，请稍后再试。' : '没有找到任何视频。' }}
    </p>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useFetch } from '#app'

const videos = ref([])

onMounted(async () => {
  const { data } = await useFetch('http://127.0.0.1:9090/media/video/list', {
    method: 'GET',
    key: '/media/video/list', // 使用缓存键
  })

  if (data.value && data.value.code === 200) {
    videos.value = data.value.rows
  }
})
</script>

<style scoped>
.video-list ul {
  list-style-type: none;
  padding: 0;
}

.video-list li {
  margin-bottom: 20px;
}

.video-list img {
  width: 100%;
  height: auto;
}

.video-list h2 {
  font-size: 1.5em;
  margin-top: 10px;
}

.video-list p {
  font-size: 1em;
  color: #555;
}
</style>