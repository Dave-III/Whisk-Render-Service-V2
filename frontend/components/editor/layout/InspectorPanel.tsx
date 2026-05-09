"use client"

type Props = {
  renderStage: string
  renderProgress: number
  renderError: string | null
  downloadUrl: string
  youtubeUrl: string
  generatedTitle: string
  onGenerateYoutube: () => void
  youtubeUploading: boolean
}

export default function InspectorPanel({
  renderStage,
  renderProgress,
  renderError,
  downloadUrl,
  youtubeUrl,
  generatedTitle,
  onGenerateYoutube,
  youtubeUploading,
}: Props) {

  return (

    <div className="w-80 h-full border-l border-zinc-800 bg-zinc-950 p-4 overflow-y-auto">

      <h2 className="text-sm font-semibold text-white mb-6">
        Render Output
      </h2>

      <div className="mb-6">

        <div className="text-xs text-zinc-400 mb-2">
          Current Stage
        </div>

        <div className="text-sm text-white mb-3">
          {renderStage}
        </div>

        <div className="h-2 w-full rounded-full bg-zinc-800 overflow-hidden">

          <div
            className="h-full bg-blue-500 transition-all duration-1000 ease-in-out"
            style={{
              width: `${renderProgress}%`
            }}
          />

        </div>

        <div className="text-xs text-zinc-500 mt-2">
          {renderProgress}%
        </div>

      </div>

      {renderError && (

        <div className="rounded-md border border-red-900 bg-red-950 p-3 text-sm text-red-300 mb-4">
          {renderError}
        </div>

      )}

      {downloadUrl && (

        <a
          href={downloadUrl}
          download={`${generatedTitle} Rendered.mp4`}
          className="
            block
            w-full
            rounded-md
            bg-green-600
            hover:bg-green-500
            transition-colors
            py-3
            text-center
            text-sm
            font-semibold
            text-white
            mb-4
          "
        >
          Download Video
        </a>

      )}
      {downloadUrl && !youtubeUrl && (

        <button
          onClick={onGenerateYoutube}
          disabled={youtubeUploading}
          className="
            w-full
            rounded-md
            bg-red-600
            hover:bg-red-500
            transition-colors
            py-3
            text-sm
            font-semibold
            text-white
            mb-4
          "
        >
          Generate YouTube URL
        </button>

      )}
      {youtubeUrl && (

        <div>

          <div className="text-xs text-zinc-400 mb-2">
            YouTube URL
          </div>

          <a
            href={youtubeUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="
              block
              w-full
              rounded-md
              border
              border-zinc-700
              bg-zinc-900
              px-3
              py-3
              text-left
              text-sm
              text-white
              break-all
              hover:border-blue-500
              transition-colors
            "
          >
            {youtubeUrl}
          </a>

        </div>

      )}

    </div>

  )
}