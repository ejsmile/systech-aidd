import { get, post, del } from './client'
import type {
  ClearHistoryResponse,
  ChatHistoryResponse,
  SendMessageRequest,
  SendMessageResponse,
} from '@/types/chat'

export interface Text2SQLResponse {
  sql: string
  result: Array<Record<string, unknown>>
  interpretation: string
}

export async function sendMessage(data: SendMessageRequest): Promise<SendMessageResponse> {
  return post<SendMessageResponse, SendMessageRequest>('/chat/message', data)
}

export async function getChatHistory(userId: string): Promise<ChatHistoryResponse> {
  return get<ChatHistoryResponse>(`/chat/history/${userId}`)
}

export async function clearChatHistory(userId: string): Promise<ClearHistoryResponse> {
  return del<ClearHistoryResponse>(`/chat/history/${userId}`)
}

export async function executeAdminQuery(query: string): Promise<Text2SQLResponse> {
  return post<Text2SQLResponse, { query: string }>('/admin/query', { query })
}
