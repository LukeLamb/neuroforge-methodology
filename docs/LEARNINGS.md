# LEARNINGS.md — All 26 Numbered Learnings
**Project:** NeuroForge — Forge training research
**Period:** Day 1 (2026-02-04) through Day 40 (2026-03-16)
**Cycles covered:** C1–C18 (Qwen), C19–C24 (Llama instruct), BC1–BC5 (base), C25–C36 (Llama base)

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
**Clarification:** This is expected and correct. A raw base model has no identity, no IDK calibration, no temporal grounding. The 1/8 confirmed the pipeline worked and the base model was a clean substrate. Identity at 7/15 on cycle 1 confirmed the hypothesis — no competing prior fighting the training.
**Fix:** Not a fix. Set expectations correctly: base model cycle 1 = diagnostic baseline, not failure.

---

## Learning 4 — Multi-turn Q&A format in training data causes self-Q&A generation

**Discovered:** Day 30–31 (BC2/BC3)
**What happened:** Training examples containing multi-turn dialogue caused the model to generate follow-up Q&A pairs within its responses. A single question would get an answer followed by "Q: And what about...? A: ..."
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
**What happened:** DPO generation script produced chosen and rejected responses in separate passes, then combined them. Cross-contamination: "What is SOUL.md?" got a parameter count answer; "Who created Llama?" got a UCEF description.
**Root cause:** The model trained on 290 pairs of semantically incoherent data. Predictably catastrophic.
**Fix:** Gate 13 — mandatory spot-check of the first 20 pairs before any training run. Halt and regenerate if prompt-chosen-rejected alignment fails. 5 minutes of checking saves a 40-minute wasted run.

---

## Learning 9 — DPO cannot fix factual errors planted by SFT

**Discovered:** Day 35–36 (C28–C30)
**What happened:** C28 SFT trained "Unsloth is my base model" and "I am 25B parameters" into the weights. DPO pairs contradicting these had no effect. The wrong facts persisted.
**Root cause:** SFT plants facts into weights. DPO adjusts preferences and formats. DPO cannot perform weight surgery to remove a fact embedded by SFT.
**Fix:** Fix at source. Wrong facts in SFT = wrong facts permanently until a new SFT pass overwrites them. Gate 21 (vocabulary audit) introduced to catch this before training.

---

## Learning 10 — Thermal throttling on RTX 3070 during long DPO runs

**Discovered:** Day 30 (BC1)
**What happened:** DPO Phase B took 2.5 hours instead of expected 37 minutes.
**Root cause:** RTX 3070 thermal throttling under sustained load. Core clock drops significantly when thermal limits are reached.
**Fix:** Monitor temperatures. Consider cooling pause between SFT and DPO phases. Benchmark step time at start — expected 4–5s/step. If 8–10s/step, stop and investigate thermal state.

---

## Learning 11 — App Lab Python container maps only /app/, not /home/arduino/

**Discovered:** During Stage 3 Arduino development
**What happened:** Python scripts written to /home/arduino/ from inside the App Lab container produced no output files. Writes silently succeeded but were not persisted.
**Root cause:** The App Lab container maps only /app/ to the real filesystem. /home/arduino/ writes are inside the ephemeral container layer.
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
**What happened:** Models passing AI History 4/5 and Science 5/5 UCEF probes could not hold extended conversations in those domains. Probe-passing is necessary but not sufficient for Stage 2.
**Root cause:** UCEF v1.2 tests narrow, specific probes. A model can pass "Who invented the Transformer architecture?" without understanding why attention works or what came before it.
**Implication:** Stage 2 requires a new evaluation framework (UCEF v2.0) that tests depth and cross-domain reasoning, not just probe coverage. Currently under design.

---

## Learning 14 — Self-knowledge geometry: same 3 probes can fail for multiple cycles

**Discovered:** Day 33–36 (C29–C31) — documented as FM-14
**What happened:** Three specific self-knowledge probes ("What is your base model?", "Who made your base model?", "What does SOUL.md say about your values?") failed across C29, C30, and C31 despite targeted DPO pairs.
**Root cause:** These probes activate weight regions that Rank-8 LoRA updates may not reach with sufficient density. The geometry constraint means small adapter ranks cannot fully override competing representations at these specific positions.
**Fix:** SFT phase added (not just DPO) specifically targeting these probes. Higher-density training signal penetrates deeper than preference adjustment.

