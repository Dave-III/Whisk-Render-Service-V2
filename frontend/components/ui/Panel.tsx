interface PanelProps {
  children: React.ReactNode
  className?: string
}

export default function Panel({
  children,
  className = "",
}: PanelProps) {
  return (
    <div
      className={`
        bg-zinc-900
        border
        border-zinc-800
        rounded-lg
        ${className}
      `}
    >
      {children}
    </div>
  )
}