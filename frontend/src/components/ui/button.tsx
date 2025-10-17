import React from 'react'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'outline' | 'ghost' | 'destructive'
  size?: 'default' | 'sm' | 'lg' | 'icon'
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className = '', variant = 'default', size = 'default', ...props }, ref) => {
    const baseStyles =
      'inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50'

    const variants = {
      default: 'bg-blue-600 text-white hover:bg-blue-700',
      outline: 'border-2 border-border bg-transparent text-foreground hover:bg-muted',
      ghost: 'hover:bg-accent hover:text-accent-foreground',
      destructive: 'bg-red-600 text-white hover:bg-red-700',
    }

    const sizes = {
      default: 'h-10 px-4 py-2',
      sm: 'h-9 rounded-md px-3 text-xs',
      lg: 'h-11 rounded-md px-8',
      icon: 'h-10 w-10',
    }

    const classes = `${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`

    return <button ref={ref} className={classes} {...props} />
  }
)

Button.displayName = 'Button'

export { Button }
