<!-- components/TradingViewScreener.vue -->
<template>
  <div class="tradingview-widget-container">
    <div ref="widgetContainer" class="tradingview-widget-container__widget"></div>
    <div class="tradingview-widget-copyright">
      <a 
        href="https://cn.tradingview.com/screener/" 
        rel="noopener nofollow" 
        target="_blank"
      >
      </a>
    </div>
  </div>
</template>

<script>
export default {
  mounted() {
    // 仅在客户端执行
    if (process.client) {
      this.loadTradingViewWidget();
    }
  },
  
  methods: {
    loadTradingViewWidget() {
      // 防止重复加载
      if (document.getElementById('tradingview-screener-script')) return;
      
      const script = document.createElement('script');
      script.id = 'tradingview-screener-script';
      script.type = 'text/javascript';
      script.src = 'https://s3.tradingview.com/external-embedding/embed-widget-screener.js';
      script.async = true;
      
      // 配置参数（JSON 格式）
      script.innerHTML = JSON.stringify({
        "market": "china",
        "showToolbar": true,
        "defaultColumn": "overview",
        "defaultScreen": "most_capitalized",
        "isTransparent": false,
        "locale": "zh_CN",
        "colorTheme": "light",
        "width": "100%",
        "height": 550
      });
      
      // 确保容器存在后再添加脚本
      this.$nextTick(() => {
        if (this.$refs.widgetContainer) {
          this.$refs.widgetContainer.appendChild(script);
        }
      });
    }
  },
  
  beforeDestroy() {
    // 组件销毁时清理脚本
    if (process.client) {
      const script = document.getElementById('tradingview-screener-script');
      if (script && script.parentNode) {
        script.parentNode.removeChild(script);
      }
      // 清空容器内容
      if (this.$refs.widgetContainer) {
        this.$refs.widgetContainer.innerHTML = '';
      }
    }
  }
}
</script>

<style scoped>
.tradingview-widget-container {
  height: 550px;
  width: 100%;
}
.tradingview-widget-copyright {
  margin-top: 8px;
  text-align: center;
}
.blue-text {
  color: #2962ff;
}
</style>