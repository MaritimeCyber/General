#!/usr/bin/env python3
"""
ShipPaulJobs — Add Internal Links (Related Articles)
------------------------------------------------------
Appends a "Related Articles" section to each of the 32 target posts.
Related posts are pre-assigned by topic cluster; author name is pulled live
from the post's author.displayName.

Clusters:
  1. E26 vs E27 개관/FAQ
  2. After Mandate ①–⑥ series
  3. ZCD series
  4. Compliance / Audit / Survey series
"""

import os

BLOG_URL         = "https://www.shippauljobs.com"
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE       = "token.json"
DRY_RUN          = False

RELATED_MARKER = "related-articles-section"

# ── Post title registry ──────────────────────────────────────────────────────
# path → display title  (used to build the anchor text in related links)
TITLES = {
    # Hub
    "/2026/08/iacs-ur-e26-vs-e27-complete-comparison.html":
        "IACS UR E26 vs E27: The Complete Comparison",
    # Cluster 1
    "/2026/08/iacs-ur-e26-complete-guide-to-cyber.html":
        "IACS UR E26: Complete Guide to Cyber Resilience",
    "/2026/08/ur-e27-response-strategies-for-marine.html":
        "UR E27 Response Strategies for Marine Equipment Manufacturers",
    "/2026/08/ur-e27-supplier-readiness-series-from.html":
        "UR E27 Supplier Readiness: From Reactive to Structured",
    "/2026/07/iacs-ur-e27-asks-you-to-prove-up-to-41.html":
        "IACS UR E27: 41 Security Capabilities — None Inspect the Model",
    "/2026/07/if-we-already-have-e27-certificate-why.html":
        "E27 Certificate in Hand — Why Is FAT Verification Still Required?",
    "/2026/07/if-it-is-out-of-scope-your-e26.html":
        "If IT Is Out of Scope, Your E26 Compliance Is Incomplete",
    "/2026/08/if-csdd-is-rushed-during-construction.html":
        "If CSDD Is Rushed During Construction, SCARP Falls Apart After Delivery",
    # Cluster 2
    "/2026/06/ur-e26-after-mandate-one-mandatory-rule.html":
        "UR E26, After the Mandate ① — One Mandatory Rule, Five Perspectives",
    "/2026/07/ur-e26-after-mandate-owners-view-where.html":
        "UR E26, After the Mandate ② — The Owner's View",
    "/2026/07/ur-e26-after-mandate-through-eyes-of.html":
        "UR E26, After the Mandate ③ — Through the Eyes of the Classification Society",
    "/2026/07/ur-e26-after-mandate-shipyards-view.html":
        "UR E26, After the Mandate ④ — The Shipyard's View",
    "/2026/07/ur-e26-after-mandate-vendors-view.html":
        "UR E26, After the Mandate ⑤ — The Vendor's View",
    "/2026/07/ur-e26-after-mandate-consultants-view.html":
        "UR E26, After the Mandate ⑥ — The Consultant's View",
    # Cluster 3
    "/2026/07/e26-zone-defense-learn-iacs-ur-e26-as.html":
        "E26 Zone Defense — Learn IACS UR E26 as a Tower Defense Game",
    "/2026/07/ship-zcd-anatomy-building-blocks-iacs-ur-e26.html":
        "Anatomy of a Ship ZCD: Building Blocks of IACS UR E26 Zone Design",
    "/2026/07/ship-zcd-failures-iacs-ur-e26-e27-seven-mistakes.html":
        "Why Most Ship ZCDs Fail: Seven Mistakes That Derail IACS Compliance",
    "/2026/07/ship-zcd-documentation-zone-conduit-diagram-iacs-ur-e26.html":
        "Ship ZCD Documentation: From Network Diagrams to Zone-Conduit Diagrams",
    "/2026/07/zone-conduit-vlan-purdue-model-ship-iacs-ur-e26.html":
        "Zone Before VLAN: Why the Purdue Model Needs Rethinking for Ship OT",
    "/2026/07/ship-ot-network-design-iacs-ur-e26-e27.html":
        "Ship OT Network Design for IACS UR E26/E27: From Cable to Cyber Resilience",
    # Cluster 4
    "/2026/07/iacs-ur-e26-compliance-series-17-cyber.html":
        "IACS UR E26 Compliance Series — The Six Core Ship-Level Deliverables",
    "/2026/06/iacs-ur-e26e27-compliance-matrix.html":
        "IACS E26/E27 Compliance Matrix: Maritime OT Cybersecurity Solutions",
    "/2026/03/iacs-ur-e27-tasoc-supplier.html":
        "IACS UR E27: TASOC and Supplier Security Obligations",
    "/2026/03/iacs-ur-e26e27-cybersecurity-on.html":
        "IACS UR E26/E27: Cybersecurity Requirements for Ships",
    "/2026/03/iacs-ur-e26e27-audits-what.html":
        "IACS UR E26/E27 Audits: What to Expect and How to Prepare",
    "/2026/03/automating-iacs-e26e27-annual-survey.html":
        "Automating IACS E26/E27 Annual Survey: What OT Monitoring Can and Cannot Do",
    "/2026/03/ship-ot-monitoring-for-iacs-e26e27.html":
        "Ship OT Monitoring for IACS E26/E27: Required Functions, Scope, and Protocols",
    "/2026/06/ship-ot-cybersecurity-iacs-e26e27.html":
        "IACS E26/E27 Compliance Guide: What Ship OT/IT Engineers Need to Know",
    "/2026/04/iacs-ur-e26e27-patching-version-control.html":
        "IACS UR E26/E27: Patching and Version Control for Ship OT Systems",
    "/2025/01/required-documents-for-iacs-ur-e27.html":
        "Required Documents for IACS UR E27 Compliance",
    "/2024/09/iacs-ur-classnk-guidelines-based.html":
        "IACS UR E26/E27 and ClassNK Guidelines: A Practical Overview",
    "/2026/06/e26-deliverable-quality-low-medium-and.html":
        "E26 Deliverable Quality — The Low, Medium, and High Tiers",
}

