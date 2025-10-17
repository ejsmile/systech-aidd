// Главный компонент приложения с роутингом

import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Chat from './pages/Chat'
import ThemeToggle from './components/ThemeToggle'

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
        <Route
          path="/chat"
          element={
            <Layout title="Chat" subtitle="Общение с ботом" rightContent={<ThemeToggle />}>
              <Chat />
            </Layout>
          }
        />
      </Routes>
    </BrowserRouter>
  )
}

export default App
