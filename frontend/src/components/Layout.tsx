// Main layout component with sidebar and content area

import Sidebar from './Sidebar'
import Header from './Header'

interface LayoutProps {
  children: React.ReactNode
  title: string
  subtitle?: string
}

export default function Layout({ children, title, subtitle }: LayoutProps) {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex flex-1 flex-col">
        <Header title={title} subtitle={subtitle} />
        <div className="container mx-auto flex-1 py-6">{children}</div>
      </main>
    </div>
  )
}
