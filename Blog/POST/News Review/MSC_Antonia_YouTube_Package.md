# YouTube Production Package
## "The MSC Antonia Grounding: GPS Spoofing, IACS E26, and the Gap No One Is Talking About"
**Channel:** ShipPaulJobs · Maritime 4.0  
**Target Length:** 9–11 minutes  
**Language:** English  
**Format:** Narration + Slides (no talking head required)

---

## 1. VIDEO TITLE OPTIONS

**Primary (recommended)**
> How a Fake GPS Signal Grounded a 304-Meter Container Ship — and Why IACS E26 Won't Stop the Next One

**Alternatives**
- The MSC Antonia Grounding: GPS Spoofing, IACS E26, and the Gap No One Is Talking About
- GPS Spoofing Grounded This 7,000 TEU Ship. Here's What Your E26 Compliance Missed.

---

## 2. THUMBNAIL

**Layout (dark navy background)**

```
[TOP — small red label]
⚠  MARITIME CYBER INCIDENT

[CENTER — large bold white text, 2 lines]
"They Navigated
to a Shoal That
Wasn't There."

[BOTTOM — smaller accent text in amber]
MSC ANTONIA · GPS SPOOFING · IACS E26 GAP
```

**Visual**: Ship silhouette (bow view) overlaid on a distorted GPS grid / radar sweep graphic. Red cross-hair on wrong position.

---

## 3. YOUTUBE DESCRIPTION

```
On May 10, 2025, the MSC Antonia — a 304-meter, 7,000 TEU container ship — ran aground near the Eliza Shoals in the Red Sea. The crew wasn't negligent. The navigation equipment wasn't malfunctioning. The GPS was lying.

Three independent intelligence firms confirmed the same verdict: deliberate GPS spoofing.

In this video I break down what actually happened technically, where IACS UR E26 falls short as a defense against this class of attack, what a properly designed GNSS integrity architecture looks like, and the four compliance questions every shipowner needs to answer before their next survey.

─────────────────────────────────────────
CHAPTERS
─────────────────────────────────────────
00:00  The Incident
01:15  What GPS Spoofing Actually Does
02:50  This Is Not a Red Sea Problem
04:10  Why IACS E26 Doesn't Catch This
06:00  What Good Architecture Looks Like
07:40  Your E26 Compliance Checklist
09:20  What I'd Recommend Right Now

─────────────────────────────────────────
SOURCES
─────────────────────────────────────────
• Pole Star Global: GPS interference caused MSC Antonia grounding — gCaptain
• Windward AI: GPS Jamming Q1 2025 report (600 km → 6,300 km average position error)
• Scientific American: GPS Spoofing in the Strait of Hormuz
• IACS UR E26 & E27 — iacs.org

─────────────────────────────────────────
WHO I WRITE AND SPEAK FOR
─────────────────────────────────────────
Maritime cybersecurity professionals, IACS E26/E27 consultants, technical superintendents, shipyard OT system designers, and operators navigating Maritime 4.0.

🌐 Full article: https://www.shippauljobs.com/2026/06/msc-antonia-gps-spoofing.html
💼 LinkedIn: https://www.linkedin.com/in/shipjobs/

#GPSSpoofing #MSCAntonia #MaritimeCyber #IACSE26 #GNSSMaritime #OTSecurity #Maritime40 #ShipCyber #RedSeaCyber #ECDISSecurity
```

---

## 4. SLIDE STRUCTURE (Scene-by-Scene)

### SLIDE 01 — COLD OPEN (0:00–0:15)
**Visual:** Black screen → slow fade to satellite image of Red Sea coastline near Jeddah  
**Text overlay (appears line by line):**
```
May 10, 2025.
Red Sea. South of Jeddah Port.
304 meters. 7,000 TEU. Familiar waters.
```
*No narration. Music only. Builds tension.*

---

### SLIDE 02 — THE HOOK (0:15–0:45)
**Visual:** AIS track replay showing erratic positional jump → ship icon on shoal  
**Text overlay:** "The ship's GPS was receiving signals. The signals were lies."

---

### SLIDE 03 — TITLE CARD (0:45–1:00)
**Visual:** Dark navy gradient background  
**Text:**
```
THE MSC ANTONIA GROUNDING
GPS Spoofing · IACS E26 · The Gap No One Is Closing

ShipPaulJobs | Maritime 4.0
```

---

