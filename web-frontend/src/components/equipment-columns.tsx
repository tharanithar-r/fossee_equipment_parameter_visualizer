"use client"

import type { ColumnDef } from "@tanstack/react-table"
import { ArrowUpDown } from "lucide-react"
import { Button } from "@/components/ui/button"

export type Equipment = {
  id: number
  equipment_name: string
  equipment_type: string
  flowrate: number
  pressure: number
  temperature: number
}

export const columns: ColumnDef<Equipment>[] = [
  {
    accessorKey: "equipment_name",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          className="hover:bg-transparent"
        >
          Name
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      )
    },
    cell: ({ row }) => <div className="font-medium">{row.getValue("equipment_name")}</div>,
  },
  {
    accessorKey: "equipment_type",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
          className="hover:bg-transparent"
        >
          Type
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      )
    },
    cell: ({ row }) => <div>{row.getValue("equipment_type")}</div>,
  },
  {
    accessorKey: "flowrate",
    header: ({ column }) => {
      return (
        <div className="text-right">
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
            className="hover:bg-transparent"
          >
            Flowrate
            <ArrowUpDown className="ml-2 h-4 w-4" />
          </Button>
        </div>
      )
    },
    cell: ({ row }) => {
      const flowrate = parseFloat(row.getValue("flowrate"))
      return <div className="text-right font-medium">{flowrate.toFixed(1)}</div>
    },
  },
  {
    accessorKey: "pressure",
    header: ({ column }) => {
      return (
        <div className="text-right">
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
            className="hover:bg-transparent"
          >
            Pressure
            <ArrowUpDown className="ml-2 h-4 w-4" />
          </Button>
        </div>
      )
    },
    cell: ({ row }) => {
      const pressure = parseFloat(row.getValue("pressure"))
      return <div className="text-right font-medium">{pressure.toFixed(1)}</div>
    },
  },
  {
    accessorKey: "temperature",
    header: ({ column }) => {
      return (
        <div className="text-right">
          <Button
            variant="ghost"
            onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
            className="hover:bg-transparent"
          >
            Temperature
            <ArrowUpDown className="ml-2 h-4 w-4" />
          </Button>
        </div>
      )
    },
    cell: ({ row }) => {
      const temperature = parseFloat(row.getValue("temperature"))
      return <div className="text-right font-medium">{temperature.toFixed(1)}</div>
    },
  },
]
