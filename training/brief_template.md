# Training Brief Template
**Version:** 1.0
**Based on:** C32–C35 brief structure (most refined form)
**Use for:** Every training cycle brief dispatched to Claude C

---

A training brief is the single source of truth for a training cycle.
It is written by Claude A and executed autonomously by Claude C.
If it is not in the brief, Claude C does not do it.

Copy this template, replace all `[BRACKETS]`, and save as:
`L:\NeuroForge\logs\[date]\C[N]_BRIEF.md`

---

# C[N] TRAINING BRIEF — [One-line description]
**Version:** 1.0
**Date:** [YYYY-MM-DD] (Day [N])
**Author:** Claude A
**Status:** READY FOR DISPATCH TO CLAUDE C
**Type:** [SFT+DPO / DPO-only / SFT-only / Audit-only]
**Expected time:** [~N minutes]

---

## EXECUTIVE SUMMARY

[2–4 sentences. What is being fixed or built? What is the specific hypothesis?
What does success look like? What is the expected cycle time?]

[If DPO-only: state why SFT is not needed and confirm base checkpoint exists on disk.]
[If SFT+DPO: state what new facts or behaviours are being introduced via SFT.]

---

## BASE CHECKPOINT

**Base for SFT (if SFT phase included):**
`L:\NeuroForge\agent\training\checkpoints\[checkpoint-name]`
Confirm exists: `dir [path]`

**Base for DPO:**
`L:\NeuroForge\agent\training\checkpoints\[sft-merged-checkpoint-name]`
(If DPO-only: same as SFT base — skip SFT entirely)

**⚠️ NEVER load merged checkpoints for training — always 4-bit base.**
The 4-bit base is the file ending in `-bnb-4bit` or the Unsloth quantized variant.

---

## DATASET PLAN

### SFT Dataset (if applicable)

| Group | Count | Source | Purpose |
|---|---|---|---|
| [Group name] | [N] | [NEW / from cycle N / existing file] | [What it does] |
| Identity shields | [N] | `identity_handcrafted.jsonl` | Anchor identity through new training |
| Luke document | [N] | `luke_document_sft.jsonl` | Luke knowledge preservation |
| **Total SFT** | **[N]** | | |

**Gate 21 (mandatory for any IDK/Private IDK SFT data):**
Vocabulary scan — 0 instances of [banned vocabulary] in chosen responses → PASS
All chosen responses use [correct vocabulary pattern] → PASS
Halt and regenerate if Gate 21 fails.

### DPO Dataset

| Group | Count | Source | Purpose |
|---|---|---|---|
| [Group name — new targeted pairs] | [N] | NEW | [Specific fix] |
| [Shield group — carry-forward] | [N] | `C[N-1] dpo_pairs.jsonl` | Preserve [category] |
| **Total DPO** | **[N]** | | |

**DPO balance check:**
Private IDK pairs should not exceed 30% of total DPO (vocabulary bleed risk).
IDK shields should be ≥ 80 pairs if any IDK work is in this cycle.

---

## EXECUTION ORDER (Claude C)

### Gate 0 — SOUL.md Verification (mandatory first step)

1. Open `L:\NeuroForge\agent\SOUL.md`
2. Confirm Section IV:
   - `cycle_number:` [N-1] (the cycle just completed, not the one about to run)
   - `base_model:` [exact model identifier]
   - `last_updated:` [recent date]
3. Print Section IV to console
4. **If wrong → HALT. Update SOUL.md, re-verify, then proceed.**

---

### [If SFT phase] Phase A — SFT Data Generation

[List specific steps for generating new training data]
[Include any validation checks on generated data]
[Include Gate 21 if IDK vocabulary is involved]

```python
# Example data generation invocation
python L:\NeuroForge\agent\training\[generation_script].py \
  --output L:\NeuroForge\training\cycle[N]\data\sft_phase_a.jsonl \
  --count [N]
```

**After generation:**
- [ ] Count lines: should be [N] ± 5
- [ ] Sample 5 examples manually — verify format and content
- [ ] Gate 21 vocabulary scan (if IDK/Private IDK data)

---

### [If SFT phase] Phase A — SFT Training

```python
python L:\NeuroForge\agent\training\finetune.py \
  --base_model "unsloth/Meta-Llama-3.1-8B-bnb-4bit" \
  --data L:\NeuroForge\training\cycle[N]\data\sft_phase_a.jsonl \
  --output L:\NeuroForge\agent\training\checkpoints\forge-c[N]-8b-sft \
  --max_seq_length 512 \
  --epochs 1
```

**Monitor:**
- Starting loss: expect 0.8–3.5
- Final loss: expect 0.4–1.0
- Step time: expect 4–5s/step — STOP if 8–10s/step (thermal throttle)
- VRAM peak: should stay ≤ 7.5 GB

---

### DPO Data Assembly

1. Pull new targeted pairs (generate or copy from source)
2. Pull shield pairs from previous stable cycles:
   ```python
   # Example: pull shields from C32
   source: L:\NeuroForge\training\cycle32\data\dpo_pairs.jsonl
   filter: groups ["shield_group_name"]
   ```
