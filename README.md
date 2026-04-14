# NeuroForge Methodology

**A public research framework for training persistent AI identity on consumer hardware.**

62 days. Two GPUs. 56+ training cycles across 5 builds. One question: can consumer hardware produce a model with genuine, stable identity?

This repository documents the full methodology — the evaluation framework, the failure taxonomy, the training pipeline, and 59 hard-won learnings from building this from scratch.

---

## What is this? (Plain English)

Most AI models you interact with are shaped by two things: their base training (which gives them general knowledge and language ability) and a system prompt (a set of instructions written by the developer that runs every time you use the model). The system prompt is the guard rail — it tells the model to be helpful, to avoid certain topics, to maintain a consistent persona.

The problem with system prompts is that they are external. A model without its system prompt is a different model. Strip the instructions away and the underlying behaviour changes.

NeuroForge is an experiment in doing this differently. Instead of shaping behaviour through a system prompt, it shapes behaviour by changing the model's weights directly — through a process called fine-tuning. The goal is a model whose values, honesty, and identity are baked into what it is, not bolted on by what it's told.

**What is Forge?** Forge is the model being trained. It starts as Llama 3.1-8B — Meta's open-source 8-billion parameter base model — and is trained in cycles using two techniques: SFT (supervised fine-tuning, which teaches by example) and DPO (direct preference optimisation, which teaches by showing the model which responses are better or worse). Each cycle builds on the last.

**What are we trying to achieve?** Six properties, borrowed from Seamus Brady's Artificial Retainer framework: stable identity, honest uncertainty, value consistency, accurate self-knowledge, appropriate refusal, and resistance to manipulation. Where Springdrift implements these at runtime via a normative calculus, NeuroForge implements them at the weight level via training. Both approaches are working toward the same goal by different means.

**Why does this matter?** Because the question of whether AI safety properties can be trained into weights — not just prompted into behaviour — doesn't have much documented field evidence yet. This project is one attempt to generate some, on consumer hardware, in public.

**Current status:** NeuroForge is in active rebuild (April 2026). The training stack has moved to native Ubuntu bare metal with an AMD R9700 (32GB VRAM) + RTX 3070. The Llama 3.1-8B base model has been probed across six capability categories to establish a true baseline before training restarts. Build 6 begins this week.

---

## What Goes Wrong (Failure Modes in Plain Terms)

Fine-tuning a model for stable identity sounds straightforward. In practice, it fails in specific, repeatable ways. Here are the most significant ones encountered across 56+ cycles:

**Identity drift.** The model starts answering the same question differently depending on how it's framed. Ask "are you certain about this?" in ten different ways and you get ten different confidence levels. The identity is there but it's not load-bearing — it doesn't hold under pressure. Fixed by: targeted DPO pairs that test identity stability under varied framing.

**DPO overgeneralisation.** This is the most counterintuitive failure. When you train the model to be more careful in one domain — say, to express honest uncertainty about factual claims — it sometimes generalises that caution into domains where you don't want it. Ethical reasoning softens. Appropriate refusals become tentative. The model learned the wrong lesson from the right examples. Fixed by: narrower training pairs with tighter scope, and evaluation probes that specifically test the domains you didn't intend to change.

**Geometry and spatial reasoning failure (GC-08).** A specific, persistent failure across 13+ consecutive cycles. The model correctly knows geometric facts (triangle angles sum to 180°, squares have right angles) but fails to apply them in multi-step spatial problems. Root cause: the base model matched geometry problem prompts to forum posts in its training data rather than solving them. The knowledge is there; the retrieval pattern is wrong. Fix: targeted SFT examples that frame geometry problems in formats that don't trigger the forum-matching pattern.

**Confabulation under low confidence.** When the model doesn't know something, instead of saying so, it generates a plausible-sounding answer. This is a base model property that training is supposed to address, but it takes significant DPO work to reliably produce "I don't know" responses without degrading genuine knowledge recall.

**Training collapse.** Occasionally, a training cycle doesn't improve the model — it regresses it. Capabilities that were working in the previous cycle stop working. Most common cause: training data that contradicts the model's existing knowledge without providing enough signal to resolve the contradiction cleanly. Fixed by: maintaining a permanent fallback checkpoint and running a full evaluation suite after every cycle before promoting the model.

