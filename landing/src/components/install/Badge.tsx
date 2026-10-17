const LABELS: Record<string, string> = {
  enforced: "Enforced",
  experimental: "Experimental",
  advisory: "Advisory",
  "coming-soon": "Soon",
}

export function Badge({ status }: { status: string }) {
  return (
    <span className="install-badge" data-badge={status}>
      {status === "enforced" && <span className="install-badge-pulse" aria-hidden="true" />}
      <span className="install-badge-text">{LABELS[status] ?? status}</span>
    </span>
  )
}
