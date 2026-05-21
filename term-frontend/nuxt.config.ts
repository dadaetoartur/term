export default defineNuxtConfig({
  devtools: { enabled: process.env.NODE_ENV !== 'production' },

  runtimeConfig: {
    public: {
      API_URL: process.env.API_URL || 'https://bimify.systems/backend',
    },
  },

  nitro: {
    routeRules: {
      '/backend/**': {
        proxy: `${process.env.BACKEND_INTERNAL_URL || 'http://localhost:5000'}/**`,
      },
    },
  },

  colorMode: {
    preference: 'light',
  },

  app: {
    head: {
      title: 'Bimify - Term',
      htmlAttrs: {
        lang: 'ru',
      },
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'format-detection', content: 'telephone=no' },
        { name: 'description', content: 'Веб-приложение для управления строительством с технологией цифрового двойника. Использование технологии цифровых двойников для улучшения управления и эксплуатации зданий, включая интеграцию с системами диспетчеризации и аналитику энергоэффективности.' },
        { name: 'keywords', content: 'строительство, BIM-модель, цифровой двойник, система диспетчеризации, веб-приложение, управление персоналом, контроль эксплуатации здания, аналитика эффективности, инженерные системы, оптимизация, цифровая модель, информационная модель, виртуальная модель, хранение файлов' },

      ],
      link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
    },
  },

  css: ['~/assets/css/normalize.css', '~/assets/scss/main.scss'],

  modules: ['@pinia/nuxt', '@nuxt/ui', '@nuxt/image'],
});
