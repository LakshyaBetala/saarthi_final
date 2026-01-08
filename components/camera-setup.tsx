"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent } from "@/components/ui/card"
import { useToast } from "@/hooks/use-toast"
import { Loader2, Camera } from "lucide-react"
import { API_BASE_URL } from "@/lib/config";

interface CameraSetupProps {
  onCameraConnected: () => void
}

export function CameraSetup({ onCameraConnected }: CameraSetupProps) {
  const [ipAddress, setIpAddress] = useState("")
  const [isConnecting, setIsConnecting] = useState(false)
  const { toast } = useToast()

  const handleConnect = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!ipAddress) {
      toast({
        title: "Error",
        description: "Please enter an IP address",
        variant: "destructive",
      })
      return
    }

    setIsConnecting(true)

    try {
      const formData = new FormData()
      // ✅ FIX: Backend expects 'url', not 'ip'
      formData.append("url", ipAddress)

      const response = await fetch(`${API_BASE_URL}/set_camera_url`, {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        // If the backend sends an error message, try to read it
        const errorData = await response.json().catch(() => null);
        console.error("Connection failed:", errorData);
        throw new Error("Failed to connect to camera")
      }

      toast({
        title: "Success",
        description: "Camera connected successfully",
      })

      onCameraConnected()
    } catch (error) {
      console.error("Error connecting to camera:", error)
      toast({
        title: "Error",
        description: "Failed to connect to camera. Please check the IP address and try again.",
        variant: "destructive",
      })
    } finally {
      setIsConnecting(false)
    }
  }

  return (
    <Card className="border-2 border-primary/20">
      <CardContent className="pt-6">
        <form onSubmit={handleConnect} className="space-y-6">
          <div className="space-y-2">
            <label htmlFor="ip-address" className="text-xl font-medium block">
              Enter your phone IP address
            </label>
            <Input
              id="ip-address"
              type="text"
              placeholder="e.g., 192.168.1.4"
              value={ipAddress}
              onChange={(e) => setIpAddress(e.target.value)}
              className="h-14 text-lg"
              aria-label="IP Address"
            />
          </div>
          <Button type="submit" className="w-full h-16 text-xl font-semibold" disabled={isConnecting}>
            {isConnecting ? (
              <>
                <Loader2 className="mr-2 h-6 w-6 animate-spin" />
                Connecting...
              </>
            ) : (
              <>
                <Camera className="mr-2 h-6 w-6" />
                Connect to Camera
              </>
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}