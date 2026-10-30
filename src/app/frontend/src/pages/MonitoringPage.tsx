import { useEffect, useState } from 'react'
import { Activity, ArrowLeft, RefreshCw } from 'lucide-react'

const API_URL = import.meta.env.VITE_API_URL ?? '/api'

type MonitoringEvent = {
  id: string
  occurred_at: string
  event_type: 'interaction' | 'llm_call' | 'tool_call'
  conversation_id: string | null
  model: string | null
  profile: string | null
  prompt: string | null
  response: string | null
  tool_name: string | null
  tool_arguments: Record<string, unknown> | null
  tool_result: unknown
  latency_ms: number | null
  prompt_tokens: number | null
  completion_tokens: number | null
  success: boolean
  error: string | null
}

type SeriesPoint = {
  date: string
  call_volume: number
  average_latency_ms: number | null
  error_rate: number
  average_response_tokens: number | null
}

type MonitoringData = {
  metrics: {
    interaction_count: number
    average_latency_ms: number | null
    error_rate: number
    prompt_tokens: number
    completion_tokens: number
    response_size_drift_percent: number | null
    drift_baseline_response_tokens: number | null
    drift_recent_response_tokens: number | null
  }
  series: SeriesPoint[]
  events: MonitoringEvent[]
}

function MetricCard({ label, value, note }: { label: string; value: string; note: string }) {
  return (
    <article className="rounded-xl border border-white/10 bg-white/[0.04] p-5">
      <p className="text-xs font-medium uppercase tracking-[0.14em] text-amber-100/50">{label}</p>
      <p className="mt-3 text-3xl font-semibold tracking-tight text-amber-50">{value}</p>
      <p className="mt-2 text-xs text-amber-100/45">{note}</p>
    </article>
  )
}

function TrendChart({
  title,
  points,
  color,
  format = (value: number) => String(value),
}: {
  title: string
  points: Array<number | null>
  color: string
  format?: (value: number) => string
}) {
  const width = 720
  const height = 180
  const values = points.filter((value): value is number => value !== null)
  const max = Math.max(...values, 1)
  const coords = points.map((value, index) => {
    const x = points.length < 2 ? width / 2 : 8 + (index / (points.length - 1)) * (width - 16)
    const y = value === null ? height - 20 : height - 20 - (value / max) * (height - 38)
    return { x, y, value }
  })

  return (
    <article className="rounded-xl border border-white/10 bg-white/[0.04] p-5">
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-sm font-medium text-amber-50">{title}</h2>
        {values.length > 0 && <span className="text-xs text-amber-100/45">{format(Math.max(...values))} peak</span>}
      </div>
      <svg viewBox={`0 0 ${width} ${height}`} className="h-40 w-full" role="img" aria-label={`${title} over 14 days`}>
        {[0, 1, 2].map((line) => {
          const y = 16 + line * 48
          return <line key={line} x1="0" x2={width} y1={y} y2={y} stroke="currentColor" className="text-white/10" />
        })}
        {coords.length > 1 && <polyline points={coords.map(({ x, y }) => `${x},${y}`).join(' ')} fill="none" stroke={color} strokeWidth="3" strokeLinejoin="round" strokeLinecap="round" />}
        {coords.map(({ x, y, value }, index) => value === null ? null : (
          <circle key={index} cx={x} cy={y} r="3" fill={color}>
            <title>{`${value} on ${index}`}</title>
          </circle>
        ))}
      </svg>
      <div className="mt-1 flex justify-between text-[10px] text-amber-100/35">
        <span>{'14 days ago'}</span><span>Today</span>
      </div>
    </article>
  )
}

function EventDetails({ event }: { event: MonitoringEvent }) {
  return (
    <details className="group border-t border-white/[0.07] px-4 py-3 first:border-t-0">
      <summary className="flex cursor-pointer list-none flex-wrap items-center gap-x-3 gap-y-1 text-xs">
        <span className={`size-2 rounded-full ${event.success ? 'bg-emerald-400' : 'bg-rose-400'}`} />
        <time className="text-amber-100/45">{new Date(event.occurred_at).toLocaleString()}</time>
        <span className="font-medium text-amber-50">{event.event_type.replace('_', ' ')}</span>
        {event.tool_name && <span className="text-violet-200">{event.tool_name}</span>}
        {event.model && <span className="text-amber-100/45">{event.model}</span>}
        {event.latency_ms !== null && <span className="ml-auto text-amber-100/55">{Math.round(event.latency_ms)} ms</span>}
        {event.prompt_tokens !== null && <span className="text-amber-100/45">{(event.prompt_tokens ?? 0) + (event.completion_tokens ?? 0)} tokens</span>}
      </summary>
      <div className="mt-3 grid gap-3 pl-5 text-xs text-amber-100/75">
        {event.prompt && <div><p className="mb-1 uppercase tracking-wider text-amber-100/40">Prompt sent</p><pre className="max-h-48 overflow-auto whitespace-pre-wrap rounded-lg bg-black/20 p-3 font-sans">{event.prompt}</pre></div>}
        {event.response && <div><p className="mb-1 uppercase tracking-wider text-amber-100/40">Response</p><pre className="max-h-48 overflow-auto whitespace-pre-wrap rounded-lg bg-black/20 p-3 font-sans">{event.response}</pre></div>}
        {event.tool_arguments && <div><p className="mb-1 uppercase tracking-wider text-amber-100/40">Tool arguments</p><pre className="overflow-auto rounded-lg bg-black/20 p-3">{JSON.stringify(event.tool_arguments, null, 2)}</pre></div>}
        {event.tool_result !== null && <div><p className="mb-1 uppercase tracking-wider text-amber-100/40">Tool result</p><pre className="max-h-48 overflow-auto whitespace-pre-wrap rounded-lg bg-black/20 p-3">{JSON.stringify(event.tool_result, null, 2)}</pre></div>}
        {event.error && <p className="text-rose-300">{event.error}</p>}
      </div>
    </details>
  )
}