### SLIDE 04 — SECTION I: WHAT HAPPENED (1:00–2:50)
**Visual:** Animated diagram — GPS satellite → ship receiver → ECDIS → shoal  
**Text:** Step-by-step numbered sequence (builds on screen as narrated)
```
① Spoofed signals overpower real satellite data
② Ship calculates a position that doesn't exist
③ ECDIS displays false chart overlay
④ Officer of the Watch navigates the false chart
⑤ The shoal exists. The coordinates didn't match.
⑥ Contact.
```

---

### SLIDE 05 — THE DATA POINT (2:50–3:20)
**Visual:** Bar chart — position error Q4 2024 vs Q1 2025  
**Text:**
```
Average GPS position error in the Red Sea:

Q4 2024 ────── 600 km
Q1 2025 ────── 6,300 km

10× increase in a single quarter.
(Source: Windward AI)
```

---

### SLIDE 06 — SECTION II: NOT A RED SEA PROBLEM (3:20–4:20)
**Visual:** World map with highlighted chokepoints — Red Sea, Strait of Hormuz, Persian Gulf  
**Text boxes appearing on each region:**
```
Jun 2025 · Persian Gulf
3,000+ vessels disrupted in 2 weeks

Feb 2026 · Strait of Hormuz
1,100+ vessels affected in 24 hours
Spoofed signals placed ships over airports
and near a nuclear power plant

The Strait of Hormuz carries ~20% of world oil.
It is 33 km wide at its narrowest point.
```

---

### SLIDE 07 — THE ASYMMETRY (4:20–4:50)
**Visual:** Simple split-screen comparison  
**Left:** "Attack cost" — SDR hardware icon, "$<100"  
**Right:** "Potential consequence" — ship silhouette, cargo value, environmental cost  
**Text:** "This is not a future risk. It is a current one."

---

### SLIDE 08 — SECTION III: THE E26 GAP (4:50–6:10)
**Visual:** IACS E26 framework diagram with one section highlighted in red  
**Text (builds progressively):**
```
IACS UR E26 requires detection of:
✓ Anomalous events on computer-based systems
✓ Unexpected network traffic
✓ Deviation from operational parameters

GPS Spoofing produces:
✗ No anomalous system event
✗ No unexpected network traffic
✗ No deviation from operational parameters

The GNSS receiver is working perfectly.
The data it outputs is the problem.
E26 cannot detect an input-level attack.
```

---

### SLIDE 09 — THE ARCHITECTURAL GAP (6:10–6:40)
**Visual:** Bridge system diagram — GNSS → ECDIS → autopilot, single data path, no cross-validation  
**Text:**
```
The question I ask at every shipyard:
"At what layer is position data validated
before it reaches ECDIS?"

The most common answer:
"It isn't."
```

---

### SLIDE 10 — SECTION IV: WHAT GOOD LOOKS LIKE (6:40–7:40)
**Visual:** 4-panel grid, each panel illustrating one solution  
```
🛰  Multi-Constellation Reception
    GPS + GLONASS + Galileo + BeiDou simultaneously
    Much harder to spoof — attacker must mimic all four

📍  Position Cross-Validation
    GNSS vs. Radar vs. INS
    >0.1nm divergence = automatic alert

⚡  Rate-of-Change Sanity Checks
    "This vessel cannot move 6,000 km in 4 seconds"
    Simple filter. Catches the most obvious attacks.

🎓  Bridge Team Training
    Sensor divergence = potential cyber event
    Not assumed to be radar error or chart discrepancy
```

---

### SLIDE 11 — SECTION V: COMPLIANCE CHECKLIST (7:40–9:00)
**Visual:** Clean checklist layout, items appear one at a time  
```
Your E26 GNSS Integrity Checklist

□ Q1  Which CBS systems receive GNSS-derived data?
      (ECDIS, AIS, autopilot, VSAT, cargo mgmt...)

□ Q2  Does your bridge system cross-validate GNSS
      against radar or INS position?
      (RAIM is NOT the same thing)

□ Q3  Is sensor divergence response documented in your SMS?

□ Q4  Are your GNSS receivers multi-constellation?
      If built before 2022 — probably not.
```

---

### SLIDE 12 — SECTION VI: RECOMMENDATIONS (9:00–10:00)
**Visual:** Three columns by stakeholder group  
```
🚢 Shipowners & Superintendents
• Audit your GNSS dependency map across the fleet
• Add "GNSS anomaly" to bridge training materials
• Raise multi-constellation capability at next survey

🏗  Shipyards & System Integrators
• Raise GNSS integrity in preliminary design review
• Map every CBS that takes GNSS as input
• Design cross-validation before commissioning

⚙  Equipment Manufacturers
• GNSS spoofing resistance is part of E27 obligation
• "Class-approved" ≠ tested against active spoofing
```

