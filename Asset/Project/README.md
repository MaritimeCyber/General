# Project — SCARP (Ship Cybersecurity and Resilience Program)

> **Status:** Project directory initialized. Tools and code are under active development.
> The folder structure below reflects the planned layout; files will be added as each tool is completed.

## Background

IACS Unified Requirements E26 and E27 impose concrete, verifiable cyber resilience obligations on ship owners, shipbuilders, and system suppliers. A central challenge in meeting these requirements is the systematic identification and documentation of all Computer-Based Systems (CBS) aboard a vessel — a process that must be initiated early in the design phase and revisited at each annual survey. Manual inventory collection is error-prone and labor-intensive; purpose-built tooling is therefore essential.

This folder publishes open tools and code developed to support CBS asset discovery, compliance gap analysis, and controlled security testing in maritime environments.

## Purpose

- Provide practical, open-source tooling for IACS UR E26 / E27 compliance workflows
- Enable ship owners, shipbuilders, and system suppliers to perform structured CBS pre-surveys
- Support annual survey teams with automated gap analysis between expected and observed asset states
- Publish responsible security testing code (DoS resilience, penetration testing) under clear authorization requirements

---

## Project Categories

### 1. CBS Asset Scanner

**Objective:** Collect preliminary CBS inventory data required under IACS UR E26 / E27 before formal survey.

Ship owners, shipbuilders, and system suppliers are required to document all CBS, including:

- Hardware inventory (model, firmware version, OS, interfaces)
- Network topology and communication paths
- Software and application inventory
- Vendor and lifecycle status

**Tool types published here:**

| Tool | Format | Description |
|---|---|---|
| **Network Discovery Scanner** | Python / Executable | Active/passive scan of onboard OT/IT networks; outputs CBS candidates with open ports, protocols, and OS fingerprints |
| **Passive Traffic Analyzer** | Python | Captures and classifies network traffic to identify undocumented CBS without active probing |
| **CBS Inventory Collector** | Python / Shell | Agent-based local data collection from individual systems (OS info, installed software, active services) |
| **Report Generator** | Python | Aggregates scan results into structured CBS inventory reports (CSV, JSON, PDF) aligned with IACS UR E27 templates |

> **Note:** Active scanning must be authorized by the vessel operator or shipyard. Do not run discovery tools on live operational networks without written authorization from the responsible party.

---

### 2. Annual Survey Gap Analyzer

**Objective:** Compare the CBS inventory from the previous survey period against the current state to identify changes, additions, removals, and compliance drift.

IACS UR E26 requires continuous cyber resilience management. Annual surveys must verify that the ship's cyber resilience posture has been maintained or improved. This toolset automates the comparison process.

**Capabilities:**

| Feature | Description |
|---|---|
| **Baseline Diff** | Compares current scan output against the approved CBS baseline from the previous survey |
| **Change Classification** | Categorizes changes as: New CBS, Removed CBS, Configuration Drift, Firmware/Software Update, or Unresolved Anomaly |
| **Compliance Mapping** | Maps each identified gap to the relevant IACS UR E26/E27 requirement clause |
| **Gap Report** | Produces a structured gap report suitable for submission to the classification society surveyor |

**Inputs:**

- Previous survey CBS inventory (JSON/CSV)
- Current scan output from the CBS Asset Scanner
- IACS requirement mapping file (maintained in this repository)

---

### 3. DoS Resilience Testing

**Objective:** Verify that onboard CBS and OT networks can maintain availability under adverse network conditions, as required by IACS UR E26 Clause 4 (Availability) and E27 Clause 3.

**Scope of tools published:**

| Tool | Protocol / Layer | Description |
|---|---|---|
| **Network Flood Tester** | TCP/UDP/ICMP | Generates controlled traffic loads to test CBS availability thresholds |
| **Protocol Fuzzer (OT)** | Modbus, DNP3, NMEA 2000 | Sends malformed or high-volume OT protocol messages to test parser robustness |
| **Resource Exhaustion Tester** | Application Layer | Tests CPU/memory behavior under sustained connection or request load |

> **Authorization Required.** These tools are intended exclusively for:
> - Authorized penetration testing engagements with a signed scope of work
> - Shipyard factory acceptance testing (FAT) or harbor acceptance testing (HAT)
> - Classification society witness testing in controlled environments
> - CTF competitions and research lab environments
>
> **Do not run these tools on operational vessels or live networks without explicit written authorization from the vessel operator and flag state authority where applicable.**

---

### 4. Penetration Testing Toolkits

