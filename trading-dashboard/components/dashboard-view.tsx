"use client"

import { useState } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import DashboardHeader from "@/components/dashboard-header"
import DashboardSidebar from "@/components/dashboard-sidebar"
import MeanReversionStrategy from "@/components/strategies/mean-reversion-strategy"
import type { CommodityData } from "@/lib/types"

// Mock data for demonstration
const mockCommodities: CommodityData[] = [
  {
    id: "gold",
    name: "Gold",
    symbol: "GC",
    price: 2318.45,
    change: 0.32,
    volume: 234567,
    historicalPrices: [2310, 2315, 2305, 2320, 2318, 2325, 2330, 2315, 2318.45],
    meanPrice: 2317.38,
    standardDeviation: 8.23,
    zScore: 0.13,
    signalStrength: "Neutral",
  },
  {
    id: "silver",
    name: "Silver",
    symbol: "SI",
    price: 27.32,
    change: -0.45,
    volume: 189234,
    historicalPrices: [27.5, 27.8, 27.6, 27.4, 27.2, 27.1, 27.3, 27.4, 27.32],
    meanPrice: 27.4,
    standardDeviation: 0.22,
    zScore: -0.36,
    signalStrength: "Weak Buy",
  },
  {
    id: "crude-oil",
    name: "Crude Oil",
    symbol: "CL",
    price: 78.65,
    change: 1.23,
    volume: 345678,
    historicalPrices: [76.5, 77.2, 77.8, 78.1, 78.4, 78.9, 79.2, 78.8, 78.65],
    meanPrice: 78.17,
    standardDeviation: 0.87,
    zScore: 0.55,
    signalStrength: "Weak Sell",
  },
  {
    id: "natural-gas",
    name: "Natural Gas",
    symbol: "NG",
    price: 2.15,
    change: -0.08,
    volume: 156789,
    historicalPrices: [2.25, 2.22, 2.18, 2.16, 2.14, 2.12, 2.16, 2.18, 2.15],
    meanPrice: 2.17,
    standardDeviation: 0.04,
    zScore: -0.5,
    signalStrength: "Moderate Buy",
  },
  {
    id: "copper",
    name: "Copper",
    symbol: "HG",
    price: 4.52,
    change: 0.05,
    volume: 123456,
    historicalPrices: [4.45, 4.48, 4.5, 4.53, 4.55, 4.54, 4.51, 4.5, 4.52],
    meanPrice: 4.51,
    standardDeviation: 0.03,
    zScore: 0.33,
    signalStrength: "Neutral",
  },
]

export default function DashboardView() {
  const [selectedCommodity, setSelectedCommodity] = useState<CommodityData>(mockCommodities[0])

  return (
    <div className="flex h-screen bg-background">
      <DashboardSidebar
        commodities={mockCommodities}
        selectedCommodity={selectedCommodity}
        onSelectCommodity={setSelectedCommodity}
      />

      <div className="flex flex-col flex-1 overflow-hidden">
        <DashboardHeader commodity={selectedCommodity} />

        <main className="flex-1 overflow-auto p-4 md:p-6">
          <Tabs defaultValue="mean-reversion" className="w-full">
            <TabsList className="grid w-full max-w-md grid-cols-3">
              <TabsTrigger value="mean-reversion">Mean Reversion</TabsTrigger>
              <TabsTrigger value="trend-following" disabled>
                Trend Following
              </TabsTrigger>
              <TabsTrigger value="breakout" disabled>
                Breakout
              </TabsTrigger>
            </TabsList>

            <TabsContent value="mean-reversion" className="mt-4">
              <MeanReversionStrategy commodity={selectedCommodity} />
            </TabsContent>

            <TabsContent value="trend-following">
              <div className="rounded-lg border p-8 text-center">
                <h3 className="text-lg font-medium">Trend Following Strategy</h3>
                <p className="text-muted-foreground mt-2">This strategy is not implemented yet.</p>
              </div>
            </TabsContent>

            <TabsContent value="breakout">
              <div className="rounded-lg border p-8 text-center">
                <h3 className="text-lg font-medium">Breakout Strategy</h3>
                <p className="text-muted-foreground mt-2">This strategy is not implemented yet.</p>
              </div>
            </TabsContent>
          </Tabs>
        </main>
      </div>
    </div>
  )
}
