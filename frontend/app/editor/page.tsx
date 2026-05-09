"use client"

import { useState } from "react"
import EditorShell from "@/components/editor/layout/EditorShell"

export default function EditorPage() {

  const [autoSync, setAutoSync] = useState(true)

  const [levelName, setLevelName] = useState("")
  const [runTime, setRunTime] = useState("")
  const [foamPlayer, setFoamPlayer] = useState("")
  const [lunaPlayer, setLunaPlayer] = useState("")

  const [loading, setLoading] = useState(false)

  const [downloadUrl, setDownloadUrl] = useState("")
  const [youtubeUrl, setYoutubeUrl] = useState("")
  const [outputFilename, setOutputFilename] = useState("")

  const [renderStage, setRenderStage] = useState("Idle")
  const [renderProgress, setRenderProgress] = useState(0)
  const [renderError, setRenderError] = useState<string | null>(null)

  const [youtubeUploading, setYoutubeUploading] = useState(false)

  const [copied, setCopied] = useState(false)

  async function handleYoutubeUpload() {

    if (!outputFilename) return

    try {

      setYoutubeUploading(true)
      const formData = new FormData()

      formData.append(
        "filename",
        outputFilename
      )

      formData.append(
        "title",
        `${levelName} ${runTime} | Foam: ${foamPlayer} | Luna: ${lunaPlayer}`
      )

      const response = await fetch(
        "http://localhost:8000/upload-youtube",
        {
          method: "POST",
          body: formData,
        }
      )

      if (!response.ok) {
        throw new Error("YouTube upload failed")
      }

      const data = await response.json()

      setYoutubeUrl(data.youtube_url)

    } catch (error) {

      console.error(error)

      alert("Failed to upload to YouTube")
    }

    finally {
      setYoutubeUploading(false)
    }
  }

  return (
    <EditorShell
      youtubeUploading={youtubeUploading}
      renderStage={renderStage}
      setRenderStage={setRenderStage}
      renderProgress={renderProgress}
      setRenderProgress={setRenderProgress}
      renderError={renderError}
      setRenderError={setRenderError}
      autoSync={autoSync}
      setAutoSync={setAutoSync}
      levelName={levelName}
      setLevelName={setLevelName}
      runTime={runTime}
      setRunTime={setRunTime}
      foamPlayer={foamPlayer}
      setFoamPlayer={setFoamPlayer}
      lunaPlayer={lunaPlayer}
      setLunaPlayer={setLunaPlayer}
      loading={loading}
      setLoading={setLoading}
      downloadUrl={downloadUrl}
      setDownloadUrl={setDownloadUrl}
      youtubeUrl={youtubeUrl}
      setYoutubeUrl={setYoutubeUrl}
      outputFilename={outputFilename}
      setOutputFilename={setOutputFilename}
      generatedTitle={`${levelName.replaceAll(" ", "_")}_${runTime}`}
      onGenerateYoutube={handleYoutubeUpload}
    />
  )
}