HUB = "/2026/08/iacs-ur-e26-vs-e27-complete-comparison.html"

# ── Related post assignments ─────────────────────────────────────────────────
# Each entry: path → [path1, path2, hub_path]
# (2 cluster peers + hub; hub entries get 3 cluster peers instead)

RELATED = {
    # ── Hub ──
    HUB: [
        "/2026/08/iacs-ur-e26-complete-guide-to-cyber.html",
        "/2026/07/if-it-is-out-of-scope-your-e26.html",
        "/2026/08/if-csdd-is-rushed-during-construction.html",
    ],

    # ── Cluster 1: E26 vs E27 개관/FAQ ──
    "/2026/08/iacs-ur-e26-complete-guide-to-cyber.html": [
        "/2026/07/if-it-is-out-of-scope-your-e26.html",
        "/2026/08/ur-e27-response-strategies-for-marine.html",
        HUB,
    ],
    "/2026/08/ur-e27-response-strategies-for-marine.html": [
        "/2026/08/ur-e27-supplier-readiness-series-from.html",
        "/2026/07/iacs-ur-e27-asks-you-to-prove-up-to-41.html",
        HUB,
    ],
    "/2026/08/ur-e27-supplier-readiness-series-from.html": [
        "/2026/08/ur-e27-response-strategies-for-marine.html",
        "/2026/07/if-we-already-have-e27-certificate-why.html",
        HUB,
    ],
    "/2026/07/iacs-ur-e27-asks-you-to-prove-up-to-41.html": [
        "/2026/07/if-we-already-have-e27-certificate-why.html",
        "/2026/08/ur-e27-supplier-readiness-series-from.html",
        HUB,
    ],
    "/2026/07/if-we-already-have-e27-certificate-why.html": [
        "/2026/07/iacs-ur-e27-asks-you-to-prove-up-to-41.html",
        "/2026/07/if-it-is-out-of-scope-your-e26.html",
        HUB,
    ],
    "/2026/07/if-it-is-out-of-scope-your-e26.html": [
        "/2026/07/if-we-already-have-e27-certificate-why.html",
        "/2026/08/if-csdd-is-rushed-during-construction.html",
        HUB,
    ],
    "/2026/08/if-csdd-is-rushed-during-construction.html": [
        "/2026/07/if-it-is-out-of-scope-your-e26.html",
        "/2026/08/ur-e27-response-strategies-for-marine.html",
        HUB,
    ],

    # ── Cluster 2: After Mandate ①–⑥ ──
    "/2026/06/ur-e26-after-mandate-one-mandatory-rule.html": [
        "/2026/07/ur-e26-after-mandate-owners-view-where.html",
        "/2026/07/ur-e26-after-mandate-through-eyes-of.html",
        HUB,
    ],
    "/2026/07/ur-e26-after-mandate-owners-view-where.html": [
        "/2026/06/ur-e26-after-mandate-one-mandatory-rule.html",
        "/2026/07/ur-e26-after-mandate-through-eyes-of.html",
        HUB,
    ],
    "/2026/07/ur-e26-after-mandate-through-eyes-of.html": [
        "/2026/07/ur-e26-after-mandate-owners-view-where.html",
        "/2026/07/ur-e26-after-mandate-shipyards-view.html",
        HUB,
    ],
    "/2026/07/ur-e26-after-mandate-shipyards-view.html": [
        "/2026/07/ur-e26-after-mandate-through-eyes-of.html",
        "/2026/07/ur-e26-after-mandate-vendors-view.html",
        HUB,
    ],
    "/2026/07/ur-e26-after-mandate-vendors-view.html": [
        "/2026/07/ur-e26-after-mandate-shipyards-view.html",
        "/2026/07/ur-e26-after-mandate-consultants-view.html",
        HUB,
    ],
    "/2026/07/ur-e26-after-mandate-consultants-view.html": [
        "/2026/07/ur-e26-after-mandate-vendors-view.html",
        "/2026/07/ur-e26-after-mandate-shipyards-view.html",
        HUB,
    ],

    # ── Cluster 3: ZCD series ──
    "/2026/07/e26-zone-defense-learn-iacs-ur-e26-as.html": [
        "/2026/07/ship-zcd-anatomy-building-blocks-iacs-ur-e26.html",
        "/2026/07/ship-zcd-failures-iacs-ur-e26-e27-seven-mistakes.html",
        HUB,
    ],
    "/2026/07/ship-zcd-anatomy-building-blocks-iacs-ur-e26.html": [
        "/2026/07/e26-zone-defense-learn-iacs-ur-e26-as.html",
        "/2026/07/ship-zcd-failures-iacs-ur-e26-e27-seven-mistakes.html",
        HUB,
    ],
    "/2026/07/ship-zcd-failures-iacs-ur-e26-e27-seven-mistakes.html": [
        "/2026/07/ship-zcd-documentation-zone-conduit-diagram-iacs-ur-e26.html",
        "/2026/07/ship-zcd-anatomy-building-blocks-iacs-ur-e26.html",
        HUB,
    ],
    "/2026/07/ship-zcd-documentation-zone-conduit-diagram-iacs-ur-e26.html": [
        "/2026/07/ship-zcd-failures-iacs-ur-e26-e27-seven-mistakes.html",
        "/2026/07/zone-conduit-vlan-purdue-model-ship-iacs-ur-e26.html",
        HUB,
    ],
    "/2026/07/zone-conduit-vlan-purdue-model-ship-iacs-ur-e26.html": [
        "/2026/07/ship-zcd-documentation-zone-conduit-diagram-iacs-ur-e26.html",
        "/2026/07/ship-ot-network-design-iacs-ur-e26-e27.html",
        HUB,
    ],
    "/2026/07/ship-ot-network-design-iacs-ur-e26-e27.html": [
        "/2026/07/zone-conduit-vlan-purdue-model-ship-iacs-ur-e26.html",
        "/2026/07/ship-zcd-documentation-zone-conduit-diagram-iacs-ur-e26.html",
        HUB,
    ],

    # ── Cluster 4: Compliance / Audit / Survey ──
    "/2026/07/iacs-ur-e26-compliance-series-17-cyber.html": [
        "/2026/06/e26-deliverable-quality-low-medium-and.html",
        "/2026/06/iacs-ur-e26e27-compliance-matrix.html",
        HUB,
    ],
    "/2026/06/iacs-ur-e26e27-compliance-matrix.html": [
        "/2026/07/iacs-ur-e26-compliance-series-17-cyber.html",
        "/2026/06/e26-deliverable-quality-low-medium-and.html",
        HUB,
    ],
    "/2026/03/iacs-ur-e27-tasoc-supplier.html": [
        "/2025/01/required-documents-for-iacs-ur-e27.html",
        "/2026/03/iacs-ur-e26e27-audits-what.html",
        HUB,
    ],
    "/2026/03/iacs-ur-e26e27-cybersecurity-on.html": [
        "/2026/06/ship-ot-cybersecurity-iacs-e26e27.html",
        "/2026/07/iacs-ur-e26-compliance-series-17-cyber.html",
        HUB,
    ],
    "/2026/03/iacs-ur-e26e27-audits-what.html": [
        "/2026/03/automating-iacs-e26e27-annual-survey.html",
        "/2026/03/iacs-ur-e26e27-cybersecurity-on.html",
        HUB,
    ],
    "/2026/03/automating-iacs-e26e27-annual-survey.html": [
        "/2026/03/ship-ot-monitoring-for-iacs-e26e27.html",
        "/2026/03/iacs-ur-e26e27-audits-what.html",
        HUB,
    ],
    "/2026/03/ship-ot-monitoring-for-iacs-e26e27.html": [
        "/2026/03/automating-iacs-e26e27-annual-survey.html",
        "/2026/06/ship-ot-cybersecurity-iacs-e26e27.html",
        HUB,
    ],
    "/2026/06/ship-ot-cybersecurity-iacs-e26e27.html": [
        "/2026/03/ship-ot-monitoring-for-iacs-e26e27.html",
        "/2026/06/iacs-ur-e26e27-compliance-matrix.html",
        HUB,
    ],
    "/2026/04/iacs-ur-e26e27-patching-version-control.html": [
        "/2026/06/ship-ot-cybersecurity-iacs-e26e27.html",
        "/2026/03/iacs-ur-e26e27-audits-what.html",
        HUB,
    ],
    "/2025/01/required-documents-for-iacs-ur-e27.html": [
        "/2026/03/iacs-ur-e27-tasoc-supplier.html",
        "/2026/07/iacs-ur-e26-compliance-series-17-cyber.html",
        HUB,
    ],
    "/2024/09/iacs-ur-classnk-guidelines-based.html": [
        "/2026/06/iacs-ur-e26e27-compliance-matrix.html",
        "/2025/01/required-documents-for-iacs-ur-e27.html",
        HUB,
    ],
    "/2026/06/e26-deliverable-quality-low-medium-and.html": [
        "/2026/07/iacs-ur-e26-compliance-series-17-cyber.html",
        "/2026/03/iacs-ur-e26e27-audits-what.html",
        HUB,
    ],
}


