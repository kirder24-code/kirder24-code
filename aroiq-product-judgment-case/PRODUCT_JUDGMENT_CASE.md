# AroIQ Product Judgment Case

## Decision in one sentence

**REVIEW — do not accept this customer onboarding yet.**

The historical back-test is numerically within the synthetic tolerance, but one SCADA tag used to interpret flare pilot state has not been semantically confirmed by the operator. A plausible number is not enough if the source meaning is unresolved.

## 1. The product question

Data Engineering can make a pipeline run. Data Science can make a model produce an output.

The Product Manager still has to answer:

> **Is this customer's data trustworthy enough to become product truth?**

That decision needs more than a green pipeline or a plausible chart.

## 2. Flow of truth

Customer SCADA → semantic tag mapping → normalized process data → model outputs → event contract → facility rollup → portfolio rollup → operator view / export

At each boundary, the meaning of the data has to survive.

A field contract should therefore define not only type and location, but semantic meaning, unit, grain, nullability, provenance, mapping version, model/method version, uncertainty and aggregation rule.

## 3. Synthetic failure case

The sample customer has three facilities.

The historical back-test reconciles within the demo tolerance:
- NS-01: 2,060 m³
- NS-02: 1,050 m³
- NS-03: 710 m³
- Portfolio: 3,820 m³

All five reference events are numerically close to the synthetic expected values.

But at NS-03, `PILOT_A → flare_pilot_status` is still awaiting operator confirmation.

If that tag does not mean what we think it means, the downstream causation may be plausible but semantically wrong.

**Decision: REVIEW, not ACCEPT.**

## 4. What I would ask before ship

### Operator / customer SME
- What physical state does `PILOT_A` actually represent?
- Is its polarity stable across all facilities or only NS-03?
- Are there operating modes where this signal is stale, bypassed or manually overridden?
- Was instrumentation or historian configuration changed during the historical period?

### Data Engineering
- Where is the tag mapping version stored?
- Can a historical record be reproduced with the mapping version that produced it?
- How are late-arriving records handled?
- What happens when a customer renames/reuses a tag?
- Can a mapping change silently restate historical events?

### Data Science / emissions analyst
- Which downstream outputs depend on this tag?
- Does it affect detection, causation, quantification, or only context?
- What evidence is required before causation can be promoted from possible to likely?
- What uncertainty should be shown if semantic context is incomplete?

### Product / Engineering
- Which value changes are release blockers?
- When must a customer-facing number be restated?
- Does the UI preserve detection, causation and quantification confidence separately?
- Can an operator see why an event changed after a model or mapping revision?

## 5. Where AI helps — and where it should stop

### AI should help with
- profiling a customer export;
- suggesting candidate tag mappings;
- detecting missing ranges, duplicates and unusual distributions;
- drafting transforms;
- comparing outputs to reference periods;
- generating candidate test cases;
- summarizing differences for review.

### AI should not decide
- what an ambiguous process tag means;
- whether a physically plausible output is operationally correct;
- whether unresolved mapping uncertainty is acceptable;
- whether a customer onboarding can be accepted;
- whether a changed regulatory/financial number is safe to publish.

**AI does the volume. The accountable human owns acceptance.**

## 6. Why I built this

I do not have access to AroIQ's internal schema, algorithms or customer data, and I intentionally did not try to imitate them.

This case is based only on the public Product Manager role and public AroIQ material. The data, facilities, tag names, tolerances and calculations are synthetic.

The goal is to show how I would approach a product decision where data is messy, a model can look correct, the numbers reconcile, but the semantic evidence is still incomplete.

That is exactly the point where product judgement matters.
