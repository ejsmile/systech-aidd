// Dashboard страница - статистика использования бота

import { useState, useEffect, useCallback } from 'react'
import type { StatisticsResponse } from '@/types/statistics'
import { getStatistics } from '@/api/statistics'
import { APIError } from '@/api/client'
import MetricCard from '@/components/MetricCard'
import MessagesByDateChart from '@/components/MessagesByDateChart'
import TopUsersTable from '@/components/TopUsersTable'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'

const REFRESH_INTERVAL = 30000 // 30 seconds

export default function Dashboard() {
  const [statistics, setStatistics] = useState<StatisticsResponse | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date())

  const loadStatistics = useCallback(async () => {
    try {
      setIsLoading(true)
      setError(null)
      const data = await getStatistics()
      setStatistics(data)
      setLastUpdate(new Date())
    } catch (err) {
      const message =
        err instanceof APIError
          ? `API Error: ${err.message}`
          : 'Failed to load statistics. Please try again.'
      setError(message)
      console.error('Failed to load statistics:', err)
    } finally {
      setIsLoading(false)
    }
  }, [])

  // Initial load and auto-refresh setup
  useEffect(() => {
    loadStatistics()

    // Set up auto-refresh interval
    const interval = setInterval(() => {
      loadStatistics()
    }, REFRESH_INTERVAL)

    return () => clearInterval(interval)
  }, [loadStatistics])

  const formatNumber = (value: number): string => {
    return value.toLocaleString()
  }

  const formatFloat = (value: number): string => {
    return value.toFixed(2)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-muted-foreground mt-2">
          Статистика использования бота и активности пользователей
        </p>
        <p className="text-muted-foreground mt-2 text-xs">
          Последнее обновление: {lastUpdate.toLocaleTimeString()}
        </p>
      </div>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive">
          <AlertDescription className="flex items-center justify-between">
            <span>{error}</span>
            <button
              onClick={loadStatistics}
              className="bg-destructive-foreground text-destructive hover:bg-destructive-foreground/90 ml-4 rounded px-3 py-1 text-sm"
            >
              Retry
            </button>
          </AlertDescription>
        </Alert>
      )}

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
        <MetricCard
          title="Всего пользователей"
          value={statistics?.total_users ?? 0}
          isLoading={isLoading}
          icon="👥"
          format={formatNumber}
        />
        <MetricCard
          title="Активные пользователи"
          value={statistics?.active_users ?? 0}
          isLoading={isLoading}
          icon="✅"
          format={formatNumber}
        />
        <MetricCard
          title="Всего сообщений"
          value={statistics?.total_messages ?? 0}
          isLoading={isLoading}
          icon="💬"
          format={formatNumber}
        />
        <MetricCard
          title="Среднее на пользователя"
          value={statistics?.avg_messages_per_user ?? 0}
          isLoading={isLoading}
          icon="📊"
          format={formatFloat}
        />
      </div>

      {/* Charts and Tables */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Messages by Date Chart */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>Сообщения по датам</CardTitle>
              <CardDescription>Распределение сообщений за последние 30 дней</CardDescription>
            </CardHeader>
            <CardContent>
              <MessagesByDateChart
                data={statistics?.messages_by_date ?? []}
                isLoading={isLoading}
              />
            </CardContent>
          </Card>
        </div>

        {/* Statistics Summary */}
        <div>
          <Card className="h-full">
            <CardHeader>
              <CardTitle>Статистика</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {isLoading ? (
                <div className="space-y-3">
                  {Array.from({ length: 3 }).map((_, i) => (
                    <div key={i} className="bg-muted h-6 animate-pulse rounded" />
                  ))}
                </div>
              ) : (
                <div className="space-y-3 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Активность:</span>
                    <span className="font-semibold">
                      {statistics
                        ? ((statistics.active_users / statistics.total_users) * 100).toFixed(1)
                        : 0}
                      %
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Среднее:</span>
                    <span className="font-semibold">
                      {statistics?.avg_messages_per_user.toFixed(2) ?? 0}
                    </span>
                  </div>
                  <hr className="my-2" />
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Всего:</span>
                    <span className="font-semibold">
                      {formatNumber(statistics?.total_messages ?? 0)}
                    </span>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Top Users Table */}
      <Card>
        <CardHeader>
          <CardTitle>Топ активные пользователи</CardTitle>
          <CardDescription>Пользователи с наибольшим количеством сообщений</CardDescription>
        </CardHeader>
        <CardContent>
          <TopUsersTable data={statistics?.top_users ?? []} isLoading={isLoading} />
        </CardContent>
      </Card>
    </div>
  )
}
