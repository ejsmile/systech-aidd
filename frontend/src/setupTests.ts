// Setup тестового окружения

import '@testing-library/jest-dom'

// Mock ResizeObserver для тестов с Recharts
global.ResizeObserver = class ResizeObserver {
  observe() {
    // do nothing
  }
  unobserve() {
    // do nothing
  }
  disconnect() {
    // do nothing
  }
}
