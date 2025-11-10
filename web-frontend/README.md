# Web Frontend - React + TypeScript + shadcn/ui

Modern web interface for the Chemical Equipment Visualizer.

## Features

- 🎨 Modern UI with shadcn/ui components
- 🌓 Dark mode support
- 📊 Interactive charts with Chart.js
- 🔐 JWT authentication
- 📱 Responsive design
- ⚡ Fast development with Vite

## Setup

1. **Install Dependencies**
```bash
npm install
```

2. **Run Development Server**
```bash
npm run dev
```

Application will be available at `http://localhost:5173`

3. **Build for Production**
```bash
npm run build
```

Output will be in the `dist/` directory.

## Project Structure

```
src/
├── components/
│   └── ui/              # shadcn/ui components
├── contexts/
│   ├── AuthContext.tsx  # Authentication state
│   └── ThemeContext.tsx # Dark mode state
├── lib/
│   ├── api.ts          # API client with axios
│   └── utils.ts        # Utility functions
├── pages/
│   ├── Login.tsx       # Login page
│   ├── Register.tsx    # Registration page
│   └── Dashboard.tsx   # Main dashboard
├── App.tsx             # Main app with routing
├── main.tsx           # Entry point
└── index.css          # Global styles with Tailwind
```

## Technologies

- **React 19** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **React Router** - Routing
- **Axios** - HTTP client
- **Chart.js** - Data visualization
- **shadcn/ui** - UI components
- **Tailwind CSS** - Styling
- **Radix UI** - Headless UI primitives

## Configuration

### API URL

Update the API URL in `src/lib/api.ts`:

```typescript
const API_URL = 'http://localhost:8000/api';
```

### Tailwind Configuration

Customize theme in `tailwind.config.js`

### Vite Configuration

Modify build settings in `vite.config.ts`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Features Guide

### Authentication

- JWT tokens stored in localStorage
- Automatic token refresh on 401 errors
- Protected routes with authentication check
- Public routes redirect to dashboard if authenticated

### Dark Mode

- Toggle with moon/sun icon in header
- Preference saved in localStorage
- Smooth transitions between themes

### Data Upload

- Drag and drop support (can be added)
- CSV validation
- Progress feedback
- Error handling with toast notifications

### Charts

- Equipment type distribution (Doughnut chart)
- Parameter statistics (Bar chart)
- Responsive and interactive
- Dark mode compatible

### PDF Export

- Download reports for any dataset
- Automatic file naming
- Browser download handling

## Customization

### Adding New Components

Use shadcn/ui CLI to add components:

```bash
npx shadcn-ui@latest add [component-name]
```

### Styling

- Use Tailwind utility classes
- Customize theme in `tailwind.config.js`
- CSS variables in `src/index.css`

### Adding New Pages

1. Create component in `src/pages/`
2. Add route in `src/App.tsx`
3. Add navigation if needed

## Troubleshooting

### Module Not Found

```bash
rm -rf node_modules package-lock.json
npm install
```

### Build Errors

```bash
npm run build -- --debug
```

### API Connection Issues

- Check backend is running on port 8000
- Verify CORS settings in backend
- Check browser console for errors

### TypeScript Errors

```bash
npm run build
# Fix any type errors shown
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Performance

- Code splitting with React.lazy (can be added)
- Optimized bundle size
- Fast refresh in development
- Production build optimizations

## Deployment

### Vercel

```bash
npm run build
vercel --prod
```

### Netlify

```bash
npm run build
netlify deploy --prod --dir=dist
```

### Static Hosting

Upload the `dist/` folder to any static hosting service.

## Environment Variables

Create `.env.local` for local development:

```env
VITE_API_URL=http://localhost:8000/api
```

Access in code:
```typescript
const apiUrl = import.meta.env.VITE_API_URL;
```
