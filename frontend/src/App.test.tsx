// Тесты для App компонента

import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import App from './App'
import { ThemeProvider } from './contexts/ThemeContext'

// Helper function to render App with ThemeProvider
const renderWithThemeProvider = () => {
  return render(
    <ThemeProvider>
      <App />
    </ThemeProvider>
  )
}

describe('App', () => {
  it('renders without crashing', () => {
    renderWithThemeProvider()
    expect(screen.getByText(/Admin Panel/i)).toBeInTheDocument()
  })

  it('renders navigation links', () => {
    renderWithThemeProvider()
    expect(screen.getAllByText(/Dashboard/i).length).toBeGreaterThan(0)
    // FloatingChat button should be present
    expect(screen.getByLabelText(/Open chat/i)).toBeInTheDocument()
  })

  it('renders messages chart', () => {
    renderWithThemeProvider()
    expect(screen.getByText(/Сообщения по датам/i)).toBeInTheDocument()
  })
})
