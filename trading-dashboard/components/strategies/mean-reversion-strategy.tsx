"use client"

import { cn } from "@/lib/utils"

import { useState } from "react"
import { ArrowDownIcon, ArrowUpIcon, InfoIcon, RefreshCw, Settings2 } from "lucide-react"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Slider } from "@/components/ui/slider"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import type { CommodityData } from "@/lib/types"
import PriceChart from "@/components/charts/price-chart"
import ZScoreChart from "@/components/charts/z-score-chart"

interface MeanReversionStrategyProps {
  commodity: CommodityData
}

export default function MeanReversionStrategy({ commodity }: MeanReversionStrategyProps) {
  const [lookbackPeriod, setLookbackPeriod] = useState(20)
  const [zScoreThreshold, setZScoreThreshold] = useState(2)
  const [positionSize, setPositionSize] = useState(10)
  const [autoTrade, setAutoTrade] = useState(false)

  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      {/* Strategy Overview */}
      <Card className="lg:col-span-2">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <div className="space-y-1">
            <CardTitle>Mean Reversion Strategy</CardTitle>
            <CardDescription>Trading based on price returning to its historical average</CardDescription>
          </div>
          <Button variant="outline" size="icon">
            <RefreshCw className="h-4 w-4" />
            <span className="sr-only">Refresh data</span>
          </Button>
        </CardHeader>
        <CardContent className="pt-4">
          <Tabs defaultValue="price">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="price">Price Chart</TabsTrigger>
              <TabsTrigger value="zscore">Z-Score</TabsTrigger>
            </TabsList>
            <TabsContent value="price" className="space-y-4">
              <div className="h-[300px]">
                <PriceChart commodity={commodity} />
              </div>
            </TabsContent>
            <TabsContent value="zscore" className="space-y-4">
              <div className="h-[300px]">
                <ZScoreChart commodity={commodity} />
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>

      {/* Strategy Parameters */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            Strategy Parameters
            <Button variant="ghost" size="icon" className="h-6 w-6">
              <Settings2 className="h-4 w-4" />
            </Button>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="lookback-period">Lookback Period</Label>
              <span className="text-sm">{lookbackPeriod} days</span>
            </div>
            <Slider
              id="lookback-period"
              min={5}
              max={100}
              step={1}
              value={[lookbackPeriod]}
              onValueChange={(value) => setLookbackPeriod(value[0])}
            />
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label htmlFor="zscore-threshold">Z-Score Threshold</Label>
              <span className="text-sm">±{zScoreThreshold.toFixed(1)}</span>
            </div>
            <Slider
              id="zscore-threshold"
              min={1}
              max={3}
              step={0.1}
              value={[zScoreThreshold]}
              onValueChange={(value) => setZScoreThreshold(value[0])}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="position-size">Position Size (%)</Label>
            <div className="flex items-center space-x-2">
              <Input
                id="position-size"
                type="number"
                value={positionSize}
                onChange={(e) => setPositionSize(Number(e.target.value))}
                min={1}
                max={100}
              />
              <Select defaultValue="usd">
                <SelectTrigger className="w-[100px]">
                  <SelectValue placeholder="Unit" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="usd">USD</SelectItem>
                  <SelectItem value="percent">Percent</SelectItem>
                  <SelectItem value="contracts">Contracts</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="flex items-center space-x-2 pt-2">
            <Switch id="auto-trade" checked={autoTrade} onCheckedChange={setAutoTrade} />
            <Label htmlFor="auto-trade">Auto-Trade</Label>
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <InfoIcon className="h-4 w-4 text-muted-foreground" />
                </TooltipTrigger>
                <TooltipContent>
                  <p>Automatically execute trades based on strategy signals</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          </div>
        </CardContent>
      </Card>

      {/* Signal Strength */}
      <Card className="lg:col-span-2">
        <CardHeader>
          <CardTitle>Current Signal</CardTitle>
          <CardDescription>Based on {lookbackPeriod}-day mean reversion</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Z-Score</p>
              <p className="text-2xl font-bold">{commodity.zScore.toFixed(2)}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Mean Price</p>
              <p className="text-2xl font-bold">${commodity.meanPrice.toFixed(2)}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Standard Deviation</p>
              <p className="text-2xl font-bold">{commodity.standardDeviation.toFixed(2)}</p>
            </div>
          </div>

          <div className="mt-6 flex items-center justify-center">
            <div className="text-center">
              <p className="text-sm text-muted-foreground">Signal Strength</p>
              <div
                className={cn(
                  "mt-2 text-3xl font-bold",
                  commodity.zScore < -zScoreThreshold
                    ? "text-green-500"
                    : commodity.zScore > zScoreThreshold
                      ? "text-red-500"
                      : "text-yellow-500",
                )}
              >
                {commodity.zScore < -zScoreThreshold
                  ? "Strong Buy"
                  : commodity.zScore > zScoreThreshold
                    ? "Strong Sell"
                    : "Neutral"}
              </div>
            </div>
          </div>
        </CardContent>
        <CardFooter className="flex justify-between">
          <Button variant="outline" className="w-[48%]" disabled={commodity.zScore > -0.5}>
            <ArrowUpIcon className="mr-2 h-4 w-4 text-green-500" />
            Buy
          </Button>
          <Button variant="outline" className="w-[48%]" disabled={commodity.zScore < 0.5}>
            <ArrowDownIcon className="mr-2 h-4 w-4 text-red-500" />
            Sell
          </Button>
        </CardFooter>
      </Card>

      {/* Trade History */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Trades</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between border-b pb-2">
              <div className="flex items-center">
                <div className="h-2 w-2 rounded-full bg-green-500 mr-2"></div>
                <span>Buy</span>
              </div>
              <span className="text-sm">$2305.20</span>
              <span className="text-xs text-muted-foreground">2h ago</span>
            </div>
            <div className="flex items-center justify-between border-b pb-2">
              <div className="flex items-center">
                <div className="h-2 w-2 rounded-full bg-red-500 mr-2"></div>
                <span>Sell</span>
              </div>
              <span className="text-sm">$2325.80</span>
              <span className="text-xs text-muted-foreground">1d ago</span>
            </div>
            <div className="flex items-center justify-between border-b pb-2">
              <div className="flex items-center">
                <div className="h-2 w-2 rounded-full bg-green-500 mr-2"></div>
                <span>Buy</span>
              </div>
              <span className="text-sm">$2290.15</span>
              <span className="text-xs text-muted-foreground">3d ago</span>
            </div>
          </div>
        </CardContent>
        <CardFooter>
          <Button variant="ghost" className="w-full text-sm">
            View All Trades
          </Button>
        </CardFooter>
      </Card>
    </div>
  )
}
