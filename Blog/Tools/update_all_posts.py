#!/usr/bin/env python3
"""
ShipPaulJobs — Comprehensive Post Updater
------------------------------------------
Per-post operations (all posts in one pass):
  1. Remove top badge-span div from custom dark card header
  2. Update "About the Author" bio with correct author-specific content
  3. Append Field Note section (only for posts defined in FIELD_NOTES)

Run:
  cd ~/VSCode_Project/MaritimeCyber/General/Blog/Tools
  ~/anaconda3/bin/python update_all_posts.py
"""

import os, re, time, json

BLOG_URL         = "https://www.shippauljobs.com"
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE       = "token.json"
DRY_RUN          = False   # Set True to preview without writing

# ── Duplicate guard ───────────────────────────────────────────────────────────
FIELD_NOTE_MARKER = "field-note-section"

# ── Author bios ───────────────────────────────────────────────────────────────
# Key = author.displayName from Blogger API (must match exactly)
AUTHOR_BIOS = {
    "Captain Paul": {
        "name":  "Captain Paul",
        "title": "Founder &amp; Editor-in-Chief · ShipPaulJobs",
        "bio":   ("Senior Manager at a global consulting firm specializing in "
                  "Maritime Cyber Security, AI, and Data Analytics. 17+ years "
                  "spanning shipbuilding R&amp;D, AI product development, and "
                  "maritime cyber compliance. Specializes in IACS UR E26/E27, "
                  "IMO MSC guidelines, and smart ship development. "
                  "Founder of ShipPaulJobs."),
        "photo": "https://github.com/MaritimeCyber/General/blob/main/Asset/img/member/insung.jpeg?raw=true",
        "link":  "https://www.linkedin.com/in/shipjobs/",
    },
    "Blue Horizonist": {
        "name":  "Blue Horizonist",
        "title": "Cybersecurity Consultant · ISP · ISMP",
        "bio":   ("IT/OT Integrated Cybersecurity specialist with expertise in "
                  "IACS UR E26/E27 compliance, N2SF, Cybersecurity Strategy &amp; "
                  "Governance, BPR, and Digital Transformation. Former IT Consultant "
                  "at KPMG (2019–2022). M.S. Information Systems, University of "
                  "Maryland, Robert H. Smith School of Business."),
        "photo": "https://github.com/MaritimeCyber/General/blob/main/Asset/img/member/lew.jpeg?raw=true",
        "link":  "https://www.linkedin.com/in/jiho-jay-%E6%99%BA%E6%99%A7-lew-1b5823364/",
    },
    "Julius Shin": {
        "name":  "Julius Shin",
        "title": "Maritime Technical Consultant · DECK",
        "bio":   ("Maritime Technical Consultant specializing in shipboard "
                  "cybersecurity and compliance across the full ship design and "
                  "build lifecycle. Expertise in cybersecurity architecture, "
                  "governance, maritime cyber policy, and international relations. "
                  "B.S. International Affairs, The George Washington University."),
        "photo": "https://github.com/MaritimeCyber/General/blob/main/Asset/img/member/Julius.jpeg?raw=true",
        "link":  "https://www.linkedin.com/in/shipsecguardian/",
    },
    "Woojin Lee": {
        "name":  "Woojin Lee",
        "title": "Automation Cyber Engineering · Cyber Tech Consultant",
        "bio":   ("Cyber Tech Consultant specializing in IACS UR E26/E27, "
                  "ISO 27001, ISO 27701, ISO 42001, and ISMS/P. Expertise in "
                  "maritime &amp; IoT security, privacy and compliance advisory, "
                  "and global enterprise security frameworks. M.S. Computer "
                  "Software Engineering, Korea University (GPA 4.15)."),
        "photo": "https://github.com/MaritimeCyber/General/blob/main/Asset/img/member/Jin.jpeg?raw=true",
        "link":  "https://www.linkedin.com/in/woojin-lee-87ab812a2/",
    },
    "Yeon": {
        "name":  "Yeon",
        "title": "Maritime / Cybersecurity Consultant · Cloud Security · DevSecOps",
        "bio":   ("Maritime and Cybersecurity Consultant specializing in Cloud "
                  "Security (AWS/GCP/Azure), Zero Trust, Kubernetes, and DevSecOps. "
                  "Microsoft Certified Cybersecurity Architect Expert (SC-100, 2025). "
                  "Expertise in maritime cybersecurity and ship/cloud/development "
                  "security integration."),
        "photo": "https://github.com/MaritimeCyber/General/blob/main/Asset/img/member/Yeon.jpeg?raw=true",
        "link":  "https://www.linkedin.com/in/jiyeonoh/",
    },
    "Changmin": {
        "name":  "Changmin",
        "title": "OT Cyber Security Engineer · Kongsberg Maritime",
        "bio":   ("OT Cyber Security Engineer at Kongsberg Maritime specializing "
                  "in maritime OT system security architecture and Defence in Depth "
                  "strategy for shipboard control systems. Bridges the operational "
                  "demands of vessel automation with cybersecurity requirements of "
                  "IACS UR E26/E27 and modern Classification Society regulations."),
        "photo": "https://github.com/MaritimeCyber/General/blob/main/Asset/img/member/changmin.png?raw=true",
        "link":  "https://www.linkedin.com/in/chang-min-park-2610a380/",
    },
    "Richard": {
        "name":  "Richard",
        "title": "Principal Maritime Engineering Leader · Technical Advisor",
        "bio":   ("Principal maritime engineering leader driving digital ship "
                  "innovation and cybersecurity across ship operations and "
                  "automation. Expertise spanning naval architecture, ICS/OT "
                  "security, offshore system design, vessel automation, "
                  "IACS UR E26/E27, and smart ship &amp; digital twin technologies."),
        "photo": "https://raw.githubusercontent.com/MaritimeCyber/General/refs/heads/main/Asset/img/member/Richard.png",
        "link":  "https://www.shippauljobs.com",
    },
    "Sheep": {
        "name":  "Sheep",
        "title": "Senior Maritime Engineering Lead · Technical Advisor",
        "bio":   ("Senior maritime engineering leader with deep expertise in "
                  "conceptual and basic design across diverse vessel types. "
                  "Brings comprehensive knowledge of global mechanical, electrical "
                  "&amp; electronics, and cybersecurity system onboard "
                  "specifications — with proven project management capability "
                  "for large-scale maritime and offshore platform construction."),
        "photo": "https://raw.githubusercontent.com/MaritimeCyber/General/refs/heads/main/Asset/img/member/Sheep.png",
        "link":  "https://www.shippauljobs.com",
    },
    "Iris": {
        "name":  "Iris",
        "title": "Maritime Engineering Specialist · Technical Advisor",
        "bio":   ("Maritime engineering specialist with deep expertise in detailed "
                  "ship design and engineering drawing analysis. Strong capability "
                  "in mechanical, electrical &amp; electronics, and cybersecurity "
                  "system onboard specification review — spanning pre-design and "
                  "post-design stages, quality inspection, and cross-functional "
                  "communication for large-scale vessel construction projects."),
        "photo": "https://raw.githubusercontent.com/MaritimeCyber/General/refs/heads/main/Asset/img/member/Iris.png",
        "link":  "https://www.shippauljobs.com",
    },
    "Brandon_Ha": {
        "name":  "Brandon Ha",
        "title": "Field Services Engineer &amp; Account Manager · Marine &amp; Offshore · Schneider Electric",
        "bio":   ("Field Services Engineer &amp; Account Manager (Marine &amp; "
                  "Offshore) at Schneider Electric with nearly 8 years of "
                  "hands-on shipboard automation and power systems experience — "
                  "preceded by 9 years as Manager at SPP Shipbuilding and 2+ "
                  "years as Engineer at DESMI. Bridges vendor-side field "
                  "engineering with full shipbuilding lifecycle expertise."),
        "photo": "https://github.com/MaritimeCyber/General/blob/main/Asset/img/member/Brandon%20Ha_w.png?raw=true",
        "link":  "https://www.linkedin.com/in/%EC%8A%B9%EB%AA%A9-brandon-%ED%95%98-ha-b9250099/",
    },
    "The Marine Surveyor": {
        "name":  "The Marine Surveyor",
        "title": "Marine Surveyor · Technical Advisor",
        "bio":   ("Marine surveyor contributing field-based technical perspectives "
                  "on vessel inspection, maritime safety, and compliance engineering. "
                  "Brings hands-on experience across commercial vessel operations "
                  "and survey practice."),
        "photo": "https://raw.githubusercontent.com/MaritimeCyber/General/refs/heads/main/Asset/img/member/Richard.png",
        "link":  "https://www.shippauljobs.com",
    },
}
# Fallback for unknown authors
AUTHOR_BIOS["__default__"] = AUTHOR_BIOS["Captain Paul"]


