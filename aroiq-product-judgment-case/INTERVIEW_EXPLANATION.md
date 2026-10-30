# Interview Explanation — AroIQ Product Judgment Case

## 30-second version

I studied Arolytics' public Product Manager role and focused on one responsibility that appears central: deciding whether newly onboarded customer data is trustworthy enough to become product truth. I built a small synthetic acceptance case where the historical numbers reconcile, but one SCADA tag mapping is still not confirmed by the operator. I deliberately return REVIEW rather than ACCEPT because a plausible number is not enough if the meaning of its source signal is unresolved.

## 90-second version

AroIQ takes customer-specific industrial telemetry and turns it into product outputs used by different teams. As that scales across customers and facilities, I think a major product challenge is preserving the meaning and traceability of a number from source data through mapping, model output, aggregation and customer-facing views.

So I created a synthetic onboarding gate. It checks a versioned event contract, source-tag mappings, separate detection/causation/quantification confidence, historical reference events and facility/portfolio reconciliation. The interesting part is that the numbers all look good, but one tag mapping remains unapproved. My decision is REVIEW, not ACCEPT.

The point is not the Python. The point is product judgement: Data Engineering can make the pipeline run and Data Science can produce an output, but Product still owns the evidence required to ship. AI can help profile and test the data, but it should not resolve ambiguous physical meaning on its own.

## What I would never claim

- I did not recreate AroIQ.
- I did not use real Arolytics/customer data.
- I am not claiming emissions-engineering expertise I do not have.
- The tag names, thresholds, volumes and schema are synthetic.

## Why this shows my fit

My strength is entering a complex domain, identifying where correctness actually matters, translating ambiguity into explicit acceptance criteria, and using AI/code to accelerate the work while keeping final judgement human-owned.

That is the same pattern I have used in regulated financial workflows, data-validation exercises, AI-agent controls and business-system projects.

## Likely interview questions

### Why did you use REVIEW instead of ACCEPT?
Because the unresolved tag mapping creates semantic uncertainty. A model can be numerically close to a reference result for the wrong reason. I would want operator confirmation of what the source signal physically means, version that mapping, rerun the reference pack, and only then decide whether to accept.

### Why didn't you build an emissions model?
Because that would have been artificial and misleading without their domain data, physics assumptions and internal methods. The role says Product works with data scientists and emissions specialists; I chose to demonstrate the part Product should own directly: evidence, contracts, acceptance and release judgement.

### What would you do first if hired?
I would learn the current customer-onboarding workflow end to end: source systems, mapping ownership, reference datasets, exception handling, model/version provenance and the current acceptance decision. I would then identify where meaning or ownership is implicit and make those gates explicit without adding unnecessary process.

### Where would you use Claude/AI?
For profiling exports, drafting candidate mappings/transforms, finding anomalies, generating test cases, comparing reference periods and summarizing differences. I would keep physical tag meaning, material exceptions and final customer-data acceptance with accountable humans.

### What is the hardest AroIQ product problem in your view?
Preserving semantic trust as customer-specific SCADA is normalized into one scalable product. When a number changes, the team should be able to explain whether the source, mapping, model/method, late-arriving data, aggregation or product logic changed.
