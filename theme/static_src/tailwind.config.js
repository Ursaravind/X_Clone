module.exports = {
  content: [
    // Templates in your theme app
    '../../core/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        'x-dark-blue': '#15202B',
        'x-black': '#000000',
        'x-gray-input': '#1A1A1A',
        'x-gray-text': '#71767B',
        'x-blue-primary': '#1D9BF0',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/line-clamp'),
    require('@tailwindcss/aspect-ratio'),
  ],
}