function MonitoringPage({ onBack }: { onBack: () => void }) {
  const [data, setData] = useState<MonitoringData | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [refreshKey, setRefreshKey] = useState(0)

  useEffect(() => {
    let active = true
    async function load() {
      try {
        const response = await fetch(`${API_URL}/monitoring/summary`)
        if (!response.ok)
          throw new Error(`Monitoring request failed (${response.status})`)
        const result = await response.json() as MonitoringData
        if (active) {
          setData(result)
          setError(null)
        }
      } catch (reason) {
        if (active)
          setError(reason instanceof Error ? reason.message : 'Could not load monitoring data.')
      }
    }
    void load()
    const timer = window.setInterval(() => void load(), 15_000)
    return () => {
      active = false
      window.clearInterval(timer)
    }
  }, [refreshKey])

  const metrics = data?.metrics
  return (
    <main className="h-dvh overflow-y-auto text-amber-50">
      <div className="mx-auto max-w-7xl px-5 py-7 md:px-8">
        <header className="mb-8 flex flex-wrap items-center justify-between gap-4">
          <div>
            <button type="button" onClick={onBack} className="mb-4 flex items-center gap-2 text-xs text-amber-100/55 hover:text-amber-50"><ArrowLeft className="size-4" /> Back to chat</button>
            <div className="flex items-center gap-3"><Activity className="size-5 text-amber-200" /><h1 className="text-2xl font-semibold tracking-tight">Logging &amp; monitoring</h1></div>
            <p className="mt-1 text-sm text-amber-100/50">Live interaction telemetry · last 14 days</p>
          </div>
          <button type="button" onClick={() => setRefreshKey((key) => key + 1)} className="flex items-center gap-2 rounded-lg border border-white/10 px-3 py-2 text-xs text-amber-100/65 hover:bg-white/5"><RefreshCw className="size-3.5" /> Refresh</button>
        </header>

        {error && <p role="alert" className="mb-5 rounded-lg border border-rose-400/20 bg-rose-400/10 p-4 text-sm text-rose-200">{error}</p>}
        {!data && !error && <p className="py-16 text-center text-sm text-amber-100/50">Loading telemetry…</p>}
        {metrics && data && <>
          <section className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
            <MetricCard label="Interactions" value={metrics.interaction_count.toLocaleString()} note="Completed and failed user turns" />
            <MetricCard label="Average latency" value={metrics.average_latency_ms === null ? '—' : `${(metrics.average_latency_ms / 1000).toFixed(2)} s`} note="End-to-end turn duration" />
            <MetricCard label="Error rate" value={`${(metrics.error_rate * 100).toFixed(1)}%`} note="Failed turns / all turns" />
            <MetricCard label="Tokens" value={(metrics.prompt_tokens + metrics.completion_tokens).toLocaleString()} note={`${metrics.prompt_tokens.toLocaleString()} prompt · ${metrics.completion_tokens.toLocaleString()} completion`} />
          </section>

          <section className="mt-5 grid gap-3 lg:grid-cols-2">
            <TrendChart title="Call volume · daily interactions" points={data.series.map((point) => point.call_volume)} color="#fbbf24" />
            <TrendChart title="Average latency · daily" points={data.series.map((point) => point.average_latency_ms)} color="#a78bfa" format={(value) => `${(value / 1000).toFixed(1)}s`} />
            <TrendChart title="Error rate · daily" points={data.series.map((point) => point.error_rate * 100)} color="#fb7185" format={(value) => `${value.toFixed(0)}%`} />
            <TrendChart title="Response-size drift · completion tokens" points={data.series.map((point) => point.average_response_tokens)} color="#34d399" />
          </section>
          <p className="mt-3 text-xs text-amber-100/40">
            Response-size drift compares average completion tokens in the recent 7 days with the prior 7 days
            {metrics.response_size_drift_percent === null ? ' (not enough token data yet).' : ` (${metrics.response_size_drift_percent >= 0 ? '+' : ''}${metrics.response_size_drift_percent.toFixed(1)}%).`}
            It is a volume signal, not a semantic quality or model-drift detector.
          </p>

          <section className="mt-8 overflow-hidden rounded-xl border border-white/10 bg-white/[0.035]">
            <div className="border-b border-white/10 px-4 py-4"><h2 className="text-sm font-medium">Recent interaction trace</h2><p className="mt-1 text-xs text-amber-100/45">Prompts, model replies, tool activity and errors · newest first</p></div>
            {data.events.length ? data.events.map((event) => <EventDetails key={event.id} event={event} />) : <p className="p-6 text-sm text-amber-100/45">No interactions recorded yet. Send a message in chat to start collecting telemetry.</p>}
          </section>
          <p className="mt-4 text-xs text-amber-100/35">Telemetry is stored locally in the configured SQLite file. Prompt and tool content may contain sensitive data.</p>
        </>}
      </div>
    </main>
  )
}

export default MonitoringPage
