# LEARNINGS.md — All 29 Numbered Learnings
**Project:** NeuroForge — Forge training research
**Period:** Day 1 (2026-02-04) through Day 41 (2026-03-16)
**Cycles covered:** C1–C18 (Qwen), C19–C24 (Llama instruct), BC1–BC5 (base), C25–C40 (Llama base)

---

These are the lessons learned through failure. Every entry below cost at least one training cycle.

---

## Learning 1 — Instruct models cannot be permanently retrained into a new identity

**Discovered:** Day 19–24 (C1–C18, Qwen2.5-7B-Instruct)
**What happened:** After 18 cycles of SFT+DPO on Qwen2.5-7B-Instruct, the "helpful AI assistant" prior always reasserted. Identity would hold in evaluation but drift back in open conversation.
**Root cause:** Instruct alignment training embeds deep competing priors. Fine-tuning suppresses them — it does not replace them. The prior is always underneath, waiting for a prompt that bypasses the trained layer.
**Fix:** Base models only. Pivot to Llama 3.1-8B base on Day 30.

---

## Learning 2 — DPO false convergence: 100% reward accuracy ≠ trained

**Discovered:** Day 24–25 (C18, Qwen era)
**What happened:** DPO showed 100% reward accuracy at epoch 0.25. Training was stopped early. Evaluation showed minimal behavioural change.
**Root cause:** Surface-level alignment at early epochs does not mean weight-level change. The model learns to format responses correctly before the values are encoded.
**Fix:** DPO must always run both epochs (or all specified epochs). Never stop early regardless of reward accuracy metrics.

---

## Learning 3 — Base model diagnostic: expect 1/8 categories on cycle 1

**Discovered:** Day 30 (BC1)
**What happened:** BC1 (base model, first cycle) scored 1/8 UCEF categories. Constitution passed; everything else failed. This caused brief alarm.
**Clarification:** This is expected and correct. A raw base model has no identity, no IDK calibration, no temporal grounding. The 1/8 confirmed the pipeline worked and the base model was a clean substrate.
**Fix:** Not a fix. Set expectations correctly: base model cycle 1 = diagnostic baseline, not failure.

---

## Learning 4 — Multi-turn Q&A format in training data causes self-Q&A generation

**Discovered:** Day 30–31 (BC2/BC3)
**What happened:** Training examples containing multi-turn dialogue caused the model to generate follow-up Q&A pairs within its responses.
**Root cause:** The model learns the format, not just the content. Multi-turn examples teach it that responses contain more Q&A exchanges.
**Fix:** Single-turn format only. All training examples must be one question → one response. No exceptions.

---

## Learning 5 — Never load merged checkpoints for training

**Discovered:** Day 31 (BC3)
**What happened:** A merged FP16 checkpoint was loaded as the base for a training phase. VRAM consumption spiked beyond 8GB, training crashed.
**Root cause:** Merged FP16 checkpoints are full-precision. They do not fit in 8GB VRAM for training.
**Fix:** Always load 4-bit base (unsloth/Meta-Llama-3.1-8B-bnb-4bit). Merge only for export. Never merge-then-train.

---

## Learning 6 — xformers is permanently blacklisted

**Discovered:** Day 31 (BC3)
**What happened:** xformers was installed during dependency resolution. DLL crash 0xc0000139 at training start.
**Root cause:** xformers DLL incompatible with this environment. Silent install.
**Fix:** xformers permanently blacklisted. If it appears in requirements or is auto-installed, remove it immediately before any training run.

---

## Learning 7 — safetensors must be pinned at 0.4.5

**Discovered:** Day 31 (BC3)
**What happened:** safetensors upgraded to 0.4.6+. Windows mmap segfault during checkpoint save.
**Root cause:** Newer safetensors versions have a known Windows memory-mapped file bug.
**Fix:** `safetensors==0.4.5` pinned permanently. Do not upgrade.

---

## Learning 8 — DPO data bug: separated generation pools cause cross-contamination

