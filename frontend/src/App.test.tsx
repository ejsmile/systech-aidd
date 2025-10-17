// Тесты для App компонента

import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import App from './App'

describe('App', () => {
  it('renders without crashing', () => {
    render(<App />)
    expect(screen.getByText(/Admin Panel/i)).toBeInTheDocument()
  })

  it('renders navigation links', () => {
    render(<App />)
    expect(screen.getAllByText(/Dashboard/i).length).toBeGreaterThan(0)
    expect(screen.getByText(/💬 Chat/i)).toBeInTheDocument()
  })

  it('renders sample chart', () => {
    render(<App />)
    expect(screen.getByText(/Sample Chart/i)).toBeInTheDocument()
  })
})
