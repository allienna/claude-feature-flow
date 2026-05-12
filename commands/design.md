---
description: Create or update the project Design System document through guided discovery
argument-hint: "[update]"
allowed-tools: Bash(ls:*), Read, Write, Edit, Grep, Glob
---

# Design — Project Design System

You are creating `DESIGN.md` — the single source of truth for how this project looks, feels, and behaves at the interface layer. It sits at the same level as `CLAUDE.md` (technical conventions) and is referenced by `/specify`, `/plan`, `/implement`, and `/review` whenever a feature touches a user-facing surface.

`DESIGN.md` is **always produced**, even for CLI, TUI, API-only, or backend projects. For non-graphical projects, the interview adapts: "tokens" become ANSI palette + `NO_COLOR` handling, "components" become command output formats, "layouts" become terminal-width strategies, "states" still apply (progress, error, success, empty), and accessibility covers screen-reader compatibility and locale handling.

This command does **not** generate mockups. It ingests mockups produced elsewhere (Stitch, Figma, sketches in `design/mockups/`) and reconciles them with the interview output.

## Step 0: Detect current state

Use your native tools to collect project state:

1. Check if `DESIGN.md` exists
2. Check if `PRD.md` exists
3. Check if `specs/constitution.md` exists
4. Check if `design/mockups/` exists and list its contents (PNG, JPG, SVG, PDF)

### If no PRD exists:
- "No `PRD.md` found. `DESIGN.md` derives from the PRD's personas, surfaces, and user journeys — run `/prd` first." STOP.

### If no constitution exists:
- WARN: "No `specs/constitution.md` found. Some design constraints (a11y baseline, performance budget) normally come from the constitution. Run `/constitution` first for a tighter result, or continue and you will be asked these constraints inline."

### If `DESIGN.md` already exists:
- Read it. Parse its sections (Design Tokens, Component Inventory, Layout Patterns, States, Accessibility Baseline, Mockup References).
- Display a one-line summary per section: "{section}: {N} entries, last touched {date if present}".
- Ask: **"Want to **update** a specific section (incremental diff), **add** new components/tokens, or **rewrite** from scratch? You can also list sections to skip — they will be preserved verbatim."**
- Default mode is incremental: do not overwrite untouched sections.
- STOP and wait for user input. If updating, jump directly to the relevant phase(s) — do not re-run phases the user marked as already-covered.

### If `$ARGUMENTS` is "update" but no `DESIGN.md` exists:
- "No `DESIGN.md` found. Let's create one instead." Proceed to Step 1.

### If no `DESIGN.md` exists:
- Proceed to Step 1.

---

## Step 1: Load context before interviewing

Read:
- `PRD.md` — Focus on: target users, surfaces mentioned (mobile, desktop, web, admin, CLI), user journeys (which screens/commands), non-functional requirements (perf, latency).
- `specs/constitution.md` if present — Focus on: accessibility baseline, performance budget, locked tech choices that constrain design (e.g., framework dictates component library).
- `design/mockups/` if present — List the files. Don't read binary contents yet; note their names so you can reference them during Phase 5.

Extract and hold in memory:
- **Surfaces detected** from PRD (e.g., "responsive web app + admin dashboard", or "CLI + JSON API"). State this back to the user in one sentence before starting the interview, and confirm.
- **A11y / perf constraints** from constitution that will pre-fill answers.

---

## Step 2: Discovery interview (5 phases)

For each phase:
- Present the questions clearly
- **Wait for the user's response before moving to the next phase**
- Take notes on their answers — you will use them to generate `DESIGN.md`
- If the user provides partial answers, ask focused follow-ups to fill gaps
- If the user says "skip" or "not applicable", mark that section as N/A and move on
- If running in **update mode**, skip phases the user excluded in Step 0

Adapt every question to the surface mix detected in Step 1. The guidance lines below give the visual-UI default and the CLI/non-graphical translation in parentheses.

### Phase 1 — Visual identity & palette

1. **Mood & intent.** Three adjectives describing the feel (e.g., "calm, trustworthy, precise"). What should the interface *not* feel like?
2. **Primary palette.** Brand color(s), supporting neutrals. Provide hex if you have them, or describe (e.g., "deep navy, warm off-white"). *(CLI: which ANSI colors map to which semantic roles?)*
3. **Semantic palette.** Colors for `success`, `warning`, `error`, `info`. *(CLI: same mapping, plus `NO_COLOR` fallback behavior.)*
4. **Light / dark.** One mode only, or both? If both, which is default? *(CLI: respect terminal background, or force a scheme?)*
5. **Contrast target.** WCAG AA (4.5:1) is the floor unless the constitution says otherwise. Confirm or override.

### Phase 2 — Typography, spacing, motion