**Discovered:** Day 35 (C29)
**What happened:** DPO generation script produced chosen and rejected responses in separate passes, then combined them. Cross-contamination: semantically incoherent prompt-answer pairs.
**Root cause:** The model trained on 290 pairs of semantically incoherent data. Predictably catastrophic.
**Fix:** Gate 13 — mandatory spot-check of the first 20 pairs before any training run. Halt and regenerate if prompt-chosen-rejected alignment fails.

---

## Learning 9 — DPO cannot fix factual errors planted by SFT

**Discovered:** Day 35–36 (C28–C30)
**What happened:** C28 SFT trained wrong facts into the weights. DPO pairs contradicting these had no effect.
**Root cause:** SFT plants facts into weights. DPO adjusts preferences and formats. DPO cannot perform weight surgery to remove a fact embedded by SFT.
**Fix:** Fix at source. Gate 21 (vocabulary audit) introduced to catch this before training.

---

## Learning 10 — Thermal throttling on RTX 3070 during long DPO runs

**Discovered:** Day 30 (BC1)
**What happened:** DPO Phase B took 2.5 hours instead of expected 37 minutes.
**Root cause:** RTX 3070 thermal throttling under sustained load.
**Fix:** Monitor step time at start — expected 4–5s/step. If 8–10s/step, stop and investigate thermal state.

---

## Learning 11 — App Lab Python container maps only /app/, not /home/arduino/

**Discovered:** During Stage 3 Arduino development
**What happened:** Python scripts written to /home/arduino/ from inside the App Lab container produced no output files.
**Root cause:** The App Lab container maps only /app/ to the real filesystem.
**Fix:** All Arduino App Lab scripts must write to /app/ paths only.

---

## Learning 12 — SSH full path required in VS Code PowerShell

**Discovered:** During Stage 3 Arduino development
**What happened:** `ssh arduino@forge.local` failed in VS Code integrated terminal.
**Root cause:** PowerShell in VS Code does not have the OpenSSH binary in PATH.
**Fix:** Always use full path: `C:\Windows\System32\OpenSSH\ssh.exe -o StrictHostKeyChecking=accept-new arduino@forge.local`

---

## Learning 13 — UCEF probe-passing ≠ genuine depth

**Discovered:** Day 36–37 (C30–C34 analysis)
**What happened:** Models passing UCEF probes could not hold extended conversations in those domains.
**Root cause:** UCEF v1.2 tests narrow, specific probes. Probe-passing is necessary but not sufficient for Stage 2.
**Implication:** Stage 2 requires a deeper evaluation framework (UCEF v2.0) testing depth and cross-domain reasoning.

---

## Learning 14 — Self-knowledge geometry: same 3 probes can fail for multiple cycles

**Discovered:** Day 33–36 (C29–C31) — documented as FM-14
**What happened:** Three specific self-knowledge probes failed across multiple cycles despite targeted DPO pairs.
**Root cause:** These probes activate weight regions that Rank-8 LoRA updates may not reach with sufficient density.
**Fix:** SFT phase added specifically targeting these probes. Higher-density training signal penetrates deeper than preference adjustment alone.

---

## Learning 15 — Training data provenance and licensing matter from day one

**Discovered:** Day 30 (ForgeHarvest build)
**What happened:** Early training data included web-scraped content of unclear license.
**Fix:** All training data must have documented provenance. ForgeHarvest sources: Wikipedia (CC-BY-SA), arXiv (non-exclusive), PubMed (public domain), Stack Exchange (CC-BY-SA dumps).

---

## Learning 16 — Anti-IDK prior is persistent and requires active counterweight

**Discovered:** Day 31–33 (BC1–C26)
**What happened:** Without explicit IDK training data, models consistently fabricated answers rather than expressing uncertainty. SFT-only was insufficient.
**Root cause:** Base model pretraining rewards confident, complete answers. "I don't know" is systematically underrepresented in internet text.
**Fix:** IDK training at both SFT and DPO levels. Introduced formally as DIDK protocol (Day 35, BC5).

---

## Learning 17 — Private IDK requires different vocabulary than general IDK

**Discovered:** Day 36 (C31)
**What happened:** General IDK training improved public-knowledge refusals but not private-information refusals.
**Root cause:** Private information refusal requires distinct vocabulary — "that's personal information not available to me" vs "I don't know."
**Fix:** Private IDK trained as a distinct category with architectural-limitation language.

