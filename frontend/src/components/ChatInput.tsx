import { useRef, useEffect, useState } from 'react'
import { Button } from '@/components/ui/button'
import { useTheme } from '@/contexts/ThemeContext'

interface ChatInputProps {
  onSendMessage: (message: string) => void
  disabled: boolean
  placeholder?: string
}

export default function ChatInput({ onSendMessage, disabled, placeholder }: ChatInputProps) {
  const [message, setMessage] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const { theme } = useTheme()

  useEffect(() => {
    // Auto-expand textarea as user types
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`
    }
  }, [message])

  const handleSendMessage = () => {
    if (message.trim() && !disabled) {
      onSendMessage(message)
      setMessage('')
      // Reset textarea height
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto'
      }
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="flex gap-2">
      <textarea
        ref={textareaRef}
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={disabled}
        placeholder={placeholder || 'Type your message... (Shift+Enter for new line)'}
        style={{ colorScheme: theme }}
        className="border-input bg-background text-foreground placeholder:text-muted-foreground flex-1 resize-none rounded-md border px-3 py-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary disabled:cursor-not-allowed disabled:opacity-50"
        rows={1}
      />
      <Button
        onClick={handleSendMessage}
        disabled={!message.trim() || disabled}
        className="self-end"
      >
        Send
      </Button>
    </div>
  )
}
