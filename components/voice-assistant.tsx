"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Mic } from "lucide-react"
import { VoiceWave } from "@/components/voice-wave"

// Prop to pass the AI's response back to the main chat window
interface VoiceAssistantProps {
  onResponse?: (data: any) => void
}

export function VoiceAssistant({ onResponse }: VoiceAssistantProps) {
  const [isListening, setIsListening] = useState(false)
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null)

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const recorder = new MediaRecorder(stream)
      const chunks: Blob[] = []

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunks.push(e.data)
      }

      recorder.onstop = async () => {
        const blob = new Blob(chunks, { type: "audio/webm" })
        await sendAudioToBackend(blob)
      }

      recorder.start()
      setMediaRecorder(recorder)
      setIsListening(true)
    } catch (err) {
      console.error("Microphone Access Denied:", err)
      alert("Please allow microphone access to use the assistant.")
    }
  }

  const stopRecording = () => {
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
      mediaRecorder.stop()
      // Stop all tracks to release the microphone
      mediaRecorder.stream.getTracks().forEach((track) => track.stop())
    }
    setIsListening(false)
  }

  const sendAudioToBackend = async (audioBlob: Blob) => {
    const formData = new FormData()
    formData.append("file", audioBlob, "voice_command.webm")

    try {
      // Use the environment variable for the API URL
      const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000"
      const response = await fetch(`${apiUrl}/assistant/audio`, {
        method: "POST",
        body: formData,
      })

      if (!response.ok) throw new Error("Backend failed to process audio")

      const data = await response.json()
      console.log("AI Response:", data)

      // Send data back to parent to update UI
      if (onResponse) {
        onResponse(data)
      }
    } catch (error) {
      console.error("Backend Error:", error)
    }
  }

  const toggleListening = () => {
    if (isListening) {
      stopRecording()
    } else {
      startRecording()
    }
  }

  return (
    <div className="flex flex-col items-center space-y-6">
      <Button
        onClick={toggleListening}
        className={`
          w-full max-w-xs h-24 rounded-full text-xl font-semibold
          transition-all duration-300 ease-in-out
          ${isListening ? "bg-red-500 hover:bg-red-600 shadow-lg scale-105" : "bg-primary hover:scale-105"}
        `}
        aria-label={isListening ? "Stop Listening" : "Start Bharat Assistant"}
      >
        {isListening ? (
          <div className="flex items-center">
            {/* ✅ FIX: Added active={true} prop here */}
            <VoiceWave active={true} /> 
            <span className="ml-3">Stop Listening</span>
          </div>
        ) : (
          <>
            <Mic className="mr-2 h-8 w-8" />
            <span>🎤 Start Assistant</span>
          </>
        )}
      </Button>

      {isListening && (
        <p className="text-center text-lg text-muted-foreground animate-pulse">
          Listening... <br />
          <span className="text-sm">(Say "Bharat detect objects" or "Bharat search...")</span>
        </p>
      )}
    </div>
  )
}