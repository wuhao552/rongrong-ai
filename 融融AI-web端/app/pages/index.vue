<script setup lang="ts">
import { sub } from 'date-fns'
import type { Period, Range } from '~/types'

const { isNotificationsSlideoverOpen } = useDashboard()

const range = ref<Range>({ start: sub(new Date(), { days: 14 }), end: new Date() })
const period = ref<Period>('daily')
</script>

<template>
  <UDashboardPage>
    <UDashboardPanel grow>
      <UDashboardNavbar title="主页">
      </UDashboardNavbar>
      <UDashboardPanelContent>
        <div class="mt-1">
          <HomeAI/>
        </div>
        
        <div class="mt-5">
          <HomeStock/>
        </div>
        <div class="mt-5">
          <HomeScreener/>
        </div>
        <!-- <div class="grid lg:grid-cols-2 lg:items-start gap-8 mt-8"> -->
          <!-- ~/components/home/HomeSales.vue -->
          <!-- <HomeSales /> -->
          <!-- ~/components/home/HomeCountries.vue -->
          <!-- <HomeCountries /> -->
        <!-- </div> -->
      </UDashboardPanelContent>
    </UDashboardPanel>
  </UDashboardPage>
</template>
