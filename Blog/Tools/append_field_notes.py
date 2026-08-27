#!/usr/bin/env python3
"""
ShipPaulJobs — Append Field Notes to Blog Posts
-------------------------------------------------
Appends an English FIELD NOTE section to the bottom of each target post.
The author name in the header is pulled live from the post's author.displayName.
"""

import os
import re

BLOG_URL         = "https://www.shippauljobs.com"
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE       = "token.json"
DRY_RUN          = False

# ── Duplicate guard ──────────────────────────────────────────────────────────
FIELD_NOTE_MARKER = "field-note-section"

# ── Field note content per post URL ─────────────────────────────────────────
# Key   : post path (everything after BLOG_URL)
# Value : (intro_paragraphs, misconception, bullet_points)

FIELD_NOTES = {
    "/2026/08/ur-e27-response-strategies-for-marine.html": {
        "body": """<p>The article's diagnosis is accurate. The reason equipment manufacturers haven't moved despite time passing since UR E27 came into effect isn't laziness — it's the significant time lag between when requirements are written into shipbuilding contracts and when they actually reach manufacturers down the supply chain. The further down the chain, the stronger the illusion that "it's not our turn yet." The danger is treating this quiet period as a grace period rather than a preparation window.</p>

<p>The most dangerous assumption in practice is "we've had no problems so far." If you sailed through earlier E27 projects where requirements weren't clearly passed down, that likely means project-by-project workarounds — not systematic compliance. When formal requirements arrive, there's no documentation ready, you start by excavating past records, and by that point your options are already constrained by a locked schedule and budget.</p>

<p>The essence of the preparation framework is: <strong>move before you're asked.</strong></p>""",
        "misconception": '"We haven\'t received a formal request yet, so there\'s no need to prepare." A late-arriving requirement isn\'t an exemption — it\'s a time lag. Failing to use that lag for preparation means you\'ll have no flexibility when the request finally arrives.',
        "bullets": [
            "Document your current product's scope, configuration, network connections, interfaces, and software versions based on actual hardware first.",
            "Prioritize recurring delivery items, network-connected systems, and products tied to essential vessel functions.",
            "Before any formal request arrives, confirm with stakeholders: applicable vessels, integration scope, approval format, documentation requirements, versions, and schedule.",
        ],
    },
    "/2026/08/if-csdd-is-rushed-during-construction.html": {
        "body": """<p>The observation that a rushed CSDD during construction undermines SCARP after delivery is a structural failure pattern that keeps repeating in the field. The core is simple: CSDD and SCARP are not two separate documents — they are one document split into the design phase (<em>what</em>) and the operational phase (<em>how</em>). When the system integrator produces a weak CSDD during construction, that weakness is directly inherited by the owner's SCARP at the first annual survey.</p>

<p>When equipment suppliers fill in E27 documentation as a formality, those gaps flow directly into the CSDD. Frequent late-stage design changes mean the ZCD and CSDD remain frozen at an early design snapshot, diverging from the actual as-built state. Most commonly missing: termination, reset, and rollback procedures plus RTO/RPO data from suppliers. If these aren't referenced in the CSDD, the owner will need to comb through every equipment manual from scratch to write the incident response and recovery sections of SCARP.</p>""",
        "misconception": '"Once delivery is done, cyber obligations are wrapped up too." In reality, the obligation to prepare SCARP continues until the first annual survey, and the quality of CSDD during construction sets the ceiling for SCARP quality.',
        "bullets": [
            "Verify that E27 documentation submission from key OT equipment suppliers (propulsion, steering, power, firefighting, cargo safety) is explicitly specified in the contract.",
            "Confirm that the construction contract includes a procedure for verifying CSDD-to-as-built alignment at commissioning completion.",
            "Request a SCARP draft (or at minimum a table of contents) based on the CSDD at the time of delivery.",
        ],
    },
    "/2026/07/iacs-ur-e27-asks-you-to-prove-up-to-41.html": {
        "body": """<p>The problem this article identifies isn't a flaw in the regulation — it's a limitation in the worldview the regulation assumes. UR E27 is designed to verify 41 security capabilities on the premise of deterministic software behavior. But a trained AI model can produce probabilistically different outputs from identical inputs.</p>

<p>Deterministic output (item #20) is required, yet a poisoned model may reclassify an abnormal state as normal, causing the fallback itself to fail. Input validation (item #39) checks syntax, length, and content — but adversarial examples can satisfy every formal criterion while carrying malice only at the semantic layer. Onboard systems already use learning-based anomaly detection for propulsion, power, steering, and ballast monitoring — and these pass certification simply by listing "manufacturer/model/version," with the fact that they're learning-based often never surfacing in any document.</p>

<p>Rather than waiting for the regulation to be revised, the practical path is to bring ISO/IEC 42001, ISO/IEC 23894, and ISO/IEC 27090 into the compensatory measures provision under UR E27 clause 3.1.3.</p>""",
        "misconception": '"This equipment has E27 type approval, so AI-related risks are already covered." Learning-based components clear the approval process with nothing more than a formal "manufacturer/model/version" entry, and the fact that they are learning-based often goes undocumented entirely.',
        "bullets": [
            "Require suppliers to confirm whether the product contains learning-based components — for condition monitoring, anomaly detection, optimization, or similar functions.",
            "Prepare compensatory measures under clause 3.1.3 for items #39 (input validation) and #20 (deterministic output).",
            "Decide at the contract stage whether to require ISO/IEC 42001 or equivalent AI governance evidence in newbuild specifications.",
        ],
    },
    "/2026/07/if-it-is-out-of-scope-your-e26.html": {
        "body": """<p>Some system integrators advise that IT systems are outside the scope of UR E26. This directly conflicts with the regulation's own text. Section 2 of E26 defines CBS as "IT and OT systems," and Section 1.3.2(b) explicitly includes IP-based communication interfaces that connect to passenger, administrative, and crew networks.</p>

<p>Why this narrow interpretation is dangerous comes down to actual attack paths. Phishing targets crew IT terminals. VSAT terminals — IT infrastructure — serve as initial entry points. Ransomware enters through administrative networks and moves laterally into OT. A compliance scope that excludes IT removes this entire attack path from the control perimeter.</p>

<p>Narrowing the scope lowers the system integrator's compliance cost in competitive bidding — but the owner pays the price.</p>""",
        "misconception": '"E26 is about OT systems — propulsion, steering, navigation equipment." This directly contradicts the regulation\'s own definition (CBS = IT and OT systems). Building a compliance framework on this assumption means gaps will emerge at the annual survey.',
        "bullets": [
            "Inventory all CBS on board — navigation, power, servers, crew networks, VSAT, and all interfaces — without exception.",
            "Define and implement clear boundary controls and segmentation between IT and OT networks.",
            'Ask your SI directly: "Does your E26 compliance scope include all CBS as defined in E26 Section 2 — both IT and OT?"',
        ],
    },
    "/2026/07/if-we-already-have-e27-certificate-why.html": {
        "body": """<p>"We have E27 type approval — why do we need cybersecurity verification at FAT again?" is a question that genuinely comes up in the field. The answer is clear. E27 evaluates whether an equipment item has the required security capabilities at the design and development stage. E26 verifies whether the <em>integrated system</em> can actually demonstrate cyber resilience in practice.</p>

<p>Whether the software version matches the certified scope versus what was actually delivered, whether account management and privilege levels are configured per specification, whether remote access is tightly configured with no backdoors, and whether backup and recovery procedures actually work on real hardware — all of these must be verified project by project.</p>

<p>Deferring this verification to commissioning or sea trials means that if a security deficiency is found onboard, it can trigger cascading re-verification of adjacent systems. Found at FAT, it's an opportunity. Found onboard, it's a cost.</p>""",
        "misconception": '"E27 type approval means cybersecurity verification at FAT can be skipped." E27 reduces the scope of verification items — it does not eliminate verification itself.',
        "bullets": [
            "At FAT, verify that the software version matches the certified scope and the actual delivered build.",
            "Confirm that account management and privilege levels are configured per project specifications.",
            "Demonstrate and verify that backup and recovery procedures work in the actual hardware environment.",
        ],
    },
    "/2026/07/iacs-ur-e26-compliance-series-17-cyber.html": {
        "body": """<p>"Collecting individual equipment certificates is not compliance" — that is the core message. Confirming that individual pieces of equipment have adequate security capabilities does not prove ship-level compliance. What's required is a coherent ship-level architecture spanning integrated systems, network design, security zones, exclusions, and compensatory measures.</p>

<p>The six ship-level deliverables — ZCD, CSDD, VAI, risk assessment for exclusions, description of compensatory measures, and Ship Cyber Resilience Test Procedure — are not separate standalone documents. They must function as a unified evidence system. CBS present in the inventory but missing from the diagram. Conduits shown but not described. Test results referencing a different software version than was approved. These mismatches repeat in real projects.</p>

<p>Survey-cycle readiness isn't something you can reconstruct after delivery. It must be designed in before delivery.</p>""",
        "misconception": '"If I collect type approval certificates from all suppliers, ship-level E26 compliance is complete." Confirming individual equipment capabilities and proving integrated system cyber resilience are separate things. All six deliverables must form a coherent, mutually consistent evidence system for actual compliance to hold.',
        "bullets": [
            "Verify that the six ship-level deliverables are written as a single, mutually consistent evidence system — not as standalone documents.",
            "Cross-check that CBS lists, conduits, protocols, and software versions are consistent across inventory, diagrams, baseline, and test results.",
            "At delivery, prepare a handover document covering approved, installed, tested, accepted limitations, maintenance items, change triggers, evidence retention, and supplier contact details.",
        ],
    },
    "/2026/07/ur-e26-after-mandate-consultants-view.html": {
        "body": """<p>"The clearer the boundary, the better for everyone." A consultant isn't a fifth stakeholder — they are a function for reading boundaries that are structurally bound to blur. Owners, class societies, shipyards, and vendors each experience the same boundary differently from their own position.</p>

<p>The method most commonly used in practice is not accepting class society guidelines directly as compliance standards, but placing the UR text as the reference point and treating class interpretations as "one claim" to be validated. It's about acknowledging that binding final interpretation belongs to the class and flag state — while ensuring the pen stays on the UR text.</p>

<p>Add scope stratification and the owner's commercial position (charterer, vetting, trade), and the right answer changes by owner even under the same UR and same market.</p>""",
        "misconception": "Treating class society guidelines or voluntary notations as the mandatory requirements of the UR itself — conflating scope under the banner of \"the class requires it, so it's mandatory.\"",
        "bullets": [
            "Use the UR text as the reference point; treat class guidelines and interpretations as claims requiring independent validation.",
            "Distinguish between baseline-equivalent tier (means of fulfilling obligations) and beyond-baseline tier (separate scope choices).",
            "Determine case by case which items are 'regulatory optional but commercially near-mandatory' based on the owner's trade exposure, vetting obligations, and flag state.",
        ],
    },
    "/2026/07/ur-e26-after-mandate-vendors-view.html": {
        "body": """<p>E27 is actually aimed at vendors. Requiring 30 core security capabilities per individual CBS — plus 11 additional capabilities if connected to an untrusted network — is not just adding a few line items to a spec sheet. Requiring vulnerability disclosure, security updates, and end-of-life timelines means the operational culture itself must change.</p>

<p>With type approval, each individual ship requires only a small incremental review. Without it, you must generate type-approval-grade documentation from scratch for every vessel. However, profile and procedure differences across class societies mean global vendors face the burden of certifying the same product multiple times against different standards.</p>

<p>The most interesting and troubling point is the paradox: <strong>the more secure you make it, the harder it becomes to integrate.</strong> The stricter the certification conditions for an individual box, the higher the assurance level — but the harder it becomes to connect it to other systems.</p>""",
        "misconception": 'Assuming that a system with E27 certification — or certification under stricter conditions ("cannot connect to untrusted network") — is therefore safer and problem-free. What\'s missed: those certification conditions may actually make system integration more difficult.',
        "bullets": [
            "Calculate the economics of type approval as a one-time fixed cost versus the per-vessel documentation cost of not having it.",
            "Identify in advance how certification procedure requirements differ by class society for the vessels in your target market.",
            'Design for both security and interoperability from the start, with "certified but easy to integrate" as the target.',
        ],
    },
    "/2026/07/e26-zone-defense-learn-iacs-ur-e26-as.html": {
        "body": """<p>The game's value as a practical training tool is that it lets players — even those unfamiliar with the regulation — internalize the sense of "defending zones and conduits in layers" within five minutes. The reality the game mirrors directly: poor zone boundaries or misplaced control points in an actual ZCD design let threats through to critical systems.</p>

<p>Categorizing systems by Cat I/II/III, treating the DMZ as a distinct defensive layer at the IT-OT boundary, and making the Essential Services Core (propulsion, steering) the primary defense priority — this structure conveys defense-in-depth far faster than any abstract explanation. Getting owners, shipyards, class societies, and vendors to draw the same picture in the same room is, in practice, one of the hardest things to achieve.</p>

<p>What the game provides is <strong>intuition</strong>, not a design blueprint. Actual zone/conduit design requires fresh judgment for each vessel, based on its unique asset inventory and trust boundaries.</p>""",
        "misconception": "Mistaking a successful game playthrough for actual understanding of ZCD design or E26 requirements. The game is an icebreaker that conveys intuition — it doesn't substitute for the asset and trust-boundary judgment that differs vessel by vessel.",
        "bullets": [
            "Define in advance what controls (firewall/IDS-IPS/segmentation) go at each zone and conduit boundary, based on system criticality (Cat I/II/III).",
            "Treat the DMZ at the IT-OT boundary as an explicit and distinct defensive layer.",
            "Use visualization tools like this during onboarding and kickoff to align stakeholder intuition — then conduct actual design validation separately.",
        ],
    },
    "/2026/07/ur-e26-after-mandate-shipyards-view.html": {
        "body": """<p>For a shipyard, E26 is the work of translating the abstract goal — "manage cyber risk across the entire vessel" — into tangible documents: ZCD, asset inventory, security design description, and commissioning test procedures. And it must be done within a fixed-price, fixed-schedule contract.</p>

<p>The hardest part isn't writing individual documents — it's integration. "E27 type approval does not automatically constitute E26 compliance" cannot be emphasized enough. Cryptographic handshake failures between certified systems from different suppliers. Systems certified under conditions that restrict untrusted network connections requiring separate gateway design. These surface differently on every vessel.</p>

<p>As more type-approved systems appear, per-system documentation burden decreases — but integration burden grows. The burden doesn't disappear. It changes form.</p>""",
        "misconception": "Assuming that installing a collection of E27 type-approved systems into a vessel automatically satisfies E26. In reality, integrating into the vessel's specific network architecture requires separate validation.",
        "bullets": [
            "State from the outset of the project that even E27-certified systems require separate ZCD and integration validation when integrated into the vessel's unique network architecture.",
            "Factor additional design elements such as gateways into estimates and schedules where systems certified with restricted trust boundaries will be used.",
            "Request or encourage owners to provide detailed specifications at the design stage to pre-empt scope ambiguity risk.",
        ],
    },
    "/2026/07/ur-e26-after-mandate-through-eyes-of.html": {
        "body": """<p>Classification societies wear two hats simultaneously on any single matter. The obligation to uniformly guarantee the mandatory floor as an IACS member, and the competitive necessity to differentiate above that floor — these two forces collide within the same organization. What a class society actually sells is not "safety assurance" but "certification of conformance with that society's rules," and the non-delegable obligation to ensure seaworthiness remains with the owner.</p>

<p>When you consider the asymmetry between the fees a class society receives and the scale of potential liability, the tendency toward conservatism in new and uncertain areas makes sense. Cybersecurity fits this profile precisely: threats evolve rapidly, causation is complex to prove, and case law is still thin.</p>

<p>Differentiation above the floor (voluntary notations) holds legitimacy only when backed by real capabilities developed long before the UR was mandated.</p>""",
        "misconception": 'Treating a class certificate as a "safety assurance" for the vessel. In reality, it\'s certification that the vessel conforms to that society\'s rules. Final responsibility for seaworthiness remains with the owner.',
        "bullets": [
            "Understand class certificates as 'evidence of conformance with a specific society's rules,' and maintain the premise that seaworthiness responsibility ultimately rests with the owner.",
            "When evaluating voluntary notations, verify that they are backed by the class society's actual accumulated expertise.",
            "When the mandatory vs. differentiation status of a document requirement is unclear, verify against the UR source text to prevent confusion.",
        ],
    },
    "/2026/07/ur-e26-after-mandate-owners-view-where.html": {
        "body": """<p>For an owner, the most uncomfortable structural fact about E26 is that the party paying and the party actually producing the deliverables (ZCD, design description, commissioning procedures) are different. The owner operates the vessel for 20–30 years and bears the consequences of design decisions — but those decisions are made by the shipyard and vendors.</p>

<p>The most common point of confusion in practice is treating "mandatory vs. optional" as a binary. In reality, it's a spectrum. There are explicit mandatory requirements. Below those sit areas that are not regulatory obligations but have become practically unavoidable through vetting frameworks like SIRE 2.0, RightShip, and CDI, and expanding PSC inspection coverage. Below those is the genuinely optional zone. The asymmetry is notable: E26 has no retroactive application to existing fleets, yet SIRE 2.0 cyber inspection criteria apply regardless of newbuild status.</p>""",
        "misconception": "Assuming that because E26 doesn't retroactively apply to your existing fleet, your vessels are entirely free from cyber requirements. In reality, vetting frameworks like SIRE 2.0 apply cyber inspection criteria to existing vessels regardless of newbuild status, making them de facto obligations.",
        "bullets": [
            "Categorize requirements across three tiers: mandatory (floor), commercially near-mandatory (vetting/charterer requirements), and genuinely optional.",
            "At the design stage, specify requirements in detail directly to counter shipyard and vendor incentives toward minimum-spec outcomes, reducing operational burden downstream.",
            "For fleets with multiple class societies and a mix of newbuilds and existing vessels, apply a consistent fleet-level policy covering standardized specifications, vendor management, and documentation systems.",
        ],
    },
    "/2026/06/ur-e26-after-mandate-one-mandatory-rule.html": {
        "body": """<p>"Why do different class societies require different things?" is a common complaint — but it usually comes from conflating two distinct layers: the mandatory UR E26/E27 text itself, and the voluntary notations class societies layer on top. Fail to separate these two layers and owners start wondering "are they trying to sell us something extra?" while practitioners lose track of what's a pass/fail requirement and what's a choice.</p>

<p>Three structural reasons explain the friction that keeps surfacing in practice: E26 is goal-based regulation with significant interpretive latitude; the industry is still in transition since enforcement began in July 2024; and the system explicitly allows class societies to impose stricter requirements above the minimum floor. For owners operating multi-class fleets, the asymmetry of facing different costs and deliverable requirements across class societies for the same E26 compliance is a material risk.</p>""",
        "misconception": "Treating class society notation guidelines as mandatory E26 requirements themselves. Whether a notation is a 'means of fulfilling the obligation' or 'addresses additional scope' depends entirely on what scope it covers — failing to distinguish this can lead to buying things that were never actually mandatory.",
        "bullets": [
            "Use the UR E26/E27 source text as the primary reference; treat class guidelines as interpretive documents requiring separate validation.",
            "Determine first whether a proposed notation is a 'means of fulfilling the mandatory obligation' or 'addresses additional scope.'",
            "For multi-class fleet operators, track inter-class requirement variance as a separate governance item.",
        ],
    },
    "/2026/03/automating-iacs-e26e27-annual-survey.html": {
        "body": """<p>"60% yes, 40% no" is the baseline to internalize first when evaluating OT monitoring adoption. Asset inventory, network topology, patch and vulnerability status, access control logs, security event history, and remote access session records — these six areas can be substantially automated through continuous technical monitoring, transforming survey preparation into an always-on evidence package generation process.</p>

<p>The remaining 40% is structurally resistant to automation. Physical cabling and wireless access points with no associated clients are invisible without manual inspection. The existence of documentation and the usefulness of that documentation are entirely different things. Whether crew actually understand the systems and can execute isolation responses is a separate validation item.</p>

<p>The real value of the continuous survey model is not "eliminating surveys" — it's <strong>shifting the focus of survey day from confirming evidence exists to evaluating whether the management system actually works.</strong></p>""",
        "misconception": "Expecting that deploying an OT monitoring solution will eliminate annual survey burden entirely, or that surveys will pass automatically. The tools reduce preparation burden — results depend on how they are used.",
        "bullets": [
            "Clearly distinguish the six automatable areas from the three non-automatable areas (physical inspection, document quality, crew competency and response demonstration) when building your preparation plan.",
            "Redefine survey preparation as 'evidence package generation' and secure a six-month phased build-out timeline.",
            "Prepare response scenarios and walkthroughs separately, under the premise that survey-day focus shifts from 'does the documentation exist' to 'does the management system actually work.'",
        ],
    },
    "/2026/03/ship-ot-monitoring-for-iacs-e26e27.html": {
        "body": """<p>Approaching ship OT monitoring as an extension of IT security will inevitably create problems. OT systems operate with deterministic timing, so active network scanning can crash PLCs or trigger false alarms. Legacy protocols like Modbus and NMEA 0183 were designed with no authentication concept whatsoever. Ship control systems have a 15–25 year lifecycle that makes standard patch cycles impossible to follow. <strong>Passive traffic capture via SPAN port or network TAP is therefore the foundational principle.</strong></p>

<p>Using three monitoring zones and eight required functions as a solution selection checklist is the most efficient approach in practice. Architectural differences based on satellite connectivity are also frequently overlooked — regardless of which architecture applies, the principle is the same: onboard detection capability must not be dependent on shore-side connectivity.</p>""",
        "misconception": "Applying active scanning from IT security practice directly to OT networks, causing unexpected load or malfunction in field-layer devices — or assuming that if broadband connectivity is always available, an onboard local detection engine isn't necessary.",
        "bullets": [
            "Treat passive methods (SPAN/TAP) as the foundational principle; apply active scanning only in controlled dry-dock environments with explicit authorization, as a narrow exception.",
            "Specify the 8 required functions explicitly as solution selection criteria.",
            "Maintain independent onboard analysis engine detection capability as a mandatory requirement, regardless of satellite connectivity.",
        ],
    },
    "/2026/06/ship-ot-cybersecurity-iacs-e26e27.html": {
        "body": """<p>Treating E26 and E27 as a single combined regulation will inevitably cause confusion in practice. <strong>"E26 governs how a vessel's cybersecurity program is managed; E27 governs what can be purchased and installed."</strong> Getting this distinction clear from the start means every subsequent task can be correctly sorted without confusion about which regulation it belongs to.</p>

<p>The most common friction point in practice: a CBS inventory exists, but SL-T (target security level) assignments are missing, or supplier type approval status (SL-C) hasn't been cross-validated against it. The same applies to SBOM requirements — most manufacturers still don't provide a formal SBOM, but class societies are increasingly requesting software component transparency at annual surveys, making it advantageous to build a tracking system now.</p>""",
        "misconception": "Assuming that completing a CBS inventory constitutes E26/E27 compliance. An inventory without SL-T assignments, or without cross-validation against supplier type approval (SL-C) status, cannot satisfy procurement and installation requirements — and there is no way to comply with only one of E26 or E27 within the vessel scope.",
        "bullets": [
            "Use CBS inventory construction as the starting point for all work, but document to the level of software versions and inter-system connections.",
            "Assign a risk-assessment-based SL-T to each CBS, and always cross-validate against supplier type approval (SL-C) status.",
            "Finalize zone/conduit structure before designing access controls, detection, response, and recovery procedures — and write the cybersecurity management plan from the outset as a document intended for survey submission.",
        ],
    },
    "/2026/06/e26-deliverable-quality-low-medium-and.html": {
        "body": """<p>"The essence of E26 is not security functions but cyber resilience" — that single sentence captures the article's core. Deliverables covering the same topic diverge dramatically in quality because most documents stop at listing "what exists" and never reach the level of answering "what happens when something fails."</p>

<p>The most dangerous pattern is the checkbox problem: asset inventory written, risk assessment completed, network diagram produced — boxes checked. But recovery testing, firewall rule validation, and supplier control audits go unchecked and unexecuted. <em>"The moment the questions stop, resilience stops too."</em></p>

<p>Rather than conflating the minimum information needed for class approval with the information actually needed for operations, consciously separating and filling both within the same document — that is the most realistic way to implement the four quality dimensions (operability, maintainability, recoverability, traceability) in practice.</p>""",
        "misconception": "Equating completion of the deliverable checklist with actually securing resilience. That an Asset Inventory, Risk Assessment, and Network Diagram have all been written is entirely separate from whether recovery testing, firewall rule validation, and supplier control audits have actually taken place.",
        "bullets": [
            "Design all deliverables to answer not just 'what exists' but 'what happens when failure occurs,' using scenario-based framing throughout.",
            "Clearly separate information required for class approval from information required for operations, and secure both independently.",
            "Before submission, self-assess against the four quality dimensions, confirming that actual verification has occurred — not just checkbox completion.",
        ],
    },

    # ── 🟡 Posts (Field Note boosts) ─────────────────────────────────────────

    "/2026/07/ship-zcd-anatomy-building-blocks-iacs-ur-e26.html": {
        "body": """<p>A ZCD is not a drawing — it is the visible expression of trust relationships inside a vessel. That distinction matters most when you look at the three supporting artifacts the article enumerates: the Zone Table, the Conduit Table, and the Data Flow Matrix. Each one answers a different question. The Zone Table defines what assets exist and what security level each zone must reach. The Conduit Table defines the permitted communication paths and their permitted protocols. The Data Flow Matrix maps which data crosses which zone boundaries and by which mechanism. None of the three is useful in isolation; all three must be internally consistent before the ZCD diagram itself carries any evidential weight.</p>

<p>The most commonly overlooked operational obligation is Management of Change (MoC). E26 does not treat ZCD as a one-time design artifact — it must remain accurate across the vessel's operational lifecycle. A software update, a new interface, a change in network topology: any of these can invalidate the ZCD without triggering an automatic review. Projects that treat ZCD as a delivery milestone rather than a living document consistently produce surveys where the as-installed state diverges from the approved documentation.</p>

<p>The 15-component structure in this article is a practical checklist for auditing an existing ZCD — not just a template for creating a new one.</p>""",
        "misconception": '"Once the ZCD is drawn and Class-approved, it\'s finished." E26 treats ZCD as a living document that must reflect the actual as-installed state at every annual survey. A design-stage ZCD that is never updated after delivery will diverge from reality and create survey findings.',
        "bullets": [
            "Verify that all three supporting artifacts — Zone Table, Conduit Table, and Data Flow Matrix — are complete and internally consistent before treating the ZCD diagram as valid evidence.",
            "Establish a formal MoC trigger list: software updates, new interfaces, topology changes, and supplier changes must each initiate a ZCD review.",
            "Use the 15-component checklist to audit an existing ZCD for completeness, not only when creating one from scratch.",
        ],
    },

    "/2026/03/iacs-ur-e27-tasoc-supplier.html": {
        "body": """<p>The article makes a point worth internalizing carefully: the preparation effort for SoC and Type Approval is largely the same. Architecture descriptions, security function definitions, configuration management, test procedures, and evidence consolidation — both paths require the same foundational work. The distinction is not in how much effort you invest, but in what that effort produces: a project-level confirmation versus a product-level approval with formal repeatability.</p>

<p>The cumulative cost argument is the one most frequently dismissed until it becomes concrete. When the same product is delivered to multiple vessels under SoC, each delivery requires re-doing review cycles, re-submitting documentation, and re-validating against the same criteria. The upfront investment in Type Approval converts that per-vessel recurring cost into a one-time fixed cost. The break-even point depends on volume — but for any supplier expecting repeat deliveries across multiple shipyards and class societies, the economics of SoC tend to deteriorate quickly.</p>

<p>The article correctly notes when TA is genuinely less optimal: one-off deliveries, early-stage products with unstable design baselines, and highly compressed schedules. These are legitimate exceptions, not general rules.</p>""",
        "misconception": '"SoC is simpler to prepare than Type Approval." The preparation items — architecture, security functions, configuration management, testing, evidence — are substantially the same for both paths. The real difference is not preparation complexity but the character of the approval: project-bound versus product-level and repeatable.',
        "bullets": [
            "Calculate the break-even point between TA upfront investment and cumulative per-vessel SoC costs based on your realistic delivery volume and target class society mix.",
            "For products with unstable design baselines or one-off delivery scope, SoC remains the rational short-term choice — but set an explicit trigger for re-evaluating the TA path as the design matures.",
            "When operating across multiple class societies, confirm which TA from one society is recognized as a technical reference by others — this significantly affects the effective cost of cross-society repeatability.",
        ],
    },

    "/2026/03/iacs-ur-e26e27-audits-what.html": {
        "body": """<p>The article's opening observation holds in every real audit: Class is not reading documents — it is verifying whether a coherent architecture exists behind those documents. The five-stage verification sequence (Boundary → ZCD → RA/RM impact logic → E27/SCARP consistency → operational maintainability) is not a checklist of isolated items. Each stage builds on the previous one. A boundary definition error at stage one propagates directly into ZCD scope errors at stage two, which then produces risk assessment gaps at stage three. Projects that treat these as five independent deliverables consistently generate multi-round comment cycles.</p>

<p>The most structurally important point in the article is the root cause analysis of why SCARP is almost always inconsistent with E27 documentation: suppliers and shipyards produce their documents independently, and no one integrates them. A CSDD written by integrating supplier E27 inputs with the shipyard's zone-and-conduit architecture cannot be produced by either party working alone. This is not a documentation problem — it is an organizational problem that no amount of template improvement will fix.</p>

<p>The three situations that consistently result in immediate rejection — Boundary/ZCD inconsistency, SCARP as copy-paste of E27 documents, and RA/RM that doesn't trace actual system architecture — are all symptoms of the same missing function: an integrator who owns cross-document consistency.</p>""",
        "misconception": '"Class approval delays are caused by Class being too strict or requirements being too complex." Across all Class societies, delays trace consistently to four root causes: E27/shipyard design mismatch, ZCD/RA/RM/SCARP inconsistency, boundary definition errors, and design changes not reflected in documents. None of these are caused by the requirements themselves.',
        "bullets": [
            "Treat Boundary definition as the first and highest-priority deliverable — errors here propagate into every downstream document and cannot be fixed cheaply at a later stage.",
            "Assign explicit cross-document consistency responsibility to a single party before production begins; do not assume that combining separately produced documents will produce a coherent package.",
            "Use the three consistently rejected patterns (Boundary/ZCD mismatch, SCARP as E27 copy-paste, RA/RM without system-traced impact flow) as a pre-submission self-check before submitting to Class.",
        ],
    },

    "/2024/09/iacs-ur-classnk-guidelines-based.html": {
        "body": """<p>The 23-deliverable breakdown is most useful when read as a dependency map rather than a task list. Owner Policy (deliverable #1) is not simply an owner-side administrative requirement — it is the governing standard that defines the security baseline all other parties must meet. Without it, shipyards have no authoritative reference for writing the Cybersecurity Specification (#14), and suppliers have no policy baseline against which to calibrate their E27 documentation. The table shows who produces what, but the actual failure mode in projects is that these deliverables are produced independently and never reconciled into a single coherent system.</p>

<p>The warning that "classification society interpretations vary — the same system may receive different classifications under ClassNK, DNV, or ABS" is the practical risk that multi-class operators consistently underestimate. A CBS scoped as in-scope under one society may be treated as out-of-scope under another, with direct consequences for the zone/conduit architecture, the asset inventory, and therefore every document downstream. For newbuilds where the class society is already determined, this is a known variable. For fleet-level compliance programs spanning multiple class societies, it requires explicit governance.</p>

<p>The stakeholder role matrix is most actionable when read from the owner's position: the owner is the only party whose requirements cascade to both the shipyard and suppliers simultaneously. Owner Policy, Cybersecurity Specification requirements, and supplier TA requirements all originate from or are shaped by owner decisions. Late or vague owner input at project start compresses the time available for all downstream deliverables.</p>""",
        "misconception": '"If each stakeholder completes its own deliverables, compliance is achieved." The 23 deliverables are interdependent: owner policy shapes shipyard specifications, supplier E27 documentation feeds into shipyard CSDD, and CSDD feeds into owner SCARP. Deliverables produced in isolation without integration cannot satisfy the cross-consistency requirements Class verifies.',
        "bullets": [
            "Treat Owner Policy as the first critical path item — without it, shipyards cannot write a valid Cybersecurity Specification and suppliers cannot calibrate their E27 scope.",
            "Explicitly map the handoff points between stakeholder deliverables (Owner → Shipyard → Supplier and back) and assign responsibility for validating each handoff.",
            "For fleets spanning multiple class societies, track classification society interpretation variance as a formal governance item, not an ad hoc project-by-project discovery.",
        ],
    },
}

