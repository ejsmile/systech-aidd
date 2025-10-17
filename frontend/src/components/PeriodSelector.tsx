// Period selector component for filtering statistics

import { Calendar } from 'lucide-react'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

export type Period = 'week' | 'month' | 'all'

interface PeriodSelectorProps {
  value: Period
  onChange: (period: Period) => void
}

export default function PeriodSelector({ value, onChange }: PeriodSelectorProps) {
  return (
    <Select value={value} onValueChange={(v) => onChange(v as Period)}>
      <SelectTrigger className="w-[160px]">
        <div className="flex items-center gap-2">
          <Calendar className="h-4 w-4" />
          <SelectValue />
        </div>
      </SelectTrigger>
      <SelectContent>
        <SelectItem value="week">Неделя</SelectItem>
        <SelectItem value="month">Месяц</SelectItem>
        <SelectItem value="all">Весь период</SelectItem>
      </SelectContent>
    </Select>
  )
}