# ── Field Notes ───────────────────────────────────────────────────────────────
# Loaded from field_notes_data.json (avoids Python string quoting issues with
# em dashes, curly quotes, and multi-line content)
_FN_PATH = os.path.join(os.path.dirname(__file__), "field_notes_data.json")
with open(_FN_PATH, encoding="utf-8") as _fp:
    FIELD_NOTES = json.load(_fp)


# ── Top badge div removal ─────────────────────────────────────────────────────

def remove_top_badge_div(content: str) -> str:
    """
    Remove the flex badge-span div at the top of the dark card header.
    Fingerprint: div style containing both 'gap: 7px' and 'margin-bottom: 18px'
    that contains ONLY <span> elements (no nested <div>).
    """
    pattern = (
        r'<div\s+style="[^"]*gap:\s*7px[^"]*margin-bottom:\s*18px[^"]*">'
        r'\s*(?:<span\b[^>]*>.*?</span>\s*)*'
        r'</div>'
    )
    new_content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
    removed = (len(content) != len(new_content))
    return new_content, removed


# ── Author bio update ─────────────────────────────────────────────────────────

def update_author_bio(content: str, api_author: str) -> str:
    """
    Find the 'About the Author' card in post body and update name, title, bio.
    The card is identified by: color:#0a2342 + font-size:14px + font-weight:800
    in the author name div.
    """
    bio_data = AUTHOR_BIOS.get(api_author, AUTHOR_BIOS["__default__"])

    changed = False

    # 1. Update author name in the bio card (dark-text name div)
    name_pattern = (
        r'(<div\s+style="[^"]*color:\s*#0a2342[^"]*font-size:\s*14px[^"]*'
        r'font-weight:\s*800[^"]*margin-bottom:\s*2px[^"]*"[^>]*>)'
        r'([^<]*)'
        r'(</div>)'
    )
    def replace_name(m):
        nonlocal changed
        if m.group(2).strip() != bio_data["name"]:
            changed = True
        return m.group(1) + bio_data["name"] + m.group(3)
    content = re.sub(name_pattern, replace_name, content, flags=re.DOTALL)

    # 2. Update author title (grey, 11px, margin-bottom:10px)
    title_pattern = (
        r'(<div\s+style="[^"]*color:\s*#6b8599[^"]*font-size:\s*11px[^"]*'
        r'margin-bottom:\s*10px[^"]*"[^>]*>)'
        r'([^<]*)'
        r'(</div>)'
    )
    def replace_title(m):
        nonlocal changed
        if m.group(2).strip() != bio_data["title"]:
            changed = True
        return m.group(1) + bio_data["title"] + m.group(3)
    content = re.sub(title_pattern, replace_title, content, flags=re.DOTALL)

    # 3. Update bio paragraph (grey, 12.5px)
    bio_pattern = (
        r'(<p\s+style="[^"]*color:\s*#6b8599[^"]*font-size:\s*12\.5px[^"]*'
        r'line-height:\s*1\.7[^"]*"[^>]*>)'
        r'(.*?)'
        r'(</p>)'
    )
    def replace_bio(m):
        nonlocal changed
        if m.group(2).strip() != bio_data["bio"]:
            changed = True
        return m.group(1) + bio_data["bio"] + m.group(3)
    content = re.sub(bio_pattern, replace_bio, content, flags=re.DOTALL)

    # 4. Fix photo alt attribute
    photo_alt_pattern = r'(alt=")([^"]*)(")(\s+loading="lazy"\s+src="[^"]*member/)'
    def replace_alt(m):
        nonlocal changed
        if m.group(2) != bio_data["name"]:
            changed = True
        return m.group(1) + bio_data["name"] + m.group(3) + m.group(4)
    content = re.sub(photo_alt_pattern, replace_alt, content)

    # 5. Fix photo src URL (replace any member/ path with correct author photo)
    photo_src_pattern = r'(src=")(https?://[^"]*member/[^"]*?)(")'
    def replace_src(m):
        nonlocal changed
        if m.group(2) != bio_data["photo"]:
            changed = True
        return m.group(1) + bio_data["photo"] + m.group(3)
    content = re.sub(photo_src_pattern, replace_src, content)

    return content, changed


