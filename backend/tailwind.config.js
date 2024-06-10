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
      fontFamily: {
        'sans': ['"Montserrat Alternates"', ...defaultTheme.fontFamily.sans],
        'serif': ['"Cormorant Infant"', ...defaultTheme.fontFamily.serif],
      },
    },
  },
  plugins: [],
}

