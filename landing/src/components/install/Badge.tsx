const LABELS: Record<string, string> = {
  enforced: "Enforced",
  experimental: "Experimental",
  advisory: "Advisory",
  "coming-soon": "Soon",
}

export function Badge({ status }: { status: string }) {
  return (
    <span className="install-badge" data-badge={status}>
      {LABELS[status] ?? status}
    </span>
  )
}