---

### SLIDE 13 — OUTRO / CALL TO ACTION (10:00–10:45)
**Visual:** Dark navy — ShipPaulJobs logo (animated float)  
**Text:**
```
The Eliza Shoals have been on charts for a very long time.
The ship knew they were there.

It just didn't know where the ship was.

─────────────────────────────────
Full article + sources → shippauljobs.com
LinkedIn → linkedin.com/in/shipjobs
Subscribe for Maritime 4.0 · AI · Cyber Intelligence
─────────────────────────────────
```

---

## 5. NARRATION SCRIPT (Full — ~1,450 words, ~10 min at 145 wpm)

---

**[COLD OPEN — no narration, 15 seconds of music]**

---

**[HOOK]**

On May 10, 2025, the container ship MSC Antonia was navigating from Marsa Bashayer to Jeddah Port — a route it had almost certainly sailed before.

304 meters long. 7,000 containers. Experienced crew. Familiar waters.

Somewhere during that transit, the ship's GPS receivers stopped tracking the real world.

They were receiving signals — strong ones. The equipment was functioning exactly as designed. But those signals were coming from a transmitter on the ground, not from satellites in orbit. And they were telling the ship it was somewhere it was not.

The Eliza Shoals were not where the ship's systems said the shoals would be.

No warning. No alarm. No dramatic failure.

Just a 304-meter ship, moving at speed, onto a shoal that the charts said wasn't there — because the chart overlay was tracking the wrong position.

Three independent intelligence firms — Windward, Pole Star Global, and MarineTraffic — confirmed the same conclusion: deliberate GPS spoofing.

This video is about what that means. Technically. Regulatorily. And for anyone working in maritime cybersecurity or IACS E26 compliance today.

---

**[SECTION I — WHAT ACTUALLY HAPPENED]**

GPS spoofing is conceptually simple. A transmitter broadcasts fake satellite signals at higher power than the real ones. The ship's GNSS receiver — doing exactly what it was designed to do — locks onto the stronger signal and starts calculating position based on that data.

The receiver isn't broken. It isn't being hacked in any traditional sense. It is functioning correctly. The input is the problem.

Here's the sequence, as reconstructed from Pole Star and Windward's post-incident analysis:

First, spoofed signals overpower the real satellite data. The ship's calculated position drifts.

Second, ECDIS — the electronic chart display that the officer of the watch navigates by — begins showing that false position on the chart. It has no way to know the data is false.

Third, the ship navigates based on what ECDIS shows.

Fourth — the Eliza Shoals exist in the real world. They don't exist at the coordinates the ship believes it's at.

And then contact.

Pole Star's analysis found something important: the AIS transponder, which is also GPS-fed, was broadcasting erratic positions consistent with spoofed data *before* the grounding. The signature was visible. It just wasn't recognized as a threat indicator.

---

**[SECTION II — THIS IS NOT A RED SEA PROBLEM]**

It's comfortable to frame this as a conflict-zone issue. "GPS spoofing near Jeddah, in a militarized waterway." It makes the threat feel geographically contained.

It isn't.

Windward's Q1 2025 data documented average GPS position errors in the Red Sea region reaching 6,300 kilometres. That's a tenfold increase from 600 kilometres the previous quarter. In a single quarter.

In June 2025, an escalation in the Persian Gulf disrupted over 3,000 vessels in two weeks.

In February 2026, a spoofing event in the Strait of Hormuz affected over 1,100 vessels in the first 24 hours — with spoofed signals placing ships over airports and near a nuclear power plant.

The Strait of Hormuz carries approximately 20 percent of the world's oil. It is 33 kilometres wide at its narrowest point.

A spoofing event at scale in that corridor is not a cybersecurity incident. It is a navigational mass-casualty scenario.

And the hardware that makes this possible? Commercially available. Widely discussed in security research circles. Entry-level spoofing capability at costs that put it within reach of non-state actors.

The asymmetry between attack cost and consequence is extreme.

---

**[SECTION III — THE E26 GAP]**

I want to be direct about this, because I see it misunderstood in compliance workshops.

IACS UR E26 does not mandate GPS spoofing detection.

What E26 does require — under its Detection function — is the ability to detect anomalous events on computer-based systems, monitor network traffic for unexpected activity, and flag deviations from expected operational parameters.

A spoofed GPS feed produces none of those signals.

The GNSS receiver is functioning normally. The data it outputs is indistinguishable from genuine positioning data at the system level. ECDIS ingests it without error. The integrated bridge system accepts it without alarm.

