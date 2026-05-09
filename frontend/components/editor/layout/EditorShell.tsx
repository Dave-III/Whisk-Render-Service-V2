import Toolbar from "./Toolbar"
import Sidebar from "./Sidebar"
import PreviewPanel from "./PreviewPanel"
import InspectorPanel from "./InspectorPanel"

type Props = {
  onGenerateYoutube: () => void
  generatedTitle: string
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

  renderStage: string
  setRenderStage: (value: string) => void

  renderProgress: number
  setRenderProgress: (value: number) => void

  renderError: string | null
  setRenderError: (value: string | null) => void

  youtubeUploading: boolean
}

export default function EditorShell(props: Props) {
  return (
    <div className="h-screen bg-zinc-950 text-white flex flex-col overflow-hidden">
      <Toolbar />

      <div className="flex flex-1 overflow-hidden p-2 gap-2">
        <Sidebar {...props} />

        <PreviewPanel
          renderedVideoUrl={props.downloadUrl}
         />

        <InspectorPanel
          youtubeUploading={props.youtubeUploading}
          renderStage={props.renderStage}
          renderProgress={props.renderProgress}
          renderError={props.renderError}
          downloadUrl={props.downloadUrl}
          youtubeUrl={props.youtubeUrl}
          generatedTitle={props.generatedTitle}
          onGenerateYoutube={props.onGenerateYoutube}
        />
      </div>
    </div>
  )
}