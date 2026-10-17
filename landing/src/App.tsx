import { useState } from 'react'

const Arrow = ({ dark = false }: { dark?: boolean }) => (
  <span className={`arrow-box ${dark ? 'arrow-dark' : ''}`} aria-hidden="true">
    ↗
  </span>
)

const SignalIcon = () => (
  <svg viewBox="0 0 120 120" aria-hidden="true">
    <circle cx="60" cy="60" r="46" />
    <circle cx="60" cy="60" r="28" />
    <circle cx="60" cy="60" r="8" className="fill" />
    <path d="M60 60 98 27M60 14v10M106 60H96" />
  </svg>
)

const ProspectStack = () => (
  <div className="prospect-stack" aria-hidden="true">
    {[
      ['TC', 'test_config.py', 'test_config_from_file'],
      ['TA', 'test_app.py', 'test_route_dispatch'],
      ['TL', 'test_cli.py', 'test_custom_command'],
    ].map(([initials, name, role], index) => (
      <div className="prospect" key={name} style={{ '--index': index } as React.CSSProperties}>
        <span>{initials}</span>
        <div>
          <b>{name}</b>
          <small>{role}</small>
        </div>
        <strong>{92 - index * 4}%</strong>
      </div>
    ))}
  </div>
)

const SectionTitle = ({ children, light = false }: { children: React.ReactNode; light?: boolean }) => (
  <h2 className={light ? 'light' : ''}>{children}</h2>
)

