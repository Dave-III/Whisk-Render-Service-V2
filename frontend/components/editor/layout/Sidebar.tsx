"use client"

import { useState } from "react"

import { renderVideo } from "@/services/renderService"

import { useEditorStore } from "@/store/editorStore"

export default function Sidebar() {

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

  const [loading, setLoading] = useState(false)

  const [youtubeUrl, setYoutubeUrl] = useState("")
  const [downloadUrl, setDownloadUrl] = useState("")
  const [outputFilename, setOutputFilename] = useState("")
  
  async function handleYoutubeUpload() {

    try {

      setLoading(true)

      const formData = new FormData()

      formData.append(
        "filename",
        outputFilename
      )

      const response = await fetch(
        "http://localhost:8000/upload-youtube",
        {
          method: "POST",
          body: formData,
        }
      )

      const result = await response.json()

      setYoutubeUrl(result.youtube_url)

    } catch (error) {

      console.error(error)

      alert("YouTube upload failed")

    } finally {

      setLoading(false)
    }
  }

  async function handleRender() {

    try {

      setLoading(true)

      const result = await renderVideo(
        clip1,
        clip2,
        clip1Url,
        clip2Url
      )

      setDownloadUrl(
        `http://localhost:8000${result.download_url}`
      )

      setOutputFilename(
        result.output_video.split("/").pop()
      )

    } catch (error) {

      console.error(error)

      alert("Render failed")

    } finally {

      setLoading(false)
    }
  }

  return (
    <div className="h-full p-4 overflow-y-auto">

      <h2 className="text-sm font-semibold text-white mb-6">
        Media
      </h2>

      {/* CLIP 1 */}
      <div className="mb-8">

        <label className="block text-xs text-zinc-400 mb-2">
          Clip 1 Upload
        </label>

        <input
          type="file"
          accept="video/mp4"
          onChange={(e) =>
            setClip1(e.target.files?.[0] || null)
          }
          className="
            mb-4
            block
            w-full
            text-sm
            text-zinc-300

            file:mr-4
            file:rounded-md
            file:border-0

            file:bg-zinc-800
            file:px-4
            file:py-2

            file:text-sm
            file:font-medium
            file:text-white

            hover:file:bg-zinc-900

            file:transition-colors
            file:cursor-pointer

            cursor-pointer
          "
        />

        {clip1 && (
          <div className="mb-3 text-xs text-green-400 break-all">
            {clip1.name}
          </div>
        )}

        <input
          type="text"
          placeholder="Or Medal URL..."
          value={clip1Url}
          onChange={(e) =>
            setClip1Url(e.target.value)
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
            outline-none
            focus:border-blue-500
          "
        />

      </div>

      {/* CLIP 2 */}
      <div className="mb-8">

        <label className="block text-xs text-zinc-400 mb-2">
          Clip 2 Upload
        </label>

        <input
          type="file"
          accept="video/mp4"
          onChange={(e) =>
            setClip2(e.target.files?.[0] || null)
          }
          className="
            mb-4
            block
            w-full
            text-sm
            text-zinc-300

            file:mr-4
            file:rounded-md
            file:border-0

            file:bg-zinc-800
            file:px-4
            file:py-2

            file:text-sm
            file:font-medium
            file:text-white

            hover:file:bg-zinc-900

            file:transition-colors
            file:cursor-pointer

            cursor-pointer
          "
        />

        {clip2 && (
          <div className="mb-3 text-xs text-green-400 break-all">
            {clip2.name}
          </div>
        )}

        <input
          type="text"
          placeholder="Or Medal URL..."
          value={clip2Url}
          onChange={(e) =>
            setClip2Url(e.target.value)
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
            outline-none
            focus:border-blue-500
          "
        />

      </div>

      {/* RENDER BUTTON */}
      <button
        onClick={handleRender}
        disabled={loading}
        className="
          w-full
          bg-blue-600
          hover:bg-blue-500
          disabled:bg-zinc-700
          disabled:cursor-not-allowed
          transition-colors
          rounded-md
          py-2
          text-sm
          font-medium
        "
      >
        {loading ? "Rendering..." : "Render Video"}
      </button>

      {/* RESULT */}
      {youtubeUrl && (
        <div className="mt-6">

          <div className="text-xs text-zinc-400 mb-2">
            YouTube URL
          </div>

          <a
            href={youtubeUrl}
            target="_blank"
            className="
              block
              text-sm
              text-blue-400
              break-all
              hover:text-blue-300
            "
          >
            {youtubeUrl}
          </a>

        </div>
      )}

    </div>
  )
}