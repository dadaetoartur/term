import type { Config } from 'tailwindcss';

export default <Partial<Config>>{
  theme: {
    extend: {
      colors: {
        blue: {
          50: '#EDEDED',
          100: '#D9D9D9',
          200: '#B3B3B3',
          300: '#6C8CAC',
          400: '#2D669F',
          500: '#004080',
          600: '#163350',
          700: '#1C2631',
          800: '#1A1A1A',
          900: '#0D0D0D',
          950: '#080808',
        },
      },
    },
  },
};
