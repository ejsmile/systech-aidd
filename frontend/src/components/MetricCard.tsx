// MetricCard component for displaying a single metric

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'

interface MetricCardProps {
  title: string
  value: number | string
  description?: string
  isLoading?: boolean
  icon?: React.ReactNode
  format?: (value: number) => string
}

export default function MetricCard({
  title,
  value,
  description,
  isLoading = false,
  icon,
  format,
}: MetricCardProps) {
  const formattedValue = typeof value === 'number' && format ? format(value) : value

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        {icon && <div className="text-2xl">{icon}</div>}
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <div className="space-y-2">
            <Skeleton className="h-7 w-24" />
            {description && <Skeleton className="h-4 w-32" />}
          </div>
        ) : (
          <>
            <div className="text-2xl font-bold">{formattedValue}</div>
            {description && <p className="text-muted-foreground mt-1 text-xs">{description}</p>}
          </>
        )}
      </CardContent>
    </Card>
  )
}
