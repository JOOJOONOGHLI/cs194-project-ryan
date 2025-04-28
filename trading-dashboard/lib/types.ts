export interface CommodityData {
  id: string
  name: string
  symbol: string
  price: number
  change: number
  volume: number
  historicalPrices: number[]
  meanPrice: number
  standardDeviation: number
  zScore: number
  signalStrength: string
}
