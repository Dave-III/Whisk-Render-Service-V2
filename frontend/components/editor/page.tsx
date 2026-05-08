import {
  PanelGroup,
  Panel,
  PanelResizeHandle,
} from "react-resizable-panels"

import Sidebar from "./components/Sidebar"
import Timeline from "./components/Timeline"
import Inspector from "./components/Inspector"

export default function EditorPage() {
  return (
    <div className="h-screen bg-zinc-950 text-white">
      <PanelGroup direction="horizontal">

        <Panel defaultSize={20}>
          <Sidebar />
        </Panel>

        <PanelResizeHandle className="w-1 bg-zinc-800" />

        <Panel>
          <Timeline />
        </Panel>

        <PanelResizeHandle className="w-1 bg-zinc-800" />

        <Panel defaultSize={25}>
          <Inspector />
        </Panel>

      </PanelGroup>
    </div>
  )
}