// /** @type {import('tailwindcss').Config} */
module.exports = {
    darkMode: 'class', // or 'media' if you prefer auto dark mode
    content: [
      './templates/**/*.html',
      './**/templates/**/*.html',
      './static/js/**/*.js',
    ],
    theme: {
      extend: {
        colors: {
          primary: {
            light: '#60a5fa', // Blue
            dark: '#3b82f6'
          },
          secondary: {
            light: '#a78bfa', // Purple
            dark: '#8b5cf6'
          },
          background: {
            light: '#f9fafb',
            dark: '#111827'
          },
          surface: {
            light: '#ffffff',
            dark: '#1f2937'
          }
        },
        animation: {
          'spin-slow': 'spin 3s linear infinite',
          'fade-in': 'fadeIn 0.5s ease-in-out'
        },
        keyframes: {
          fadeIn: {
            '0%': { opacity: '0' },
            '100%': { opacity: '1' }
          }
        }
      }
    },
    plugins: []
  }