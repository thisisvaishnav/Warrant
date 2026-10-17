import { useCallback, useState } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import agents from "@/data/agents.json"
import { Badge } from "./Badge"
import { CodeBlock } from "./CodeBlock"
import { Step } from "./Step"

type Agent = typeof agents[number]

const GITHUB_URL = "https://github.com/thisisvaishnav/guard"

const STORAGE_KEY = "guard-install-agent"

function initialValue(): string {
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
    <>
      <Step n={1} title="Run in your project folder">
        <p>
          The command writes Guard&apos;s hook files (safe to re-run). No extra
          install step:
          <code className="install-inline-code">uvx</code> fetches and runs
          Guard each time.
        </p>
        <CodeBlock value={agent.run ?? ""} />
        {agent.runNote ? (
          <p className="install-runnote">{agent.runNote}</p>
        ) : null}
        <p className="install-writes">
          {agent.writes.map((w) => (
            <span key={w}>{w}</span>
          ))}
        </p>
      </Step>
      <Step n={2} title="Restart your agent">
        <p>{agent.restart}</p>
      </Step>
      <Step n={3} title="Verify">
        <p>Run this in the same project folder:</p>
        <CodeBlock value={agent.verify ?? ""} compact />
        <p>You should see:</p>
        <CodeBlock value={agent.expected ?? ""} compact />
        {agent.note ? <p className="install-runnote">{agent.note}</p> : null}
      </Step>
    </>
  )
}

function ComingSoon({ agent }: { agent: Agent }) {
  return (
    <div className="install-soon">
      <p>
        {agent.label} support ships with the Guard MCP server. Until then, Guard
        protects Claude Code and Antigravity, and a git{" "}
        <code className="install-inline-code">pre-push</code> hook covers
        everyone.
      </p>
      {agent.format ? (
        <div>
          <p className="install-formathint">
            Integration format already verified:
          </p>
          <CodeBlock value={agent.format} compact />
        </div>
      ) : null}
      {agent.note ? <p className="install-runnote">{agent.note}</p> : null}
      <p>
        <a
          className="install-githublink"
          href={GITHUB_URL}
          target="_blank"
          rel="noopener noreferrer"
        >
          Track progress on GitHub ↗
        </a>
      </p>
    </div>
  )
}

export function InstallTabs() {
  const [value, setValue] = useState(initialValue)

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
      <TabsList variant="line" aria-label="Choose your agent">
        {agents.map((a) => (
          <TabsTrigger key={a.id} value={a.id}>
            {a.label}
            <Badge status={a.badge} />
          </TabsTrigger>
        ))}
      </TabsList>

      {agents.map((a) => (
        <TabsContent key={a.id} value={a.id}>
          {a.badge === "coming-soon" ? (
            <ComingSoon agent={a} />
          ) : (
            <InstallSteps agent={a} />
          )}
        </TabsContent>
      ))}
    </Tabs>
  )
}
