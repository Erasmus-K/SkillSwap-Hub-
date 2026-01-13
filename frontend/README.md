# SkillSwap Hub - Frontend

React frontend for the SkillSwap Hub application built with Vite, React Router, and TailwindCSS.

## Features

- **Authentication**: Login/Register with JWT tokens
- **Dashboard**: Overview of available sessions and user stats
- **Skills Browser**: Browse and search available skills
- **Session Management**: Create and manage teaching sessions
- **Bookings**: Book sessions and manage your bookings
- **Profile**: User profile management
- **Responsive Design**: Mobile-friendly interface with TailwindCSS

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **React Router v6** - Client-side routing
- **Axios** - HTTP client
- **TailwindCSS** - Utility-first CSS framework
- **Context API** - State management

## Getting Started

### Prerequisites

- Node.js 16+ and npm

### Installation

1. Install dependencies:
```bash
npm install
```

2. Copy environment variables:
```bash
cp .env.example .env
```

3. Update environment variables in `.env`:
```
VITE_API_BASE_URL=http://localhost:8000
VITE_GOOGLE_CLIENT_ID=your_google_client_id_here
```

### Development

Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Build

Build for production:
```bash
npm run build
```

### Preview

Preview the production build:
```bash
npm run preview
```

## Project Structure

```
src/
├── api/           # API client functions
├── components/    # Reusable UI components
├── context/       # React Context providers
├── pages/         # Page components
├── routes/        # Routing configuration
├── App.jsx        # Main app component
├── main.jsx       # App entry point
└── index.css      # Global styles
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Environment Variables

- `VITE_API_BASE_URL` - Backend API URL
- `VITE_GOOGLE_CLIENT_ID` - Google OAuth client ID

## Deployment

The frontend is configured for deployment on Vercel. Simply connect your repository to Vercel and it will automatically deploy on every push to main.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request