# ── Field Notes HTML builder ──────────────────────────────────────────────────

def build_field_note_html(author: str, note: dict) -> str:
    bullets_html = "\n".join(
        f'            <li style="margin-bottom:8px;">{b}</li>'
        for b in note["bullets"]
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


# ── Auth ──────────────────────────────────────────────────────────────────────

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
    print(f"✅ Blog: {data['name']}  ID: {data['id']}")
    return data["id"]


def get_all_posts(session, blog_id: str):
    """Fetch all live posts (paginated)."""
    posts = []
    page_token = None
    while True:
        params = {
            "maxResults": 500,
            "status":     "live",
            "fields":     "items(id,title,url,content,author),nextPageToken",
        }
        if page_token:
            params["pageToken"] = page_token
        r = session.get(f"{BASE}/blogs/{blog_id}/posts", params=params)
        r.raise_for_status()
        data = r.json()
        posts.extend(data.get("items", []))
        page_token = data.get("nextPageToken")
        if not page_token:
            break
        print(f"  ... {len(posts)} posts fetched so far")
    return posts


def patch_post(session, blog_id: str, post_id: str, body: dict):
    r = session.patch(f"{BASE}/blogs/{blog_id}/posts/{post_id}", json=body)
    r.raise_for_status()
    return r.json()


def url_path(url: str) -> str:
    """Extract path from full URL, e.g. /2026/08/...html"""
    return "/" + "/".join(url.split("/")[3:])


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 65)
    print("ShipPaulJobs — Comprehensive Post Updater")
    print(f"  Mode : {'[DRY RUN]' if DRY_RUN else '[LIVE — writing to Blogger]'}")
    print(f"  Tasks: ① Remove top badge div  ② Fix author bio  ③ Add Field Notes")
    print("=" * 65)

    session = get_session()
    blog_id = get_blog_id(session)

    print("\n📥 Fetching all posts...")
    posts = get_all_posts(session, blog_id)
    print(f"   Total: {len(posts)} posts\n")

    stats = {"badge_removed": 0, "bio_updated": 0, "fn_added": 0, "patched": 0, "skipped": 0, "failed": 0}

    for post in posts:
        post_id  = post["id"]
        title    = post.get("title", "?")
        url      = post.get("url", "")
        content  = post.get("content", "")
        author   = post.get("author", {}).get("displayName", "Captain Paul")
        path     = url_path(url)

        print(f"\n🔗 {path}")
        print(f"   [{post_id}] {title[:60]!r}  (author: {author})")

        original  = content
        modified  = False
        op_notes  = []

        # ── Operation 1: Remove top badge div ──────────────────────────────
        content, badge_removed = remove_top_badge_div(content)
        if badge_removed:
            stats["badge_removed"] += 1
            modified = True
            op_notes.append("✂️ badge div removed")

        # ── Operation 2: Update About the Author bio ────────────────────────
        if "color:#0a2342" in content or "color: #0a2342" in content:
            content, bio_changed = update_author_bio(content, author)
            if bio_changed:
                stats["bio_updated"] += 1
                modified = True
                op_notes.append("👤 author bio updated")

        # ── Operation 3: Append Field Notes ────────────────────────────────
        note = FIELD_NOTES.get(path)
        if note:
            if FIELD_NOTE_MARKER in content:
                op_notes.append("⏭️ field note already present")
            else:
                fn_html  = build_field_note_html(author, note)
                content += fn_html
                stats["fn_added"] += 1
                modified = True
                op_notes.append("📌 field note added")

        # ── Patch ───────────────────────────────────────────────────────────
        print(f"   {' | '.join(op_notes) if op_notes else '— no changes needed'}")

        if modified:
            if DRY_RUN:
                print("   [DRY RUN] would patch")
                stats["patched"] += 1
            else:
                try:
                    patch_post(session, blog_id, post_id, {"content": content})
                    stats["patched"] += 1
                    print("   ✅ patched")
                    time.sleep(0.8)   # respect API rate limit
                except Exception as e:
                    print(f"   ❌ patch failed: {e}")
                    stats["failed"] += 1
        else:
            stats["skipped"] += 1

    print("\n" + "=" * 65)
    print("Summary")
    print(f"  Badge divs removed : {stats['badge_removed']}")
    print(f"  Author bios updated: {stats['bio_updated']}")
    print(f"  Field Notes added  : {stats['fn_added']}")
    print(f"  Posts patched      : {stats['patched']}")
    print(f"  Posts skipped      : {stats['skipped']}")
    print(f"  Failures           : {stats['failed']}")
    print("=" * 65)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
