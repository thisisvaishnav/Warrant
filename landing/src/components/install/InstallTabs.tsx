import { useCallback, useRef, useState } from "react"
import { Tabs, TabsContent, TabsIndicator, TabsList, TabsTrigger } from "@/components/ui/tabs"
import agents from "@/data/agents.json"
import { Badge } from "./Badge"
import { CodeBlock } from "./CodeBlock"
import { Step } from "./Step"
import { AgentIcon } from "./AgentIcon"
import { ArrowRight, CheckCircle2, FileCode, RotateCcw } from "lucide-react"

type Agent = (typeof agents)[number]

const GITHUB_URL = "https://github.com/thisisvaishnav/guard"
const STORAGE_KEY = "guard-install-agent"

function initialValue(): string {
  if (typeof window === "undefined") return agents[0].id
  const requested = new URLSearchParams(window.location.search).get("agent")
  if (requested && agents.some((a) => a.id === requested)) return requested
  try {
    const saved = window.localStorage.getItem(STORAGE_KEY)
    if (saved && agents.some((a) => a.id === saved)) return saved
  } catch {
    // private mode blocks localStorage
  }
  return agents[0].id
}

function InstallSteps({ agent }: { agent: Agent }) {
  return (
    <div className="install-steps-wrapper">
      <div className="install-agent-banner">
        <div className="install-agent-banner-icon" aria-hidden="true">
          <AgentIcon id={agent.id} size={22} />
        </div>
        <div className="install-agent-banner-info">
          <h3 className="install-agent-banner-title">{agent.label}</h3>
          <span className="install-agent-banner-sub">Hook configuration &amp; verification</span>
        </div>
      </div>

      <Step n={1} title="Run in your project folder" tag="One command">
        <p>
          The command configures Guard&apos;s enforcement hook for{" "}
          <strong>{agent.label}</strong> (safe to re-run). No extra setup
          step: <code className="install-inline-code">uvx</code> runs Guard on demand.
        </p>
        <CodeBlock value={agent.run ?? ""} label="bash" isCommand />
        {agent.runNote ? (
          <p className="install-runnote">{agent.runNote}</p>
        ) : null}

        <div className="install-writes-box">
          <div className="install-writes-label">
            <FileCode size={13} className="install-writes-icon" aria-hidden="true" />
            <span>Files configured automatically:</span>
          </div>
          <div className="install-writes">
            {agent.writes.map((w) => (
              <span key={w} className="install-file-pill">
                <code>{w}</code>
              </span>
            ))}
          </div>
        </div>
      </Step>

      <Step n={2} title="Restart your agent" tag="Reload">
        <div className="install-restart-box">
          <div className="install-restart-icon-wrap" aria-hidden="true">
            <RotateCcw size={15} className="install-restart-icon" />
          </div>
          <p className="install-restart-text">{agent.restart}</p>
        </div>
      </Step>

      <Step n={3} title="Verify integration" tag="Doctor check" isLast>
        <p>Run the diagnostic check in your terminal to ensure hooks are active:</p>
        <CodeBlock value={agent.verify ?? "guard doctor"} label="verify" compact isCommand />
        <div className="install-verify-expected">
          <div className="install-verify-header">
            <CheckCircle2 size={13} className="install-verify-icon" aria-hidden="true" />
            <span>Expected health report:</span>
          </div>
          <CodeBlock
            value={agent.expected ?? ""}
            label="doctor report"
            compact
            isCommand={false}
          />
        </div>
        {agent.note ? <p className="install-runnote">{agent.note}</p> : null}
      </Step>
    </div>
  )
}

function ComingSoon({ agent }: { agent: Agent }) {
  return (
    <div className="install-soon-card">
      <div className="install-soon-badge-wrap">
        <span className="install-soon-status">Phase 3 · Roadmap</span>
      </div>
      <div className="install-agent-banner">
        <div className="install-agent-banner-icon" aria-hidden="true">
          <AgentIcon id={agent.id} size={22} />
        </div>
        <div className="install-agent-banner-info">
          <h3 className="install-agent-banner-title">{agent.label}</h3>
          <span className="install-agent-banner-sub">Native MCP integration in development</span>
        </div>
      </div>
      <p>
        Full native hook integration for <strong>{agent.label}</strong> is
        scheduled with the Guard MCP server release. In the interim, Guard
        safeguards Claude Code and Antigravity, and a git{" "}
        <code className="install-inline-code">pre-push</code> hook protects your team.
      </p>

      {agent.format ? (
        <div className="install-soon-preview">
          <div className="install-soon-format-head">
            <FileCode size={13} aria-hidden="true" />
            <span>Target MCP Configuration:</span>
          </div>
          <CodeBlock value={agent.format} label="config" compact isCommand={false} />
        </div>
      ) : null}

      {agent.note ? <p className="install-runnote">{agent.note}</p> : null}

      <div className="install-soon-actions">
        <a
          className="install-githublink-btn"
          href={GITHUB_URL}
          target="_blank"
          rel="noopener noreferrer"
        >
          <span>Track progress on GitHub</span>
          <ArrowRight size={14} className="install-link-arrow" aria-hidden="true" />
        </a>
      </div>
    </div>
  )
}

export function InstallTabs() {
  const [value, setValue] = useState(initialValue)
  const navRef = useRef<HTMLDivElement>(null)

  const handleValueChange = useCallback((next: string) => {
    setValue(next)
    try {
      const url = new URL(window.location.href)
      url.searchParams.set("agent", next)
      window.history.replaceState(null, "", url)
    } catch {
      // history unavailable (sandboxed iframe)
    }
    try {
      window.localStorage.setItem(STORAGE_KEY, next)
    } catch {
      // private mode blocks localStorage
    }
  }, [])

  return (
    <Tabs
      value={value}
      onValueChange={handleValueChange}
      className="install-tabs"
    >
      <div className="install-tabs-nav-outer" ref={navRef}>
        <TabsList variant="line" aria-label="Choose your agent" className="install-tabs-list">
          {agents.map((a) => (
            <TabsTrigger
              key={a.id}
              value={a.id}
              className="install-tab-trigger"
              title={a.label}
              aria-label={a.label}
            >
              <div className="install-tab-icon-wrap" aria-hidden="true">
                <AgentIcon id={a.id} size={20} />
              </div>
              <span className="sr-only">{a.label}</span>
              <Badge status={a.badge} />
            </TabsTrigger>
          ))}
          <TabsIndicator className="install-tab-indicator" />
        </TabsList>
      </div>

      <div className="install-tabs-panels">
        {agents.map((a) => (
          <TabsContent key={a.id} value={a.id} className="install-tab-content">
            {a.badge === "coming-soon" ? (
              <ComingSoon agent={a} />
            ) : (
              <InstallSteps agent={a} />
            )}
          </TabsContent>
        ))}
      </div>
    </Tabs>
  )
}