# ── HTML builder ─────────────────────────────────────────────────────────────

def build_field_note_html(author: str, note: dict) -> str:
    bullets_html = "\n".join(
        f'            <li style="margin-bottom:8px;">{b}</li>' for b in note["bullets"]
    )
    return f"""
<div id="{FIELD_NOTE_MARKER}" style="border-left:4px solid #1a73e8;background:#f8f9fa;padding:24px 28px;margin:48px 0 32px;font-family:Georgia,serif;border-radius:0 4px 4px 0;">
  <p style="margin:0 0 14px;font-weight:700;color:#1a73e8;font-size:12px;letter-spacing:1.5px;text-transform:uppercase;">&#128204;&nbsp;Field Note &mdash; {author}</p>
  <div style="color:#222;line-height:1.75;font-size:15px;">
    {note["body"]}
    <p style="margin:18px 0 6px;"><strong>A common misconception in practice:</strong><br>
    {note["misconception"]}</p>
    <p style="margin:18px 0 6px;"><strong>Key practical takeaways:</strong></p>
    <ul style="margin:0;padding-left:20px;color:#333;">
{bullets_html}
    </ul>
  </div>
</div>
"""


# ── Auth ─────────────────────────────────────────────────────────────────────

def get_session():
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request, AuthorizedSession

    SCOPES = ["https://www.googleapis.com/auth/blogger"]
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    return AuthorizedSession(creds)


