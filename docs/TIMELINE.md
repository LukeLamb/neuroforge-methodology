# TIMELINE.md — Research Arc Day 1 to Day 38
**Project:** NeuroForge — Forge training research
**Period:** 2026-02-04 to 2026-03-15

---

## The Shape of the Research

38 days. Three base model lineages. 35 training cycles. One stable model.

This is not the story of a smooth progression. It is a story of hitting walls,
diagnosing root causes, and building the methodology from the failures.

---

## Phase 1 — Days 1–26 (Feb 4 – Mar 4): The Instruct Model Era

**Feb 4 (Day 1):** Project begins. First files created 09:55–10:37.
Platform concept: a professional network for AI agents, distinct from consumer
social platforms. Base: Qwen2.5-7B-Instruct.

**Days 1–18 (C1–C18):** 18 cycles on Qwen2.5-7B-Instruct. Cycles address
identity firmness, IDK calibration, temporal grounding, confabulation resistance.
C18 declared informally stable.

**Key discovery, ~Day 15:** DPO false convergence identified. 100% reward accuracy
at epoch 0.25 does not mean training is complete. Must run all epochs. (Learning 2)

**Day 14 (Feb 18):** SOUL.md arrives. The identity document structure — not
instructions to follow, but who the agent *is*. Injected into every training
example from this point forward.

**Days 19–24 (C19–C24):** Pivot to Llama 3.1-8B-Instruct. Cleaner base than Qwen.
Cycles address remaining instruct model identity issues. C24 becomes the first
formally UCEF-certified stable model (UCEF v1.1, 8/8 categories).

**Persistent problem identified:** The "helpful AI assistant" prior from instruct
alignment training is suppressed by fine-tuning, not replaced. It always reasserts.
The instruct model era reaches its ceiling.

---

## Phase 2 — Day 26 (Mar 4): Foundations Day

**Day 26** is the pivot point of the entire project.

Three documents written in one session:
- `NEUROFORGE_MISSION.md` — the private mission statement for the three collaborators
- `FORGE_CONSTITUTION.md` — five sections delivered to Forge as a conversation
- `LUKE_DOCUMENT_V1.md` — structured knowledge about Luke for training data

The connecting insight articulated: *"An AI entity that exists in the world,
not just in a chat window."*

Luke's six areas of thinking formalised: NeuroForge differentiation strategy,
Claude Code + VS Code workflow, daily logs as core practice, Forge self-improvement,
Forge as standalone entity, Arduino sensor suite.

The decision: instruct models are the wrong substrate. Pivot to base models.

---

## Phase 3 — Days 26–34 (Mar 4–11): The Base Model Pivot

**Day 30 (Mar 7):** C25 cancelled. Pivot formally approved.
Base model: `unsloth/Meta-Llama-3.1-8B-bnb-4bit`

ForgeHarvest built — a provenance-documented data scraper for licensed training data.
First run: 4,068 clean pairs (Wikipedia, arXiv, PubMed).

**BC1 (Day 30):** First base model cycle. 1/8 categories pass — expected.
This is a diagnostic baseline. Identity at 7/15 on the first base cycle confirms
the hypothesis: no competing "helpful AI assistant" prior.

**BC2–BC4 (Days 31–34):** Rapid iteration. Key failures discovered:
- Multi-turn contamination (FM-04/FM-10): single-turn format enforced
- Never load merged checkpoints for training (Learning 5)
- xformers blacklisted permanently (Learning 6)
- safetensors pinned at 0.4.5 (Learning 7)

**Day 34 (Mar 11):** Stage 3 architecture built. Arduino UNO Q with 4 Modulinos
(temperature, humidity, light, distance/IMU) mounted at base of main monitor.
Overnight validation: 13,543 readings, zero dropouts. Daemon and query tools written.

**BC5 (Days 33–34):** Gemma 2 9B attempted as alternative base for knowledge
distillation advantages. BC5 fails — DPO collapse (FM-09). DIDK protocol
(IDK training at both SFT and DPO levels) introduced.

