/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#2D5A47',
          light: '#4A7C66',
          dark: '#1E3D30'
        },
        secondary: '#E8DDD4',
        accent: '#C4A77D',
        background: '#FAFAF8',
        surface: '#FFFFFF',
        'text-primary': '#1A1A1A',
        'text-secondary': '#6B6B6B',
        border: '#E5E5E3'
      },
      fontFamily: {
        serif: ['Cormorant Garamond', 'Georgia', 'serif'],
        sans: ['Noto Sans SC', 'system-ui', 'sans-serif']
      },
      spacing: {
        '18': '4.5rem',
        '22': '5.5rem'
      },
      transitionTimingFunction: {
        'gentle': 'cubic-bezier(0.25, 0.1, 0.25, 1)'
      }
    },
  },
  plugins: [],
}
