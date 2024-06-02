/** @type {import('tailwindcss').Config} */
const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  content: [
      './src/**/*.{css,js}',
      './templates/*.html',
      './**/templates/**/*.html',
      './**/jinja2/**/*.html',
  ],
  theme: {
    extend: {
      screens: {
        xs: '320px'
      },
      fontFamily: {
        'sans': ['"Montserrat Alternates"', ...defaultTheme.fontFamily.sans],
        // 'Cormorant': ['"Cormorant Infant"', "sans-serif"],
        'serif': ['"Cormorant Infant"', ...defaultTheme.fontFamily.serif],
      },
    },
  },
  plugins: [],
}

