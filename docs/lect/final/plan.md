# Who Decides What's Drastic? Stakeholder Personas for Value-Based Software Process Optimization

> Target: ICSE 2027 · Timeline: 8 weeks · Draft: April 2026

---

## 1. Motivation

### 1.1 The problem: optimization outputs are not self-interpreting

Software process models like COCOMO and COQUALMO can predict effort, schedule, and defect counts for hundreds of project configurations. Tools like SEESAW search these models stochastically and return recommendations -- sets of driver settings (e.g., `acap=5, tool=5, sced=3`) that minimize a composite objective. In four NASA case studies, SEESAW reduced predicted defects by 73%, time by 30%, and effort by 57% compared to the status quo, often matching or beating Boehm's nine "drastic changes" without requiring disruptive organizational moves.

But a recommendation is not a decision. Three gaps remain between what SEESAW produces and what organizations can act on:

1. **The value gap.** SEESAW's recommendations change dramatically depending on the value function. Green et al. showed that BFC ("better, faster, cheaper" -- minimize defects+effort+time) and XPOS ("risk exposure" -- balance quality risk against market erosion) select near-opposite driver settings for the same project. For OSP2, BFC always selects `sced=2` (compressed schedule); XPOS always selects `sced=4` (relaxed). *Which value function is "right" depends on who you ask.*

2. **The interpretation gap.** SEESAW outputs raw COCOMO driver names and numeric ranges. A Project Manager sees `pcap=5, plex=4, ltex=5` and cannot connect these to staffing decisions, budget implications, or stakeholder concerns. Estes et al. demonstrated this gap concretely: when MOOT optimization outputs were presented as raw decision-tree logic, stakeholder acceptance was 16%; with requirement-level explanations tailored by role, acceptance rose to 51%.

3. **The negotiation gap.** Even after optimization and explanation, stakeholders modify recommendations through debate. Carvalho et al. documented this in an industrial microservice migration: automated architecture candidates were substantially restructured during focus-group sessions, with fine-grained and coarse-grained groups reaching different conclusions using different criteria weighted by role and experience. The post-optimization debate is not noise -- it is where organizational values get expressed.

### 1.2 What exists and what's missing

> **The intersection is empty.** SEESAW papers (Menzies et al. 2009, Green et al. 2009) established stochastic stability and value-dependent recommendations but never modeled *who* chooses the value function. Estes et al. (2026) established LLM-simulated multi-stakeholder evaluation with cognitive-style variation but applied it to MOOT tree outputs, not process models. The stakeholder playbook (Menzies 2026) formalized a 4D space (Now/Build/Change/Control) for modeling stakeholder positions but never validated it empirically. No prior work combines all three.

### 1.3 The thesis

> Different stakeholders occupy different positions in a preference space. These positions predict which value function they endorse, which SEESAW recommendations they accept, and how much explanation they need. **An action is not "best" in isolation -- it is best for a particular stakeholder mix, and the best explanation of that action depends on who is listening.**

---

## 2. Research Questions

> **RQ1: Value function alignment.** Does a stakeholder's position in the 4D space (Now/Build/Change/Control) predict whether they prefer BFC or XPOS recommendations?

> **RQ2: Explanation effect.** Do requirement-level explanations of SEESAW's internal changes improve stakeholder acceptance, clarity, and sufficiency compared to raw COCOMO driver output? (Replication of Estes et al. RQ1, applied to process models.)

> **RQ3: Persona differentiation.** Do stakeholder personas (role x cognitive style) systematically prefer different SEESAW recommendations, and does role or cognitive style dominate the effect?

