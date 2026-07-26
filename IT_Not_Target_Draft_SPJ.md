# Why Someone Said "IT Is Not the Target System" — And Why That Interpretation Gets It Wrong

**Category:** Rules and Compliance | IACS UR E26 / E27  
**Series:** Maritime Cyber Insight  
**Author:** Captain Paul  
**Target:** System Integrators, Ship Owners, Cyber Compliance Officers

---

## Introduction

A growing concern is emerging within the maritime cybersecurity community: some System Integrators (SIs) are advising ship owners and operators that **IT systems onboard vessels are not subject to IACS UR E26 requirements**. The argument is simple — read the regulation literally, identify the explicit scope, and conclude that only OT systems require cybersecurity management.

This interpretation is not only narrow. When examined against the full body of IACS Unified Requirements — E10, E22, E26, and E27 — combined with post-delivery operational realities and annual survey obligations, it becomes clear that this reading **actively distorts the purpose and direction the regulations were designed to achieve**.

This article presents a comprehensive interpretation based on NIST cybersecurity principles and the holistic intent of IACS UR E26 and E27, with the goal of achieving genuine **cyber resilience** — not mere checkbox compliance.

---

## 1. Where the Confusion Starts: A Literal Reading of E26

IACS UR E26 — *Cyber Resilience of Ships* — defines its primary subject as **Computer Based Systems (CBS)**. At first glance, the regulation's language centers on systems used for "control, monitoring, alarming, and reporting" functions aboard ships. A surface-level reading leads some SIs to conclude:

> *"E26 applies to OT control systems. Administrative IT systems — email servers, crew welfare networks, office computers — are outside its scope."*

This conclusion feels logical when read in isolation. The problem is that **IACS UR E26 was never designed to be read in isolation**.

---

## 2. What IACS UR E26 Actually Defines

Section 2 of IACS UR E26 defines **Computer Based System (CBS)** as:

> *"A system that processes, transmits or stores data in digital form, including systems used for control, monitoring, alarming and reporting functions."*

The critical phrase is **"including"** — not "limited to." The word "including" in regulatory language signals that what follows is an illustrative list, not an exhaustive boundary. Administrative systems, navigation data servers, VSAT communication terminals, and crew management platforms all **process, transmit, and store data in digital form**.

By the plain text definition in E26 Section 2, **IT systems are CBS**. The narrow OT-only interpretation contradicts the regulation's own terminology.

---

## 3. The Full Picture: E10, E22, E26, and E27 Read Together

Regulatory frameworks are rarely standalone documents. IACS Unified Requirements are a connected body of rules designed to work together. Reading E26 without E10, E22, and E27 produces an incomplete — and potentially dangerous — understanding.

### IACS UR E22 — Onboard Computers and Networks

E22 predates E26 and specifically addresses **onboard computer systems and data networks**. Its scope explicitly includes workstations, servers, local area networks (LAN), and administrative computing infrastructure. E22 established the foundational requirement that **all onboard computer systems must be managed with integrity and security in mind** — including IT systems.

E26 builds on E22. It does not replace it. An SI who excludes IT systems from E26 compliance is also implicitly undermining E22's established framework.

### IACS UR E10 — Automatic and Remote Control Installations

E10 governs automatic and remote control systems. In modern vessels, these systems do not operate in a closed vacuum. They interface with:

- Remote monitoring platforms (cloud-based, IT-dependent)
- Crew and operator workstations (IT endpoints)
- Shore-based operations centers (IT/OT bridge)

Excluding IT from the cybersecurity management scope while maintaining E10-covered OT systems creates **unprotected interfaces** — exactly the attack surface that threat actors exploit.

### IACS UR E27 — Cyber Resilience of Onboard Systems and Equipment

E27 extends E26's requirements to the **equipment manufacturer level**, requiring that equipment suppliers implement cybersecurity throughout the product lifecycle. Critically, E27 does not distinguish between IT and OT equipment. It applies to **any Computer Based System or equipment component** that forms part of the ship's operational infrastructure.

If equipment manufacturers must apply cybersecurity principles to all CBS — including those with IT components — it is logically inconsistent to argue that ship operators can exclude IT from their own cybersecurity management obligations.

---

## 4. The NIST Lens: Cyber Resilience Does Not Draw an IT/OT Line

IACS UR E26 and E27 are explicitly aligned with the **NIST Cybersecurity Framework (CSF)**. The NIST CSF's five core functions — **Identify, Protect, Detect, Respond, Recover** — apply uniformly across all digital assets, systems, and networks. NIST does not partition its framework by IT vs. OT.

Furthermore, **NIST SP 800-82** (Guide to Industrial Control Systems Security) and **NIST SP 800-53** (Security and Privacy Controls) both recognize the convergence of IT and OT environments. SP 800-82 explicitly states:

> *"ICS security should not be designed in isolation from enterprise IT security."*

If IACS UR E26 references NIST principles as its cybersecurity foundation, and NIST does not permit the exclusion of IT systems from the security scope, then **any interpretation of E26 that excludes IT systems contradicts its own foundational reference framework**.

The five NIST functions, applied to the maritime context, require:

| NIST Function | IT Relevance Onboard |
|---|---|
| **Identify** | Asset inventory must include IT systems, not just OT |
| **Protect** | Access control, patching, and hardening apply to IT endpoints |
| **Detect** | Network monitoring must cover IT segments — primary threat entry points |
| **Respond** | Incident response plans must address IT-originated incidents |
| **Recover** | Business continuity requires IT system restoration alongside OT |

Excluding IT from E26's scope invalidates all five functions.

