import { useEffect, useState } from 'react'
import FloatingChatButton from './FloatingChatButton'
import FloatingChatWindow from './FloatingChatWindow'
import {
  clearChatHistory,
  getChatHistory,
  sendMessage,
  executeAdminQuery,
  type Text2SQLResponse,
} from '@/api/chat'
import { APIError } from '@/api/client'
import type { ChatMessage as ChatMessageType } from '@/types/chat'

const USER_ID = 'web-user-1'

export default function FloatingChat() {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<ChatMessageType[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [isSending, setIsSending] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isAdminMode, setIsAdminMode] = useState(false)
  const [sqlResult, setSqlResult] = useState<Text2SQLResponse | null>(null)
  const [inputValue, setInputValue] = useState('')

  // Load chat history when opening chat
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      loadHistory()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isOpen])

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

  async function handleSendMessage() {
    if (!inputValue.trim()) return

    try {
      setIsSending(true)
      setError(null)
      setSqlResult(null)

      if (isAdminMode) {
        // Admin mode: use Text2SQL
        const result = await executeAdminQuery(inputValue)
        setSqlResult(result)
        setInputValue('')
      } else {
        // Normal mode: regular chat
        const userMessage: ChatMessageType = {
          role: 'user',
          content: inputValue,
          created_at: new Date().toISOString(),
        }
        setMessages((prev) => [...prev, userMessage])
        setInputValue('')

        // Send to API
        const response = await sendMessage({
          user_id: USER_ID,
          message: inputValue,
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
      setSqlResult(null)
    } catch (err) {
      const message = err instanceof APIError ? err.message : 'Failed to clear history'
      setError(message)
      console.error('Error clearing history:', err)
    }
  }

  function handleToggleMode() {
    setIsAdminMode(!isAdminMode)
    setSqlResult(null)
  }

  function handleClose() {
    setIsOpen(false)
    // Clear SQL result when closing
    setSqlResult(null)
  }

  return (
    <>
      <FloatingChatButton
        onClick={() => setIsOpen(!isOpen)}
        isAdminMode={isAdminMode}
        isOpen={isOpen}
      />
      <FloatingChatWindow
        isOpen={isOpen}
        onClose={handleClose}
        isAdminMode={isAdminMode}
        onToggleMode={handleToggleMode}
        messages={messages}
        isLoading={isLoading}
        isSending={isSending}
        error={error}
        sqlResult={sqlResult}
        inputValue={inputValue}
        onInputChange={setInputValue}
        onSendMessage={handleSendMessage}
        onClearHistory={handleClearHistory}
      />
    </>
  )
}