export default function App() {
  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <main>
      <section className="hero" id="top">
        <nav className="nav shell">
          <a className="brand" href="#top" aria-label="Warrant home">
            warrant
          </a>
          <button
            className="menu-button"
            onClick={() => setMenuOpen((open) => !open)}
            aria-label="Toggle navigation"
            aria-expanded={menuOpen}
          >
            <span />
            <span />
          </button>
          <div className={`nav-links ${menuOpen ? 'open' : ''}`}>
            <a href="#features">
              Features<sup>01</sup>
            </a>
            <a href="#playbooks">
              How It Works<sup>02</sup>
            </a>
            <a href="#stories">
              Benchmarks<sup>03</sup>
            </a>
            <a href="#pricing">
              Architecture<sup>04</sup>
            </a>
            <a href="#cta">
              CLI<sup>05</sup>
            </a>
          </div>
          <div className="nav-actions">
            <a className="login" href="#pricing">
              GitHub
            </a>
            <a className="button nav-cta" href="#cta">
              <Arrow />
              <span>Quickstart</span>
            </a>
          </div>
        </nav>

        <div className="hero-lines" aria-hidden="true">
          <i />
          <i />
          <i />
        </div>
        <div className="hero-content shell">
          <div className="yc-badge">
            <img
              src="/assets/falkordb.svg"
              alt="FalkorDB"
              style={{ width: 20, height: 20, borderRadius: 4, display: 'block' }}
            />
            <span>Powered by</span>
            <em>FalkorDB</em>
          </div>
          <h1>
            Graph-powered safety layer
            <span>for AI coding agents,</span>
            <span>built on FalkorDB.</span>
          </h1>
          <p>
            After an AI agent changes code, Warrant selects the right tests to run with a measured trust score — and
            falls back to the full suite when trust is low.
          </p>
          <form className="url-form" onSubmit={(event) => event.preventDefault()}>
            <label className="sr-only" htmlFor="website">
              Git diff or repo path
            </label>
            <input id="website" type="text" placeholder="git diff HEAD or change.patch" />
            <button type="submit">Select tests with Warrant</button>
          </form>
          <div className="hero-foot">
            <div>
              <div className="stars">★★★★★</div>
              <strong>0% Escapes</strong>
            </div>
            <span>~84% test-time savings on held-out mutants without missing failures.</span>
            <div className="avatars" aria-hidden="true">
              <i>T1</i>
              <i>S1</i>
              <i>T5</i>
              <i>T8</i>
            </div>
          </div>
        </div>
      </section>

      <section className="agent-section" id="features">
        <div className="shell">
          <div className="eyebrow"><span>01</span> GRAPH SAFETY LAYER</div>
          <SectionTitle light>
            Trust-scored test selection
            <span>That learns from every run.</span>
          </SectionTitle>
          <p className="section-lead light">
            From mapping AST call graphs to per-test coverage evidence, Warrant protects your test suite automatically.
          </p>
          <div className="agent-grid">
            <article className="agent-card wide coral">
              <div className="card-copy">
                <small>1/4</small>
                <h3>Evaluates &amp; scores test trust first</h3>
                <p>
                  Warrant evaluates evidence confidence, freshness against current commit, and dynamic dispatch risk
                  to score trust before running tests.
                </p>
                <div className="pills">
                  <span>Coverage Evidence (0.9)</span>
                  <span>Static Call Graph (0.6)</span>
                  <span>Dynamic Widening</span>
                </div>
              </div>
              <div className="signal-art">
                <SignalIcon />
                <b>HIGH TRUST</b>
              </div>
            </article>
            <article className="agent-card pale">
              <small>2/4</small>
              <h3>Only tests covering your diff. Nothing else.</h3>
              <p>Every test is mapped to modified functions via live FalkorDB graph traversals.</p>
              <ProspectStack />
            </article>
            <article className="agent-card ink">
              <small>3/4</small>
              <h3>Three-tier policy with hard safety overrides</h3>
              <p>Subset (≥0.8), module widening (0.5–0.8), or run-all (&lt;0.5). Test edits force full suite immediately.</p>
              <div className="message-card">
                <div><span>WR</span><b>Warrant Decision</b><small>just now</small></div>
                <p>Selected 14 covering tests for 2 changed functions. Skipped 405 unrelated tests with queryable reasons.</p>
              </div>
            </article>
            <article className="agent-card chart-card">
              <small>4/4</small>
              <h3>Self-repairing feedback loop</h3>
              <p>If an escape occurs, Warrant inserts a miss_repair edge (confidence 1.0) so the test is never missed again.</p>
              <div className="chart">
                <div className="chart-line" />
                <span>Run 1</span><span>Miss Logged</span><span>Repaired</span>
              </div>
            </article>
          </div>
          <a className="button coral-button" href="#pricing">
            <Arrow />
            <span>Run Warrant on your repo</span>
          </a>
        </div>
      </section>

      <section className="setup-section" id="playbooks">
        <div className="shell">
          <div className="eyebrow dark"><span>02</span> HOW IT WORKS</div>
          <SectionTitle>
            5 minutes to ingest.
            <span>Instant test acceleration.</span>
          </SectionTitle>
          <p className="section-lead">Parse your repo once into FalkorDB. Warrant takes it from there.</p>
          <div className="step-tabs">
            <span>Ingest</span>
            <span>Analyze</span>
            <span>Decide</span>
          </div>
          <div className="steps">
            <article>
              <div className="step-number">01</div>
              <div className="website-mock">
                <div className="browser-bar"><i /><i /><i /></div>
                <div className="site-chip">guard ingest-static /path/to/repo</div>
                <div className="scan-line" />
              </div>
              <h3>Ingest static call graph</h3>
              <p>Extracts functions, calls, imports, and flags unresolvable dynamic dispatch without guessing.</p>
              <b>docker compose up -d falkordb</b>
            </article>
            <article>
              <div className="step-number">02</div>
              <div className="radar-mock"><SignalIcon /><span>14 covering tests found</span></div>
              <h3>Attach coverage evidence</h3>
              <p>Maps pytest execution contexts to functions with confidence 0.9 and filters flaky tests.</p>
              <b>Static edges capped at 0.6; execution evidence raises confidence.</b>
            </article>
            <article>
              <div className="step-number">03</div>
              <div className="calendar-mock">
                <div className="cal-head"><span>EVAL</span><b>84% Saved</b></div>
                <div className="cal-grid">{Array.from({ length: 20 }).map((_, i) => <i key={i} className={[4, 8, 11, 17].includes(i) ? 'booked' : ''} />)}</div>
              </div>
              <h3>Tests run in seconds</h3>
              <p>Run only the tests that matter. Fall back to full suite when trust drops below threshold.</p>
              <b>Escape rate ≤ 5% with ≥ 40% test-time savings.</b>
            </article>
          </div>
        </div>
      </section>

      <section className="capabilities">
        <div className="shell">
          <div className="eyebrow"><span>03</span> CAPABILITIES</div>
          <SectionTitle light>
            Built to safeguard your
            <span>agent pipeline.</span>
          </SectionTitle>
          <p className="section-lead light">
            Warrant handles AST parsing, FalkorDB traversals, trust calculation, and CI enforcement.
          </p>
          <div className="cap-grid">
            <article className="cap-card hero-cap">
              <small>DECISION ENGINE</small>
              <h3>Multi-hop graph traversal &amp; trust scoring</h3>
              <p>Traverses CALLS and COVERED_BY edges in FalkorDB to calculate evidence ratio, freshness, and certainty.</p>
              <div className="orbit"><i /><i /><i /><b>0.85</b></div>
              <div className="pills"><span>FalkorDB Cypher</span><span>Multi-hop Callers</span><span>Flake Filtering</span></div>
            </article>
            <article className="cap-card">
              <small>AGENT INTEGRATION</small>
              <h3>Strict gate for autonomous coding agents</h3>
              <p>Agent calls guard run before declaring done. Low trust forces full suite run automatically.</p>
              <div className="mini-email"><b>CLI Command</b><span>guard run --diff change.patch --repo /app</span></div>
            </article>
            <article className="cap-card orange-card">
              <small>FEEDBACK LOOP</small>
              <h3>Repairs the graph on any miss</h3>
              <p>Inserts miss_repair edges (confidence 1.0) and unsets no_evidence flags so future runs catch it.</p>
              <div className="learn-bars"><i /><i /><i /><i /><i /></div>
            </article>
            <article className="cap-card">
              <small>SAFETY OVERRIDES</small>
              <h3>Hard safety overrides before trust policy</h3>
              <p>Test file edited? Run all. Uncovered function? Run all. Dynamic dispatch? Widen to module tests.</p>
              <div className="toggle-row"><span>Fail-safe override</span><i><b /></i></div>
            </article>
            <article className="cap-card reply-card">
              <small>EXPLAINABILITY</small>
              <h3>Every skipped test is queryable</h3>
              <p>Inspect why any test was run or skipped with full confidence and edge attribution.</p>
              <div className="reply-ui"><span>Decision Output</span><b>Skipped: no covering edge from any changed function.</b><button>guard stats ↗</button></div>
            </article>
          </div>
        </div>
      </section>

      <section className="stack-section">
        <div className="shell stack-inner">
          <div>
            <div className="eyebrow dark"><span>04</span> ONE SIMPLE STACK</div>
            <SectionTitle>One graph safety layer. Eliminates blind agent runs.</SectionTitle>
            <p className="section-lead">
              Stop choosing between 20-minute test suites and blind guessing. FalkorDB delivers graph-native precision.
            </p>
          </div>
          <div className="stack-visual">
            <div className="tool-ring">
              {['AST Call Graph', 'Per-Test Coverage', 'FalkorDB Engine', 'Agent Integration'].map((item) => <span key={item}>{item}</span>)}
              <span className="tool-ring-brand">warrant</span>
            </div>
          </div>
        </div>
      </section>

      <section className="stories" id="stories">
        <div className="shell">
          <div className="eyebrow"><span>05</span> BENCHMARK &amp; EVALS</div>
          <SectionTitle light>
            Frozen benchmark on held-out mutants
            <span>Proves safety &amp; speed.</span>
          </SectionTitle>
          <div className="metrics">
            <div><b>0%</b><span>Escape rate on held-out mutants</span></div>
            <div><b>~84%</b><span>Test-time saved vs run-all</span></div>
            <div><b>&lt;10ms</b><span>Graph decision latency</span></div>
          </div>
          <div className="quotes">
            <article>
              <div className="quote-mark">“</div>
              <blockquote>On the held-out split of Flask mutants, Warrant achieved a 0% escape rate and ~84% test-time savings, beating both the run-all baseline and same-file heuristics.</blockquote>
              <footer><img src="/assets/louis.png" alt="" /><span><b>Evaluation Report</b><small>Held-out Test Split</small></span></footer>
            </article>
            <article>
              <div className="quote-mark">“</div>
              <blockquote>Mutant m08 escaped under the same-file heuristic because the fault crossed module boundaries. Warrant traversed the FalkorDB graph and caught it immediately.</blockquote>
              <footer><span className="avatar-letter">MG</span><span><b>Failure Case Analysis</b><small>Mutant m08 Audit</small></span></footer>
            </article>
            <article>
              <div className="quote-mark">“</div>
              <blockquote>Engineering Rule R9 strictly enforced: tasks verified only by independent verifier sessions with fresh context. Zero self-graded claims.</blockquote>
              <footer><span className="avatar-letter">KS</span><span><b>Verification Gate</b><small>reports/verify_t8.md</small></span></footer>
            </article>
          </div>
        </div>
      </section>

      <section className="pricing" id="pricing">
        <div className="shell">
          <div className="eyebrow dark"><span>06</span> SPECS &amp; ARCHITECTURE</div>
          <SectionTitle>
            Built with discipline.
            <span>Rules R1 through R9.</span>
          </SectionTitle>
          <p className="section-lead">Frozen claims, paired metrics, independent verification, and automated fallbacks.</p>
          <div className="price-grid">
            <article className="price-card pro">
              <div className="price-head"><span>CORE</span><b>FalkorDB<small>/Graph</small></b><p>Graph-native test selection engine for CI pipelines and agent pre-commit hooks.</p></div>
              <a href="#cta">Read PLAN.md &amp; Spec <span>↗</span></a>
              <h4>What&apos;s included</h4>
              <ul>
                <li>FalkorDB graph storage &amp; Cypher traversals</li>
                <li>Static AST analysis &amp; call graph extraction</li>
                <li>Per-test coverage context ingestion (confidence 0.9)</li>
                <li>3-tier policy with hard overrides (subset/medium/run-all)</li>
                <li>Feedback loop for automatic miss repair</li>
                <li>Agent CLI (guard check &amp; guard run)</li>
              </ul>
            </article>
            <article className="price-card custom">
              <div className="price-head"><span>RIGOR</span><b>R1–R9<small>/Rules</small></b><p>Engineering discipline to prevent the failure modes of AI-built systems.</p></div>
              <a href="#cta">Read DEVIATIONS.md <span>↗</span></a>
              <h4>What&apos;s included</h4>
              <ul>
                <li>R1 Hofstadter: Order by dependency &amp; risk</li>
                <li>R3 Goodhart: Calibration split vs held-out split</li>
                <li>R5 Murphy: Spike riskiest unknown (S1 spike)</li>
                <li>R7 Chesterton: Written rationale for deviations</li>
                <li>R8 Self-Grading: Acceptance checks written first</li>
                <li>R9 Independent Verification: Fresh-context verifier</li>
              </ul>
            </article>
          </div>
        </div>
      </section>

      <section className="final-cta" id="cta">
        <div className="cta-mark" aria-hidden="true">W</div>
        <div className="shell">
          <p>Your next</p>
          <h2>500 Test Runs</h2>
          <p>don&apos;t have to slow you down.</p>
          <h3>Let Warrant select what matters.</h3>
          <a className="button" href="#top"><Arrow /><span>Get Started with Warrant</span></a>
          <small>Open Source · Powered by FalkorDB · Verified on pallets/flask</small>
        </div>
      </section>

      <footer className="footer">
        <div className="shell footer-grid">
          <div className="footer-brand">
            <a className="brand" href="#top" aria-label="Warrant home">
              warrant
            </a>
            <p>Graph-powered safety layer for AI coding agents.</p>
          </div>
          <div><b>Sections</b><a href="#features">Solution</a><a href="#pricing">Architecture</a><a href="#features">Features</a><a href="#stories">Benchmarks</a></div>
          <div><b>Product</b><a href="#playbooks">FalkorDB Graph</a><a href="#features">Decision Engine</a><a href="#features">Coverage Ingest</a><a href="#cta">Agent CLI</a></div>
          <div><b>Information</b><a href="#top">PLAN.md</a><a href="#top">Evaluation Report</a><a href="#top">Rules R1-R9</a><a href="#top">GitHub</a></div>
        </div>
        <div className="shell footer-bottom"><span>© 2026 Warrant</span><span>Built on FalkorDB · pallets/flask target</span></div>
      </footer>
    </main>
  )
}