---

## 5. Post-Delivery Operations and Annual Survey Reality

The IT-exclusion argument also fails when examined against the **operational lifecycle** of a ship beyond the initial delivery and class certification.

### 5.1 Annual Surveys

IACS member classification societies are increasingly incorporating cyber resilience assessments into annual and periodic surveys. These assessments evaluate the **overall cyber posture of the vessel** — not a subset of OT systems. Surveyors are trained to examine:

- Network segmentation (IT/OT boundary controls)
- Patch management status across all CBS
- Access control policies covering IT and OT systems
- Incident response documentation

A ship delivered with an IT-exclusion posture will face growing compliance gaps with each subsequent survey cycle.

### 5.2 The Attack Vector Reality

Maritime cyber incidents consistently demonstrate that **IT systems are the primary entry point for attackers**, not OT systems:

- **Phishing emails** target crew and officer IT endpoints
- **VSAT and satellite communication terminals** (IT infrastructure) are compromised for initial access
- **USB devices and crew personal devices** introduce malware through IT interfaces
- **Ransomware** enters through administrative networks before pivoting to operational systems

Once an attacker has a foothold in the IT network, **lateral movement to OT systems** is the standard progression. BIMCO, IMO, and classification societies have all documented this attack pattern.

Declaring IT out of scope does not make IT systems safe. It makes them unmonitored and unprotected — exactly the condition attackers rely on.

### 5.3 ISM Code Integration

The International Safety Management (ISM) Code requires ship operators to maintain **procedures for all safety-critical operations**, including communications and data management. Cyber incidents affecting IT systems — cargo management data, crew documentation, communications — directly impact ISM compliance. The ISM Code's requirement for a Safety Management System (SMS) must evolve to incorporate cyber considerations across all onboard digital systems.

---

## 6. Why the Narrow Interpretation Is Commercially Problematic

There is an important question worth asking: **Who benefits from the IT-exclusion interpretation?**

Narrowing E26's scope to OT-only systems reduces the cost and complexity of compliance delivery for SIs. Fewer systems to assess, fewer controls to implement, fewer documentation requirements. In competitive bidding environments, a narrowly-scoped compliance package appears more cost-effective.

But this creates a fundamental market distortion:

1. Ship owners receive a **false assurance of compliance** that will not hold under annual survey scrutiny or Port State Control (PSC) inspections
2. The cybersecurity posture of the fleet is **structurally weakened** by design
3. When an IT-originated breach occurs — and the statistical probability is high — the ship owner bears the liability while the SI's narrow-scope delivery appears technically complete on paper

This is not compliance. It is **the appearance of compliance**, engineered to reduce delivery costs at the expense of genuine cyber resilience.

---

## 7. The Correct Approach: Cyber Resilience as the Objective

IACS UR E26 Section 1 states its purpose clearly:

> *"The objective of this UR is to ensure that ships are delivered with cyber resilient Computer Based Systems."*

**Cyber resilience** — not OT compliance. Not partial system coverage. The word "resilience" implies the ability to withstand, absorb, and recover from cyber incidents regardless of where they originate. A ship with resilient OT and vulnerable IT is not a cyber-resilient ship.

The correct approach for SIs, ship owners, and compliance officers involves:

**Step 1 — Comprehensive CBS Inventory (NIST: Identify)**  
Document all Computer Based Systems onboard — OT and IT alike. Navigation systems, power management, administrative servers, crew networks, VSAT terminals, and all interfaces between them.

**Step 2 — IT/OT Network Segmentation and Boundary Protection (NIST: Protect)**  
Define and implement controls at the boundary between IT and OT networks. This boundary, not the IT systems themselves, is the critical control point — and it can only be managed if IT is within scope.

**Step 3 — Unified Security Monitoring (NIST: Detect)**  
Monitoring systems must cover IT network segments. Anomalous behavior on IT networks is frequently the earliest detectable indicator of a developing attack.

**Step 4 — Integrated Incident Response (NIST: Respond)**  
Incident response plans must address IT-originated incidents. Crew training must cover IT threat vectors — phishing, removable media, unauthorized access.

**Step 5 — Continuity and Recovery Planning (NIST: Recover)**  
Recovery procedures must restore both IT and OT systems. An operator who can restore OT but not IT cannot resume full commercial operations or satisfy ISM reporting requirements.

---

## Conclusion

The argument that "IT is not the target system under E26" is not a legitimate regulatory interpretation. It is a selective reading that contradicts the plain language of E26's CBS definition, ignores the connected framework of E10, E22, E26, and E27, conflicts with NIST's foundational principles that E26 references, and disregards the operational reality of post-delivery annual surveys and real-world cyber attack patterns.

IACS established E26 and E27 with a clear objective: **cyber resilience for ships**. That resilience cannot be achieved by protecting one half of a ship's digital ecosystem while leaving the other half unmanaged.

For ship owners evaluating cybersecurity proposals, the question to ask any SI is direct:  
**"Does your E26 compliance scope include all Computer Based Systems — IT and OT — as defined in E26 Section 2?"**

If the answer is no, the compliance package on offer does not meet the standard the regulation was written to achieve.

---

*Captain Paul is a maritime cybersecurity specialist focused on IACS UR E26 and E27 compliance, OT/IT security convergence, and practical cyber resilience for the global fleet. ShipPaulJobs.com.*

---

**Tags:** IACS UR E26, IACS UR E27, IACS UR E22, IACS UR E10, Maritime Cybersecurity, OT Security, IT Security, NIST CSF, Cyber Resilience, Ship Compliance, Annual Survey, ISM Code