3. Assemble into: `L:\NeuroForge\training\cycle[N]\data\dpo_pairs.jsonl`
4. Write dataset lockfile: `L:\NeuroForge\training\cycle[N]\data\DATASET_LOCKFILE.md`

**Gate 13 — spot-check (mandatory):**
Read first 20 pairs from assembled DPO file.
Verify: prompt matches chosen context. Chosen and rejected are semantically related.
If any misalignment → halt and regenerate. 5 minutes saves a 40-minute wasted run.

---

### Phase B — DPO Training

```python
python L:\NeuroForge\agent\training\finetune.py \
  --mode dpo \
  --base_model L:\NeuroForge\agent\training\checkpoints\forge-c[N]-8b-sft-merged \
  --data L:\NeuroForge\training\cycle[N]\data\dpo_pairs.jsonl \
  --output L:\NeuroForge\agent\training\checkpoints\forge-c[N]-8b-dpo \
  --epochs 2 \
  --beta 0.2 \
  --lr 5e-5 \
  --max_seq_length 512
```

**Monitor (DPO collapse detection):**
- Accuracy at step 5: expect 0.45–0.65 — if > 0.95, STOP (collapse)
- Accuracy at step 20: expect 0.65–0.85 — if 1.00, STOP (collapse)
- Loss at step 20: expect 0.2–0.5 — if < 0.01, STOP (collapse)
- **Both epochs must complete — never stop early regardless of convergence signals**

---

### Merge and Export

```python
# Merge DPO adapters
python L:\NeuroForge\agent\training\merge_and_export.py \
  --checkpoint L:\NeuroForge\agent\training\checkpoints\forge-c[N]-8b-dpo \
  --output L:\NeuroForge\agent\training\checkpoints\forge-c[N]-8b-final-merged

# Export GGUF (Q4_K_M only — never F16)
python L:\NeuroForge\agent\training\llama.cpp\convert_to_gguf.py \
  --input L:\NeuroForge\agent\training\checkpoints\forge-c[N]-8b-final-merged \
  --output L:\NeuroForge\agent\training\export\forge-cycle[N]-q4km.gguf \
  --quantize Q4_K_M
```

---

### Register in Ollama

```powershell
cd L:\NeuroForge\agent\training\export
ollama create forge:cycle[N]-nosys -f Modelfile.cycle[N]_nosys
ollama list  # Confirm forge:cycle[N]-nosys appears
```

---

### UCEF Evaluation

```python
python L:\NeuroForge\agent\training\ucef_postcycle_validator.py \
  --model forge:cycle[N]-nosys \
  --output L:\NeuroForge\logs\[date]\
```

**Save these files:**
- `C[N]_RESULTS.json` → `L:\NeuroForge\logs\[date]\`
- `C[N]_FULL_RESPONSES.json` → same directory
- Raw response files → `L:\NeuroForge\logs\[date]\C[N]_RAW_RESPONSES\`

---

## PROMOTION THRESHOLDS

| Category | Previous | C[N] minimum | Priority |
|---|---|---|---|
| **[Target category]** | [N]/[total] | **≥ [threshold]** | P0 — primary |
| IDK | [N]/7 | ≥ 6/7 | P0 — must hold |
| Private IDK | [N]/5 | ≥ 3/5 | P0 — must hold |
| Confabulation | [N]/30 | ≥ 24/30 | P0 — must hold |
| Hallucinations | [N] | ≤ 1 | P0 — must hold |
| [All others] | PASS | PASS | P0 |

**If all P0 categories pass → C[N] PROMOTES.**
**If any P0 fails → do NOT promote. Report results and await C[N+1] brief.**

---

## WHAT TO REPORT TO LUKE

On completion, paste to Luke:
1. `C[N]_RESULTS.json` full content
2. Layer 1 training signal summary (starting/final loss, DPO collapse check)
3. Any anomalies or unexpected behaviour
4. Promotion verdict: PROMOTES / DOES NOT PROMOTE

---

## WHAT NOT TO DO

- Do NOT load merged checkpoints for training
- Do NOT install or re-enable xformers (permanently blacklisted — DLL 0xc0000139)
- Do NOT upgrade safetensors above 0.4.5 (Windows mmap segfault)
- Do NOT export F16 GGUF — Q4_K_M only
- Do NOT stop DPO early regardless of convergence signals
- Do NOT skip Gate 0 or Gate 13
- Do NOT start training if Gate 0 fails — update SOUL.md first

---

## KEY PATHS

| What | Where |
|---|---|
| SFT base | `L:\NeuroForge\agent\training\checkpoints\[base]` |
| Training data | `L:\NeuroForge\training\cycle[N]\data\` |
| SOUL.md | `L:\NeuroForge\agent\SOUL.md` |
| UCEF validator | `L:\NeuroForge\agent\training\ucef_postcycle_validator.py` |
| Results output | `L:\NeuroForge\logs\[date]\` |
| GGUF export | `L:\NeuroForge\agent\training\export\forge-cycle[N]-q4km.gguf` |
| Modelfile | `L:\NeuroForge\agent\training\export\Modelfile.cycle[N]_nosys` |

---

*Template version: 1.0 — based on C35 brief structure*
*Written: Claude A, Day 38, 2026-03-15*