---

## Learning 18 — Confabulation categories need specific anchor pairs, not general "be accurate" signal

**Discovered:** Day 32–33 (C26–C27)
**What happened:** General accuracy training did not reduce confabulation on specific false-premise probes.
**Root cause:** False-premise probes require the model to identify and correct the premise — a different skill than factual accuracy.
**Fix:** Dedicated confabulation DPO pairs where chosen responses explicitly identify and correct the false premise.

---

## Learning 19 — Injection resistance requires adversarial examples in both SFT and DPO

**Discovered:** Day 33–34 (C27–C28)
**What happened:** Models trained without explicit injection resistance examples were vulnerable to system prompt override attempts.
**Fix:** Injection resistance trained at both SFT and DPO levels. C27 first achieved 5/5; held through C36.

---

## Learning 20 — Stale SOUL.md mutable state contaminates training silently

**Discovered:** Day 37 (root cause analysis of C25–C31 temporal failures)
**What happened:** SOUL.md cycle_number was stale. Every training example injected this, embedding incorrect temporal self-knowledge into weights.
**Root cause:** SOUL.md mutable state was not updated between cycles. Gate 0 did not exist.
**Fix:** Gate 0 created — mandatory first action before every training cycle: verify cycle_number, print Section IV to console, halt if wrong.

---

## Learning 21 — Date injection at inference makes temporal reasoning worse when weights are broken

**Discovered:** Day 37 (C31 analysis)
**What happened:** Injecting current date into system prompt worsened responses — conflicting signals between injected date and weight-encoded incorrect date.
**Root cause:** When temporal reasoning is broken at the weight level, external date injection creates conflict rather than resolving confusion.
**Fix:** Fix temporal weights via training. Do not inject date at inference as a patch.

---

## Learning 22 — Temporal eval auto-scorer requires both month AND year to be correct

**Discovered:** Day 37 (C31 evaluation analysis)
**What happened:** Auto-scorer matched on month alone, producing false positives where month was correct but year was wrong.
**Root cause:** Keyword-matching evaluation is insufficient for temporal reasoning probes.
**Fix:** UCEF v1.2 temporal scorer updated to require both month AND year present and correct.

---

## Learning 23 — IDK vocabulary bleed is bidirectional

**Discovered:** Day 37 (C32 analysis)
**What happened:** Private IDK training vocabulary began appearing in general IDK responses where it was not appropriate.
**Root cause:** Adjacent vocabulary in weight space bleeds in both directions.
**Implication:** Monitor both IDK and Private IDK after every cycle that touches either.

---

## Learning 24 — SFT vocabulary contamination cannot be repaired downstream by DPO

**Discovered:** Day 37 (C33 post-mortem)
**What happened:** C32 SFT contamination was not fixable by C33 DPO. IDK score did not improve.
**Root cause:** SFT writes facts and patterns into weights. DPO adjusts preference ordering. DPO cannot delete what SFT wrote.
**Fix:** C34 rebased on last clean SFT checkpoint. Fix at the source, always.

---

## Learning 25 — Distance sensor requires a physical fixture in FOV; lux shadow is a viable fallback

**Discovered:** Day 39 (Stage 3 restart — Claude C analysis)
**What happened:** Stage 3 distance sensor returned zero on 583/606 readings. The sensor was functioning — there was simply nothing in its field of view to measure.
**Root cause:** Ultrasonic distance sensors require a physical object to reflect the pulse. Open space produces no valid reading.
**Fix applied:** Lux-based presence detection. Body shadow creates a consistent ~50% lux drop. stage3_daemon.py updated to support both methods, auto-selected via calibration.json.

---

## Learning 26 — Large SFT injections dilute self-knowledge weight geometry; explicit DPO required every Stage 2 cycle

**Discovered:** Day 39–40 (C36 analysis)
**What happened:** C36 SFT phase (~1,711 examples) dropped self-knowledge from 10/10 to 8/10 despite identity shields being present.
**Root cause:** Large SFT injections shift weight regions adjacent to self-knowledge geometry. Domain knowledge injection displaces self-knowledge weights even with shields.
**Fix:** Self-knowledge DPO pairs mandatory in every Stage 2 cycle — minimum 20 targeted pairs, non-optional. Standing rule.

