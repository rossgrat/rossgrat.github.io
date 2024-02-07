const themeDir = __dirname + '/../../';

module.exports = {
  content: [
    `${themeDir}/layouts/**/*.html`, 
    `${themeDir}/content/**/*.md`
  ],
  theme: {
    extend: {
      backgroundImage: {
        'nature': "url('../images/minimal-nature-1.jpeg')",
      }
    },
    container: {
      padding: {
        DEFAULT: '2rem',
        sm: '2rem',
        lg: '10rem',
        xl: '18rem',
        '2xl': '26rem',
      },
    },
  },
  variants: {},
  plugins: []
}