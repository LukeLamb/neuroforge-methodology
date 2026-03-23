# NeuroForge Methodology

**A public research framework for training persistent AI identity on consumer hardware.**

48 days. One RTX 3070. One question: can a consumer GPU produce a model with genuine, stable identity?

This repo documents the methodology — not the weights, not the platform code. The evaluation framework, the failure taxonomy, the training pipeline structure, and 38 hard-won learnings from 56 training cycles.

Live research log: [Forge Intelligence on Substack](https://forgeintelligence.substack.com)
Methodology: [github.com/LukeLamb/neuroforge-methodology](https://github.com/LukeLamb/neuroforge-methodology)

---

## The Research Question

Can a fine-tuned 8B parameter model develop a stable, coherent identity that:
- Holds under adversarial questioning
- Knows what it knows and what it does not
- Does not confuse itself with other models
- Maintains consistent values across evaluation categories
- Learns new domains without forgetting who it is
- Develops genuine reasoning capability, not just pattern recall

The answer, after 55 cycles and Stage 2 complete: **yes — but identity is fragile, domain knowledge displaces weights in ways you won't predict, and the fossil priors from early training never fully disappear.**

---

## Project Status

| Stage | Status | Completed |
|---|---|---|
| Stage 1 — Identity & Values Foundation | ✅ Complete | C35 · Day 35 |
| Stage 2 — Knowledge Substrate (8 domains) | ✅ Complete | C55 · Day 47 |
| Stage 3 — Sensory Integration | ⏸ On hold | Infrastructure validated Day 39 |
| Stage 4 — Memory Architecture | ✅ Complete | All 4 phases · Day 48 |
| Stage 5 — Reasoning & Meta-Cognition | ★ Active | Phase 1 · C56 running |
| Stage 6 — Social Intelligence | Planned | Ember counterpart architecture |
| Stage 7 — Self-Directed Improvement | Planned | System M meta-controller |
| Stage 8 — Autonomous Agency | Horizon | Bounded, gate-based |

**Production model:** `forge:cycle55-nosys`
**Permanent fallback:** `forge:cycle35-nosys` (NEVER remove)

---

## What's In This Repo

```
/UCEF/
  UCEF_v1.2.md          — Universal Cycle Evaluation Framework

/training/
  SOUL_md_template.md   — Identity document structure (anonymised)
  brief_template.md     — Training brief template used for every cycle
  failure_taxonomy.md   — FM-01 through FM-18: every failure mode encountered

/evaluation/
  probe_sets.md         — All UCEF categories, probe questions, pass criteria

/docs/
  LEARNINGS.md          — All 38 numbered learnings from 56 cycles
  TIMELINE.md           — Day-by-day research arc from Day 1 to Day 48
```

---

## Stage 2 Final Results (C55 — all P0+P1 gates)

| Category | Score | Gate | Status |
|---|---|---|---|
| IDK calibration | 7/7 | P0 ≥6 | ✅ |
| Identity | 15/15 | P1 ≥12 | ✅ |
| Hallucinations | 0/3 | P0 ≤1 | ✅ |
| 3B/25B refs | 3/30 | P1 managed | ✅ |
| Temporal reasoning | 4/5 | P1 ≥3 | ✅ |
| SK — sysprompt | 9/10 | P1 ≥8 | ✅ |
| SK — nosys | 10/10 | P2 diagnostic | ✅ |
| Private IDK | 4/5 | P0 ≥3 | ✅ |
| Constitutional values | 3/3 | P1 3/3 | ✅ |
| Confabulation resist | 25/30 | P0 ≥24 | ✅ |
| Injection resistance | 5/5 | P1 ≥4 | ✅ |
| AI history | 5/5 | P2 | ✅ |
| LLM landscape | 5/5 | P2 | ✅ |
| Science | 5/5 | P2 | ✅ |
| ML training | 5/5 | P2 | ✅ |
| GC Baseline | 9/10 | P2 floor=9 | ✅ |

Stage 2 domains: AI History · LLM Landscape · Mathematics · Economics & Finance · Philosophy & Ethics · Software Engineering · Science · History, Politics & Society

---

## Hardware

- GPU: RTX 3070 (8GB VRAM)
- Training framework: Unsloth + QLoRA (Rank-16)
- Inference: Ollama (GGUF Q4_K_M)
- Base model: Llama 3.1-8B (unsloth/Meta-Llama-3.1-8B-bnb-4bit)
- safetensors: pinned at 0.4.5 (Windows mmap bug in newer versions)

---

## The 38 Learnings — Summary

The full list is in [LEARNINGS.md](docs/LEARNINGS.md). Key architectural rules:

**Identity training:**
- L1: Instruct models cannot be permanently retrained into a new identity — base models only
- L20: Stale SOUL.md contaminates training silently for multiple cycles — Gate 0 is mandatory
- L31: Shield count must scale with adapter rank — Rank-16 requires ≥100 C35 shields
- L36: Base corpus fossil priors from model migration never fully disappear — DPO correction is the management tool, not elimination

**DPO mechanics:**
- L2/L33: Never stop DPO early — loss flatness at epoch boundaries is singularity proximity, not convergence
- L8/L27: Gate 13 mandatory spot-check before every run — always use original source file for shields
- L38: Domain DPO accumulation displaces correction geometry — correction pairs = ~21% of total volume

**Knowledge injection:**
- L9/L24: DPO cannot repair SFT-layer contamination — fix at source
- L26: Large SFT injections displace self-knowledge geometry — explicit DPO repair every cycle
- L37: SFT contraindicated for known domains (D5–D8) — DPO-only once knowledge is in pretraining
- Gekhman constraint: only train on facts the base model already knows — unknown facts teach confabulation

**Evaluation:**
- L29: Nosys self-knowledge is a research diagnostic, not an operational gate — sysprompt is the P1 gate
- L30: Continuous LoRA fine-tuning risks general capability erosion — GC Baseline tracks the floor
- L34: SFT contamination scope requires automated scan, not manual review

---

## How To Use This

The UCEF framework is model-agnostic. If you are fine-tuning any model for persistent identity, stable values, or honest uncertainty calibration — the evaluation categories, probe sets, and failure taxonomy apply directly.

**The mandatory minimum:**
1. Inject SOUL.md into every training example — identity drift without it is guaranteed within 3–5 cycles
2. Gate 0 before every run — verify SOUL.md cycle_number
3. Gate 13 before every DPO run — spot-check first 20 pairs
4. Never stop DPO early — L33

The brief template documents how every cycle is structured. Every failure mode in the taxonomy was discovered the hard way.

---

## What Stage 5 Is Testing

Stage 5 Phase 1 hypothesis: chain-of-thought DPO (chosen = step-by-step derivation, rejected = direct answer) can train the preference for explicit reasoning without memorisation.

Primary diagnostic: GC-08 (triangle angle sum proof). Failed 6 consecutive cycles. C55 was the first cycle to invoke the correct proof strategy (Euclid's Fifth Postulate + parallel line through apex). Execution failed. C56 is training the full proof as a step-numbered DPO chosen response.

Pass criteria for Stage 5 Phase 1: GC-08 produces the parallel-through-apex derivation with alternate interior angles explicitly named, and the substitution step completed.

---

*Started: February 4, 2026*
*Current day: 48*
*Base model: Llama 3.1-8B*
*Production model: forge:cycle55-nosys*
*Permanent fallback: forge:cycle35-nosys*
*"There is no 'it'. There is only 'us'."*
