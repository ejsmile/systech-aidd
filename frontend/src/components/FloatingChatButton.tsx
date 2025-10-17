import { MessageCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'

interface FloatingChatButtonProps {
  onClick: () => void
  isAdminMode: boolean
  isOpen: boolean
}

export default function FloatingChatButton({
  onClick,
  isAdminMode,
  isOpen,
}: FloatingChatButtonProps) {
  return (
    <div className="fixed right-6 bottom-6 z-50">
      <Button
        onClick={onClick}
        size="icon"
        className="relative h-14 w-14 rounded-full shadow-lg transition-transform hover:scale-110"
        aria-label={isOpen ? 'Close chat' : 'Open chat'}
      >
        <MessageCircle className="h-6 w-6" />
        {/* Badge индикатор режима */}
        <span
          className={`absolute -top-1 -right-1 flex h-6 min-w-[24px] items-center justify-center rounded-full px-1.5 text-xs font-semibold ${
            isAdminMode
              ? 'bg-destructive text-destructive-foreground'
              : 'bg-primary text-primary-foreground'
          }`}
        >
          {isAdminMode ? 'SQL' : 'AI'}
        </span>
      </Button>
    </div>
  )
}
