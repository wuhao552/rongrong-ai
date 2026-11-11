"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
// https://nuxt.com/docs/api/configuration/nuxt-config
exports.default = defineNuxtConfig({
    extends: ['@nuxt/ui-pro'],
    modules: [
        '@nuxt/eslint',
        '@nuxt/ui',
        '@vueuse/nuxt',
        '@element-plus/nuxt',
        "@pinia/nuxt",
        "@pinia-plugin-persistedstate/nuxt",
    ],
    echarts: {
        charts: ['BarChart'],
        components: ['DatasetComponent', 'GridComponent', 'TooltipComponent'],
    },
    ui: {
        safelistColors: ['primary', 'red', 'orange', 'green']
    },
    colorMode: {
        disableTransition: true
    },
    routeRules: {
        // Temporary workaround for prerender regression. see https://github.com/nuxt/nuxt/issues/27490
        '/': { prerender: true }
    },
    serverMiddleware: [
        { path: '/api', handler: '~/api/proxy.js' }
      ],
    devtools: {
        enabled: true
    },
    typescript: {
        strict: false
    },
    future: {
        compatibilityVersion: 4
    },
    eslint: {
        config: {
            stylistic: {
                commaDangle: 'never',
                braceStyle: '1tbs'
            }
        }
    },
    compatibilityDate: '2024-07-11'
});
