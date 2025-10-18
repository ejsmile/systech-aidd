// Главный компонент приложения с роутингом

import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import ThemeToggle from './components/ThemeToggle'
import FloatingChat from './components/FloatingChat'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <Layout title="Dashboard" rightContent={<ThemeToggle />}>
              <Dashboard />
            </Layout>
          }
        />
      </Routes>
      <FloatingChat />
    </BrowserRouter>
  )
}

export default App
