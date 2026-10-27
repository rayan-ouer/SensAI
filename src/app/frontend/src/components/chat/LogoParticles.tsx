/*
** EPITECH PROJECT, 2026
** SensAI
** File description:
** LogoParticles
*/

import { useEffect, useRef, useState } from 'react'

const LOGO_SRC = '/logo.svg'
const LOGO_SIZE = 96
const CANVAS_SIZE = 176
const SAMPLE_STEP = 2
const MAX_DELAY = 0.35
const LOGO_FADE = 0.3
const TRANSITION_MS = 1100
const RING_RADIUS = 36
const RING_WIDTH = 9
const SPIN_PER_MS = 0.0011
const REST_COLOR = [192, 140, 34]
const RING_COLOR = [252, 211, 77]

type Particle = {
  homeX: number
  homeY: number
  angle: number
  offset: number
  delay: number
  burstX: number
  burstY: number
}

type Point = { x: number; y: number }

type Scene = { image: HTMLImageElement; particles: Particle[] }

async function loadLogo(): Promise<HTMLImageElement> {
  const image = new Image()
  image.src = LOGO_SRC
  await image.decode()
  return image
}

function sampleLogo(image: HTMLImageElement): Point[] {
  const canvas = document.createElement('canvas')
  canvas.width = canvas.height = LOGO_SIZE
  const context = canvas.getContext('2d', { willReadFrequently: true })!
  context.drawImage(image, 0, 0, LOGO_SIZE, LOGO_SIZE)
  const { data } = context.getImageData(0, 0, LOGO_SIZE, LOGO_SIZE)
  const points: Point[] = []
  for (let y = 0; y < LOGO_SIZE; y += SAMPLE_STEP)
    for (let x = 0; x < LOGO_SIZE; x += SAMPLE_STEP)
      if (data[(y * LOGO_SIZE + x) * 4 + 3] > 128)
        points.push({ x: x - LOGO_SIZE / 2, y: y - LOGO_SIZE / 2 })
  return points
}

function toParticles(points: Point[]): Particle[] {
  const sorted = points
    .map((point) => ({ ...point, direction: Math.atan2(point.y, point.x) }))
    .sort((a, b) => a.direction - b.direction)
  return sorted.map((point, index) => {
    const burst = 14 + Math.random() * 26
    return {
      homeX: point.x,
      homeY: point.y,
      angle: (index / sorted.length) * Math.PI * 2 - Math.PI,
      offset: (Math.random() - 0.5) * RING_WIDTH,
      delay: Math.random() * MAX_DELAY,
      burstX: Math.cos(point.direction) * burst + (Math.random() - 0.5) * 10,
      burstY: Math.sin(point.direction) * burst + (Math.random() - 0.5) * 10,
    }
  })
}

function easeInOut(t: number): number {
  return t < 0.5 ? 4 * t * t * t : 1 - (-2 * t + 2) ** 3 / 2
}

function mix(from: number[], to: number[], t: number): string {
  const [r, g, b] = from.map((value, i) => Math.round(value + (to[i] - value) * t))
  return `rgb(${r} ${g} ${b})`
}

function drawParticle(context: CanvasRenderingContext2D, particle: Particle, progress: number, time: number, opacity: number) {
  const local = easeInOut(Math.min(1, Math.max(0, (progress - particle.delay) / (1 - MAX_DELAY))))
  const angle = particle.angle + time * SPIN_PER_MS
  const radius = (RING_RADIUS + particle.offset) * (1 + 0.06 * Math.sin(time * 0.002 + particle.angle * 3))
  const burst = Math.sin(Math.PI * local)
  const x = particle.homeX + (Math.cos(angle) * radius - particle.homeX) * local + particle.burstX * burst
  const y = particle.homeY + (Math.sin(angle) * radius - particle.homeY) * local + particle.burstY * burst
  const size = 2.2 - 0.8 * local
  context.globalAlpha = opacity * (1 - local * 0.25 * (1 - Math.sin(angle)))
  context.fillStyle = mix(REST_COLOR, RING_COLOR, local)
  context.fillRect(x - size / 2, y - size / 2, size, size)
}

function drawFrame(canvas: HTMLCanvasElement, scene: Scene, progress: number, time: number) {
  const ratio = window.devicePixelRatio || 1
  if (canvas.width !== CANVAS_SIZE * ratio)
    canvas.width = canvas.height = CANVAS_SIZE * ratio
  const context = canvas.getContext('2d')!
  context.setTransform(ratio, 0, 0, ratio, (CANVAS_SIZE / 2) * ratio, (CANVAS_SIZE / 2) * ratio)
  context.clearRect(-CANVAS_SIZE / 2, -CANVAS_SIZE / 2, CANVAS_SIZE, CANVAS_SIZE)
  const fade = easeInOut(Math.min(1, progress / LOGO_FADE))
  context.globalAlpha = 1 - fade
  context.drawImage(scene.image, -LOGO_SIZE / 2, -LOGO_SIZE / 2, LOGO_SIZE, LOGO_SIZE)
  for (const particle of scene.particles)
    drawParticle(context, particle, progress, time, fade)
}

type LogoParticlesProps = {
  active: boolean
}

function LogoParticles({ active }: LogoParticlesProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const sceneRef = useRef<Scene | null>(null)
  const activeRef = useRef(active)
  const progressRef = useRef(0)
  const frameRef = useRef(0)
  const [resting, setResting] = useState(true)

  useEffect(() => {
    loadLogo().then((image) => {
      sceneRef.current = { image, particles: toParticles(sampleLogo(image)) }
    }).catch(() => {})
    return () => cancelAnimationFrame(frameRef.current)
  }, [])

  useEffect(() => {
    activeRef.current = active
    if (!active || frameRef.current !== 0)
      return
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    let last = performance.now()

    function step(now: number) {
      const target = activeRef.current ? 1 : 0
      const delta = reducedMotion ? 1 : (now - last) / TRANSITION_MS
      last = now
      progressRef.current = target > progressRef.current
        ? Math.min(target, progressRef.current + delta)
        : Math.max(target, progressRef.current - delta)
      if (sceneRef.current && canvasRef.current)
        drawFrame(canvasRef.current, sceneRef.current, progressRef.current, now)
      if (progressRef.current === 0 && !activeRef.current) {
        frameRef.current = 0
        setResting(true)
        return
      }
      frameRef.current = requestAnimationFrame(step)
    }
    if (sceneRef.current && canvasRef.current)
      drawFrame(canvasRef.current, sceneRef.current, progressRef.current, last)
    setResting(false)
    frameRef.current = requestAnimationFrame(step)
  }, [active])

  return (
    <div className="relative size-24" role={active ? 'status' : undefined} aria-label={active ? 'SensAI is listening' : undefined}>
      <img src={LOGO_SRC} alt="SensAI" className={`size-24 ${resting ? '' : 'invisible'}`} />
      <canvas
        ref={canvasRef}
        aria-hidden="true"
        className={`pointer-events-none absolute top-1/2 left-1/2 -translate-1/2 ${resting ? 'invisible' : ''}`}
        style={{ width: CANVAS_SIZE, height: CANVAS_SIZE }}
      />
    </div>
  )
}

export default LogoParticles
