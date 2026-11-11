<template>

  <div class="tradingview-widget-container" ref="container" style="height: 500px; width: 100%;">
    <div class="tradingview-widget-container__widget" style="height: calc(500px - 32px); width: 100%;"></div>
    <div class="tradingview-widget-copyright">
    </div>
  </div>

  
</template>

<script>
export default {
  name: 'TradingViewWidget',
  mounted() {
    this.loadTradingViewScript();
  },
  methods: {
    loadTradingViewScript() {
      const script = document.createElement('script');
      script.src = 'https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js';
      script.type = 'text/javascript';
      script.async = true;
      script.innerHTML = `
        {
          "height": 500,
          "autosize": true,
          "symbol": "SSE:000001",
          "interval": "D",
          "timezone": "Asia/Shanghai",
          "theme": "light",
          "style": "1",
          "locale": "zh_CN",
          "allow_symbol_change": true,
          "calendar": false,
          "support_host": "https://www.tradingview.com"
        }`;
      this.$refs.container.appendChild(script);
    }
  }
}
</script>

<style scoped>
/* 根据需要添加样式 */
</style>