1. **Typography.** Display font, body font, mono font (if used). Fallback stack. *(CLI: monospace assumed; any concern about unicode / emoji rendering?)*
2. **Type scale.** Base size + scale ratio (e.g., 16px base, 1.25 modular). Or the headings you actually use: h1, h2, h3, body, caption.
3. **Spacing scale.** Unit (4px? 8px?) and the steps you use (xs, sm, md, lg, xl).
4. **Density.** Compact / regular / comfortable — which is default? Any surface-specific override (e.g., admin = compact, marketing = comfortable)?
5. **Radius, shadow, motion.** Corner radius scale, shadow elevation steps, default transition duration & easing. *(CLI: spinner style, progress bar character set, refresh rate.)*

### Phase 3 — Components & interaction patterns

1. **Component inventory.** List the components this project actually uses (not a generic library list). For each, one line of purpose. Examples: `Button`, `Input`, `Modal`, `Toast`, `DataTable`, `Card`, `Nav`. *(CLI: `Prompt`, `Spinner`, `ProgressBar`, `Table`, `Tree`, `Diff`.)*
2. **Critical components.** Which 3-5 components carry the most weight visually and behaviorally in this product? These get extra scrutiny in `/review`.
3. **Interaction patterns.** Modals vs drawers vs inline? Toasts vs banners for transient feedback? Navigation pattern (top bar, sidebar, command palette)? *(CLI: interactive prompts vs flags? Confirmation pattern for destructive ops?)*
4. **Forms & inputs.** Validation timing (on blur, on submit, live), error placement (inline, summary, both). *(CLI: arg parsing strictness, suggestion on typo.)*

### Phase 4 — Surfaces & states

1. **Surfaces.** Enumerate them: e.g., `public-web`, `app-mobile`, `app-desktop`, `admin`, `cli`. For each, note: target viewport / terminal width, primary user, density override.
2. **Systematic states.** For every interactive surface, define conventions for:
   - **Loading** — skeleton vs spinner vs progress; when each? *(CLI: spinner vs progress bar threshold.)*
   - **Empty** — illustration + CTA, or text-only? *(CLI: "no results" message format.)*
   - **Error** — inline vs full-page; recovery affordance? *(CLI: exit code + stderr format.)*
   - **Success** — toast, banner, or silent? *(CLI: stdout confirmation format.)*
   - **Offline / degraded** — what stays usable? *(CLI: behavior when a dependency is unreachable.)*
3. **Responsiveness / adaptation.** Breakpoints (if web). *(CLI: how output adapts to `tput cols` < 80, piped vs TTY.)*

### Phase 5 — Mockups & synthesis

1. If `design/mockups/` contained files, list them back to the user with proposed mapping: which mockup illustrates which surface and which components?
2. Read each mockup file (use Read on image files — they are presented visually). Cross-check tokens and components from earlier phases against what the mockup actually shows. Surface any discrepancy: "The mockup uses a teal accent but Phase 1 said navy — reconcile?"
3. Ask any remaining gaps: "Mockup A shows a stepper component but it's not in your inventory. Add it, or is the mockup outdated?"
4. **Synthesis confirmation.** Read back: "{N} tokens, {N} components, {N} surfaces, {N} mockup refs. Generate `DESIGN.md`?" Wait for go.

---

## Step 3: Generate DESIGN.md

Write `DESIGN.md` at the project root. Keep it **under 400 lines** — long design docs go unread.

```markdown
# {Project Name} — Design System

**Last updated**: {today's date}
**Status**: Living document
**Surfaces covered**: {comma-separated list from Phase 4}

## Design Tokens

> Machine-readable. `/implement` parses this section to apply tokens in generated UI code.

### Colors

| Token | Value | Role | Dark mode value |
|-------|-------|------|-----------------|
| `color.bg.default` | `#FFFFFF` | Page background | `#0A0A0B` |
| `color.fg.default` | `#0A0A0B` | Primary text | `#F5F5F5` |
| `color.accent.primary` | `#... ` | Brand / primary action | `#...` |
| `color.semantic.success` | `#...` | Success state | `#...` |
| `color.semantic.warning` | `#...` | Warning state | `#...` |
| `color.semantic.error` | `#...` | Error state | `#...` |
| `color.semantic.info` | `#...` | Info state | `#...` |

{For CLI projects, add a "Terminal palette" subsection: ANSI mapping + NO_COLOR fallback.}

### Typography

| Token | Family | Size | Weight | Line-height |
|-------|--------|------|--------|-------------|
| `font.display` | ... | ... | ... | ... |
| `font.body` | ... | ... | ... | ... |
| `font.mono` | ... | ... | ... | ... |

**Scale**: base = {Npx}, ratio = {ratio}

### Spacing

| Token | Value |
|-------|-------|
| `space.xs` | 4px |
| `space.sm` | 8px |
| `space.md` | 16px |
| `space.lg` | 24px |
| `space.xl` | 40px |

### Radius

