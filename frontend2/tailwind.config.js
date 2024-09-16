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
      },},
  },
  plugins: [],
}

