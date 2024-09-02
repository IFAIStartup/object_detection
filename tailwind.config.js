/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*"],
  theme: {
    extend: {
      fontFamily :{
        "nunito" : ["Nunito", "sans-serif"],
        "poppins" : ["Poppins", "sans-serif"],
        "teko" : ["Teko", "sans-serif"]
      }
    },
    letterSpacing: {
      tightest: '-.075em',
      tighter: '-.05em',
      tight: '-.025em',
      normal: '0',
      wide: '.025em',
      wider: '.05em',
      widest: '.1em',
      widest: '.25em',
      longest: ".43em"
    }
  },
  plugins: [],
}

