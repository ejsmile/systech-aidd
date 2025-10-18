export interface ChatMessage {
  role: 'system' | 'user' | 'assistant'
  content: string
  created_at: string
}

export interface SendMessageRequest {
  user_id: string
  message: string
}

export interface SendMessageResponse {
  response: string
  message_id: number
}

export interface ChatHistoryResponse {
  messages: ChatMessage[]
}

export interface ClearHistoryResponse {
  success: boolean
  deleted_count: number
}
