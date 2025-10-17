// Messages by date chart component

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts'
import type { MessageByDate } from '@/types/statistics'

interface MessagesByDateChartProps {
  data: MessageByDate[]
  isLoading?: boolean
}

export default function MessagesByDateChart({ data, isLoading = false }: MessagesByDateChartProps) {
  if (isLoading) {
    return (
      <div className="text-muted-foreground flex h-80 w-full items-center justify-center">
        Loading chart...
      </div>
    )
  }

  if (!data || data.length === 0) {
    return (
      <div className="text-muted-foreground flex h-80 w-full items-center justify-center">
        No data available
      </div>
    )
  }

  // Transform data for Recharts - use last 30 days or all available data
  const chartData = data.map((item) => {
    // Handle both ISO date and ISO datetime formats
    const dateStr = typeof item.date === 'string' ? item.date.split('T')[0] : item.date
    const [, month, day] = dateStr.split('-')
    return {
      date: `${month}-${day}`, // Format: MM-DD
      count: item.count,
    }
  })

  return (
    <div className="h-80 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData} margin={{ top: 5, right: 30, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="date"
            stroke="hsl(var(--muted-foreground))"
            style={{ fontSize: '12px' }}
          />
          <YAxis stroke="hsl(var(--muted-foreground))" style={{ fontSize: '12px' }} />
          <Tooltip
            contentStyle={{
              backgroundColor: 'hsl(var(--background))',
              border: '1px solid hsl(var(--border))',
              borderRadius: '6px',
            }}
            labelStyle={{ color: 'hsl(var(--foreground))' }}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="count"
            stroke="hsl(var(--primary))"
            dot={{ fill: 'hsl(var(--primary))' }}
            strokeWidth={2}
            name="Messages"
            isAnimationActive={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
