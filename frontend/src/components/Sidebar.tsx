// Sidebar navigation component

import { Link, useLocation } from 'react-router-dom'
import { cn } from '@/lib/utils'

export default function Sidebar() {
  const location = useLocation()
  const isActive = (path: string) => location.pathname === path

  return (
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
      </nav>
    </aside>
  )
}