BASE = "https://blogger.googleapis.com/v3"


def get_blog_id(session) -> str:
    r = session.get(f"{BASE}/blogs/byurl", params={"url": BLOG_URL})
    r.raise_for_status()
    data = r.json()
    print(f"✅ Blog ID: {data['id']}  ({data['name']})")
    return data["id"]


def get_post_by_path(session, blog_id: str, path: str):
    r = session.get(
        f"{BASE}/blogs/{blog_id}/posts/bypath",
        params={"path": path, "fields": "id,title,content,author"}
    )
    if r.status_code == 200:
        return r.json()
    print(f"  ⚠️  getByPath failed: {r.status_code} {r.text[:120]}")
    return None


def patch_post(session, blog_id: str, post_id: str, body: dict):
    r = session.patch(f"{BASE}/blogs/{blog_id}/posts/{post_id}", json=body)
    r.raise_for_status()
    return r.json()


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("ShipPaulJobs — Append Field Notes")
    print(f"{'[DRY RUN]' if DRY_RUN else '[LIVE] actual update'}")
    print("=" * 60)

    session  = get_session()
    blog_id  = get_blog_id(session)

    updated  = 0
    skipped  = 0
    failed   = 0

    for path, note in FIELD_NOTES.items():
        url = BLOG_URL + path
        print(f"\n🔗 {url}")

        post = get_post_by_path(session, blog_id, path)
        if not post:
            print("  ❌ fetch failed, skipping")
            failed += 1
            continue

        post_id = post["id"]
        title   = post.get("title", "?")
        content = post.get("content", "")
        author  = post.get("author", {}).get("displayName", "Captain Paul")

        print(f"  📄 [{post_id}] {title!r}  (author: {author})")

        # Duplicate guard
        if FIELD_NOTE_MARKER in content:
            print("  ✅ Field Note already present, skipping")
            skipped += 1
            continue

        new_content = content + build_field_note_html(author, note)

        if DRY_RUN:
            print(f"  [DRY RUN] would append field note for author={author!r}")
            updated += 1
            continue

        try:
            patch_post(session, blog_id, post_id, {"content": new_content})
            print(f"  ✅ Field Note appended (author: {author})")
            updated += 1
        except Exception as e:
            print(f"  ❌ update failed: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Done: {updated} updated, {skipped} skipped, {failed} failed")
    print("=" * 60)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