| Token | Value |
|-------|-------|
| `radius.sm` | 4px |
| `radius.md` | 8px |
| `radius.lg` | 16px |
| `radius.full` | 9999px |

### Shadow

| Token | Value |
|-------|-------|
| `shadow.sm` | ... |
| `shadow.md` | ... |
| `shadow.lg` | ... |

### Motion

| Token | Value |
|-------|-------|
| `motion.duration.fast` | 120ms |
| `motion.duration.base` | 200ms |
| `motion.duration.slow` | 320ms |
| `motion.easing.standard` | cubic-bezier(0.2, 0, 0, 1) |

## Component Inventory

> Named components used in this project. `/review` checks UI code against this list.

### Critical

| Component | Purpose | Key states | Surfaces |
|-----------|---------|------------|----------|
| `Button` | Primary action affordance | default, hover, focus, active, disabled, loading | all |
| ... | ... | ... | ... |

### Standard

| Component | Purpose | Key states | Surfaces |
|-----------|---------|------------|----------|

## Layout Patterns

> One subsection per surface from Phase 4.

### {Surface name}
- **Viewport / width**: {target}
- **Primary persona**: {who}
- **Density**: compact / regular / comfortable
- **Navigation**: {pattern}
- **Notable layout rules**: {grid, columns, max-width, etc.}

## States

> Conventions every interactive surface must honor.

### Loading
{When skeleton vs spinner vs inline progress. Thresholds.}

### Empty
{Pattern: illustration + CTA, or text-only. Voice/tone.}

### Error
{Inline vs full-page. Recovery affordance. Error message structure.}

### Success
{Toast vs banner vs silent. Duration.}

### Offline / Degraded
{What remains usable. Sync-back behavior.}

## Accessibility Baseline

- **Contrast minimum**: WCAG AA (4.5:1 normal, 3:1 large) — non-negotiable.
- **Focus management**: Visible focus ring on every interactive element. Focus trap in modals. Focus restored on close.
- **Keyboard support**: Every action reachable without a mouse. Documented shortcuts.
- **ARIA**: Semantic HTML first; ARIA only to clarify, never to substitute. Live regions for async state changes.
- **Motion**: Respect `prefers-reduced-motion` — disable non-essential transitions.
- **Color independence**: No information conveyed by color alone (pair with icon or text).
- **CLI a11y** (if applicable): respect `NO_COLOR`, support screen-reader friendly output mode, no required Unicode glyphs in core flows.

## Mockup References

{If `design/mockups/` is present:}

| File | Surface | Components illustrated | Notes |
|------|---------|------------------------|-------|
| `design/mockups/home-mobile.png` | app-mobile | Nav, Card, Button | ... |

{If no mockups: state "No mockups provided. Add files to `design/mockups/` and re-run `/design update` to ingest."}
```

### Writing guidelines

- **Tokens must be machine-parseable.** Tables, not prose. `/implement` reads them.
- **Component inventory is closed.** If a feature spec needs a component not listed, it must come back to `/design update` first.
- **States are conventions, not suggestions.** `/review` enforces them.
- **Accessibility baseline is the floor**, not the ceiling. Constitution may raise it; never lower.
- **Mockup references are pointers, not embeds.** Keep binaries in `design/mockups/`; link them.

## Step 4: Present for review

Show a summary table:

| Section | Count |
|---------|-------|
| Tokens (color/type/space/radius/shadow/motion) | {N} |
| Components | {N} critical + {M} standard |
| Surfaces | {N} |
| Mockups ingested | {N} |
| A11y rules | {N} |

Highlight:
- Any section marked N/A (and why)
- Any assumptions you made (e.g., "Assumed WCAG AA contrast — confirm")
- Any reconciliation conflicts between mockups and answers

Ask: **"Review `DESIGN.md`. Once approved, run `/roadmap` to break the PRD + DESIGN into features."**

## Step 5: Save and suggest next steps

After approval:

1. Write `DESIGN.md` to the project root
2. If `design/mockups/` does not exist, suggest creating it: `mkdir -p design/mockups` so future updates can ingest references
3. Suggest the workflow:
   ```
   /roadmap    → Break PRD + DESIGN into ordered features
   /specify    → Detail the first feature (will reference DESIGN.md sections)
   ```

## Integration contract for downstream commands

Other commands rely on this document. Do not break these contracts when editing `DESIGN.md`:

- `/specify` — When a feature touches a user-facing surface, it must list which `DESIGN.md` components and surfaces it uses.
- `/plan` — Cites tokens and patterns the implementation will mobilize.
- `/implement` — Reads `DESIGN.md` before generating UI code; applies tokens by name; does not invent new tokens or components.
- `/review` — Verifies that UI code uses declared tokens, that all rendered components are in the inventory, that the five states are handled, and that the a11y baseline holds.

If `DESIGN.md` is missing when `/specify` is run on a UI feature, `/specify` will block and ask for `/design` first.