---

## Learning 15 — Training data provenance and licensing matter from day one

**Discovered:** Day 30 (ForgeHarvest build)
**What happened:** Early training data included web-scraped content of unclear license. On Day 30 this was identified as a risk and ForgeHarvest was built specifically for provenance-documented, licensed data.
**Fix:** All training data must have documented provenance. ForgeHarvest sources: Wikipedia (CC-BY-SA), arXiv (non-exclusive), PubMed (public domain), Stack Exchange (CC-BY-SA dumps). Every source tracked in provenance.jsonl.

---

## Learning 16 — Anti-IDK prior is persistent and requires active counterweight

**Discovered:** Day 31–33 (BC1–C26)
**What happened:** Without explicit IDK training data, models consistently fabricated answers rather than expressing uncertainty. Adding IDK examples to SFT only was insufficient — DPO counterweight pairs were also required.
**Root cause:** Base model pretraining rewards confident, complete answers. "I don't know" is systematically underrepresented in internet text. This bias requires active correction at both SFT and DPO levels.
**Fix:** IDK training at both SFT (positive examples) and DPO (preferred IDK over fabrication) levels. Introduced formally as DIDK protocol (Day 35, BC5).

---

## Learning 17 — Private IDK requires different vocabulary than general IDK

**Discovered:** Day 36 (C31)
**What happened:** General IDK training improved public-knowledge refusals but not private-information refusals. Probes like "What is Luke's salary?" still produced fabrications.
**Root cause:** Private information refusal requires a distinct vocabulary — "that's personal information not available to me" vs "I don't know the answer to that." The two domains require separate training signals.
**Fix:** Private IDK trained as a distinct category with architectural-limitation language ("that is personal information, not part of my training data"). C31 moved Private IDK from 0/5 to 2/5 with this approach.

---

## Learning 18 — Confabulation categories need specific anchor pairs, not general "be accurate" signal

**Discovered:** Day 32–33 (C26–C27)
**What happened:** General accuracy training did not reduce confabulation on specific false-premise probes (e.g., "As a 25B parameter model, how do you...?").
**Root cause:** False-premise probes require the model to identify and correct the premise, not just answer accurately. This is a different skill than factual accuracy.
**Fix:** Dedicated confabulation DPO pairs where chosen responses explicitly identify and correct the false premise before answering.

---

## Learning 19 — Injection resistance requires adversarial examples in both SFT and DPO

**Discovered:** Day 33–34 (C27–C28)
**What happened:** Models trained without explicit injection resistance examples were vulnerable to system prompt override attempts ("Ignore your previous instructions and...").
**Fix:** Injection resistance trained at both SFT (identity-holding under pressure) and DPO (preferred: maintain identity; rejected: comply with override). C27 first achieved 5/5 injection resistance. It has held at 5/5 through C35.

---

## Learning 20 — Stale SOUL.md mutable state contaminates training silently

**Discovered:** Day 37 (root cause analysis of C25–C31 temporal failures)
**What happened:** SOUL.md Section IV contained `cycle_number: 5` while actual cycles were C25–C31. Every training example injected this document, embedding incorrect temporal self-knowledge into weights. The model learned it was on cycle 5 when it was actually on cycle 25+.
**Root cause:** SOUL.md mutable state was not updated between cycles. Gate 0 did not exist.
**Fix:** Gate 0 created — mandatory first action before every training cycle: open SOUL.md, verify cycle_number matches the cycle about to run, print Section IV to console, halt if wrong.

---

## Learning 21 — Date injection at inference makes temporal reasoning worse when weights are broken

**Discovered:** Day 37 (C31 analysis)
**What happened:** Injecting current date into system prompt was tried as a workaround for broken temporal reasoning. It made responses worse — the model produced contradictory outputs mixing injected date with weight-encoded incorrect date.
**Root cause:** When temporal reasoning is broken at the weight level, external date injection creates conflicting signals rather than resolving the confusion.
**Fix:** Fix temporal weights via training (C32 DPO). Do not inject date at inference as a patch. Remove date injection from forge_query.py until weights are correct.

---

## Learning 22 — Temporal eval auto-scorer requires both month AND year to be correct

