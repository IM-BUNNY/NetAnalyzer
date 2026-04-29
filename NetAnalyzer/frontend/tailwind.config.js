/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        hv: {
          bg:       '#080B0F',
          surface:  '#0D1117',
          card:     '#111820',
          border:   '#1C2A3A',
          green:    '#00FF88',
          cyan:     '#00D4FF',
          red:      '#FF2D55',
          amber:    '#FFA500',
          muted:    '#4A5568',
          text:     '#C9D1D9',
          bright:   '#E6EDF3',
        }
      },
      fontFamily: {
        mono:  ['"JetBrains Mono"', '"Fira Code"', '"Courier New"', 'monospace'],
        sans:  ['"Inter"', '"SF Pro Display"', 'system-ui', 'sans-serif'],
      },
      animation: {
        'pulse-slow':    'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'blink':         'blink 1s step-end infinite',
        'scanline':      'scanline 3s linear infinite',
        'glow-green':    'glowGreen 2s ease-in-out infinite alternate',
        'slide-up':      'slideUp 0.4s ease-out',
        'fade-in':       'fadeIn 0.6s ease-out',
        'flicker':       'flicker 0.15s infinite',
      },
      keyframes: {
        blink:     { '0%, 100%': { opacity: 1 }, '50%': { opacity: 0 } },
        scanline:  { '0%': { top: '0%' }, '100%': { top: '100%' } },
        glowGreen: {
          '0%':   { boxShadow: '0 0 5px #00FF8833' },
          '100%': { boxShadow: '0 0 20px #00FF8866, 0 0 40px #00FF8822' },
        },
        slideUp:   { from: { opacity: 0, transform: 'translateY(16px)' }, to: { opacity: 1, transform: 'translateY(0)' } },
        fadeIn:    { from: { opacity: 0 }, to: { opacity: 1 } },
        flicker:   { '0%, 100%': { opacity: 1 }, '50%': { opacity: 0.8 } },
      },
      boxShadow: {
        'green-glow':  '0 0 15px rgba(0, 255, 136, 0.25)',
        'cyan-glow':   '0 0 15px rgba(0, 212, 255, 0.2)',
        'red-glow':    '0 0 15px rgba(255, 45, 85, 0.25)',
        'card':        '0 4px 24px rgba(0,0,0,0.5)',
      },
      backgroundImage: {
        'grid-pattern': "linear-gradient(rgba(0,255,136,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(0,255,136,0.03) 1px, transparent 1px)",
        'hero-gradient': "radial-gradient(ellipse at 50% 0%, rgba(0, 255, 136, 0.08) 0%, transparent 60%)",
      },
      backgroundSize: {
        'grid': '40px 40px',
      }
    },
  },
  plugins: [],
}
