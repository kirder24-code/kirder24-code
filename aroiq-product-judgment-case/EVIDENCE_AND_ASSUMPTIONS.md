# Evidence vs. Assumptions

This artifact deliberately separates what Arolytics says publicly from what I invented for the demonstration.

## Source-backed facts

From Arolytics' public careers/product material:

- AroIQ turns existing oil & gas SCADA into emission events with quantified volume and likely cause.
- AroIQ is scaling from a handful of sites to hundreds.
- The Product Manager owns acceptance criteria, UAT, release decisions, customer onboarding acceptance, data contracts, reference datasets and regression checks.
- The Product Manager is expected to understand data flow from source to screen and reconcile numbers across sources.
- Arolytics describes industrial telemetry as high-volume, gapped and noisy.
- Their careers material describes roughly 500 sensor readings per minute per facility.
- Detection, causation and quantification are distinct model/product concerns.
- A near-horizon product problem is keeping confidence/uncertainty separate for detection, causation and quantification.
- Trials use historical customer SCADA before broader production use.
- Customer data can move via exports, SFTP or historian connector.
- Customer-facing users include operations, reliability/maintenance, environment/compliance and leadership.
- Arolytics states that calculations must be explainable, reproducible and defensible.

## Synthetic assumptions used only for this demo

The following are **not claims about AroIQ**:

- customer `northstar`;
- facilities `NS-01`, `NS-02`, `NS-03`;
- tag `PILOT_A`;
- event IDs and volumes;
- demo tolerance thresholds;
- field names in the example JSON contract;
- exact acceptance status rules;
- exact semantics of a flare pilot tag;
- any calculation or quantification method.

These exist only to make the product judgement executable and reviewable.

## Public sources used in constructing the case

1. Arolytics — Product Manager, AroIQ role  
   https://www.arolytics.com/careers/product-manager
2. Arolytics — Careers  
   https://www.arolytics.com/careers
3. Arolytics — Trial / contact flow  
   https://www.arolytics.com/contact
4. Arolytics — AroIQ launch description  
   https://arolytics.com/post/Arolytics-Launches-AroIQ-SCADA-Based-Emissions-Management-Platform
5. Arolytics — Data Scientist role  
   https://arolytics.com/post/Data-Scientist-Full-Time-Calgary-Based-hybrid-remote