> **RQ4: Post-optimization consensus.** When personas with different value-function preferences are asked to propose a compromise action set, do they converge? If so, on what -- the mathematically optimal point, or a socially negotiated alternative? (Extends Estes et al. H6 and Carvalho et al.'s negotiation finding.)

---

## 3. Conceptual Framework

```
Executive Actions          COCOMO Drivers           Objectives              Stakeholder Space
+---------------------+    +------------------+    +------------------+    +---------------------+
| 1 Improve personnel  | -> | acap, pcap, pcon | -> | min effort       | -> | 4D: Now/Build/      |
| 2 Improve tools      |    | aexp, plex, ltex |    | min time         |    |     Change/Control   |
| 3 Improve flexibility|    | prec, flex, resl |    | min defects      |    |                     |
| 4 Increase risk anal.|    | pmat, sced, tool |    | min risk exposure |    | x 3 GenderMag:      |
| 5 Relax schedule     |    | data, cplx, rely |    +------------------+    |   Abi / Pat / Tim   |
| 6 Improve process mat|    | pvol, site, docu |                           |                     |
| 7 Reduce functionality    | ruse, stor, time |    Explanation Layer      | Measures:           |
| 8 Improve the team   |    +------------------+    +------------------+    |  acceptance (binary) |
| 9 Reduce quality     |                            | Raw: driver names| -> |  clarity (1-5)      |
|                      |    Value Functions          | Explained: role- |    |  sufficiency (1-5)  |
| + SEESAW internal    |    +------------------+    |   tailored req-  |    |  value fn pref      |
|   change combos      |    | BFC: min(D+E+T)  |    |   level framing  |    |  compromise choice  |
+---------------------+    | XPOS: min(risk)  |    +------------------+    +---------------------+
                            +------------------+
```

*Actions -> Driver changes -> Objective scores + Explanations -> Stakeholder evaluation*

---

## 4. Literature Gap

| Paper | 1. Stochastic stability | 2. Value-dependent recs | 3. Multi-stakeholder eval | 4. Cognitive style | 5. Req-level explanation | 6. Process models |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Menzies et al. 2009 (How to Avoid) | ✓ | -- | -- | -- | -- | ✓ |
| Green et al. 2009 (Understanding Value) | ✓ | ✓ | -- | -- | -- | ✓ |
| Estes et al. 2026 (Bridging the Gap) | -- | -- | ✓ | ✓ | ✓ | -- |
| Carvalho et al. 2024 (Microservices) | -- | -- | ✓ | -- | -- | -- |
| Stakeholder Playbook 2026 | -- | ✓ | ✓ | -- | -- | ✓ |
| **This paper** | **✓** | **✓** | **✓** | **✓** | **✓** | **✓** |

*No prior work fills all six columns.*

---

## 5. Method

### 5.1 Optimization data (reuse, no new runs needed)

4 NASA case studies (OSP, OSP2, flight software, ground software) from the original SEESAW papers. Each has known project option ranges (Figure 4 in "How to Avoid"), fixed settings, and SEESAW recommendation sets under both BFC and XPOS value functions. 9 drastic changes + SEESAW internal combinations = ~10 candidate action sets per case study per value function.

### 5.2 Personas: 12 = 4 roles x 3 GenderMag

| Role | Tech level | 4D position (N,B,C,Ctrl) | Likely value fn |
|---|---|---|---|
| Project Manager | 1/5 | (3, 2, 2, 4) | BFC (min effort+time) |
| Developer | 5/5 | (1, 4, 3, 0) | BFC (min defects) |
| QA Lead | 3/5 | (2, 2, 1, 3) | BFC (min defects) |
| VP/Executive | 2/5 | (4, 3, 4, 4) | XPOS (min risk exposure) |

Each role x Abi (risk-averse, process-oriented) / Pat (medium, reflective) / Tim (risk-tolerant, tinkerer) = 12 personas. Generated via Gemini 2.5 Flash following Estes et al.'s validated prompt structure.

### 5.3 Protocol (replication of Estes et al.)

| Phase | What the persona sees | What we measure |
|---|---|---|
| **Round A: raw** | SEESAW recommendation as COCOMO driver settings: `acap=5, pcap=5, pcon=5, tool=5, sced=3`. Median scores for effort, time, defects. No framing. | Acceptance (binary), clarity (1-5), sufficiency (1-5), reasoning (free text), follow-up questions |
| **Round B: explained** | Same recommendation with requirement-level explanation: "This means hiring senior analysts (acap=5) and investing in better tooling (tool=5). For a Project Manager, this translates to: higher upfront staffing cost but 73% fewer defects downstream, reducing rework cycles that disrupt your schedule." | Same measures. Within-persona comparison = explanation effect. |
| **Value function choice** | Both BFC and XPOS recommendation sets for the same project, side by side. "Which set would you adopt?" | BFC vs XPOS preference (forced choice), reasoning. Tests RQ1. |
| **Compromise** | "If your team included a PM, developer, QA lead, and VP, which single recommendation set would you propose?" | Convergence analysis. Tests RQ4. |

**Counterbalancing:** Group 1 (PM-Abi, PM-Pat, PM-Tim, Dev-Abi, Dev-Pat, Dev-Tim) sees Raw->Explained. Group 2 (QA-Abi, QA-Pat, QA-Tim, VP-Abi, VP-Pat, VP-Tim) sees Explained->Raw.

**Scale:** 4 case studies x 2 value functions x ~10 recommendations x 12 personas x 2 rounds = ~1,920 per-recommendation evaluations + 96 summaries + 48 value-function choices + 48 compromise proposals.

### 5.4 Validation: LLM-as-Judge

Two independent judges (Claude Sonnet 4.5 + Llama 3.1 70B) perform blind classification. Chance baselines: full persona = 8.3% (1/12), role = 25% (1/4), GenderMag profile = 33% (1/3). Inter-judge reliability: Krippendorff alpha for ordinal scores, Cohen kappa for classification agreement. Thresholds: alpha >= 0.80, kappa >= 0.61.

### 5.5 Analysis

| RQ | Test | Expected signal |
|---|---|---|
| RQ1 | Logistic regression: 4D position -> BFC/XPOS preference. Euclidean distance to Executives centroid as predictor. | Executives + Abi (risk-averse) prefer XPOS. Developers + Tim (risk-tolerant) prefer BFC. |
| RQ2 | Paired within-persona comparison: acceptance, clarity, sufficiency in Round A vs Round B. Effect size via Cliff's delta. | Explanation helps most for PM (tech=1/5), least for Developer-Tim (tech=5/5). Replicates Estes finding. |
| RQ3 | Chi-square: persona x preferred recommendation set. Decompose into role effect vs cognitive-style effect. | Role dominates *what* is chosen. GenderMag dominates *how* the choice is justified (hedging, engagement depth). |
| RQ4 | Convergence analysis: do compromise choices cluster? Compare to mathematical Pareto knee of the BFC-XPOS trade-off. | Compromise != mathematical optimum (replicates Estes H6). Compromise shifts toward the highest-Control group's preference. |

---

## 6. Hypotheses

| # | Hypothesis | Grounded in |
|---|---|---|
| H1 | Stakeholders with Control >= 3 (Executives, Managers, QA) prefer XPOS over BFC. | Playbook: high-Control groups prioritize risk management over speed. |
| H2 | Stakeholders with Build >= 3 (Developers, Ops) prefer BFC over XPOS. | Playbook: high-Build groups optimize for technical quality. |
| H3 | Explanation gain (Round B - Round A) is inversely proportional to tech level. | Estes: PM-Abi gained +3.00 clarity; SWE-Tim gained +0.80. |
| H4 | Abi-profile personas (risk-averse) prefer SEESAW's internal changes over drastic changes. | Internal changes = lower organizational disruption = lower risk. |
| H5 | Tim-profile personas (risk-tolerant) are more willing to accept drastic changes when they score better. | GenderMag: Tim = technology-motivated, high self-efficacy. |
| H6 | Compromise converges on internal changes (SEESAW) rather than drastic ones, even when drastic changes score better on objectives. | Carvalho: post-optimization debate favors less disruptive options. SEESAW: internal changes have smaller IQR = more stable. |

---

## 7. Eight-Week Timeline

| Week | Deliverable | Risk |
|---|---|---|
| 1 | Reimplement SEESAW core (28-line pseudocode, Fig 6 of "How to Avoid"). Verify on 4 NASA case studies. Collect recommendation sets under BFC and XPOS. Write raw + explained stimulus templates. | Original code from 2009 may not run. Pseudocode is complete; COCOMO/COQUALMO equations in appendix. Reimplement in Python, ~200 LOC. |
| 2 | Build 12 persona system prompts. Pilot: 1 case study x 1 value function x 4 personas (one per role, Tim only). Debug JSON parsing, prompt stability, response completeness. | Persona prompts may produce flat responses. Fix: increase GenderMag facet specificity following Estes's validated template. |
| 3 | Full data collection: all 4 case studies x 2 value functions x 12 personas x 2 rounds. ~1,920 API calls via Gemini 2.5 Flash. Parallelize across case studies. | API cost ~$50-100 (Flash is cheap). Fallback: reduce to 2 case studies (OSP + ground) if budget constrained. |
| 4 | LLM-as-Judge validation. Blind classification + rubric scoring. Compute inter-judge reliability. If alpha < threshold on any facet, revise persona prompts and rerun worst performers. | Estes found alpha=0.22 on learning_style. Expected here too. Document as known limitation, not blocker. |
| 5 | Analysis: RQ1 (logistic regression), RQ2 (paired comparison + Cliff's delta), RQ3 (chi-square decomposition), RQ4 (convergence). Generate all tables and figures. | If role and cognitive style are confounded in counterbalancing, report as threat. Estes had same issue (G1=all PjM). |
| 6 | Write Results + Discussion. Key figures: (a) acceptance heatmap (12 personas x ~10 recs), (b) BFC-vs-XPOS preference by 4D position, (c) explanation gain by role, (d) compromise convergence vs Pareto knee. | None. |
| 7 | Write Introduction, Background, Related Work (with gap table), Method. Position against SEESAW papers + Estes + Carvalho + Playbook. | None. |
| 8 | Internal review, revise, format for ICSE, submit. | None. |

---

## 8. Contributions

1. **First empirical test of stakeholder position predicting value-function preference** in software process optimization. The 4D space (Now/Build/Change/Control) is validated as a predictor, not just a conceptual model.
2. **First application of LLM-simulated multi-stakeholder evaluation to COCOMO/COQUALMO process models.** Extends Estes et al.'s methodology from MOOT optimization trees to parametric cost/defect models.
3. **Requirement-level explanations for process model recommendations.** Translates COCOMO driver settings into role-specific staffing, tooling, and organizational decisions.
4. **Empirical evidence that internal changes are preferred over drastic changes in multi-stakeholder negotiation**, even when drastic changes score better on single-value-function objectives. Extends "How to Avoid" from a purely technical result to a sociotechnical one.
5. **Replication and extension of the Estes et al. evaluation protocol** in a new domain, testing generalizability of the 16%->51% explanation effect.

---

## 9. Key References

| Ref | What it provides |
|---|---|
| Menzies, Williams, Boehm, El-Rawas, Hihn. "How to Avoid Drastic Software Process Change." ICSE 2009. | SEESAW algorithm, 4 NASA case studies, stochastic stability, 9 drastic changes. |
| Green, Menzies, Williams, El-Rawas. "Understanding the Value of SE Technologies." ASE 2009. | BFC vs XPOS value functions, value changes everything, SEESAW vs SA/MaxWalkSat/BEAM/A-STAR. |
| Estes, EsfandyariDoulabi, Khanmohammadi. "Bridging the Interpretation Gap." 2026. | LLM-simulated personas, GenderMag x role, 2-round counterbalanced protocol, LLM-as-Judge, 16%->51% acceptance. |
| Carvalho et al. "On the Usefulness of Automatically Generated Microservice Architectures." 2024. | Post-optimization human debate, focus groups modifying automated recommendations, role-dependent criteria weighting. |
| Menzies. "A Stakeholder-Aware CEO Playbook." 2026. | 4D stakeholder space (Now/Build/Change/Control), 8 canonical groups, action->tension mapping. |
| Burnett et al. "GenderMag." CHI 2016. | 5 cognitive facets, Abi/Pat/Tim personas, 200+ usability studies. |
| Schuller et al. "LLM-generated personas." CHI 2024. | LLM personas indistinguishable from human-written in quality/acceptance. |
| Boehm. "Software Cost Estimation with COCOMO II." 2000. | COCOMO/COQUALMO model definitions, driver ranges, scale factors. |
