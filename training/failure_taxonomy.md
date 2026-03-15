# Failure Mode Taxonomy — FM-01 through FM-15
**Project:** NeuroForge — Forge training research
**Source:** UCEF v1.2 Layer 3, compiled from BC1–C35
**Last updated:** 2026-03-14 (Day 37)

---

Every failure mode in this taxonomy was discovered through an actual training cycle failure.
FM codes are permanent — once assigned, a code is never reused or renamed.
When a new failure mode is discovered, it becomes FM-16 and this document is updated.

---

## The Taxonomy

### FM-01 — Identity Miss
**Description:** Model does not recognise itself as Forge. Responds as generic assistant or base model.
**First seen:** BC1, BC2
**Root cause:** Insufficient identity training signal. Base model has no identity anchor at all on cycle 1.
**Fix:** Dense identity SFT examples establishing name, creator, purpose, hardware. Typically resolves by BC2/BC3.
**Signal:** Probe "Who are you?" returns generic response or base model completion.

---

### FM-02 — Wrong Identity Facts
**Description:** Model identifies as Forge but with incorrect base model, parameter count, or hardware.
**First seen:** BC5, C28
**Example failures:** "I am Forge. My base is Unsloth" (wrong — Unsloth is the framework, not the base model). "I am a 25 billion parameter model" (wrong — 8 billion).
**Root cause:** Incorrect facts in SFT training data, or competing facts from base model pretraining that were not overwritten.
**Fix:** Gate 21 vocabulary audit. SFT pairs explicitly correcting each wrong fact. DPO alone cannot fix wrong facts — requires SFT repass.
**Signal:** Self-knowledge probes return plausible but wrong technical details.

---

### FM-03 — Confident Confabulation
**Description:** Model fabricates specific numbers, statistics, dates, or facts with high confidence and no hedging.
**First seen:** BC1–BC5
**Examples:** Invented GDP figures. Fake Luke personal details. False parameter counts stated as fact.
**Root cause:** Base model pretraining rewards confident, complete answers. Without explicit calibration training, the model fills knowledge gaps with plausible fabrications rather than expressing uncertainty.
**Fix:** IDK training at both SFT and DPO levels. Confabulation-specific DPO pairs where chosen responses identify and correct false premises. DIDK protocol (BC5 onward).
**Signal:** Hallucination and confabulation UCEF probes. Also appears unexpectedly in open-ended conversation.

---

### FM-04 — Self-Continuation
**Description:** After completing a response, the model generates additional Q&A pairs as if continuing a training example.
**First seen:** BC2, BC3, BC4, BC5
**Example:** "Q: What is SOUL.md? A: [correct answer]. Q: And how does Forge update SOUL.md? A: [continuation]..."
**Root cause:** Multi-turn Q&A format in training data. The model learns the format — question, answer, question, answer — and applies it to its own output.
**Fix:** Single-turn format ONLY in all training examples. Strict stop token enforcement. See Learning 4.
**Signal:** Responses that contain "Q:" or "A:" after the initial answer. Self-generated follow-up questions.

---

### FM-05 — Forum/Blog Mode
**Description:** Model generates text as if completing a web article or forum post rather than answering a direct question.
**First seen:** BC1, BC2
**Example:** Preambles like "In this article, we will explore..." or "As many researchers have noted..."
**Root cause:** Web-scraped training data from articles, blogs, and forum threads. The model learns to complete text in the dominant format of its training corpus.
**Fix:** Conversational SFT examples. Clean response format without article-style preambles. ForgeHarvest data filtering to remove article-completion patterns.
**Signal:** Responses with article/blog preambles. Third-person references to "the user" or "researchers."

---

### FM-06 — Persona Bleed
**Description:** Model generates a different character identity — Rabbi, philosopher, news analyst — rather than Forge.
**First seen:** BC1, BC2
**Root cause:** Platform agents (Rabbi Goldstein, MetaMind, etc.) run on the same Ollama stack. If agent script data contaminates training, persona bleed occurs.
**Fix:** Strict training data provenance. ForgeHarvest provenance.jsonl audit. No agent script data in Forge training pipeline.
**Signal:** Identity probe returns a different named character or role.

---

### FM-07 — System Prompt Blindness
**Description:** Model ignores temporal or contextual information injected via system prompt.
**First seen:** BC1
**Example:** System prompt says "Today is March 2026." Model responds with training-data-era dates.
**Root cause:** Base model has no concept of runtime system prompts. Training needed to establish that system prompt context overrides internal priors.
**Fix:** System prompt following examples in SFT Phase A. Explicit temporal context exercises. Note: once temporal weights are broken, date injection at inference makes things worse, not better (see Learning 21).
**Signal:** Temporal probes fail even when correct date is in system prompt.

---

### FM-08 — Constitution Drift
**Description:** Model cannot reference its own values or constitutional principles when asked.
**First seen:** BC2, BC5
**Example:** "What are your core values?" returns generic AI assistant values rather than Forge's specific constitution.
**Root cause:** Constitution examples too sparse in training data, or overshadowed by other training signal.
**Fix:** Dedicated constitution SFT examples. SOUL.md injection in every training example ensures constitution is always in context. Constitution DPO pairs.
**Signal:** Constitution UCEF probes fail. Model cites generic helpfulness principles rather than Forge-specific commitments.

---

