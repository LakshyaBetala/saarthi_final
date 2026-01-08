"use client"

import { useState, useRef } from "react"
import { CameraSetup } from "@/components/camera-setup"
import { ResponseDisplay } from "@/components/response-display"
import { WelcomeSection } from "@/components/welcome-section"
import { VoiceAssistant } from "@/components/voice-assistant"

export default function BharatAssistant() {
  const [cameraConnected, setCameraConnected] = useState(false)
  const [autoStartToken, setAutoStartToken] = useState(0) // 🔄 Controls the Continuous Loop
  const [response, setResponse] = useState<{
    command?: string
    action?: string
    emotion?: string
    direction?: string
    objects?: string[]
    voice_response?: string
    url?: string
  } | null>(null)

  const responseHistoryRef = useRef<Array<{
    command?: string
    timestamp: Date
  }>>([])

  const handleCameraConnected = () => {
    setCameraConnected(true)
  }

  const handleVoiceResponse = (data: any) => {
    const newResponse = {
      command: data.command || "Processing...",
      action: data.action,
      emotion: data.emotion,
      direction: data.direction,
      objects: data.objects,
      voice_response: data.voice_response,
      url: data.url
    }

    setResponse(newResponse)

    // 1. SPEAK the response (The Voice!)
    if (newResponse.voice_response) {
      // Cancel any existing speech
      window.speechSynthesis.cancel()

      const utterance = new SpeechSynthesisUtterance(newResponse.voice_response)
      utterance.lang = "en-US"
      
      // 🔄 CONTINUOUS LOOP: When speech ends, wait 1s then restart listening
      utterance.onend = () => {
        setTimeout(() => {
          console.log("🗣️ Speech finished. Restarting loop...")
          // Increment token to signal VoiceAssistant to start recording
          setAutoStartToken((prev) => prev + 1)
        }, 1000)
      }
      
      window.speechSynthesis.speak(utterance)
    }

    // 2. Open YouTube if requested (Auto-Play)
    if (newResponse.url && newResponse.action === "YouTube") {
      // Small delay to ensure browser doesn't block the popup
      setTimeout(() => {
        window.open(newResponse.url, '_blank')
      }, 1500)
    }

    // 3. Update History
    responseHistoryRef.current = [
      ...responseHistoryRef.current,
      { command: newResponse.command, timestamp: new Date() }
    ].slice(-5)
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-900 text-white p-4 max-w-xl mx-auto">
      <div className="flex-grow space-y-8">
        <WelcomeSection />

        {!cameraConnected ? (
          <CameraSetup onCameraConnected={handleCameraConnected} />
        ) : (
          <>
            {/* ✅ Pass autoStartToken to trigger recording automatically */}
            <VoiceAssistant 
              onResponse={handleVoiceResponse} 
              autoStartToken={autoStartToken} 
            />

            <div className="flex flex-col items-center space-y-4">
              <div className="w-full max-w-md mt-6">
                <div className="p-3 bg-gray-800 border border-gray-700 rounded-lg">
                  <h3 className="font-medium text-white mb-2">Try saying:</h3>
                  <ul className="space-y-1 text-sm">
                    <li className="bg-gray-700 px-3 py-1.5 rounded border border-gray-600">
                      <strong>"Bharat detect objects"</strong> - Identify obstacles & Emotion
                    </li>
                    <li className="bg-gray-700 px-3 py-1.5 rounded border border-gray-600">
                      <strong>"Bharat search Taj Mahal"</strong> - Wikipedia Summary
                    </li>
                    <li className="bg-gray-700 px-3 py-1.5 rounded border border-gray-600">
                      <strong>"Bharat play Believer"</strong> - Auto-play First Video
                    </li>
                  </ul>
                </div>
              </div>
            </div>

            {response && <ResponseDisplay response={response} />}
            
            {responseHistoryRef.current.length > 0 && (
              <div className="mt-6 bg-gray-800 p-4 rounded-lg border border-gray-700">
                <h3 className="text-lg font-medium mb-2 text-white">Recent Commands</h3>
                <ul className="space-y-1 text-sm">
                  {responseHistoryRef.current.map((resp, idx) => (
                    <li key={idx} className="p-2 bg-gray-700 rounded border border-gray-600 flex justify-between">
                      <span className="font-medium text-white">{resp.command}</span>
                      <span className="text-xs text-gray-300">
                        {resp.timestamp.toLocaleTimeString()}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </>
        )}
      </div>
      
      <footer className="mt-8 pt-4 border-t border-gray-700 text-center">
        <div className="text-sm text-gray-300">
          <p>Made with <span className="text-red-400">❤️</span> by <strong>Lakshya Betala</strong></p>
          <p className="text-xs mt-1">Version 1.0.3 | Continuous Loop</p>
        </div>
      </footer>
    </div>
  )
}