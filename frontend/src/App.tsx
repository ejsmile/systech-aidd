// Главный компонент приложения с роутингом

import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Chat from './pages/Chat'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <Layout title="Dashboard" subtitle="Статистика использования бота">
              <Dashboard />
            </Layout>
          }
        />
        <Route
          path="/chat"
          element={
            <Layout title="Chat" subtitle="Общение с ботом">
              <Chat />
            </Layout>
          }
        />
      </Routes>
    </BrowserRouter>
  )
}

export default App
