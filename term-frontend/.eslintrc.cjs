module.exports = {
  env: {
    browser: true,
    node: true,
    es2021: true,
  },
  extends: [
    'airbnb-base',
    'plugin:vue/vue3-recommended',
    'plugin:nuxt/recommended',
    'plugin:@typescript-eslint/recommended',
  ],
  parser: 'vue-eslint-parser',
  parserOptions: {
    ecmaVersion: 'latest',
    parser: '@typescript-eslint/parser',
    sourceType: 'module',
  },
  plugins: [
    'vue',
    '@typescript-eslint',
  ],
  rules: {
    'vue/multi-word-component-names': 0,
    'no-undef': 0,
    'no-underscore-dangle': 0,
    'no-restricted-syntax': 0,
    'import/extensions': 0,
    'max-len': 0,
    '@typescript-eslint/no-explicit-any': ['off'],
  },
  settings: {
    'import/resolver': {
      nuxt: {
        extensions: ['.js', 'ts', '.vue'],
      },
      typescript: {},
    },
  },
};
