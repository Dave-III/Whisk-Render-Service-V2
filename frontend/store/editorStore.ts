import { create } from "zustand"

type FocusedVideo =
  | "clip1"
  | "clip2"
  | null

type EditorStore = {

  clip1: File | null
  clip2: File | null

  clip1Url: string
  clip2Url: string

  focusedVideo: FocusedVideo

  setClip1: (file: File | null) => void
  setClip2: (file: File | null) => void

  setClip1Url: (url: string) => void
  setClip2Url: (url: string) => void

  setFocusedVideo: (
    video: FocusedVideo
  ) => void
}

export const useEditorStore =
  create<EditorStore>((set) => ({

    clip1: null,
    clip2: null,

    clip1Url: "",
    clip2Url: "",

    focusedVideo: null,

    setClip1: (file) =>
      set({ clip1: file }),

    setClip2: (file) =>
      set({ clip2: file }),

    setClip1Url: (url) =>
      set({ clip1Url: url }),

    setClip2Url: (url) =>
      set({ clip2Url: url }),

    setFocusedVideo: (video) =>
      set({ focusedVideo: video }),
}))