**Objective:** Identify exploitable vulnerabilities in onboard CBS before an attacker does, supporting the intent of IACS UR E26 / E27 and IMO MSC-FAL.1/Circ.3 risk management requirements.

**Tool categories:**

| Category | Description |
|---|---|
| **Reconnaissance Scripts** | Automated CBS fingerprinting, service enumeration, and vulnerability signature matching |
| **OT Protocol Exploits** | PoC exploit code targeting known CVEs in maritime OT protocols and systems (Modbus, NMEA, proprietary ICS) |
| **Credential Testing** | Default/weak credential checks against common marine systems (ECDIS, VDR, AMS, SCADA HMI) |
| **Lateral Movement Simulation** | Scripts demonstrating OT-to-IT pivot paths in segmented maritime networks |
| **Post-Exploitation Analysis** | Forensic artifact collection scripts for incident response exercises |

> **Responsible Disclosure Policy.** Any vulnerability discovered using tools from this repository that has not yet been publicly disclosed should be reported to the affected vendor through a responsible disclosure process before public sharing. Do not use these tools for unauthorized access to any system.

---

## Folder Structure

```
Project/
├── asset-scanner/
│   ├── network-discovery/      # Active/passive CBS network scanner
│   ├── host-collector/         # Local CBS data collection agent
│   └── report-generator/       # Inventory report builder
├── gap-analyzer/
│   ├── baseline-diff/          # Survey-to-survey comparison engine
│   ├── compliance-mapper/      # IACS clause mapping logic
│   └── gap-report/             # Output report templates
├── dos-testing/
│   ├── network-flood/          # Layer 3/4 availability tester
│   ├── ot-fuzzer/              # OT protocol fuzzer (Modbus, DNP3, NMEA)
│   └── resource-exhaustion/    # Application layer load tester
├── pentest/
│   ├── recon/                  # CBS fingerprinting and enumeration
│   ├── ot-exploits/            # OT-specific PoC exploit modules
│   ├── credential-testing/     # Default credential checker
│   └── lateral-movement/       # OT-IT pivot simulation
└── shared/
    ├── iacs-mapping/           # IACS UR E26/E27 requirement clause database
    ├── cbs-templates/          # CBS inventory data schemas
    └── utils/                  # Shared parsing and reporting utilities
```

---

## File Naming Convention

```
[Category]_[ToolName]_[Version].[ext]
```

Examples:
- `scanner_network-discovery_v1.0.py`
- `gap_baseline-diff_v2.1.py`
- `dos_ot-fuzzer_v1.0.py`
- `pentest_credential-check_v1.3.py`

---

## Usage Requirements

All tools in this project are published for **authorized, lawful use only**.

| Requirement | Detail |
|---|---|
| **Authorization** | Written authorization from the system/network owner is required before running any active scanning, DoS, or penetration testing tool |
| **Scope** | Use is limited to the systems and networks explicitly included in the authorization |
| **Environment** | Prefer isolated test environments (lab, FAT/HAT berth, simulation network) over live operational systems |
| **Legal Compliance** | Users are responsible for compliance with applicable national laws, maritime regulations, and flag state requirements |
| **Disclosure** | Undisclosed vulnerabilities found must be reported through responsible disclosure before public sharing |

---

## Contribution Guide

Each tool submission should include:

- **README** — Purpose, scope, usage instructions, authorization requirements
- **Source code** — Python preferred; executables may be provided alongside source
- **Test environment notes** — What environment was it tested in? (e.g., lab network, specific CBS/OT vendor)
- **IACS mapping** — Which UR E26/E27 clause does the tool support?
- **Known limitations** — False positive rates, protocol coverage gaps, OS/platform dependencies

---

## Related Standards

| Standard | Relevance to This Project |
|---|---|
| **IACS UR E26** | Cyber resilience of ships — asset inventory, availability, access control requirements |
| **IACS UR E27** | Cyber resilience of on-board systems — CBS documentation, segmentation, patching |
| **IACS Rec. 166** | Recommended practice for CBS software maintenance |
| **IEC 62443-2-4** | Security program requirements for IACS service providers |
| **NIST SP 800-82** | Guide to ICS security — scanning and assessment methodology |
| **BIMCO Guidelines v4** | Operational context for crew-facing cyber security procedures |

---

> Back to [Asset](../README.md) | [Repository Root](../../README.md)

---

<p align="center">
  <i>Tools built for safer ships. Use responsibly. — Maritime 4.0 Crew</i>
</p>
