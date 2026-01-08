"use client"

import { useState, useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Mic } from "lucide-react"
import { VoiceWave } from "@/components/voice-wave"

interface VoiceAssistantProps {
  onResponse?: (data: any) => void
  autoStartToken?: number // New Prop: Changing this number triggers recording
}

export function VoiceAssistant({ onResponse, autoStartToken }: VoiceAssistantProps) {
  const [isListening, setIsListening] = useState(false)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)

  // ✅ Auto-Start Effect
  useEffect(() => {
    if (autoStartToken && autoStartToken > 0) {
      console.log("🔄 Auto-starting listening...")
      startRecording()
    }
  }, [autoStartToken])

  const startRecording = async () => {
    try {
      if (isListening) return // Don't double start

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const recorder = new MediaRecorder(stream)
      const chunks: Blob[] = []

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunks.push(e.data)
      }

      recorder.onstop = async () => {
        const blob = new Blob(chunks, { type: "audio/webm" })
        setIsListening(false) // Visual update
        await sendAudioToBackend(blob)
      }

      recorder.start()
      mediaRecorderRef.current = recorder
      setIsListening(true)
    } catch (err) {
      console.error("Mic Error:", err)
      setIsListening(false)
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== "inactive") {
      mediaRecorderRef.current.stop()
      mediaRecorderRef.current.stream.getTracks().forEach((t) => t.stop())
    }
  }

  const sendAudioToBackend = async (audioBlob: Blob) => {
    const formData = new FormData()
    formData.append("file", audioBlob, "voice_command.webm")

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000"
      const response = await fetch(`${apiUrl}/assistant/audio`, {
        method: "POST",
        body: formData,
      })

      if (!response.ok) throw new Error("Backend Error")

      const data = await response.json()
      if (onResponse) onResponse(data)
      
    } catch (error) {
      console.error("API Error:", error)
    }
  }

  return (
    <div className="flex flex-col items-center space-y-6">
      <Button
        onClick={isListening ? stopRecording : startRecording}
        className={`
          w-full max-w-xs h-24 rounded-full text-xl font-semibold
          transition-all duration-300 ease-in-out
          ${isListening ? "bg-red-500 hover:bg-red-600 shadow-lg scale-105" : "bg-primary hover:scale-105"}
        `}
      >
        {isListening ? (
          <div className="flex items-center">
            <VoiceWave active={true} /> 
            <span className="ml-3">Listening...</span>
          </div>
        ) : (
          <>
            <Mic className="mr-2 h-8 w-8" />
            <span>🎤 Tap to Start</span>
          </>
        )}
      </Button>
    </div>
  )
}