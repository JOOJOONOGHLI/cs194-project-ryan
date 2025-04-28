import { Bell, Settings } from "lucide-react"
import { Button } from "@/components/ui/button"
import type { CommodityData } from "@/lib/types"

interface DashboardHeaderProps {
  commodity: CommodityData
}

export default function DashboardHeader({ commodity }: DashboardHeaderProps) {
  return (
    <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-14 items-center px-4 md:px-6">
        <div className="flex-1">
          <h1 className="text-xl font-semibold">
            {commodity.name} ({commodity.symbol})
          </h1>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="icon">
            <Bell className="h-4 w-4" />
            <span className="sr-only">Notifications</span>
          </Button>
          <Button variant="outline" size="icon">
            <Settings className="h-4 w-4" />
            <span className="sr-only">Settings</span>
          </Button>
        </div>
      </div>
    </header>
  )
}
