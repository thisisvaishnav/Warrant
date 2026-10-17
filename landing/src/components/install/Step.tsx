import type { ReactNode } from "react"

export function Step({
  n,
  title,
  children,
}: {
  n: number
  title: string
  children: ReactNode
}) {
  return (
    <article className="install-step">
      <div className="install-step-num" aria-hidden="true">
        {String(n).padStart(2, "0")}
      </div>
      <div className="install-step-body">
        <h3>{title}</h3>
        {children}
      </div>
    </article>
  )
}
