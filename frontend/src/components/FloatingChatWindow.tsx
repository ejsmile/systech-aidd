import { useEffect, useRef } from 'react'
import { X, Loader2, Trash2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { ChatInput, ChatInputTextArea, ChatInputSubmit } from '@/components/ui/chat-input'
import ChatMessage from '@/components/ChatMessage'
import SQLResultDisplay from '@/components/SQLResultDisplay'
import type { ChatMessage as ChatMessageType } from '@/types/chat'
import type { Text2SQLResponse } from '@/api/chat'

interface FloatingChatWindowProps {
  isOpen: boolean
  onClose: () => void
  isAdminMode: boolean
  onToggleMode: () => void
  messages: ChatMessageType[]
  isLoading: boolean
  isSending: boolean
  error: string | null
  sqlResult: Text2SQLResponse | null
  inputValue: string
  onInputChange: (value: string) => void
  onSendMessage: () => void
  onClearHistory: () => void
}

export default function FloatingChatWindow({
  isOpen,
  onClose,
  isAdminMode,
  onToggleMode,
  messages,
  isLoading,
  isSending,
  error,
  sqlResult,
  inputValue,
  onInputChange,
  onSendMessage,
  onClearHistory,
}: FloatingChatWindowProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages, isOpen, isSending])

  if (!isOpen) return null

  return (
    <>
      {/* Mobile: Full screen overlay */}
      <div className="bg-background fixed inset-0 z-40 md:hidden">
        <div className="flex h-full flex-col">
          {/* Header */}
          <div className="bg-card border-b px-4 py-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <h2 className="text-lg font-semibold">AI Assistant</h2>
                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    id="admin-mode-mobile"
                    checked={isAdminMode}
                    onChange={onToggleMode}
                    className="border-input accent-primary h-4 w-4 cursor-pointer rounded"
                  />
                  <label
                    htmlFor="admin-mode-mobile"
                    className="text-foreground cursor-pointer text-sm font-medium"
                  >
                    SQL Mode
                  </label>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={onClearHistory}
                  disabled={messages.length === 0}
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
                <Button variant="ghost" size="icon" onClick={onClose}>
                  <X className="h-5 w-5" />
                </Button>
              </div>
            </div>
          </div>

          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-4">
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
                    <div className="bg-muted h-12 w-48 animate-pulse rounded-lg" />
                  </div>
                ))}
              </div>
            ) : messages.length === 0 ? (
              <div className="flex h-full items-center justify-center">
                <p className="text-muted-foreground text-center">
                  No messages yet. Start a conversation!
                </p>
              </div>
            ) : (
              <>
                {messages
                  .filter((msg) => msg.role !== 'system')
                  .map((msg, idx) => (
                    <ChatMessage
                      key={idx}
                      role={msg.role as 'user' | 'assistant'}
                      content={msg.content}
                      timestamp={msg.created_at}
                    />
                  ))}
                {isSending && (
                  <div className="mb-4 flex justify-start">
                    <div className="bg-muted text-muted-foreground flex items-center gap-2 rounded-lg px-4 py-2">
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
            <div className="px-4 py-2">
              <Alert variant="destructive">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            </div>
          )}

          {/* Input Area */}
          <div className="bg-card border-t p-4">
            <ChatInput
              variant="default"
              value={inputValue}
              onChange={(e) => onInputChange(e.target.value)}
              onSubmit={onSendMessage}
              loading={isSending}
            >
              <ChatInputTextArea
                placeholder={isAdminMode ? 'Ask a database question...' : 'Type your message...'}
                disabled={isSending || isLoading}
              />
              <ChatInputSubmit />
            </ChatInput>
          </div>
        </div>
      </div>

      {/* Desktop: Floating window */}
      <Card className="fixed right-6 bottom-24 z-40 hidden w-96 shadow-2xl transition-all md:block">
        <div className="flex h-[600px] flex-col">
          {/* Header */}
          <div className="bg-card border-b px-4 py-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <h2 className="text-lg font-semibold">AI Assistant</h2>
                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    id="admin-mode-desktop"
                    checked={isAdminMode}
                    onChange={onToggleMode}
                    className="border-input accent-primary h-4 w-4 cursor-pointer rounded"
                  />
                  <label
                    htmlFor="admin-mode-desktop"
                    className="text-foreground cursor-pointer text-xs font-medium"
                  >
                    SQL
                  </label>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={onClearHistory}
                  disabled={messages.length === 0}
                  className="h-8 w-8"
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
                <Button variant="ghost" size="icon" onClick={onClose} className="h-8 w-8">
                  <X className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>

          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-4">
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
                    <div className="bg-muted h-12 w-48 animate-pulse rounded-lg" />
                  </div>
                ))}
              </div>
            ) : messages.length === 0 ? (
              <div className="flex h-full items-center justify-center">
                <p className="text-muted-foreground text-center text-sm">
                  No messages yet.
                  <br />
                  Start a conversation!
                </p>
              </div>
            ) : (
              <>
                {messages
                  .filter((msg) => msg.role !== 'system')
                  .map((msg, idx) => (
                    <ChatMessage
                      key={idx}
                      role={msg.role as 'user' | 'assistant'}
                      content={msg.content}
                      timestamp={msg.created_at}
                    />
                  ))}
                {isSending && (
                  <div className="mb-4 flex justify-start">
                    <div className="bg-muted text-muted-foreground flex items-center gap-2 rounded-lg px-4 py-2">
                      <Loader2 className="h-4 w-4 animate-spin" />
                      <span className="text-sm">
                        {isAdminMode ? 'Executing query...' : 'Typing...'}
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
            <div className="px-4 py-2">
              <Alert variant="destructive">
                <AlertDescription className="text-xs">{error}</AlertDescription>
              </Alert>
            </div>
          )}

          {/* Input Area */}
          <div className="bg-card border-t p-3">
            <ChatInput
              variant="default"
              value={inputValue}
              onChange={(e) => onInputChange(e.target.value)}
              onSubmit={onSendMessage}
              loading={isSending}
            >
              <ChatInputTextArea
                placeholder={isAdminMode ? 'Ask a database question...' : 'Type your message...'}
                disabled={isSending || isLoading}
              />
              <ChatInputSubmit />
            </ChatInput>
          </div>
        </div>
      </Card>
    </>
  )
}
