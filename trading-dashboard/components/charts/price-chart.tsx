"use client"

import { useEffect, useRef } from "react"
import type { CommodityData } from "@/lib/types"

interface PriceChartProps {
  commodity: CommodityData
}

export default function PriceChart({ commodity }: PriceChartProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    if (!canvasRef.current) return

    const canvas = canvasRef.current
    const ctx = canvas.getContext("2d")
    if (!ctx) return

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    // Set dimensions
    const width = canvas.width
    const height = canvas.height
    const padding = 40

    // Get data
    const prices = commodity.historicalPrices
    const meanPrice = commodity.meanPrice

    // Calculate min and max for scaling
    const minPrice = Math.min(...prices) * 0.995
    const maxPrice = Math.max(...prices) * 1.005

    // Draw axes
    ctx.beginPath()
    ctx.strokeStyle = "#94a3b8"
    ctx.lineWidth = 1
    ctx.moveTo(padding, padding)
    ctx.lineTo(padding, height - padding)
    ctx.lineTo(width - padding, height - padding)
    ctx.stroke()

    // Draw price line
    ctx.beginPath()
    ctx.strokeStyle = "#0ea5e9"
    ctx.lineWidth = 2

    const xStep = (width - 2 * padding) / (prices.length - 1)

    prices.forEach((price, i) => {
      const x = padding + i * xStep
      const y = height - padding - ((price - minPrice) / (maxPrice - minPrice)) * (height - 2 * padding)

      if (i === 0) {
        ctx.moveTo(x, y)
      } else {
        ctx.lineTo(x, y)
      }
    })

    ctx.stroke()

    // Draw mean line
    const meanY = height - padding - ((meanPrice - minPrice) / (maxPrice - minPrice)) * (height - 2 * padding)

    ctx.beginPath()
    ctx.strokeStyle = "#f59e0b"
    ctx.lineWidth = 1
    ctx.setLineDash([5, 3])
    ctx.moveTo(padding, meanY)
    ctx.lineTo(width - padding, meanY)
    ctx.stroke()
    ctx.setLineDash([])

    // Draw labels
    ctx.fillStyle = "#64748b"
    ctx.font = "10px sans-serif"
    ctx.textAlign = "right"
    ctx.fillText(maxPrice.toFixed(2), padding - 5, padding)
    ctx.fillText(minPrice.toFixed(2), padding - 5, height - padding)
    ctx.fillText("Mean: " + meanPrice.toFixed(2), width - padding, meanY - 5)

    // Draw current price
    const currentPrice = prices[prices.length - 1]
    const currentX = padding + (prices.length - 1) * xStep
    const currentY = height - padding - ((currentPrice - minPrice) / (maxPrice - minPrice)) * (height - 2 * padding)

    ctx.beginPath()
    ctx.arc(currentX, currentY, 4, 0, 2 * Math.PI)
    ctx.fillStyle = "#0ea5e9"
    ctx.fill()

    ctx.fillStyle = "#0f172a"
    ctx.textAlign = "left"
    ctx.fillText("Current: " + currentPrice.toFixed(2), currentX + 10, currentY)
  }, [commodity])

  return <canvas ref={canvasRef} width={800} height={300} className="w-full h-full" />
}