# ── HTML builder ─────────────────────────────────────────────────────────────

def build_related_html(path: str) -> str:
    related_paths = RELATED.get(path, [])
    if not related_paths:
        return ""

    items_html = "\n".join(
        f'      <li style="margin-bottom:10px;">'
        f'<a href="{BLOG_URL}{p}" style="color:#1a73e8;text-decoration:none;">'
        f'{TITLES.get(p, p)}</a></li>'
        for p in related_paths
    )

    return f"""
<div id="{RELATED_MARKER}" style="border-top:2px solid #e8eaed;padding:28px 0 8px;margin:40px 0 0;">
  <p style="margin:0 0 14px;font-weight:700;font-size:13px;letter-spacing:1px;text-transform:uppercase;color:#5f6368;">Related Articles</p>
  <ul style="list-style:none;margin:0;padding:0;font-size:15px;line-height:1.6;">
{items_html}
  </ul>
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
    print(f"  ⚠️  getByPath failed: {r.status_code} {r.text[:100]}")
    return None


def patch_post(session, blog_id: str, post_id: str, body: dict):
    r = session.patch(f"{BASE}/blogs/{blog_id}/posts/{post_id}", json=body)
    r.raise_for_status()
    return r.json()


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("ShipPaulJobs — Add Internal Links (Related Articles)")
    print(f"{'[DRY RUN]' if DRY_RUN else '[LIVE] actual update'}")
    print(f"Target posts: {len(RELATED)}")
    print("=" * 60)

    session = get_session()
    blog_id = get_blog_id(session)

    updated = skipped = failed = 0

    for path in RELATED:
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

        print(f"  📄 [{post_id}] {title!r}")

        if RELATED_MARKER in content:
            print("  ✅ Related Articles already present, skipping")
            skipped += 1
            continue

        related_html = build_related_html(path)
        if not related_html:
            print("  ⚠️  No related posts defined, skipping")
            skipped += 1
            continue

        new_content = content + related_html

        if DRY_RUN:
            links = RELATED[path]
            print(f"  [DRY RUN] would add {len(links)} links:")
            for p in links:
                print(f"    → {TITLES.get(p, p)}")
            updated += 1
            continue

        try:
            patch_post(session, blog_id, post_id, {"content": new_content})
            print(f"  ✅ Added {len(RELATED[path])} related links")
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
