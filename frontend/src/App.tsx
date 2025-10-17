// Главный компонент приложения с роутингом

import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import Chat from './pages/Chat'
import SampleChart from './components/SampleChart'
import { cn } from './lib/utils'

function Layout({ children }: { children: React.ReactNode }) {
  const location = useLocation()

  const isActive = (path: string) => location.pathname === path

  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <aside className="bg-card w-64 border-r">
        <div className="p-6">
          <h2 className="text-xl font-bold">Admin Panel</h2>
        </div>
        <nav className="space-y-1 px-3">
          <Link
            to="/"
            className={cn(
              'block rounded-md px-3 py-2 text-sm font-medium transition-colors',
              isActive('/')
                ? 'bg-primary text-primary-foreground'
                : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
            )}
          >
            📊 Dashboard
          </Link>
          <Link
            to="/chat"
            className={cn(
              'block rounded-md px-3 py-2 text-sm font-medium transition-colors',
              isActive('/chat')
                ? 'bg-primary text-primary-foreground'
                : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
            )}
          >
            💬 Chat
          </Link>
        </nav>
      </aside>

      {/* Main content */}
      <main className="flex-1">
        <div className="container mx-auto py-6">{children}</div>
      </main>
    </div>
  )
}

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/chat" element={<Chat />} />
        </Routes>

        {/* Sample chart для проверки Recharts */}
        <div className="bg-card mt-8 rounded-lg border p-6">
          <h3 className="mb-4 text-lg font-semibold">Sample Chart (Recharts Test)</h3>
          <SampleChart />
        </div>
      </Layout>
    </BrowserRouter>
  )
}

export default App
