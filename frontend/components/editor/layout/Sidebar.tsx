"use client"

import { useEffect, useMemo } from "react"
import { renderVideo, getRenderStatus } from "@/services/renderStatusService"
import { useEditorStore } from "@/store/editorStore"


type Props = {
  renderStage: string
  setRenderStage: (value: string) => void

  renderProgress: number
  setRenderProgress: (value: number) => void

  renderError: string | null
  setRenderError: (value: string | null) => void
  autoSync: boolean
  setAutoSync: (value: boolean) => void

  levelName: string
  setLevelName: (value: string) => void

  runTime: string
  setRunTime: (value: string) => void

  foamPlayer: string
  setFoamPlayer: (value: string) => void

  lunaPlayer: string
  setLunaPlayer: (value: string) => void

  loading: boolean
  setLoading: (value: boolean) => void

  setDownloadUrl: (value: string) => void
  setYoutubeUrl: (value: string) => void

  setOutputFilename: (value: string) => void
}

export default function Sidebar({
  renderStage,
  setRenderStage,

  renderProgress,
  setRenderProgress,

  renderError,
  setRenderError,

  autoSync,
  setAutoSync,

  levelName,
  setLevelName,

  runTime,
  setRunTime,

  foamPlayer,
  setFoamPlayer,

  lunaPlayer,
  setLunaPlayer,

  loading,
  setLoading,

  setDownloadUrl,
  setYoutubeUrl,
  setOutputFilename,
}: Props) {
  const {
    clip1,
    clip2,
    clip1Url,
    clip2Url,
    setClip1,
    setClip2,
    setClip1Url,
    setClip2Url,
  } = useEditorStore()

  const generatedTitle = useMemo(() => {
    if (!levelName || !runTime || !foamPlayer || !lunaPlayer) {
      return "Generated title preview..."
    }

    return `${levelName} ${runTime} | Foam: ${foamPlayer} | Luna: ${lunaPlayer}`
  }, [levelName, runTime, foamPlayer, lunaPlayer])

  useEffect(() => {

    if (!loading) return

    const interval = setInterval(async () => {

      try {

        const status = await getRenderStatus()

        setRenderStage(status.stage)

        setRenderProgress(status.progress)

        setRenderError(status.error)

        if (!status.is_rendering) {
          if (status.download_url) {

            setDownloadUrl(
              `http://localhost:8000${status.download_url}`
            )

          }

          if (status.output_filename) {

            setOutputFilename(
              status.output_filename
            )

          }

          setLoading(false)
          clearInterval(interval)

        }

      } catch (error) {

        console.error(error)

      }

    }, 500)

    return () => clearInterval(interval)

  }, [
    loading,
    setRenderStage,
    setRenderProgress,
    setRenderError,
  ])

  async function handleRender() {
    try {
      setLoading(false)

      if (!levelName || !runTime) {
        alert("Level name and runtime required")
        return
      }

      if (!clip1 && !clip1Url) {
        alert("Clip 1 missing")
        return
      }

      if (!clip2 && !clip2Url) {
        alert("Clip 2 missing")
        return
      }

      setLoading(true)
      setYoutubeUrl("")
      setDownloadUrl("")
      setOutputFilename("")



      await renderVideo(
        clip1,
        clip2,
        clip1Url,
        clip2Url,
        autoSync,
        `${levelName}_${runTime}`
      )

    } catch (error) {

      console.error(error)

      setLoading(false)

      alert("Render failed")
    }
  }

  return (
    <div className="w-80 h-full border-r border-zinc-800 bg-zinc-950 p-4 overflow-y-auto">
      <h2 className="text-sm font-semibold text-white mb-6">
        Upload & Details
      </h2>

      <div className="space-y-6">
        <div>
          <div className="text-xs text-zinc-400 mb-2">Clip 1</div>

          <input
            type="file"
            accept="video/mp4"
            onChange={(e) => setClip1(e.target.files?.[0] || null)}
            className="
              block w-full text-sm text-zinc-300
              file:mr-4 file:rounded-md file:border-0
              file:bg-zinc-800 file:px-4 file:py-2
              file:text-sm file:font-medium file:text-white
              hover:file:bg-zinc-900 file:transition-colors
              file:cursor-pointer cursor-pointer
            "
          />

          {clip1 && (
            <div className="mt-2 text-xs text-green-400 break-all">
              {clip1.name}
            </div>
          )}

          <input
            type="text"
            placeholder="Or paste Clip 1 URL"
            value={clip1Url}
            onChange={(e) => setClip1Url(e.target.value)}
            className="mt-3 w-full rounded-md border border-zinc-800 bg-zinc-900 px-3 py-2 text-sm outline-none focus:border-blue-500"
          />
        </div>

        <div>
          <div className="text-xs text-zinc-400 mb-2">Clip 2</div>

          <input
            type="file"
            accept="video/mp4"
            onChange={(e) => setClip2(e.target.files?.[0] || null)}
            className="
              block w-full text-sm text-zinc-300
              file:mr-4 file:rounded-md file:border-0
              file:bg-zinc-800 file:px-4 file:py-2
              file:text-sm file:font-medium file:text-white
              hover:file:bg-zinc-900 file:transition-colors
              file:cursor-pointer cursor-pointer
            "
          />

          {clip2 && (
            <div className="mt-2 text-xs text-green-400 break-all">
              {clip2.name}
            </div>
          )}

          <input
            type="text"
            placeholder="Or paste Clip 2 URL"
            value={clip2Url}
            onChange={(e) => setClip2Url(e.target.value)}
            className="mt-3 w-full rounded-md border border-zinc-800 bg-zinc-900 px-3 py-2 text-sm outline-none focus:border-blue-500"
          />
        </div>

        <label className="flex items-center gap-3 text-sm text-zinc-300">
          <input
            type="checkbox"
            checked={autoSync}
            onChange={(e) => setAutoSync(e.target.checked)}
          />
          Auto-sync runs
        </label>

        <div className="space-y-3">
          <input
            type="text"
            placeholder="Level Name"
            value={levelName}
            onChange={(e) => setLevelName(e.target.value)}
            className="w-full rounded-md border border-zinc-800 bg-zinc-900 px-3 py-2 text-sm outline-none focus:border-blue-500"
          />

          <input
            type="text"
            placeholder="Run Time (12.483)"
            value={runTime}
            onChange={(e) => setRunTime(e.target.value)}
            className="w-full rounded-md border border-zinc-800 bg-zinc-900 px-3 py-2 text-sm outline-none focus:border-blue-500"
          />

          <input
            type="text"
            placeholder="Foam Player"
            value={foamPlayer}
            onChange={(e) => setFoamPlayer(e.target.value)}
            className="w-full rounded-md border border-zinc-800 bg-zinc-900 px-3 py-2 text-sm outline-none focus:border-blue-500"
          />

          <input
            type="text"
            placeholder="Luna Player"
            value={lunaPlayer}
            onChange={(e) => setLunaPlayer(e.target.value)}
            className="w-full rounded-md border border-zinc-800 bg-zinc-900 px-3 py-2 text-sm outline-none focus:border-blue-500"
          />
        </div>

        <div>
          <div className="text-xs text-zinc-400 mb-2">
            Generated Title
          </div>

          <div className="rounded-md border border-zinc-800 bg-zinc-900 p-3 text-sm text-white break-words">
            {generatedTitle}
          </div>
        </div>

        <button
          onClick={handleRender}
          disabled={loading}
          className="
            w-full rounded-md bg-blue-600 hover:bg-blue-500
            disabled:bg-zinc-700 disabled:cursor-not-allowed
            transition-colors py-3 text-sm font-semibold text-white
          "
        >
          {loading ? "Rendering..." : "Render Video"}
        </button>
      </div>
    </div>
  )
}