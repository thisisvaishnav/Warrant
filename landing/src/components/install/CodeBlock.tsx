import { useEffect, useRef, useState } from "react"
import { Check, Copy, Terminal } from "lucide-react"

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
  label,
  isCommand = true,
}: {
  value: string
  compact?: boolean
  label?: string
  isCommand?: boolean
}) {
  const [copied, setCopied] = useState(false)
  const timer = useRef<number>(0)

  useEffect(() => () => window.clearTimeout(timer.current), [])

  const onCopy = async () => {
    const ok = await copyText(value)
    if (!ok) return
    setCopied(true)
    window.clearTimeout(timer.current)
    timer.current = window.setTimeout(() => setCopied(false), 1800)
  }

  const displayLabel = label ?? (compact ? "terminal" : "zsh")

  return (
    <div className={`install-code-wrap${compact ? " compact" : ""}`}>
      <div className="install-code-header">
        <div className="install-code-dots" aria-hidden="true">
          <span className="dot dot-close" />
          <span className="dot dot-min" />
          <span className="dot dot-max" />
        </div>
        <div className="install-code-title">
          <Terminal className="install-code-term-icon" size={12} aria-hidden="true" />
          <span>{displayLabel}</span>
        </div>
        <button
          className="install-copy-btn"
          onClick={onCopy}
          data-copied={copied}
          type="button"
          aria-label={copied ? "Copied command to clipboard" : "Copy command to clipboard"}
        >
          {copied ? (
            <>
              <Check className="install-copy-icon icon-copied" size={13} aria-hidden="true" />
              <span>Copied!</span>
            </>
          ) : (
            <>
              <Copy className="install-copy-icon" size={13} aria-hidden="true" />
              <span>Copy</span>
            </>
          )}
        </button>
      </div>

      <div className="install-code-body">
        <pre className="install-code">
          <code>
            {isCommand && !compact && <span className="install-prompt-symbol" aria-hidden="true">$ </span>}
            {value}
          </code>
        </pre>
      </div>
    </div>
  )
}
