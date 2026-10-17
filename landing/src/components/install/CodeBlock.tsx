import { useEffect, useRef, useState } from "react"

async function copyText(text: string): Promise<boolean> {
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text)
      return true
    }
  } catch {
    // clipboard API blocked (insecure context, sandbox) — fall through
  }
  try {
    const ta = document.createElement("textarea")
    ta.value = text
    ta.style.position = "fixed"
    ta.style.opacity = "0"
    document.body.appendChild(ta)
    ta.select()
    const ok = document.execCommand("copy")
    document.body.removeChild(ta)
    return ok
  } catch {
    return false
  }
}

export function CodeBlock({
  value,
  compact = false,
}: {
  value: string
  compact?: boolean
}) {
  const [copied, setCopied] = useState(false)
  const timer = useRef<number>(0)

  useEffect(() => () => window.clearTimeout(timer.current), [])

  const onCopy = async () => {
    const ok = await copyText(value)
    if (!ok) return
    setCopied(true)
    window.clearTimeout(timer.current)
    timer.current = window.setTimeout(() => setCopied(false), 1500)
  }

  return (
    <div className={`install-code-wrap${compact ? " compact" : ""}`}>
      <pre className="install-code">
        <code>{value}</code>
      </pre>
      <button
        className="install-copy"
        onClick={onCopy}
        data-copied={copied}
        aria-label={copied ? "Copied to clipboard" : "Copy to clipboard"}
      >
        {copied ? "Copied" : "Copy"}
      </button>
    </div>
  )
}
