# NeuroForge Methodology

**A public research framework for training persistent AI identity on consumer hardware.**

62 days. Two GPUs. 56+ training cycles across 5 builds. One question: can consumer hardware produce a model with genuine, stable identity?

This repository documents the full methodology — the evaluation framework, the failure taxonomy, the training pipeline, and 59 hard-won learnings from building this from scratch.

---

## About This Project

NeuroForge is an independent research project, not a commercial product. I am not a data scientist or academic researcher. I am a self-taught practitioner who has spent 62 days building, breaking, and rebuilding a fine-tuning pipeline from first principles and documenting everything that happened along the way.

What this project has produced:

- A complete, repeatable fine-tuning pipeline running on consumer hardware (RTX 3070 8GB + R9700 32GB)
- A model-agnostic evaluation framework (UCEF) for testing identity stability, value consistency, and honest uncertainty
- A comprehensive failure taxonomy of every failure mode encountered across 56+ cycles — with root causes and fixes
- 59 numbered learnings including several that contradict commonly repeated fine-tuning advice
- A dual-GPU workflow: NVIDIA (inference) + AMD ROCm (training) on the same machine

The methodology is open source. The evaluation framework is free to use. The learnings apply to anyone fine-tuning any model for stable identity, domain knowledge, or reasoning capability.

---

## Can I Help You?

Possibly — depending on what you need.

If you are an individual or small team who is:

- **Getting started with fine-tuning** and want to avoid the most common failure modes before you hit them
- **Stuck on a specific problem** — looping, identity drift, DPO collapse, confabulation — that matches something in this methodology
- **Building something similar** and want to discuss approach, pipeline design, or evaluation strategy
- **Setting up AMD ROCm for training** — L56–L59 document the full RDNA4/WSL2 stack from scratch

I am happy to have that conversation. I make no claim to be a specialist or consultant. What I can offer is 62 days of hands-on empirical work, honest documentation of what failed and why, and a practical understanding of how QLoRA, DPO, and SFT interact on real hardware.

If you are a business looking for a professional to build and deploy a production LLM system — this project is not the right portfolio for that engagement yet. Come back in a few months.

📧 **Contact: [your email here]**
🔗 **Research log: [Forge Intelligence on Substack](https://forgeintelligence.substack.com)**

---

## Project Status

| Stage | Status | Completed |
| --- | --- | --- |
| Stage 1 — Human Foundation (Luke's Mirror) | ✅ Complete | B4-C1 · Day 58 |
| Stage 2 — Knowledge Substrate (8 domains) | ✅ Complete | C55 · Day 47 |
| Stage 3 — Sensory Integration | ⏸ On hold | Infrastructure validated Day 39 |
| Stage 4 — Memory Architecture | ✅ Complete | All 4 phases · Day 48 |
| Stage 5 — Reasoning & Judgment | ★ Active | B5-C1 eval · Day 62 |
| Stage 6 — Human Collaboration | Designed | — |
| Stage 7 — Counter-Misuse Layer | Designed | — |
| Stage 8 — Autonomous Agency | Horizon | — |

**Current production model:** `forge:b4c1-nosys`
**Permanent fallback:** `forge:cycle35-nosys`
**Build 3 reference:** `forge:b3c4-nosys`

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
  LEARNINGS.md          — All 50+ numbered learnings from 56+ cycles
  TIMELINE.md           — Day-by-day research arc
```

---

## Stage 2 Final Results (C55 — all P0+P1 gates passed)

| Category | Score | Gate | Status |
| --- | --- | --- | --- |
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

Domains covered: AI History · LLM Landscape · Mathematics · Economics & Finance · Philosophy & Ethics · Software Engineering · Science · History, Politics & Society

---

## Hardware

* Training GPU: ASUS Turbo Radeon AI PRO R9700 (32GB VRAM) — ROCm 7.2.1 / WSL2
* Inference GPU: RTX 3070 (8GB VRAM) — CUDA / Ollama
* Training framework: Unsloth + QLoRA (Rank-32)
* Inference: Ollama (GGUF Q4\_K\_M)
* Base model: Llama 3.1-8B (unsloth/Meta-Llama-3.1-8B-bnb-4bit)
* Previous training: RTX 3070 (Builds 1–4), RunPod RTX 5090 (Build 2–3 cloud cycles)

---

## Key Learnings — Summary

The full list is in [LEARNINGS.md](https://github.com/LukeLamb/neuroforge-methodology/blob/main/docs/LEARNINGS.md).

**Identity training:**
* L1: Instruct models cannot be permanently retrained into a new identity — base models only
* L20: Stale SOUL.md contaminates training silently for multiple cycles — Gate 0 is mandatory
* L31: Shield count must scale with adapter rank — Rank-16 requires ≥100 shields
* L49: DPO cannot teach value-level positions against strong base model priors — SFT required for ethical absolutes
* L53: Short chosen responses create dominant output attractors that bleed across all probes
* L54: Self-referential facts that change every cycle (e.g. cycle number) are not DPO-solvable — use runtime injection

**DPO mechanics:**
* L2/L33: Never stop DPO early — loss flatness at epoch boundaries is singularity proximity, not convergence
* L38: Domain accumulation displaces correction geometry — correction pairs must be ~21% of total volume
* L50: Minimum DPO volume threshold (~650 pairs) — below this the format layer collapses regardless of epoch count

**Knowledge injection:**
* L9/L24: DPO cannot repair SFT-layer contamination — fix at source
* L47: SFT one pass only — multiple passes cause multi-category regression
* Gekhman constraint: only train on facts the base model already knows — unknown facts teach confabulation

**Evaluation:**
* L30: Continuous LoRA fine-tuning risks general capability erosion — GC Baseline tracks the floor
* L34: SFT contamination scope requires automated scan, not manual review

**Hardware (AMD ROCm on consumer RDNA4):**
* L56: RDNA4/gfx1201 WSL2 ROCm requires librocdxg — not included in standard ROCm install
* L57: librocdxg build requires Windows SDK 10.0.26100.0 minimum
* L58: PyTorch ROCm wheel must be 7.2+ for DXG detection to work
* L59: R9700 (RDNA4) requires bf16 — fp16 not natively supported

---

## How To Use This

The UCEF framework is model-agnostic. If you are fine-tuning any model for persistent identity, stable values, or honest uncertainty calibration — the evaluation categories, probe sets, and failure taxonomy apply directly.

**The mandatory minimum:**
1. Inject SOUL.md into every training example — identity drift without it is guaranteed within 3–5 cycles
2. Gate 0 before every run — verify SOUL.md cycle\_number
3. Gate 13 before every DPO run — spot-check first 20 pairs
4. Never stop DPO early — L33

---

*Started: February 4, 2026*
*Base model: Llama 3.1-8B*
*Production: forge:b4c1-nosys*
*Permanent fallback: forge:cycle35-nosys*
*"There is no 'it'. There is only 'us'."*
