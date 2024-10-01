/** @type {import('tailwindcss').Config} */
export default {
  
  content: [ "./index.html",
            "./src/**/*.{js,ts,jsx,tsx}",],
  theme: {
    extend: {margin: {
        '5p': '5%',
        '10p': '10%',
        '15p': '15%',
        '20p': '20%',
      },
      fontSize: {
        'xxs': '0.625rem', // This is equivalent to 10px (0.625rem * 16 = 10px)
      }, }, 

  },
  plugins: [],
}

