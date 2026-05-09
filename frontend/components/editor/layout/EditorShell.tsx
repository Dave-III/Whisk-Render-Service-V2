import Toolbar from "./Toolbar"
import Sidebar from "./Sidebar"
import PreviewPanel from "./PreviewPanel"
import InspectorPanel from "./InspectorPanel"

type Props = {
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

  downloadUrl: string
  setDownloadUrl: (value: string) => void

  youtubeUrl: string
  setYoutubeUrl: (value: string) => void

  outputFilename: string
  setOutputFilename: (value: string) => void
}

export default function EditorShell(props: Props) {
  return (
    <div className="h-screen bg-zinc-950 text-white flex flex-col overflow-hidden">
      <Toolbar />

      <div className="flex flex-1 overflow-hidden p-2 gap-2">
        <Sidebar {...props} />

        <PreviewPanel />

        <InspectorPanel />
      </div>
    </div>
  )
}