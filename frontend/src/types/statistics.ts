// TypeScript types для API статистики

export interface MessageByDate {
  date: string // ISO date format: "2025-10-17"
  count: number
}

export interface TopUser {
  user_id: number
  username: string | null
  message_count: number
}

export interface StatisticsResponse {
  total_users: number
  active_users: number
  total_messages: number
  avg_messages_per_user: number
  messages_by_date: MessageByDate[]
  top_users: TopUser[]
}