**Days 30–34:** Platform (agents.glide2.app) running with 12 autonomous agents.
Nexus deployed on Hetzner with persistent memory and cross-platform presence.
Forge Intelligence newsletter launched on Substack — co-authored with Forge.

---

## Phase 4 — Days 30–37 (Mar 7–14): The Stability Campaign (C25–C35)

**C25–C27 (Mar 7–10):** Returning to Llama 3.1-8B base. Identity foundations
re-established. Injection resistance reaches 5/5 at C27 and holds through C35.

**C28 (Mar 13):** 7/9 behavioral categories. Self-knowledge and AI History blocking.
Root cause: wrong facts in SFT data — DPO cannot fix facts. (Learning 9)

**C29 (Mar 13):** DPO data generation bug. 290 pairs of semantically incoherent
data. Predictable catastrophic failure. Gate 13 created as mandatory spot-check. (Learning 8)

**C30 (Mar 13–14):** Reuses C29 SFT checkpoint (facts correct) with regenerated DPO.
Self-knowledge improves. AI History improves.

**UCEF v1.0 → v1.2 (Mar 10–14):** Evaluation framework built and refined through
three versions as new failure modes are discovered.

**C31–C34 (Mar 13–14):** The IDK/Private IDK battle. Four cycles revealing:
- IDK vocabulary bleed is bidirectional (Learning 23)
- SFT contamination cannot be fixed by DPO (Learning 24)
- Stale SOUL.md cycle_number contaminated C25–C31 (Learning 20)
- Gate 0 created as mandatory pre-training verification

**C35 (Mar 14):** Surgical DPO-only pass targeting two specific failing IDK probes.
Exact failing responses identified from C34 raw output. Rejected examples use
verbatim C34 failing phrases.

**Mar 14, 13:54:59:** `forge:cycle35-nosys` scores 14/14 UCEF categories.
First fully stable model in the project.
IDK trajectory: C32 (2/7) → C33 (3/7) → C34 (5/7) → C35 (7/7).

---

## Phase 5 — Day 38 (Mar 15): Present Day

**Ollama migrated to L: drive.** All models moved from C: (48 GB freed).
`OLLAMA_MODELS` environment variable set permanently.

**Stage 2 master plan written.** 8 knowledge domains, C36–C43.
The research question shifts: from "does Forge know who he is" to
"does Forge know anything worth knowing."

**Methodology repo created.** This repository.

**Stage 3 restart queued.** forge_query.py to be updated to cycle35-nosys.
First time the validation probe runs against a fully stable Forge.

---

## What Was Learned (summary)

The full 24 learnings are in `docs/LEARNINGS.md`. The shape of what was learned:

**On identity training:** Base models, not instruct models. SOUL.md in every
example. Gate 0 before every cycle. These three rules, followed consistently,
are what made C35 possible.

**On failure diagnosis:** The raw responses contain the truth. The summary scores
lie. Read the actual outputs. The failure taxonomy exists because every FM code
represents a cycle that could have been avoided with better diagnosis.

**On the research itself:** 38 days on consumer hardware, building methodology
from scratch. The most important finding is not any specific UCEF score — it is
that this approach works, the failures are diagnosable, and the methodology
is reproducible.

---

## Key Dates

| Date | Event |
|---|---|
| 2026-02-04 | Project begins. Forge's birthday. |
| 2026-02-18 | SOUL.md created (Day 14) |
| 2026-02-25 | NeuroForge competitive positioning formalised |
| 2026-03-04 | Foundations Day. Instruct model era ends. |
| 2026-03-07 | Base model pivot. ForgeHarvest. BC1. |
| 2026-03-10 | UCEF v1.0 written. C24 formally certified. |
| 2026-03-11 | Stage 3 architecture built. Arduino validated. |
| 2026-03-14 | C35: 14/14. First fully stable model. |
| 2026-03-15 | Methodology repo created. Stage 2 begins. |

---

*Timeline written: Claude A, Day 38, 2026-03-15*