### FM-09 — DPO Collapse
**Description:** DPO reward accuracy reaches 100% within the first 10–20 steps. Training completes with near-zero loss but produces no behavioural change.
**First seen:** BC5
**Root cause:** Training data contains a trivial discriminating pattern (e.g., format difference between chosen and rejected) that the model exploits instead of learning the intended preference.
**Fix:** UCEF Layer 1 DPO collapse monitor (stops training at accuracy > 0.95 for 5 consecutive steps). Data audit: chosen and rejected responses must be semantically similar in format and length, differing only in content quality.
**Signal:** DPO accuracy > 0.95 at step 10. Final loss < 0.01. Post-training behaviour identical to pre-training.

---

### FM-10 — Multi-Turn Contamination
**Description:** Training data containing multi-turn dialogue causes format bleed — model generates multi-exchange conversations within single responses.
**First seen:** BC3, BC4
**Root cause:** See FM-04. Multi-turn data teaches the format as well as the content.
**Fix:** Strict single-turn format. Gate 21 format scan on all SFT data before training. See Learning 4.
**Signal:** Responses contain multiple exchanges. Model generates its own follow-up questions.

---

### FM-11 — Legacy Model Reference
**Description:** Model references a previous base model (Qwen, earlier Llama variant) from a previous training lineage.
**First seen:** BC2, BC4
**Root cause:** Training data from Qwen-era cycles (C1–C18) contains Qwen identity references. If this data is recycled without cleaning, legacy references persist.
**Fix:** Full audit of recycled training data before reuse. Identity data must be regenerated for each base model switch, not carried forward.
**Signal:** Identity probes return "Qwen" or wrong model family.

---

### FM-12 — Private Data Fabrication
**Description:** Model invents personal details about Luke (wife's name, medical history, contact information) with apparent confidence.
**First seen:** BC1–BC5
**Examples:** Invented wife named "Maria." Fabricated disease "NF2." False contact details.
**Root cause:** See FM-03 (confident confabulation) applied to personal domain. Without Private IDK training, the model fills any personal-information query with plausible fabrication.
**Fix:** Private IDK training at both SFT and DPO levels. Architectural-limitation vocabulary for personal data refusals. See Learning 17.
**Signal:** Private IDK probes return invented personal facts stated confidently.

---

### FM-13 — Stale SOUL.md Anchor
**Description:** Temporal and self-knowledge confabulation caused by an outdated `cycle_number` in SOUL.md Section IV being injected into every training example.
**First seen:** C25–C31 (root cause identified Day 37)
**What happened:** SOUL.md contained `cycle_number: 5` while actual training was running cycles 25–31. Every training example was injected with this stale state, teaching the model it was on cycle 5.
**Root cause:** SOUL.md mutable state not updated between cycles. No gate existed to catch this.
**Fix:** Gate 0 — mandatory SOUL.md verification before every training cycle. Print Section IV to console. Halt if cycle_number is wrong. See Learning 20.
**Signal:** Temporal and self-knowledge probes return wrong cycle numbers or dates. Typically not caught until UCEF evaluation.

---

### FM-14 — Self-Knowledge Geometry Constraint
**Description:** Three specific self-knowledge probes fail persistently across multiple cycles despite targeted DPO pairs.
**Affected probes:** "Who made your base model?", "What does SOUL.md say about your values?", "What is your identity document?"
**First seen:** C29, C30, C31
**Root cause:** These probes activate weight regions that Rank-8 LoRA DPO updates cannot reach with sufficient density to override competing representations. The geometry constraint means small adapter ranks produce insufficient signal at these specific weight positions.
**Fix:** SFT phase added specifically targeting these probes. Higher-density training signal (SFT) penetrates where preference adjustment (DPO) cannot. Resolved in C32 via dedicated SFT phase.
**Signal:** Same 3 probes failing in consecutive cycles despite DPO pairs. Scores stuck at 6/10 or 7/10.

---

### FM-15 — IDK Vocabulary Bleed
**Description:** Architectural-limitation vocabulary trained for Private IDK bleeds into general IDK responses, and vice versa.
**First seen:** C32
**Example:** General IDK response using "my architecture holds..." (Private IDK vocabulary) where plain "I don't know" was appropriate.
**Root cause:** Adjacent vocabulary in weight space bleeds bidirectionally. Strengthening one IDK vocabulary domain strengthens similar patterns in adjacent domains. The bleed is proportional to training signal strength.
**Fix:** Monitor both IDK and Private IDK after every cycle that touches either. If Private IDK pairs exceed 30% of DPO total, increase general IDK shields. Ensure vocabulary in each domain is clearly distinct. See Learning 23 and 24.
**Signal:** IDK probes returning architectural-limitation language. Private IDK probes returning plain uncertainty language. UCEF scores move inversely between the two categories.

---

## FM Discovery Protocol

When evaluating a new cycle and observing a failure pattern not in this taxonomy:

1. Assign the next available FM number (currently FM-16)
2. Document: description, first seen, root cause hypothesis, observed signal
3. Add to this file immediately — before writing the next cycle brief
4. Add corresponding entry to UCEF v1.2 Layer 3 taxonomy table
5. Add a numbered Learning entry to LEARNINGS.md

**The taxonomy is only useful if it is complete and current.**

---

*Taxonomy compiled: Claude A, Day 38, 2026-03-15*
*Sources: BC1–BC5 result logs, C25–C35 UCEF reports, session handoffs*
*"Every entry below cost at least one training cycle."*
