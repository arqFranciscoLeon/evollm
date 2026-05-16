# PR: Cross-provider n=500 extension + verifiable replication package

**Base:** `main`  ·  **Compare:** `claude/stupefied-mclaren`

## Summary

Extends the Willis et al. (2025) EvoLLM benchmark to four 2025–2026 frontier
models (Claude Sonnet 4.6, Gemini 2.5 Flash, Gemini 3.1 Pro, GPT-5.4 Mini)
across 3 prompt styles × 4 population regimes, at **n=500 Moran iterations per
condition**. Upstream structure (`src/evollm/`, `strategies/`, `tests/`) is
preserved so results stay comparable and reproducible.

## What's included

- **n=500 results**: `results/modal_waves_final_*.json` — authoritative,
  48 conditions, integer win counts summing to 500.
- **Wave-based Modal harness**: `modal_moran_waves.py` (checkpointed; avoids
  starter-tier preemption that fails a single 12k-task submission).
- **Paper-view GUI**: new "📄 Vista Paper" Streamlit tab reproducing
  Tables 5/6/8 and Figure 2 from the n=500 JSON, with CSV export.
- **Self-contained verification**: `reproduce_tables.py` — stdlib-only,
  one command, reproduces every paper number (no API keys / cloud / scipy).
- **Replication hardening**: `LICENSE` (MIT, credits upstream),
  `REPRODUCE.md` (tiered verification ladder), `CHECKSUMS.txt` (SHA-256
  integrity manifest), pinned `environment.yml` (axelrod==4.14.0),
  `.env.example`, hardened `.gitignore` (no secrets, no scaffold).
- **`EXTENSION.md`**: scientific overview, hypotheses (incl. corrected H4
  *suggestive — not robustly confirmed*), reproduction guide, citation.

## Hypotheses (peer-reviewed; AAMAS R&R Minor Revisions)

- H1 cooperative bias persists — Confirmed within the tested library (9/12)
- H2 aggressive capability parity — Partially supported
- H3 cross-provider divergence — Confirmed (z up to 17.1, Holm-Bonferroni)
- H4 noise robustness improves — Suggestive, NOT robustly confirmed
  (cross-study comparison not significant once the n=100 predecessor's
  sampling error is propagated; predecessor deliberately not re-run to
  avoid result-driven analysis)

## Verification (reviewer can run in ~1 minute)

```bash
python reproduce_tables.py    # reproduces Tables 5/6/8 + H3/H4, matches manuscript
```

## Test plan

- [ ] `python reproduce_tables.py` output matches the manuscript tables
- [ ] `sha256sum -c` against `CHECKSUMS.txt` passes
- [ ] `python -m streamlit run gui.py` → "Vista Paper" tab renders
- [ ] No secrets in the diff (`.env` git-ignored; `.env.example` is a template)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
