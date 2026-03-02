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
- Knowledge sharing through book reviews and curated research papers
- Community-driven development open to researchers, practitioners, and students

---

## Coverage Areas

| Area                           | Description                                                   |
| ------------------------------ | ------------------------------------------------------------- |
| **IACS UR E26 / E27**    | Cyber resilience requirements for ship computer-based systems |
| **IMO Cyber Guidelines** | MSC-FAL.1/Circ.3, maritime cyber risk management              |
| **OT/IT Security**       | OT/OT security architecture for vessels and shipyards         |
| **SCARP**                | Ship Cybersecurity and Resilience Program                     |
| **Smart Shipyard**       | Digital twin and automated system security                    |
| **Ship Cyber Policy**    | Fleet-wide cyber security policy at the shipowner level       |

---

## Repository Structure

```
General/
├── Asset/
│   ├── Books/              # Book reviews and summaries
│   │   ├── img/            # Book cover and reference images
│   │   └── review/         # Individual book review HTML templates
│   ├── Paper/              # Maritime cyber security research papers
│   │   ├── img/            # Paper-related figures and thumbnails
│   │   └── review/         # Individual paper summary HTML templates
│   ├── Compliances/        # Cyber compliance docs & class society guidelines
│   │   └── review/         # Compliance review templates
│   ├── Project/            # SCARP project deliverables and tools
│   ├── theCrew.html        # Team introduction page
│   └── img/
│       ├── common/         # Shared logos and site assets
│       └── member/         # Team member profile images (6 members)
├── Blog/
│   ├── Backend/            # Blog backend widgets (hosted on GitHub, injected via Blogger gadget)
│   │   ├── Hello_GuestInfo.html               # Hello Guest widget — IP/geo/OSI layer info
│   │   ├── InjectionCode_Hello.html           # Blogger gadget: fetches & injects Hello Guest
│   │   ├── ShipOrderTrends.html               # Ship order news widget (RSS aggregator)
│   │   └── InjectionCode_ShipOrderTrends.html # Blogger gadget: fetches & injects ShipOrderTrends
│   ├── Top/                # Blog header area widgets
│   │   ├── Header.html                        # Blog header widget
│   │   └── InjectionCode_Header.html          # Blogger gadget: fetches & injects Header
│   ├── SideBar/            # Blog sidebar widgets (GitHub link, intro, icon)
│   │   ├── Find Us on GitHub.html
│   │   ├── Maritime Cyber Intelligence.html
│   │   ├── Who We Are.html
│   │   ├── shipjobsIcon.html
│   │   └── InjectionCode_Temp.html            # Generic injection code template
│   └── contents/           # Article templates
│       └── tempplate_Who_am_I.html
└── README.md
```

---

## Folder Guide

### 📚 Books — Book Reviews

`Asset/Books/`

Reviews, key summaries, and practical insights on books related to maritime and cyber security.
Review files are stored in `review/`; cover images and reference visuals in `img/`.

- Cyber security fundamentals and advanced topics
- OT/ICS security books
- Books on digital transformation in the maritime and shipbuilding industry

---

### 📄 Paper — Research Papers

`Asset/Paper/`

A curated collection of domestic and international research papers and technical reports on cyber security in the maritime, port, and shipbuilding sectors.
Summary files are stored in `review/`; figures and thumbnails in `img/`.

- Technical reports from IMO, IACS, and classification societies (DNV, LR, BV, ClassNK, etc.)
- Academic journal and conference papers (IEEE, MDPI, etc.)
- Korean academic journals and research institute publications

---

### 🛡️ Compliances — Compliance & Class Society Guidelines

`Asset/Compliances/`

Cyber compliance documents and class society guidelines required in the shipbuilding, maritime, and port sectors, organized by country and organization.

| Category                      | Key Documents                                           |
| ----------------------------- | ------------------------------------------------------- |
| **International (IMO)** | MSC-FAL.1/Circ.3, MSC.428(98)                           |
| **IACS**                | UR E26, UR E27, Rec. 166                                |
| **DNV**                 | DNV-RP-0496, DNV CPS                                    |
| **Lloyd's Register**    | LR Cyber Enabled Ships Rules                            |
| **ClassNK**             | ClassNK Cyber Security Guidelines                       |
| **Bureau Veritas**      | BV NR659                                                |
| **USA**                 | USCG Cyber Strategy, NIST SP 800-82                     |
| **Europe (EU)**         | NIS2 Directive, ENISA Maritime Guidelines               |
| **Korea**               | MOF Guidelines, KR Class Society Guidelines             |
| **Port Security**       | ISPS Code cyber application, Port OT security standards |

---

### 🔧 Project — Projects

`Asset/Project/`

Practical deliverables open to the public, including compliance tools, checklist templates, and risk assessment utilities.

---

### 🖥️ Blog — Blog Widget Assets

`Blog/`

HTML widgets and injection gadgets powering the [Maritime 4.0 blog](https://shippauljobs.blogspot.com/).
Widgets are hosted as raw files on GitHub and injected into Blogger via paired `InjectionCode_*.html` gadgets.

| Directory     | Description                                                                                     |
| ------------- | ----------------------------------------------------------------------------------------------- |
| **Backend/**  | Main widget logic files + Blogger injection gadgets                                             |
| **Top/**      | Blog header area widget + injection gadget                                                      |
| **SideBar/**  | Sidebar widgets (GitHub link, team intro, logo icon)                                            |
| **contents/** | Blog post article templates                                                                     |

**Key widgets:**

- **Hello_GuestInfo** — Greets visitors with localized language, IP geo-info, device/referrer details, and a full OSI 7-layer / PDU stack view (client-side). Supports 19 languages.
- **ShipOrderTrends** — Aggregates maritime RSS news (Google News + gCaptain) with category filtering (Tanker / Container / LNG / Bulk / Car) and 30-minute localStorage caching.

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
- Team: [The Crew] (Asset/theCrew.html) , https://shippauljobs.blogspot.com/2025/06/the-crew-behind-shipjobs.html

---

## License

Unless otherwise noted, all materials in this repository are distributed under the **CC BY 4.0** license.
Please credit the source for commercial use.

---

<p align="center">
  <i>Built with passion for safer seas. — Maritime 4.0 Crew</i>
</p>