E26 was designed around the assumption that anomalies can be detected by monitoring the *behaviour* of networked systems.

GPS spoofing attacks the *data* that feeds those systems. Not the systems themselves.

It is an input-level attack on a compliance framework built to detect process-level anomalies.

This is not a criticism of E26. It is a gap that the industry needs to understand clearly — because treating E26 compliance as GPS spoofing protection is a dangerous misreading of what the regulation actually covers.

---

**[SECTION IV — WHAT GOOD ARCHITECTURE LOOKS LIKE]**

When I'm engaged on an E26 compliance project at a shipyard, one of the most important questions I ask the design team is this:

"At what layer is the position data validated before it reaches ECDIS?"

In most current designs, the answer is: it isn't.

A properly designed GNSS integrity architecture has four components.

First: multi-constellation reception. A receiver pulling simultaneously from GPS, GLONASS, Galileo, and BeiDou is significantly harder to spoof — the attacker must convincingly mimic signals from four independent satellite networks in precise coordination.

Second: position cross-validation against independent sources. Radar-derived position, inertial navigation output, and GNSS position should be actively compared. A divergence beyond a defined threshold — say, 0.1 nautical miles — should trigger an alert before ECDIS auto-updates.

Third: rate-of-change sanity checks. The MSC Antonia's position "jumped" thousands of kilometres in spoofing event signatures. A simple velocity plausibility filter would catch the most egregious attack patterns at the system level.

Fourth — and this is the biggest gap I find in practice — bridge team training. When radar position and GNSS position disagree, the instinct of most bridge teams is to assume radar error or chart discrepancy. Not GPS spoofing. That instinct needs to be retrained.

None of these measures are exotic. The obstacle is not technical. It's that they require conscious design intent — and that intent must be present during the E26 compliance conversation at the shipyard. Not after the vessel is already trading.

---

**[SECTION V — YOUR COMPLIANCE CHECKLIST]**

If you are working on E26 compliance right now — whether as a shipowner, technical superintendent, or shipyard consultant — here are four questions to pressure-test your position.

Question one: which computer-based systems on this vessel receive GNSS-derived data as input? ECDIS is obvious. But also: autopilot, AIS transponders, VSAT antenna tracking, dynamic positioning, any bridge automation that uses position as a parameter. That's your GNSS dependency map. If you don't have it, you can't protect it.

Question two: does your integrated bridge system cross-validate GNSS against radar or INS position? If the answer is "it has a RAIM alarm," that is not the same thing. RAIM detects signal quality degradation. It does not detect a high-quality spoofed signal.

Question three: what is the bridge team's documented procedure when navigation sensor sources diverge? If that procedure is not in your Safety Management System, it will be noticed at your first E26-relevant survey.

Question four: are your GNSS receivers multi-constellation? If the vessel was designed before 2022, single-constellation receivers are likely. Retrofitting is not trivial — but the risk calculus needs to be formally on record.

---

**[OUTRO]**

The entire GNSS architecture was built on an implicit assumption: that satellite signals are authoritative and uncontested. That assumption was valid for the first three decades of commercial maritime GNSS use. It is no longer valid across an increasing proportion of the world's strategic waterways.

What happened to the MSC Antonia was entirely predictable to anyone watching the Red Sea spoofing pattern from Q4 2024 onward. The data showed average position errors increasing tenfold in a single quarter. The conclusion — that a vessel would eventually be placed on a shoal by a spoofed track — was not a surprising prediction. It was a scheduled outcome.

The gap between a compliance document and a bridge system that actually catches a spoofed position before it becomes a grounding — that gap is where the next incident is already forming.

The Eliza Shoals have been on charts for a very long time.

The ship knew they were there.

It just didn't know where the ship was.

---

*If you found this useful — subscribe, and share it with a colleague in ship design or fleet management. The full article with all sources is linked below.*

*I'm Captain Paul. This is ShipPaulJobs. Maritime 4.0.*

---

## 6. PRODUCTION NOTES

| Item | Detail |
|------|--------|
| Estimated runtime | 9:30 – 10:45 |
| Narration pace | ~145 wpm (professional, measured) |
| Music | Ambient/cinematic — low tempo. No beats. Fade under narration. |
| Visuals | Slides + AIS track footage + maritime B-roll (no talking head needed) |
| Tools (free) | DaVinci Resolve (editing) · Canva (slides) · ElevenLabs or own voice (narration) |
| Captions | Auto-generate in YouTube Studio → review for technical terms |
| Best upload time | Tuesday or Wednesday, 6–8am KST |
| Suggested series tag | Maritime Cyber Brief #001 |
