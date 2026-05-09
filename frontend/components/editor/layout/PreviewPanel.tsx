"use client"

import { useEffect, useState } from "react"
import { useEditorStore } from "@/store/editorStore"

type Props = {
  renderedVideoUrl?: string
}

export default function PreviewPanel({
  renderedVideoUrl,
}: Props) {
  const {
    clip1,
    clip2,
    clip1Url,
    clip2Url,
    focusedVideo,
    setFocusedVideo,
} = useEditorStore()

const [localClip1Url, setLocalClip1Url] = useState("")
const [localClip2Url, setLocalClip2Url] = useState("")

useEffect(() => {

  if (!clip1) {
    setLocalClip1Url("")
    return
  }

  const objectUrl = URL.createObjectURL(clip1)

  setLocalClip1Url(objectUrl)

  return () => {
    URL.revokeObjectURL(objectUrl)
  }

}, [clip1])

useEffect(() => {

  if (!clip2) {
    setLocalClip2Url("")
    return
  }

  const objectUrl = URL.createObjectURL(clip2)

  setLocalClip2Url(objectUrl)

  return () => {
    URL.revokeObjectURL(objectUrl)
  }

}, [clip2])

  useEffect(() => {
    function handleEscape(e: KeyboardEvent) {
      if (e.key === "Escape") {
        setFocusedVideo(null)
      }
    }

    window.addEventListener("keydown", handleEscape)
    return () => window.removeEventListener("keydown", handleEscape)
  }, [setFocusedVideo])

  const finalClip1Source = localClip1Url || clip1Url
  const finalClip2Source = localClip2Url || clip2Url

  function isDirectVideoUrl(url: string) {
    return url.endsWith(".mp4") || url.includes(".mp4?")
  }

  const canPreviewClip1 = !!localClip1Url || isDirectVideoUrl(clip1Url)
  const canPreviewClip2 = !!localClip2Url || isDirectVideoUrl(clip2Url)
  if (renderedVideoUrl) {

    return (
      <div className="flex-1 min-w-0 h-full p-2">

        <div className="w-full h-full bg-zinc-950 rounded-lg border border-zinc-800 overflow-hidden">

          <div className="w-full h-full p-2">

            <div className="relative w-full h-full rounded-lg overflow-hidden border border-zinc-800 bg-black">

              <video
                src={renderedVideoUrl}
                controls
                autoPlay
                className="w-full h-full object-contain"
              />

              <div className="absolute top-3 left-3 bg-black/70 px-2 py-1 rounded text-xs text-white">
                Final Render
              </div>

            </div>

          </div>

        </div>

      </div>
    )
  }
  const layoutMode =
  focusedVideo
    ? `focused-${focusedVideo}`
    : finalClip1Source && finalClip2Source
      ? "dual"
      : "single"
  
  function renderVideo(
    src: string,
    label: string,
    focusKey: "clip1" | "clip2",
    canPreview: boolean
  ) {
    return (
      <div className="relative group w-full h-full min-h-0 bg-black rounded-lg overflow-hidden border border-zinc-800">
        {canPreview ? (
          <video
            key={`${focusKey}-${layoutMode}`}
            src={src}
            controls
            playsInline
            preload="metadata"
            className="w-full h-full object-contain bg-black"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-sm text-zinc-500 p-4 text-center">
            Preview unavailable for external URL
          </div>
        )}

        <button
          onClick={() => setFocusedVideo(focusKey)}
          className="
            absolute
            top-3
            right-3
            z-10
            rounded-md
            bg-black/70
            px-3
            py-1.5
            text-xs
            text-white
            opacity-0
            group-hover:opacity-100
            hover:bg-black
            transition-all
          "
        >
          Click to Focus
        </button>

        <div className="absolute top-3 left-3 bg-black/70 px-2 py-1 rounded text-xs text-white">
          {label}
        </div>
      </div>
    )
  }

  return (
    <div className="flex-1 min-w-0 h-full p-2">
      <div className="w-full h-full bg-zinc-950 rounded-lg border border-zinc-800 overflow-hidden">
        {!finalClip1Source && !finalClip2Source && (
          <div className="w-full h-full flex items-center justify-center text-zinc-500 text-sm">
            Video Preview
          </div>
        )}

        {finalClip1Source && !finalClip2Source && (
          <div className="w-full h-full p-2">
            {renderVideo(finalClip1Source, "Clip 1", "clip1", canPreviewClip1)}
          </div>
        )}

        {!finalClip1Source && finalClip2Source && (
          <div className="w-full h-full p-2">
            {renderVideo(finalClip2Source, "Clip 2", "clip2", canPreviewClip2)}
          </div>
        )}

        {finalClip1Source && finalClip2Source && !focusedVideo && (
          <div className="grid grid-cols-2 gap-2 p-2 w-full h-full min-h-0">
            {renderVideo(finalClip1Source, "Clip 1", "clip1", canPreviewClip1)}
            {renderVideo(finalClip2Source, "Clip 2", "clip2", canPreviewClip2)}
          </div>
        )}

        {focusedVideo === "clip1" && (
          <div className="w-full h-full p-2">
            {renderVideo(finalClip1Source, "Clip 1", "clip1", canPreviewClip1)}
          </div>
        )}

        {focusedVideo === "clip2" && (
          <div className="w-full h-full p-2">
            {renderVideo(finalClip2Source, "Clip 2", "clip2", canPreviewClip2)}
          </div>
        )}
      </div>
    </div>
  )
}
