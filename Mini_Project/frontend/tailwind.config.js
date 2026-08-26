/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        base: {
          950: "#07070c",
          900: "#0d0e17",
          800: "#12131f",
          700: "#1a1c2c",
          600: "#24263a",
          500: "#33354d",
        },
        accent: {
          400: "#8b7bff",
          500: "#7c5cff",
          600: "#6a3ffa",
        },
        mint: {
          400: "#38e0c0",
          500: "#22c9a8",
        },
        coral: {
          400: "#ff6b81",
          500: "#f43f5e",
        },
        amber: {
          400: "#ffb454",
          500: "#f59e0b",
        },
      },
      fontFamily: {
        display: ["'Sora'", "system-ui", "sans-serif"],
        body: ["'Inter'", "system-ui", "sans-serif"],
      },
      boxShadow: {
        glow: "0 0 40px -8px rgba(124, 92, 255, 0.45)",
        card: "0 8px 30px -12px rgba(0,0,0,0.45)",
      },
      backgroundImage: {
        "grad-primary": "linear-gradient(135deg, #7c5cff 0%, #38e0c0 100%)",
        "grad-warm": "linear-gradient(135deg, #ff6b81 0%, #ffb454 100%)",
        "grad-dark": "radial-gradient(circle at 20% 0%, #1a1c2c 0%, #07070c 60%)",
      },
      borderRadius: {
        xl2: "1.25rem",
      },
    },
  },
  plugins: [],
};
