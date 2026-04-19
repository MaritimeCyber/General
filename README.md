# Maritime Compliance & Cyber Security — Open Resource Hub

> Linked with the blog [Maritime 4.0: Innovation Driven by AI, Data, and Cyber Security](https://shippauljobs.blogspot.com/),
> this repository serves as a collaborative space for researching cyber security compliance in the shipbuilding, maritime, and port industries,
> and for publishing open resources including programs, book reviews, papers, and templates.

---

## Purpose

The modern maritime industry faces cyber security requirements from a wide range of international regulatory bodies including IMO, IACS, and Flag States.
This repository is operated with the following goals:

- Research on cyber security compliance technologies for shipbuilding, maritime, and port sectors (IACS UR E26/E27, IMO MSC-FAL.1/Circ.3, etc.)
- Open-source publication of tools, templates, and guidelines applicable in practice
- Knowledge sharing through book reviews, curated research papers, and R&D notes
- Community-driven development open to researchers, practitioners, and students

---

## Coverage Areas

| Area                           | Description                                                   |
| ------------------------------ | ------------------------------------------------------------- |
| **IACS UR E26 / E27**          | Cyber resilience requirements for ship computer-based systems |
| **IMO Cyber Guidelines**       | MSC-FAL.1/Circ.3, maritime cyber risk management              |
| **OT/IT Security**             | OT/IT security architecture for vessels and shipyards         |
| **Edge AI / R&D**              | Applied AI research (fatigue detection, anomaly detection)    |
| **Smart Shipyard**             | Digital twin and automated system security                    |
| **Ship Cyber Policy**          | Fleet-wide cyber security policy at the shipowner level       |

---

## Repository Structure

```
General/
├── Asset/
│   └── img/
│       ├── common/         # Shared logos and site assets (shipjobs*.png, favicon, etc.)
│       └── member/         # Team member profile images
├── Blog/
│   ├── Backend/            # Live widgets hosted on GitHub, injected into Blogger via gadgets
│   │   ├── Hello_GuestInfo.html                        # Hello Guest widget — IP/geo/OSI layer info
│   │   ├── InjectionCode_Hello.html                    # Blogger gadget: fetches & injects Hello Guest
│   │   ├── ShipOrderTrends.html                        # [Live Feed] Ship order news (RSS aggregator)
│   │   ├── MaritimeCyberNews.html                      # [Live Feed] Maritime cyber threat intel
│   │   ├── InjectionCode_MaritimeCyberIntelligence.html# Blogger gadget: injects MaritimeCyberNews
│   │   └── MaritimeJobsFeed.html                       # [Live Feed] Maritime AI/Data/Cyber jobs feed
│   ├── Main/               # Blog theme & layout widgets
│   │   ├── Main.html                                   # Full Blogger theme XML backup (live theme)
│   │   ├── theme-8002758868633250458.xml               # Theme backup file
│   │   ├── Top/
│   │   │   ├── Header.html                             # Blog header widget
│   │   │   └── InjectionCode_Header.html               # Blogger gadget: injects Header
│   │   └── SideBar/
│   │       ├── Find Us on GitHub.html                  # GitHub repository link widget
│   │       ├── Maritime Cyber ​​Intelligence.html       # Blog intro widget
│   │       ├── Who We Are.html                         # Team introduction widget
│   │       ├── shipjobsIcon.html                       # Blog icon/logo widget
│   │       ├── InjectionCode_Temp.html                 # Generic injection code template
│   │       └── tempplate_Who_am_I.html                 # Author intro article template
│   ├── POST/               # Blog article templates by category
│   │   ├── Books/          # Book review templates (lew series)
│   │   ├── Compliances/    # Compliance article templates + README
│   │   ├── Crew/           # Team intro article
│   │   ├── InsightTrend/   # Insight & trend article templates (Ethan, Yeon, Blue Horizonist)
│   │   ├── Paper/          # Research paper summary templates + README
│   │   └── RND/            # R&D article templates (Edge AI, applied research)
│   └── README.md
└── README.md
```

---

## Folder Guide

### 🖥️ Blog — Blog Widget Assets

`Blog/`

HTML widgets and injection gadgets powering the [Maritime 4.0 blog](https://shippauljobs.blogspot.com/).
Backend widgets are hosted as raw files on GitHub and injected into Blogger via paired `InjectionCode_*.html` gadgets.

**Key Live Feed services (shippauljobs.com):**

| Widget | URL | Description |
| --- | --- | --- |
| **ShipOrderTrends** | [Ship Order Trends](https://www.shippauljobs.com/2026/04/ship-order-trends-provided-by-shipjobs.html) | Global newbuilding ship order news — RSS aggregator (Google News + gCaptain) |
| **MaritimeCyberNews** | [Maritime Cyber Threat Intel](https://www.shippauljobs.com/2026/04/live-feed-maritime-cyber-threat-intel.html) | Ransomware / GPS jamming / port attacks / IMO regulation — Live Feed |
| **MaritimeJobsFeed** | [Maritime Jobs Feed](https://www.shippauljobs.com/2026/04/live-feed-maritime-jobs-feed-ai-data.html) | AI, Data & Cyber career opportunities in maritime — Live Feed |

---

### 📝 Blog/POST — Article Templates

`Blog/POST/`

Article HTML templates organized by type. Each template follows the Maritime 4.0 design system (full inline styles only — no `<style>` block).

| Directory         | Author / Series       | Description                                          |
| ----------------- | --------------------- | ---------------------------------------------------- |
| **Books/**        | Lew                   | Book review templates (lew1 ~ lew3)                  |
| **Compliances/**  | Team                  | Cyber compliance article templates                   |
| **Crew/**         | Team                  | Team introduction article                            |
| **InsightTrend/** | Ethan, Yeon, Blue Horizonist | Insight & trend analysis articles             |
| **Paper/**        | Insung                | Research paper summary templates                     |
| **RND/**          | Ethan                 | R&D / applied research articles (Edge AI, etc.)      |

**Two article style variants:**
- 💡 **Insight**: `Blog/POST/InsightTrend/tempplate_Ethan_Insight.html` — analysis & opinion
- 🔬 **R&D**: `Blog/POST/RND/tempplate_Ethan_RnD.html` — technical research & implementation

---

### 🖼️ Asset/img — Shared Image Assets

`Asset/img/`

| Directory    | Contents                                        |
| ------------ | ----------------------------------------------- |
| **common/**  | Blog logos (`shipjobs*.png`), favicon, UI icons |
| **member/**  | Team member profile images (8 members)          |

---

## Maritime 4.0 Design System

All article templates use **full inline styles only** (no `<style>` block — Blogger strips CSS blocks).

| Element           | Style                                                      |
| ----------------- | ---------------------------------------------------------- |
| Header gradient   | `linear-gradient(135deg,#0a2342,#154f7a,#1a9e82)`          |
| Section bar       | `background:linear-gradient(#0a2342,#154f7a)` 4px wide     |
| Problem/Risk card | `background:#fff8f0;border-left:4px solid #e67e22`         |
| Info/Why card     | `background:#f0f7ff;border-left:4px solid #154f7a`         |
| Conclusion block  | `background:linear-gradient(135deg,#0a2342,#154f7a)`       |
| Live Feed accent  | Cyber: `#ef4444` · Jobs: `#f59e0b` · Orders: `#1a9e82`    |

---

## How to Contribute

This repository is open to anyone interested in maritime cyber security.

1. **Fork** this repository.
2. Create a new branch. (`git checkout -b feature/your-contribution`)
3. Commit your changes. (`git commit -m 'Add: description'`)
4. Push to your branch. (`git push origin feature/your-contribution`)
5. Open a **Pull Request**.

Contributions welcome: book reviews, paper summaries, compliance checklists, risk assessment tools, guide documents, code, translations, and more.

---

## Related Links

- Blog: [Maritime 4.0 — shippauljobs.blogspot.com](https://shippauljobs.blogspot.com/)
- Services: [shippauljobs.com](https://www.shippauljobs.com/)
- Team: [The Crew](https://shippauljobs.blogspot.com/2025/06/the-crew-behind-shipjobs.html)

---

## License

Unless otherwise noted, all materials in this repository are distributed under the **CC BY 4.0** license.
Please credit the source for commercial use.

---

<p align="center">
  <i>Built with passion for safer seas. — Maritime 4.0 Crew</i>
</p>
