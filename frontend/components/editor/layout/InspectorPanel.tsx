"use client"

import { useMemo } from "react"

type Props = {
  levelName: string
  setLevelName: (
    value: string
  ) => void

  runTime: string
  setRunTime: (
    value: string
  ) => void

  foamPlayer: string
  setFoamPlayer: (
    value: string
  ) => void

  lunaPlayer: string
  setLunaPlayer: (
    value: string
  ) => void

  loading: boolean

  downloadUrl: string
  youtubeUrl: string

  onYoutubeUpload: () => void
}

export default function InspectorPanel({
  levelName,
  setLevelName,

  runTime,
  setRunTime,

  foamPlayer,
  setFoamPlayer,

  lunaPlayer,
  setLunaPlayer,

  loading,

  downloadUrl,
  youtubeUrl,

  onYoutubeUpload,
}: Props) {

  const generatedTitle = useMemo(() => {

    if (
      !levelName ||
      !runTime ||
      !foamPlayer ||
      !lunaPlayer
    ) {
      return "Generated title preview..."
    }

    return (
      `${levelName} — ` +
      `${runTime} | ` +
      `Foam: ${foamPlayer} | ` +
      `Luna: ${lunaPlayer}`
    )

  }, [
    levelName,
    runTime,
    foamPlayer,
    lunaPlayer,
  ])

  return (
    <div className="w-80 h-full p-4 overflow-y-auto border-l border-zinc-800">

      <h2 className="text-sm font-semibold text-white mb-6">
        Run Details
      </h2>

      <div className="space-y-4">

        <input
          type="text"
          placeholder="Level Name"
          value={levelName}
          onChange={(e) =>
            setLevelName(e.target.value)
          }
          className="
            w-full
            bg-zinc-900
            border
            border-zinc-800
            rounded-md
            px-3
            py-2
            text-sm
          "
        />

        <input
          type="text"
          placeholder="Time (12.483)"
          value={runTime}
          onChange={(e) =>
            setRunTime(e.target.value)
          }
          className="
            w-full
            bg-zinc-900
            border
            border-zinc-800
            rounded-md
            px-3
            py-2
            text-sm
          "
        />

        <input
          type="text"
          placeholder="Foam Player"
          value={foamPlayer}
          onChange={(e) =>
            setFoamPlayer(e.target.value)
          }
          className="
            w-full
            bg-zinc-900
            border
            border-zinc-800
            rounded-md
            px-3
            py-2
            text-sm
          "
        />

        <input
          type="text"
          placeholder="Luna Player"
          value={lunaPlayer}
          onChange={(e) =>
            setLunaPlayer(e.target.value)
          }
          className="
            w-full
            bg-zinc-900
            border
            border-zinc-800
            rounded-md
            px-3
            py-2
            text-sm
          "
        />

      </div>

      <div className="mt-8">

        <div className="text-xs text-zinc-400 mb-2">
          Generated Title
        </div>

        <div
          className="
            rounded-md
            border
            border-zinc-800
            bg-zinc-900
            p-3
            text-sm
            text-white
            break-words
          "
        >
          {generatedTitle}
        </div>

      </div>

      {downloadUrl && (

        <div className="mt-8 space-y-3">

          <a
            href={downloadUrl}
            download
            className="
              block
              w-full
              rounded-md
              bg-green-600
              hover:bg-green-500
              transition-colors
              py-2
              text-center
              text-sm
              font-medium
            "
          >
            Download Video
          </a>

          <button
            onClick={onYoutubeUpload}
            disabled={loading}
            className="
              w-full
              rounded-md
              bg-red-600
              hover:bg-red-500
              transition-colors
              py-2
              text-sm
              font-medium
            "
          >
            Generate YouTube URL
          </button>

        </div>

      )}

      {youtubeUrl && (

        <div className="mt-8">

          <div className="text-xs text-zinc-400 mb-2">
            YouTube URL
          </div>

          <div
            className="
              rounded-md
              border
              border-zinc-800
              bg-zinc-900
              p-3
              text-sm
              break-all
            "
          >
            {youtubeUrl}
          </div>

        </div>

      )}

    </div>
  )
}