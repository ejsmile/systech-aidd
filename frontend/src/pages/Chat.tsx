import { useEffect, useRef, useState } from 'react'
import { AlertCircle, Loader2 } from 'lucide-react'

import { clearChatHistory, getChatHistory, sendMessage, executeAdminQuery, type Text2SQLResponse } from '@/api/chat'
import { APIError } from '@/api/client'
import ChatInput from '@/components/ChatInput'
import ChatMessage from '@/components/ChatMessage'
import SQLResultDisplay from '@/components/SQLResultDisplay'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import type { ChatMessage as ChatMessageType } from '@/types/chat'

const USER_ID = 'web-user-1'

export default function Chat() {
  const [messages, setMessages] = useState<ChatMessageType[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSending, setIsSending] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isAdminMode, setIsAdminMode] = useState(false)
  const [sqlResult, setSqlResult] = useState<Text2SQLResponse | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Load chat history on mount
  useEffect(() => {
    loadHistory()
  }, [])

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function loadHistory() {
    try {
      setIsLoading(true)
      setError(null)
      const response = await getChatHistory(USER_ID)
      setMessages(response.messages)
    } catch (err) {
      const message = err instanceof APIError ? err.message : 'Failed to load chat history'
      setError(message)
      console.error('Error loading history:', err)
    } finally {
      setIsLoading(false)
    }
  }

  async function handleSendMessage(text: string) {
    if (!text.trim()) return

    try {
      setIsSending(true)
      setError(null)
      setSqlResult(null)

      if (isAdminMode) {
        // Admin mode: use Text2SQL
        const result = await executeAdminQuery(text)
        setSqlResult(result)
      } else {
        // Normal mode: regular chat

        // Add user message to UI immediately
        const userMessage: ChatMessageType = {
          role: 'user',
          content: text,
          created_at: new Date().toISOString(),
        }
        setMessages((prev) => [...prev, userMessage])

        // Send to API
        const response = await sendMessage({
          user_id: USER_ID,
          message: text,
        })

        // Add assistant response
        const assistantMessage: ChatMessageType = {
          role: 'assistant',
          content: response.response,
          created_at: new Date().toISOString(),
        }
        setMessages((prev) => [...prev, assistantMessage])
      }
    } catch (err) {
      const message = err instanceof APIError ? err.message : 'Failed to send message'
      setError(message)
      console.error('Error sending message:', err)

      // Remove the user message if sending failed (only for normal mode)
      if (!isAdminMode) {
        setMessages((prev) => prev.slice(0, -1))
      }
    } finally {
      setIsSending(false)
    }
  }

  async function handleClearHistory() {
    if (!confirm('Are you sure you want to clear the chat history?')) return

    try {
      setError(null)
      await clearChatHistory(USER_ID)
      setMessages([])
    } catch (err) {
      const message = err instanceof APIError ? err.message : 'Failed to clear history'
      setError(message)
      console.error('Error clearing history:', err)
    }
  }

  return (
    <div className="flex h-full flex-col">
      {/* Header */}
      <div className="flex items-center justify-between border-b px-6 py-4">
        <div className="flex items-center gap-4">
          <h1 className="text-2xl font-bold">Chat with AI Assistant</h1>
          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="admin-mode"
              checked={isAdminMode}
              onChange={(e) => {
                setIsAdminMode(e.target.checked)
                setSqlResult(null)
              }}
              className="h-4 w-4 cursor-pointer"
            />
            <label htmlFor="admin-mode" className="cursor-pointer text-sm font-medium">
              Admin Mode (Text2SQL)
            </label>
          </div>
        </div>
        <Button variant="outline" onClick={handleClearHistory} disabled={messages.length === 0}>
          Clear History
        </Button>
      </div>

      {/* Messages area */}
      <div className="flex-1 overflow-y-auto p-6">
        {isAdminMode && sqlResult ? (
          <SQLResultDisplay
            sql={sqlResult.sql}
            result={sqlResult.result}
            interpretation={sqlResult.interpretation}
          />
        ) : isLoading ? (
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="flex gap-2">
                <Skeleton className="h-12 w-48 rounded-lg" />
              </div>
            ))}
          </div>
        ) : messages.length === 0 ? (
          <div className="flex h-full items-center justify-center">
            <p className="text-center text-gray-500">
              No messages yet. Start a conversation!
            </p>
          </div>
        ) : (
          <>
            {messages.map((msg, idx) => (
              <ChatMessage
                key={idx}
                role={msg.role}
                content={msg.content}
                timestamp={msg.created_at}
              />
            ))}
            {isSending && (
              <div className="mb-4 flex justify-start">
                <div className="flex items-center gap-2 rounded-lg bg-gray-200 px-4 py-2 text-gray-600">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span className="text-sm">
                    {isAdminMode ? 'Executing query...' : 'Assistant is typing...'}
                  </span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Error message */}
      {error && (
        <div className="px-6 py-2">
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        </div>
      )}

      {/* Input area */}
      <div className="border-t bg-white p-6">
        <ChatInput
          onSendMessage={handleSendMessage}
          disabled={isSending || isLoading}
          placeholder={
            isAdminMode
              ? 'Ask a database question... (e.g., "How many users are there?")'
              : 'Type your message...'
          }
        />
      </div>
    </div>
  )
}
