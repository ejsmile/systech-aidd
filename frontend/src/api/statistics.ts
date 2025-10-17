// API методы для статистики

import { get } from './client'
import type { StatisticsResponse } from '@/types/statistics'

export async function getStatistics(
  startDate?: string,
  endDate?: string
): Promise<StatisticsResponse> {
  const params = new URLSearchParams()
  if (startDate) {
    params.append('start_date', startDate)
  }
  if (endDate) {
    params.append('end_date', endDate)
  }

  const queryString = params.toString()
  const url = queryString ? `/statistics?${queryString}` : '/statistics'

  return get<StatisticsResponse>(url)
}
