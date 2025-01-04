const themeDir = __dirname + '/../../';

module.exports = {
  content: [
    `${themeDir}/layouts/**/*.html`, 
    `${themeDir}/content/**/*.md`
  ],
  theme: {
    container: {},
    extend: {
      width: {
        'lg': '1024px'
      }
    }
  },
  variants: {},
  plugins: []
}