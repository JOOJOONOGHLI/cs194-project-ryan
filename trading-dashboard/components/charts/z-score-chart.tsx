"use client"

import { useEffect, useRef } from "react"
import type { CommodityData } from "@/lib/types"

interface ZScoreChartProps {
  commodity: CommodityData
}

export default function ZScoreChart({ commodity }: ZScoreChartProps) {
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

    // Generate mock z-score data based on historical prices
    const zScores = commodity.historicalPrices.map((price, i, arr) => {
      if (i === 0) return 0
      const prevPrice = arr[i - 1]
      return (price - commodity.meanPrice) / commodity.standardDeviation
    })

    // Calculate min and max for scaling
    const minZScore = Math.min(-3, Math.min(...zScores))
    const maxZScore = Math.max(3, Math.max(...zScores))

    // Draw axes
    ctx.beginPath()
    ctx.strokeStyle = "#94a3b8"
    ctx.lineWidth = 1
    ctx.moveTo(padding, padding)
    ctx.lineTo(padding, height - padding)
    ctx.lineTo(width - padding, height - padding)
    ctx.stroke()

    // Draw zero line
    const zeroY = height - padding - ((0 - minZScore) / (maxZScore - minZScore)) * (height - 2 * padding)
    ctx.beginPath()
    ctx.strokeStyle = "#94a3b8"
    ctx.setLineDash([5, 3])
    ctx.moveTo(padding, zeroY)
    ctx.lineTo(width - padding, zeroY)
    ctx.stroke()
    ctx.setLineDash([])

    // Draw threshold lines
    const upperThresholdY = height - padding - ((2 - minZScore) / (maxZScore - minZScore)) * (height - 2 * padding)
    const lowerThresholdY = height - padding - ((-2 - minZScore) / (maxZScore - minZScore)) * (height - 2 * padding)

    ctx.beginPath()
    ctx.strokeStyle = "#ef4444"
    ctx.setLineDash([2, 2])
    ctx.moveTo(padding, upperThresholdY)
    ctx.lineTo(width - padding, upperThresholdY)
    ctx.stroke()

    ctx.beginPath()
    ctx.strokeStyle = "#22c55e"
    ctx.moveTo(padding, lowerThresholdY)
    ctx.lineTo(width - padding, lowerThresholdY)
    ctx.stroke()
    ctx.setLineDash([])

    // Draw z-score line
    ctx.beginPath()
    ctx.strokeStyle = "#8b5cf6"
    ctx.lineWidth = 2

    const xStep = (width - 2 * padding) / (zScores.length - 1)

    zScores.forEach((zScore, i) => {
      const x = padding + i * xStep
      const y = height - padding - ((zScore - minZScore) / (maxZScore - minZScore)) * (height - 2 * padding)

      if (i === 0) {
        ctx.moveTo(x, y)
      } else {
        ctx.lineTo(x, y)
      }
    })

    ctx.stroke()

    // Draw labels
    ctx.fillStyle = "#64748b"
    ctx.font = "10px sans-serif"
    ctx.textAlign = "right"
    ctx.fillText(maxZScore.toFixed(1), padding - 5, padding)
    ctx.fillText(minZScore.toFixed(1), padding - 5, height - padding)
    ctx.fillText("0", padding - 5, zeroY)

    ctx.fillStyle = "#ef4444"
    ctx.fillText("+2 (Sell)", width - padding, upperThresholdY - 5)

    ctx.fillStyle = "#22c55e"
    ctx.fillText("-2 (Buy)", width - padding, lowerThresholdY - 5)

    // Draw current z-score
    const currentZScore = commodity.zScore
    const currentY = height - padding - ((currentZScore - minZScore) / (maxZScore - minZScore)) * (height - 2 * padding)

    ctx.beginPath()
    ctx.arc(width - padding, currentY, 4, 0, 2 * Math.PI)
    ctx.fillStyle = "#8b5cf6"
    ctx.fill()

    ctx.fillStyle = "#0f172a"
    ctx.textAlign = "left"
    ctx.fillText("Current: " + currentZScore.toFixed(2), width - padding - 100, currentY)
  }, [commodity])

  return <canvas ref={canvasRef} width={800} height={300} className="w-full h-full" />
}
