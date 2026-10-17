import type { ReactNode } from "react"

export function Step({
  n,
  title,
  children,
  isLast = false,
  tag,
}: {
  n: number
  title: string
  children: ReactNode
  isLast?: boolean
  tag?: string
}) {
  return (
    <article
      className={`install-step install-step-${n}${isLast ? " is-last" : ""}`}
      style={{ "--step-idx": n } as React.CSSProperties}
    >
      <div className="install-step-track">
        <div className="install-step-badge" aria-hidden="true">
          <span className="install-step-num">{String(n).padStart(2, "0")}</span>
        </div>
        {!isLast && <div className="install-step-rail" aria-hidden="true" />}
      </div>
      <div className="install-step-body">
        <div className="install-step-header">
          <h3>{title}</h3>
          {tag ? <span className="install-step-tag">{tag}</span> : null}
        </div>
        <div className="install-step-content">{children}</div>
      </div>
    </article>
  )
}
