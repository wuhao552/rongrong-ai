<script setup lang="ts">
const route = useRoute()
const appConfig = useAppConfig()
const { isHelpSlideoverOpen } = useDashboard()

const links = [{
  id: 'home',
  label: '主页',
  icon: 'i-heroicons-home',
  to: '/',
  tooltip: {
    text: '主页',
    shortcuts: ['G', 'H']
  }
},  {
  id: 'aichat',
  label: '融融AI',
  icon: 'i-heroicons-chat-bubble-bottom-center-text',
  to: '/aichat',
  tooltip: {
    text: '融融AI',
    shortcuts: ['G', 'U']
  }
}, {
  id: 'agents',
  label: '个性化智能体',
  icon: 'i-heroicons-user-circle',
  to: '/agents',
  tooltip: {
    text: '个性化智能体',
    shortcuts: ['G', 'A']
  }
},{
  id: 'news',
  label: '新闻',
  icon: 'i-heroicons-newspaper',
  to: '/news',
  tooltip: {
    text: '新闻',
    shortcuts: ['G', 'T']
  }
}, {
  id: 'video',
  label: '视频',
  icon: 'i-heroicons-play',
  to: '/video',
  tooltip: {
    text: '视频',
    shortcuts: ['G', 'V']
  }
}, {
  id: 'settings',
  label: '设置',
  to: '/settings',
  icon: 'i-heroicons-cog-8-tooth',
  children: [{
    label: '常规',
    to: '/settings',
    exact: true
  },],
  tooltip: {
    text: '设置',
    shortcuts: ['G', 'S']
  }
}]


const groups = [{
  key: 'links',
  label: 'Go to',
  commands: links.map(link => ({ ...link, shortcuts: link.tooltip?.shortcuts }))
}]

</script>

<template>
  <UDashboardLayout>
    <UDashboardPanel
      :width="250"
      :resizable="{ min: 200, max: 300 }"
      collapsible
    >
      <UDashboardSidebar>
        <template #header>
          <UDashboardSearchButton />
        </template>
        <UDashboardSidebarLinks :links="links" />
        <div class="flex-1" />
      </UDashboardSidebar>
    </UDashboardPanel>
    <slot />

    <!-- ~/components/HelpSlideover.vue -->
    <HelpSlideover />
    

    <ClientOnly>
      <LazyUDashboardSearch :groups="groups" />
    </ClientOnly>
  </UDashboardLayout>
</template>