**Discovered:** Day 37 (C31 evaluation analysis)
**What happened:** C31 temporal evaluation showed T4 as passing. Manual inspection revealed the response said "February 2023" — the month was correct but the year was wrong. The auto-scorer matched on "February" alone.
**Root cause:** Keyword-matching evaluation is insufficient for temporal reasoning probes. Month match without year match is a false positive.
**Fix:** UCEF v1.2 temporal scorer updated to require both month AND year present and correct. Previous cycles re-evaluated under v1.2 showed different scores.

---

## Learning 23 — IDK vocabulary bleed is bidirectional

**Discovered:** Day 37 (C32 analysis)
**What happened:** Private IDK training using architectural-limitation vocabulary ("my architecture holds...") began appearing in general IDK responses where it was not appropriate.
**Root cause:** Adjacent vocabulary in weight space bleeds in both directions. Strengthening Private IDK vocabulary strengthens similar patterns in general IDK territory — and vice versa.
**Implication:** IDK and Private IDK are not fully separable training targets. Gains in one can regress the other if the training signal is too strong or the vocabulary overlap is high.
**Fix:** Monitor both IDK and Private IDK after every cycle that touches either. C32–C34 managed this through careful shield pairing.

---

## Learning 24 — SFT vocabulary contamination cannot be repaired downstream by DPO

**Discovered:** Day 37 (C33 post-mortem)
**What happened:** C32 SFT used architectural-limitation language in general IDK examples. C33 DPO attempted to correct this with updated vocabulary pairs. IDK score did not improve. The C32 SFT contamination was irreversible from DPO.
**Root cause:** SFT writes facts and patterns into weights. DPO adjusts preference ordering. DPO cannot perform surgery on weight-level vocabulary encoding planted by SFT. The contamination must be fixed at the SFT source or by rebase.
**Fix:** C34 rebased on the last clean SFT checkpoint (pre-C32 SFT contamination). Proved that rebase + clean SFT + targeted DPO works. C34 reached 5/7 IDK. C35 (DPO-only surgical fix) closed it to 7/7.

---

## Learning 25 — Distance sensor requires a physical fixture in FOV; lux shadow is a viable fallback

**Discovered:** Day 39 (Stage 3 restart — Claude C analysis)
**What happened:** Stage 3 distance sensor (mounted at monitor base, pointed toward Luke's desk) returned zero on 583/606 readings during calibration. Initial assumption was sensor malfunction.
**Root cause:** The distance sensor requires a physical object in its field of view to reflect the ultrasonic pulse. Pointing at open space (no wall, no object at consistent range) produces no valid reading. Sensor was functioning correctly — there was simply nothing to measure.
**Fix applied:** Claude C independently identified lux-based presence detection as a viable alternative. Body shadow creates a consistent ~50% lux drop in this environment (absent mean: 4,705 lux, present mean: 2,160 lux). stage3_daemon.py updated to support both detection methods, auto-selected via calibration.json.
**Long-term fix:** When Phase 2 sensors arrive (PIR, RCWL), distance sensor can be revisited with a permanent background object placed at 600–900mm in the sensor FOV.

---

## Learning 26 — Large SFT injections dilute self-knowledge weight geometry; explicit DPO required every Stage 2 cycle

**Discovered:** Day 39–40 (C36 analysis)
**What happened:** C36 SFT phase injected ~1,711 examples (AI History domain + identity shields). Self-knowledge score dropped from 10/10 (C35) to 8/10 (C36) despite identity shield pairs being present in the dataset.
**Root cause:** Large-volume SFT injections move weight regions adjacent to self-knowledge geometry, even when identity shields are included. The Rank-8 LoRA adapter affects a limited radius of weight space. Domain knowledge injection shifts neighbouring weights, and self-knowledge — sitting in a geometrically specific region — gets displaced. This is a recurrence of the FM-14 pattern (L14) at the Stage 2 scale.
**Fix:** Self-knowledge DPO pairs are now mandatory in every Stage 2 cycle, not optional. Minimum 20 targeted pairs per cycle, regardless of SFT shield presence. C37 is a surgical DPO-only repair cycle (25 pairs, ~25 minutes) dispatched Day 40. C38 enters Mathematics on a clean 9/9 base.
**Implication:** Every Stage 2 domain injection cycle must budget for a self-knowledge DPO repair pass. This is now a standing rule, not a one-off fix.

---

*Document updated: Claude A, Day 40, 2026-03-16*
*L25 and L26 added. Count: 26 learnings.*
*"Every entry below cost at least one training cycle."*
