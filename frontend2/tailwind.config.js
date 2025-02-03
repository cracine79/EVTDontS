/** @type {import('tailwindcss').Config} */
export default {
  
  content: [ "./index.html",
            "./src/**/*.{js,ts,jsx,tsx}",],
  theme: {
    extend: {
      margin: {
        '5p': '5%',
        '10p': '10%',
        '15p': '15%',
        '20p': '20%',
      },
      fontSize: {
        'xxs': '0.625rem', // This is equivalent to 10px (0.625rem * 16 = 10px)
      }, keyframes: {
        shine: {
          "0%": { opacity: "0", left: "-20%" },
          "50%": { opacity: "1" },
          "100%": { opacity: "0", left: "120%" },
        },
      },
      animation: {
        shine: "shine 0.5s linear",
      },
    }, 

  },
  plugins: [],
}

