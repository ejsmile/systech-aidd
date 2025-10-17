// Пример компонента с графиком для проверки Recharts

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

const sampleData = [
  { date: '2025-10-10', count: 45 },
  { date: '2025-10-11', count: 52 },
  { date: '2025-10-12', count: 38 },
  { date: '2025-10-13', count: 65 },
  { date: '2025-10-14', count: 48 },
  { date: '2025-10-15', count: 55 },
  { date: '2025-10-16', count: 42 },
]

export default function SampleChart() {
  return (
    <div className="h-80 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={sampleData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="count" stroke="hsl(var(--primary))" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