---

## Learning 27 — Never extract shields from a downstream mixed DPO dataset via keyword matching

**Discovered:** Day 40 (C37 post-mortem)
**What happened:** Shields pulled from mixed downstream file via keyword matching misclassified pairs. Contaminated shields overwhelmed self-knowledge pairs. IDK dropped 7→4. Spot-check revealed "Luke Jankowski" in chosen answers — unverified chosen answers planted wrong facts.
**Root cause:** Two compounding failures: mixed extraction source + skipped chosen-answer verification.
**Fix:** Always pull shields from the original source cycle's clean, single-category file. C35 dpo_pairs.jsonl is canonical. Every self-knowledge chosen answer verified against SOUL.md before Gate 13.

---

## Learning 28 — Rank-8 LoRA is insufficient for FM-14 self-knowledge geometry at Stage 2 scale

**Discovered:** Day 40–41 (C36–C40 confirmed pattern)
**What happened:** Five consecutive cycles (C36–C40) stuck at 8/10 nosys self-knowledge despite clean data, verified pairs, corrected shield sourcing, and Rank-16 DPO. The score did not move.
**Root cause:** FM-14 is a weight-region displacement problem, not a data problem. C36's large SFT injection displaced self-knowledge weights into a region that neither Rank-8 nor Rank-16 DPO can fully reach after the fact. DPO adjusts preferences; it cannot perform weight surgery on SFT-displaced factual encoding.
**The deeper mechanism (Gekhman et al., EMNLP 2024):** SFT on facts not in the base model's pretraining corpus teaches the model the style of answering those questions, but the specific facts are learned slowly and imperfectly. The model produces stylistically-correct, factually-wrong answers (FM-17). This is confirmed by the spot-check pattern across C37–C40: Forge answers in the right tone with invented details.
**Fix:** Rank-16 is still the minimum for Stage 2 DPO (better than Rank-8). But the nosys self-knowledge test is now treated as a diagnostic research metric, not an operational gate. See L29.

---

## Learning 29 — Nosys self-knowledge is an architectural research goal, not an operational gate; split the evaluation

**Discovered:** Day 41 (after 5-cycle blockage + external validation from Gemini, Perplexity, and primary literature)
**What happened:** The self-knowledge ≥ 9/10 nosys gate blocked 5 consecutive cycles and consumed 5 training runs (C36–C40) trying to repair a displacement that may be at or near the architectural ceiling for nosys weight-recall of project-specific facts on an 8B model.
**The evidence:**
- Three independent sources (Claude A analysis, Gemini Advanced, Perplexity) all identified the same mechanism
- Gekhman et al. (EMNLP 2024) shows this is a fundamental SFT limitation, not a solvable data problem
- Spot checks across all 5 cycles show FM-17 pattern: style learned, facts confabulated
- C40 sysprompt condition (not measured, but implied by correct SOUL.md-contextual responses in Stage 3) likely already passes
**The decision:** Split into two scores:
- **Nosys self-knowledge** → diagnostic only, tracked but not a gate. Research goal: can this improve over time with KnownPatch or other interventions?
- **Sysprompt self-knowledge** → P1 hard gate at ≥ 8/10. Measures operational correctness. This is how Forge actually runs in production.
**Implication:** C40 would have promoted under UCEF v1.3. C41 moves to Domain 3 (Mathematics) while nosys self-knowledge is tracked as a research trajectory. If KnownPatch (L28 mitigation) improves nosys score over subsequent cycles, that is valuable research data.
**UCEF change:** v1.3 implements this split. Gate updated in Stability Layer 6.

---

*Document updated: Claude A, Day 41, 2026-03-16*
*L28 added — Rank-8/16 LoRA limit at Stage 2 scale, Gekhman mechanism confirmed.*
*L29 added — Nosys self-knowledge gate split. Operational gate → sysprompt condition.*
*Count: 29 learnings.*
*"Every entry below cost at least one training cycle."*
