# Blog — Maritime 4.0 Blog Assets

This directory contains HTML widgets and gadgets used in the
[Maritime 4.0: Innovation Driven by AI, Data, and Cyber Security](https://shippauljobs.blogspot.com/) blog.

## Structure

```
Blog/
├── Backend/                                        # Backend widgets hosted on GitHub
│   ├── Hello_GuestInfo.html                        # Hello Guest widget (main logic)
│   ├── InjectionCode_Hello.html                    # Blogger gadget: fetches & injects Hello Guest
│   ├── ShipOrderTrends.html                        # Ship order news widget (RSS aggregator)
│   └── InjectionCode_ShipOrderTrends.html          # Blogger gadget: fetches & injects ShipOrderTrends
├── Top/                                            # Blog header area widgets
│   ├── Header.html                                 # Blog header widget
│   └── InjectionCode_Header.html                   # Blogger gadget: fetches & injects Header
├── SideBar/                                        # Sidebar widgets for the blog
│   ├── Find Us on GitHub.html                      # GitHub repository link widget
│   ├── Maritime Cyber Intelligence.html            # Blog introduction widget
│   ├── Who We Are.html                             # Team introduction widget
│   ├── shipjobsIcon.html                           # Blog icon/logo widget
│   └── InjectionCode_Temp.html                     # Generic injection code template
└── contents/                                       # Article layout templates
    └── tempplate_Who_am_I.html                     # Author introduction article template
```

## Widget Architecture

Backend widgets follow a two-file pattern:

| File | Role |
|------|------|
| `*.html` (e.g. `Hello_GuestInfo.html`) | Full widget logic — HTML + CSS + JS. Hosted as a raw GitHub file. |
| `InjectionCode_*.html` | Blogger gadget pasted into Layout. Fetches the raw file via `fetch()` and injects it into the DOM, re-executing `<script>` tags manually (required because `innerHTML` blocks script execution). |

### Key Widgets

**Hello_GuestInfo** (`Backend/Hello_GuestInfo.html`)
- Greets visitors in their native language (19 languages supported)
- Displays IP geo-info: country flag, ISP, local time, currency, dial code, network type
- Shows device info (OS, browser, resolution) and referrer source
- Renders a full OSI 7-layer / PDU stack view using client-side detection
- Uses `ipapi.co` API with 30-minute `localStorage` cache

**ShipOrderTrends** (`Backend/ShipOrderTrends.html`)
- Aggregates maritime RSS feeds: Google News (×2 queries) + gCaptain
- Parallel fetch via `rss2json` and `allorigins` (race pattern — fastest wins)
- Category tabs: All / Tanker / Container / LNG / Bulk / Car
- 30-minute `localStorage` cache; Refresh button for live fetch

## Usage

### Backend widgets (Backend/ and Top/)
1. The `InjectionCode_*.html` gadget is pasted into Blogger → **Layout → Add a Gadget → HTML/JavaScript**.
2. It fetches the corresponding `*.html` from the GitHub raw URL at runtime.
3. No manual copy-paste needed for the main widget file — push to GitHub and it updates live.

### Sidebar widgets (SideBar/)
1. Open the target `.html` file.
2. Copy the full content.
3. In Blogger, navigate to **Layout → Add a Gadget → HTML/JavaScript**.
4. Paste and save.

### Article templates (contents/)
1. Open the template `.html` file.
2. Copy the content and paste into the Blogger post editor in HTML view.
3. Fill in the article-specific fields and publish.

> Back to [Repository Root](../README.md)
