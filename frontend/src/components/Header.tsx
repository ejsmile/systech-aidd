// Header component with page title and timestamp

interface HeaderProps {
  title: string
  subtitle?: string
  rightContent?: React.ReactNode
}

export default function Header({ title, subtitle, rightContent }: HeaderProps) {
  return (
    <div className="bg-background border-b">
      <div className="flex items-center justify-between px-6 py-4">
        <div>
          <h1 className="text-2xl font-bold">{title}</h1>
          {subtitle && <p className="text-muted-foreground mt-1 text-sm">{subtitle}</p>}
        </div>
        {rightContent && <div className="flex items-center gap-3">{rightContent}</div>}
      </div>
    </div>
  )
}
