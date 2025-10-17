// API методы для статистики

import { get } from './client'
import type { StatisticsResponse } from '@/types/statistics'

export async function getStatistics(): Promise<StatisticsResponse> {
  return get<StatisticsResponse>('/statistics')
}