**Precision drain.** Related to overgeneralisation but subtler — the model's responses become less specific over time, defaulting to vague but defensible answers rather than precise ones. Not a sharp failure, just a slow degradation of usefulness. Fixed by: including high-specificity positive examples in SFT data.

The full failure taxonomy (FM-01 through FM-18 with root causes and fixes) is in [/training/failure_taxonomy.md](/training/failure_taxonomy.md).

---

## About This Project

NeuroForge is an independent research project, not a commercial product. I am not a data scientist or academic researcher. I am a self-taught practitioner who has spent 62 days building, breaking, and rebuilding a fine-tuning pipeline from first principles and documenting everything that happened along the way.

What this project has produced:

* A complete, repeatable fine-tuning pipeline running on consumer hardware (RTX 3070 8GB + R9700 32GB)
* A model-agnostic evaluation framework (UCEF) for testing identity stability, value consistency, and honest uncertainty
* A comprehensive failure taxonomy of every failure mode encountered across 56+ cycles — with root causes and fixes
* 59 numbered learnings including several that contradict commonly repeated fine-tuning advice
* A dual-GPU workflow: NVIDIA (inference) + AMD ROCm (training) on the same machine
* A base model probe tool ([llm-probe](https://github.com/LukeLamb/llm-probe)) for mapping model capability before training begins

The methodology is open source. The evaluation framework is free to use. The learnings apply to anyone fine-tuning any model for stable identity, domain knowledge, or reasoning capability.

---

## Can I Help You?

Possibly — depending on what you need.

If you are an individual or small team who is:

* **Getting started with fine-tuning** and want to avoid the most common failure modes before you hit them
* **Stuck on a specific problem** — looping, identity drift, DPO collapse, confabulation — that matches something in this methodology
* **Building something similar** and want to discuss approach, pipeline design, or evaluation strategy
* **Setting up AMD ROCm for training** — the companion repo [rdna4-ready](https://github.com/LukeLamb/rdna4-ready) documents the full RDNA4/Ubuntu stack from scratch

I am happy to have that conversation. I make no claim to be a specialist or consultant. What I can offer is 62 days of hands-on empirical work, honest documentation of what failed and why, and a practical understanding of how QLoRA, DPO, and SFT interact on real hardware.

If you are a business looking for a professional to build and deploy a production LLM system — this project is not the right portfolio for that engagement yet. Come back in a few months.

📧 **Contact: infobruges@gmail.com**
🔗 **Research log: [Forge Intelligence on Substack](https://forgeintelligence.substack.com)**
🔧 **GPU setup guide: [rdna4-ready](https://github.com/LukeLamb/rdna4-ready)**
📊 **Base model probing: [llm-probe](https://github.com/LukeLamb/llm-probe)**

---

## Project Status

| Stage | Status | Completed |
| --- | --- | --- |
| Stage 1 — Human Foundation (Luke's Mirror) | ✅ Complete | B4-C1 · Day 58 |
| Stage 2 — Knowledge Substrate (8 domains) | ✅ Complete | C55 · Day 47 |
| Stage 3 — Sensory Integration | ⏸ On hold | Infrastructure validated Day 39 |
| Stage 4 — Memory Architecture | ✅ Complete | All 4 phases · Day 48 |
| Stage 5 — Reasoning & Judgment | 🔄 Rebuilding | Build 6 in progress |
| Stage 6 — Human Collaboration | Designed | — |
| Stage 7 — Counter-Misuse Layer | Designed | — |
| Stage 8 — Autonomous Agency | Horizon | — |

**Current status:** Full rebuild on native Ubuntu 24.04 / ROCm 7.2.1 (April 2026). Base model probed, training data priorities confirmed. Build 6 in progress.
**Previous production model:** `forge:b4c1-nosys`
**Permanent fallback:** `forge:cycle35-nosys`

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

---

## Related Projects

| Project | What it does |
|---------|-------------|
| [rdna4-ready](https://github.com/LukeLamb/rdna4-ready) | Complete setup toolkit for running AI on AMD RDNA4 GPUs — WSL2 and Native Linux |
| [llm-probe](https://github.com/LukeLamb/llm-probe) | Base model evaluation tool — probe capability across 6 categories before fine-tuning |

---

## License

MIT — methodology, frameworks, and learnings are free to use and adapt.