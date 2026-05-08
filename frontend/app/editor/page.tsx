"use client"

import { useState } from "react"

import EditorShell from "@/components/editor/layout/EditorShell"

export default function EditorPage() {

  const [levelName, setLevelName] = useState("")
  const [runTime, setRunTime] = useState("")

  const [foamPlayer, setFoamPlayer] = useState("")
  const [lunaPlayer, setLunaPlayer] = useState("")

  const [loading, setLoading] = useState(false)

  const [downloadUrl, setDownloadUrl] = useState("")
  const [youtubeUrl, setYoutubeUrl] = useState("")

  return (
    <EditorShell

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
    />
  )
}