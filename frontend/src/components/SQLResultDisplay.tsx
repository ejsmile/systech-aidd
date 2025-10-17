import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Card } from '@/components/ui/card'

interface SQLResultDisplayProps {
  sql: string
  result: Array<Record<string, unknown>>
  interpretation: string
}

export default function SQLResultDisplay({ sql, result, interpretation }: SQLResultDisplayProps) {
  const columns = result.length > 0 ? Object.keys(result[0]) : []

  return (
    <div className="space-y-4">
      {/* SQL Query */}
      <Card className="p-4">
        <h3 className="mb-2 font-semibold">SQL Query:</h3>
        <pre className="bg-muted text-foreground overflow-x-auto rounded p-3 text-sm">
          <code>{sql}</code>
        </pre>
      </Card>

      {/* Results Table */}
      {result.length > 0 ? (
        <Card className="p-4">
          <h3 className="mb-2 font-semibold">Results:</h3>
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow>
                  {columns.map((col) => (
                    <TableHead key={col}>{col}</TableHead>
                  ))}
                </TableRow>
              </TableHeader>
              <TableBody>
                {result.map((row, idx) => (
                  <TableRow key={idx}>
                    {columns.map((col) => (
                      <TableCell key={`${idx}-${col}`}>{String(row[col] ?? 'null')}</TableCell>
                    ))}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </Card>
      ) : (
        <Card className="p-4">
          <p className="text-muted-foreground">No results returned.</p>
        </Card>
      )}

      {/* Interpretation */}
      <Card className="p-4">
        <h3 className="mb-2 font-semibold">Interpretation:</h3>
        <p className="text-foreground">{interpretation}</p>
      </Card>
    </div>
  )
}
