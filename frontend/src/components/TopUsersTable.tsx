// Top users table component

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import type { TopUser } from '@/types/statistics'
import { Skeleton } from '@/components/ui/skeleton'

interface TopUsersTableProps {
  data: TopUser[]
  isLoading?: boolean
}

export default function TopUsersTable({ data, isLoading = false }: TopUsersTableProps) {
  if (isLoading) {
    return (
      <div className="space-y-2">
        {Array.from({ length: 5 }).map((_, i) => (
          <Skeleton key={i} className="h-12 w-full" />
        ))}
      </div>
    )
  }

  if (!data || data.length === 0) {
    return <div className="text-muted-foreground py-8 text-center">No users available</div>
  }

  // Take only top 10
  const topUsers = data.slice(0, 10)

  return (
    <div className="overflow-hidden rounded-lg border">
      <Table>
        <TableHeader>
          <TableRow className="bg-muted/50">
            <TableHead className="w-12">Rank</TableHead>
            <TableHead>User ID</TableHead>
            <TableHead>Username</TableHead>
            <TableHead className="text-right">Messages</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {topUsers.map((user, index) => (
            <TableRow key={user.user_id}>
              <TableCell className="text-muted-foreground font-semibold">#{index + 1}</TableCell>
              <TableCell className="font-mono text-sm">{user.user_id}</TableCell>
              <TableCell>{user.username || 'Unknown'}</TableCell>
              <TableCell className="text-right font-semibold">{user.message_count}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}
