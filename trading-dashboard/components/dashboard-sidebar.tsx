"use client"

import { Home, BarChart3, LineChart, Settings, LogOut } from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import type { CommodityData } from "@/lib/types"

interface DashboardSidebarProps {
  commodities: CommodityData[]
  selectedCommodity: CommodityData
  onSelectCommodity: (commodity: CommodityData) => void
}

export default function DashboardSidebar({ commodities, selectedCommodity, onSelectCommodity }: DashboardSidebarProps) {
  return (
    <div className="hidden border-r bg-muted/40 md:block md:w-64">
      <div className="flex h-full max-h-screen flex-col gap-2">
        <div className="flex h-14 items-center border-b px-4 lg:h-[60px] lg:px-6">
          <span className="font-semibold">Commodities Trader</span>
        </div>
        <div className="flex-1 overflow-auto py-2">
          <nav className="grid items-start px-2 text-sm font-medium">
            <Button variant="ghost" className="justify-start gap-2">
              <Home className="h-4 w-4" />
              Dashboard
            </Button>
            <Button variant="ghost" className="justify-start gap-2">
              <BarChart3 className="h-4 w-4" />
              Analytics
            </Button>
            <Button variant="ghost" className="justify-start gap-2">
              <LineChart className="h-4 w-4" />
              Trading History
            </Button>
            <Button variant="ghost" className="justify-start gap-2">
              <Settings className="h-4 w-4" />
              Settings
            </Button>
          </nav>

          <div className="px-3 py-2">
            <h2 className="mb-2 px-2 text-xs font-semibold tracking-tight">Commodities</h2>
            <ScrollArea className="h-[300px]">
              <div className="space-y-1 p-1">
                {commodities.map((commodity) => (
                  <Button
                    key={commodity.id}
                    variant={commodity.id === selectedCommodity.id ? "secondary" : "ghost"}
                    className="w-full justify-start"
                    onClick={() => onSelectCommodity(commodity)}
                  >
                    <span className="truncate">{commodity.name}</span>
                    <span className={cn("ml-auto", commodity.change >= 0 ? "text-green-500" : "text-red-500")}>
                      {commodity.change >= 0 ? "+" : ""}
                      {commodity.change.toFixed(2)}%
                    </span>
                  </Button>
                ))}
              </div>
            </ScrollArea>
          </div>
        </div>
        <div className="mt-auto p-4">
          <Button variant="outline" className="w-full justify-start gap-2">
            <LogOut className="h-4 w-4" />
            Logout
          </Button>
        </div>
      </div>
    </div>
  )
}
