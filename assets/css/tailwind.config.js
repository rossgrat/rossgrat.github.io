const themeDir = __dirname + '/../../';

module.exports = {
  content: [
    `${themeDir}/layouts/**/*.html`, 
    `${themeDir}/content/**/*.md`
  ],
  theme: {
    container: {
        padding: {
          DEFAULT: '1rem',
          sm: '2rem',
          lg: '10rem',
          xl: '18rem',
          '2xl': '26rem',
        },
      },
    extend: {}
  },
  variants: {},
  plugins: []
}