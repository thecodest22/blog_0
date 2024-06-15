/** @type {import('tailwindcss').Config} */
const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  content: [
      './build/**/*.{css,js}',
      '../backend/**/*.html',
  ],
  theme: {
    extend: {
      maxWidth: {
        '8xl': '90rem'
      },
      spacing: {
        '100': '25rem',
      },
      fontFamily: {
        'sans': ['"Montserrat Alternates"', ...defaultTheme.fontFamily.sans],
        'serif': ['"Cormorant Infant"', ...defaultTheme.fontFamily.serif]
      },
    },
  },
  plugins: [],
}

