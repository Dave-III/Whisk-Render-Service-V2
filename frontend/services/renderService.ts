const API_URL = "http://localhost:8000"

export async function renderVideo(
  clip1: File | null,
  clip2: File | null,
  clip1Url?: string,
  clip2Url?: string
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