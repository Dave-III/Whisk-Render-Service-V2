import Toolbar from "./Toolbar"
import Sidebar from "./Sidebar"
import PreviewPanel from "./PreviewPanel"
import InspectorPanel from "./InspectorPanel"

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
  setLoading: (
    value: boolean
  ) => void

  downloadUrl: string
  setDownloadUrl: (
    value: string
  ) => void

  youtubeUrl: string
  setYoutubeUrl: (
    value: string
  ) => void
}

export default function EditorShell({

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

  downloadUrl,
  setDownloadUrl,

  youtubeUrl,
  setYoutubeUrl,

}: Props) {

  return (
    <div className="h-screen bg-zinc-950 text-white flex flex-col overflow-hidden">

      <Toolbar />

      <div className="flex flex-1 overflow-hidden p-2 gap-2">

        <Sidebar

          loading={loading}
          setLoading={setLoading}

          setDownloadUrl={setDownloadUrl}
          setYoutubeUrl={setYoutubeUrl}
        />

        <PreviewPanel />

        <InspectorPanel

          levelName={levelName}
          setLevelName={setLevelName}

          runTime={runTime}
          setRunTime={setRunTime}

          foamPlayer={foamPlayer}
          setFoamPlayer={setFoamPlayer}

          lunaPlayer={lunaPlayer}
          setLunaPlayer={setLunaPlayer}

          loading={loading}

          downloadUrl={downloadUrl}
          youtubeUrl={youtubeUrl}

          onYoutubeUpload={() => {}}
        />

      </div>

    </div>
  )
}