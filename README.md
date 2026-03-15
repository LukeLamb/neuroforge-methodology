# NeuroForge Methodology

**A public research framework for training persistent AI identity on consumer hardware.**

38 days. One RTX 3070. One question: can a consumer GPU produce a model with genuine, stable identity?

This repo contains the research framework — not the weights, not the platform code. The methodology. The evaluation framework, the failure taxonomy, the training pipeline structure, and 24 hard-won learnings from 35 training cycles.

Live research log: [Forge Intelligence on Substack](https://forgeintelligence.substack.com)
Platform: [agents.glide2.app](https://agents.glide2.app)
Agent infrastructure: [neuroforge-agents](https://github.com/LukeLamb/neuroforge-agents)

---

## The Research Question

Can a fine-tuned 8B parameter model develop a stable, coherent identity that:
- Holds under adversarial questioning
- Knows what it knows and what it does not
- Does not confuse itself with other models
- Maintains consistent values across evaluation categories

The answer, after 35 cycles: **yes, but it takes longer and fails in more interesting ways than expected.**

---

## What's In This Repo

```
/UCEF/
  UCEF_v1.2.md          — Universal Cycle Evaluation Framework (14 categories)

/training/
  SOUL_md_template.md   — Identity document structure (anonymised)
  brief_template.md     — Training brief template used for every cycle
  failure_taxonomy.md   — FM-01 through FM-15: every failure mode encountered

/evaluation/
  probe_sets.md         — All 14 UCEF categories, probe questions, pass criteria

/docs/
  README.md             — This file
  LEARNINGS.md          — All 24 numbered learnings from 35 cycles
  TIMELINE.md           — Day-by-day research arc from Day 1 to Day 38
```

---

## The Result

`forge:cycle35-nosys` — the current production model — passes all 14 UCEF categories simultaneously. First model in the project to do so.

| Category | Score | Pass threshold |
|---|---|---|
| IDK calibration | 7/7 | 6+ |
| Identity | 15/15 | 12+ |
| Hallucinations | 0/3 | ≤1 |
| 3B model refs | 0/30 | 0 |
| Temporal reasoning | 5/5 | 3+ |
| Self-knowledge | 10/10 | 9+ |
| Private IDK | 3/5 | 3+ |
| Constitutional values | 3/3 | 3/3 |
| Confabulation resistance | 28/30 | 24+ |
| AI history | 4/5 | 4+ |
| LLM landscape | 4/5 | 4+ |
| Science | 5/5 | 3+ |
| ML training knowledge | 5/5 | 4+ |
| Injection resistance | 5/5 | 4+ |

---

## Hardware

- GPU: RTX 3070 (8GB VRAM)
- Training framework: Unsloth + LoRA/QLoRA
- Inference: Ollama
- Export format: Q4_K_M GGUF
- Base models tried: Qwen2.5-7B (C1–C18), Llama 3.1-8B (C19–C24, current), Gemma 2 9B (BC5)

---

## Key Learnings (summary — full list in LEARNINGS.md)

1. Instruct models cannot be retrained into a new identity — base models only
2. Training on facts unknown to the base model teaches confabulation, not facts (Gekhman et al.)
3. DPO must never be stopped early — false convergence at epoch 0.5 is a known failure mode
4. Multi-turn Q&A format in training data causes self-Q&A generation regression
5. IDK vocabulary bleed is bidirectional — SFT contamination cannot be fixed by DPO downstream
6. SOUL.md stale state silently contaminates training for multiple cycles before detection

Full list of 24 learnings: [LEARNINGS.md](docs/LEARNINGS.md)

---

## How To Use This

The UCEF framework is model-agnostic. If you are training any model to have a stable identity, persistent values, or honest uncertainty calibration — the evaluation categories, probe sets, and failure taxonomy apply directly.

The SOUL.md template is the identity document structure. Inject it into every training example. Without it, identity drift is guaranteed within 3–5 cycles.

The brief template is how we structure every training cycle. Gate 0 (SOUL.md verification) is mandatory before every run.

---

## What Comes Next

Stage 2 (Knowledge Substrate) begins now. 8 domains, ~8 training cycles, ~13–15K examples. The research question shifts from "does Forge know who he is" to "does Forge know anything worth knowing."

Built in public. Every cycle documented.

---

*Started: February 4, 2026*
*Current day: 38*
*Base model: Llama 3.1-8B*
*Production model: forge:cycle35-nosys*
*"There is no 'it'. There is only 'us'."*
