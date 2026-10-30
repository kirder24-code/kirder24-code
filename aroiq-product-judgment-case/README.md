# AroIQ Product Judgment Case

**Candidate:** Kirill Derhachenko — Calgary, AB  
**Role:** Product Manager, AroIQ

This is a small synthetic product case built from Arolytics' public Product Manager role and public AroIQ material. It does **not** use Arolytics or customer data and does not claim to reproduce AroIQ's internal implementation.

## The product question

A pipeline can run and a model can produce plausible numbers, but the Product Manager still has to decide:

> **Is this customer's data trustworthy enough to become product truth?**

In this case, the historical back-test reconciles within the synthetic tolerance, but one SCADA tag mapping has not been confirmed by the operator. The correct decision is therefore **REVIEW — do not accept yet**.

## Why I chose this case

Arolytics describes this role as owning customer-data acceptance, data contracts, reference datasets, regression checks, UAT, acceptance criteria and the final decision on what ships. The company also describes AroIQ as scaling across many facilities while preserving explainable, reproducible numbers and keeping detection, causation and quantification uncertainty distinct.

I wanted to demonstrate the judgement at that boundary rather than build a UI mock-up or pretend to reproduce Arolytics' emissions models.

## Start here

1. **[Product Judgment Case](PRODUCT_JUDGMENT_CASE.md)** — the 3–5 minute explanation.
2. **[Evidence vs. Assumptions](EVIDENCE_AND_ASSUMPTIONS.md)** — what comes from public Arolytics material vs. what is synthetic.
3. **[Synthetic onboarding result](output/onboarding_report.html)** — the decision output.
4. `acceptance_gate.py` + `tests/` — supporting executable evidence.
5. **[Interview explanation](INTERVIEW_EXPLANATION.md)** — how I would explain the case in an interview.

## Flow of truth

`Customer SCADA → semantic mapping → model outputs → event contract → facility rollup → portfolio rollup → operator view / export`

The central idea is simple: **numerical plausibility is not the same as semantic correctness**.

AI can accelerate profiling, mapping suggestions, anomaly detection and test generation. It should not decide what an ambiguous process signal means or whether unresolved uncertainty is safe to ship.

## Run locally

```bash
python acceptance_gate.py
python -m unittest discover tests -v
```

The sample is intentionally expected to return `REVIEW`.
