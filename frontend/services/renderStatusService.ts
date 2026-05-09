const API_URL = "http://localhost:8000"

export async function getRenderStatus() {
  const response = await fetch(`${API_URL}/render-status`)

  if (!response.ok) {
    throw new Error("Failed to fetch render status")
  }

  return response.json()
}


export async function renderVideo(
  clip1: File | null,
  clip2: File | null,
  clip1Url?: string,
  clip2Url?: string,
  autosync?: boolean,
  outputName?: string
) {
  const formData = new FormData()

  if (clip1) {
    formData.append("clip1", clip1)
  }

  if (clip2) {
    formData.append("clip2", clip2)
  }

  if (clip1Url) {
    formData.append("clip1_url", clip1Url)
  }

  if (clip2Url) {
    formData.append("clip2_url", clip2Url)
  }

  formData.append("auto_sync", String(autosync))

  if (outputName) {
    formData.append("output_name", outputName)
  }

  const response = await fetch(
    `${API_URL}/render`,
    {
      method: "POST",
      body: formData,
    }
  )

  if (!response.ok) {
    throw new Error("Render failed")
  }

  return response.json()
}