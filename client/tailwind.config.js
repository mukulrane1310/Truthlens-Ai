/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        plum: {
          background: '#19121E',
          surface: '#281B2D',
        },
        coral: '#FF8D79',
        lavender: '#C7A0E8',
        cream: '#FFF5F0',
        muted: '#B8A6B9',
      },
    },
  },
  plugins: [],
};
