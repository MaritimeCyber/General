
  (function () {
    "use strict";

    /* Blogger's public summary feed does NOT return a clean auto-summary —
       e.summary.$t is just the first ~400 raw characters of the post's
       HTML source, truncated mid-tag or mid comment-marker. Every article
       in this repo opens with a long boxed "Article: ..." HTML comment
       header, so that raw slice is usually mostly (or entirely) that
       header, sometimes cut off partway through it. Strip fully-closed
       comment blocks, then any comment left open by the truncation, then
       any remaining tags. Each pattern spells the comment open/close
       markers with an escaped hyphen between the two dashes so the
       literal marker text never appears contiguously in this inline
       script block's source (that text appearing in script data can push
       an HTML parser into its "script data escaped" state per HTML5). */
    function cleanSummary(s) {
      return (s || "")
        .replace(/<!\-\-[\s\S]*?\-\->/g, " ")
        .replace(/<!\-\-[\s\S]*$/, " ")
        .replace(/<[^>]+>/g, " ")
        .replace(/&nbsp;/g, " ")
        .replace(/\s+/g, " ")
        .trim();
    }

    var LABEL = "Publications";
    var FEED_BASE = "https://www.shippauljobs.com/feeds/posts/summary/-/" + encodeURIComponent(LABEL) + "?alt=json";
    /* Additional labels whose posts are merged in (deduplicated by URL).
       "SERIES" posts that don't also carry the "Publications" label would
       otherwise never be fetched — they must be pulled separately so
       buildGroups() can place them in the "Completed Series" bucket. */
    var EXTRA_FEED_LABELS = ["SERIES"];
    /* Versioned so that adding fields to mapEntry() (author/comments/labels)
       automatically invalidates any visitor's stale cached items instead of
       rendering "undefined" for the new fields — same pattern as apl_cache_v5
       in Main.html's Explore All Posts widget. */
    var CACHE_KEY = "pub_cache_v1"; /* was "mcp_cache_v1" — collided with Maritime Compliance.html's cache key (both localStorage-based, same origin), and could also have cached a truncated (45-post) result from the pagination bug */
    var CACHE_TTL = 30 * 60 * 1000;
    var VIEW_NS = "shippauljobs-views"; /* shared sitewide counter — same namespace the other MAIN MENU hub pages use */
    var MONTHS_SHORT = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    var RANK_CANDIDATE_POOL = 40; /* Compare view counts only among the N most recent posts (limits API call volume) */
    var RANK_SHOW = 6;
    var pubSortMode = "alpha"; /* 'alpha' = A-Z (default) | 'count' = most posts first */

    var allItems = [];
    var periodMode = 'recent50';
    function filterByPeriod(items) {
      var sorted = items.slice().sort(function(a,b){ return new Date(b.published).getTime() - new Date(a.published).getTime(); });
      if (periodMode === 'recent50') return sorted.slice(0, 50);
      if (periodMode === 'all') return items;
      var days = {'1m':30,'3m':90,'6m':180,'1y':365}[periodMode]||999999;
      var cutoff = new Date(Date.now() - days*86400000);
      return sorted.filter(function(p){ return new Date(p.published) >= cutoff; });
    }

    /* "✓ Read" badge state — reads the same site-wide "spj_read" localStorage
       set that Main.html's global read-tracker script writes to on every
       post visit (matching #apl-cards' own readSet/normUrl pattern). This
       card only reads it, never writes it. */
    var readSet = {};
    function normUrl(u) {
      return (u || "").split("?")[0].split("#")[0].replace(/\/+$/, "");
    }
    function refreshReadSet() {
      try {
        readSet = JSON.parse(localStorage.getItem("spj_read") || "{}");
      } catch (e) {
        readSet = {};
      }
    }

    /*── Cache ──*/
    function loadCache() {
      try {
        var r = localStorage.getItem(CACHE_KEY);
        if (!r) return null;
        var o = JSON.parse(r);
        if (!o || !o.items || Date.now() - o.ts > CACHE_TTL) return null;
        return o.items;
      } catch (e) {
        return null;
      }
    }
    function saveCache(items) {
      try {
        localStorage.setItem(CACHE_KEY, JSON.stringify({ ts: Date.now(), items: items }));
      } catch (e) {}
    }

    /*── Feed fetch (paginated) ──*/
    /* Blogger serves images (post thumbnails, author avatars) in two different
       URL shapes, and the size token needs to be swapped differently for each:
         1) path-segment: .../s72-w629-h285-c/filename.png  (older blogspot host)
         2) query-suffix: ...AVvXsE...=s72-c                (blogger.googleusercontent.com/img/a/…)
       A naive "/s72-c/" regex matches neither real-world shape above — images
       would silently stay at their original tiny size (hence the blur).
       background-size:cover on the target box handles the final crop-to-box
       regardless of the exact source ratio, so any wide/tall token works. */
    function upsizeGoogleImg(url, token) {
      if (!url) return url;
      if (/\/s\d+(-w\d+-h\d+)?(-c)?\//.test(url)) {
        return url.replace(/\/s\d+(-w\d+-h\d+)?(-c)?\//, "/" + token + "/");
      }
      if (/=s\d+(-w\d+-h\d+)?(-c)?$/.test(url)) {
        return url.replace(/=s\d+(-w\d+-h\d+)?(-c)?$/, "=" + token);
      }
      return url;
    }

    function mapEntry(e) {
      var link = "#";
      (e.link || []).forEach(function (l) {
        if (l.rel === "alternate") link = l.href;
      });
      var thumb = null;
      if (e.media$thumbnail && e.media$thumbnail.url) {
        /* ~3x the card's rendered box (260–440px wide × 120px tall) so it
           stays sharp even on 3x-density retina displays. */
        thumb = upsizeGoogleImg(e.media$thumbnail.url, "w1080-h500");
      }
      var summary = "";
      if (e.summary && e.summary.$t) {
        summary = cleanSummary(e.summary.$t).slice(0, 130);
      }
      var authorEntry = e.author && e.author[0];
      var author = (authorEntry && authorEntry.name && authorEntry.name.$t) || "";
      var authorImgRaw = (authorEntry && authorEntry["gd$image"] && authorEntry["gd$image"].src) || "";
      var authorImg = authorImgRaw ? upsizeGoogleImg(authorImgRaw, "s80-c") : "";
      var comments = e["thr$total"] ? parseInt(e["thr$total"].$t, 10) || 0 : 0;
      var labels = (e.category || []).map(function (c) { return c.term; });
      return {
        title: (e.title && e.title.$t) || "(untitled)",
        link: link,
        published: (e.published && e.published.$t) || "",
        summary: summary,
        thumb: thumb,
        author: author,
        authorImg: authorImg,
        comments: comments,
        labels: labels,
      };
    }

    function fetchLabel(feedUrl, cb) {
      var collected = [];
      function page(start) {
        fetch(feedUrl + "&max-results=150&start-index=" + start)
          .then(function (r) { return r.json(); })
          .then(function (d) {
            var entries = (d.feed && d.feed.entry) || [];
            entries.forEach(function (e) { collected.push(mapEntry(e)); });
            if (entries.length > 0 && start < 1500) {
              page(start + entries.length);
            } else {
              cb(collected);
            }
          })
          .catch(function () { cb(collected); });
      }
      page(1);
    }

    function fetchAllPosts(cb) {
      /* Fetch the primary label + each extra label, then merge & deduplicate
         by post URL so the same post is never shown twice. */
      var feeds = [FEED_BASE].concat(EXTRA_FEED_LABELS.map(function (l) {
        return "https://www.shippauljobs.com/feeds/posts/summary/-/" + encodeURIComponent(l) + "?alt=json";
      }));
      var results = [];
      var done = 0;
      feeds.forEach(function (url) {
        fetchLabel(url, function (items) {
          results = results.concat(items);
          done++;
          if (done === feeds.length) {
            var seen = {};
            var merged = [];
            results.forEach(function (p) {
              if (!seen[p.link]) { seen[p.link] = true; merged.push(p); }
            });
            cb(merged);
          }
        });
      });
    }

    /*── Grouping: only these two topic tags form groups — every other label
         a post carries is ignored for grouping purposes (still shown in the
         card's own tag chips, just not used to bucket it). A post with
         neither tag doesn't appear in the archive section at all (it can
         still surface in Top Ranked, which reads allItems directly). A post
         with both appears in both groups. ──*/
    var GROUP_MAP = [
      { name: "Book Reviews",      labels: ["Knowledge Resources"] },
      { name: "Paper Reviews",     labels: ["Research Papers & Studies"] },
      { name: "Completed Series",  labels: ["SERIES","Completed Series"] },
      { name: "Leadership Series", labels: ["Leadership","Leadership Series"] }
    ];
    function buildGroups(items) {
      var labelToGroup = {};
      GROUP_MAP.forEach(function(g) {
        g.labels.forEach(function(l) { labelToGroup[l] = g.name; });
      });
      var groups = {};
      GROUP_MAP.forEach(function(g) { groups[g.name] = []; });
      items.forEach(function(p) {
        var matched = {};
        (p.labels || []).forEach(function(l) {
          var gname = labelToGroup[l];
          if (gname && !matched[gname]) { matched[gname] = true; groups[gname].push(p); }
        });
      });
      return groups;
    }

    function slugTag(t) {
      return (t || "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "") || "tag";
    }

    function fmtCardDate(ds) {
      var d = new Date(ds);
      if (isNaN(d.getTime())) return "—";
      return MONTHS_SHORT[d.getMonth()] + " " + d.getDate();
    }

    function escAttr(s) {
      return (s || "").replace(/"/g, "&quot;").replace(/</g, "&lt;");
    }
    function escHTML(s) {
      return (s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }

    /*── Verification badge (Verified / Expert Reviewed / Industry Validated),
         same priority order and policy link as the theme's own spjBadge()
         helpers in Main.html. ──*/
    var VERIFY_BADGES = [
      { name: "Industry Validated", cls: "spj-badge-l3", title: "Industry Validated — Shipyard / Class / Supplier Feedback" },
      { name: "Expert Reviewed", cls: "spj-badge-l2", title: "Expert Reviewed — Technical Advisory Board" },
      { name: "Verified", cls: "spj-badge-l1", title: "Verified — Editorial Team Review" },
    ];
    /* Rendered as a span element (not an anchor) because every call site
       nests this inside an outer card/row link — a real nested anchor
       would be invalid HTML and browsers would mangle the outer link's
       clickable area.
       Clicking still opens the policy page, just via JS instead of a
       native href, with stopPropagation so it doesn't also trigger the
       outer card's own navigation. */
    function verifyBadgeHTML(labels, extraClass) {
      if (!labels || !labels.length) return "";
      var POLICY_URL = "https://www.shippauljobs.com/p/editorial-verification-policy.html";
      for (var i = 0; i < VERIFY_BADGES.length; i++) {
        var b = VERIFY_BADGES[i];
        if (labels.indexOf(b.name) !== -1) {
          return (
            '<span class="spj-badge ' + b.cls + (extraClass ? " " + extraClass : "") + '" ' +
            'onclick="event.preventDefault();event.stopPropagation();window.open(\'' + POLICY_URL + '\',\'_blank\',\'noopener\');" ' +
            'role="link" style="cursor:pointer" tabindex="0" title="' + escAttr(b.title) + '">' +
            '<img alt="SPJ Verified" loading="lazy" src="https://raw.githubusercontent.com/MaritimeCyber/General/main/Asset/img/common/shipjobs2.png" />' +
            "</span>"
          );
        }
      }
      return "";
    }

    /*── Card markup — thumb + title/desc + footer (date · share button) ──*/
    var SHARE_SVG =
      '<svg fill="none" height="12" stroke="white" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.4" viewBox="0 0 24 24" width="12">' +
      '<circle cx="18" cy="5" r="3"></circle><circle cx="6" cy="12" r="3"></circle><circle cx="18" cy="19" r="3"></circle>' +
      '<line x1="8.59" x2="15.42" y1="13.51" y2="17.49"></line><line x1="15.41" x2="8.59" y1="6.51" y2="10.49"></line></svg>';

    /*── Share panel — same visual/behavior as the main page's card share
         button (scsShareCard/ms-track), reimplemented locally because the
         theme only defines window.scsShareCard inside a
         "data:view.isHomepage or data:view.isMultipleItems" block, which
         never runs on a static Page. Reuses the theme's own global
         .b1-share-panel / .b1-share-btn CSS and #spj-ico-* SVG sprite (both
         confirmed present on every page via the post's own header share
         row), so the resulting panel looks identical. Falls back to
         window.scsShareCard if the theme ever makes it available here. ──*/
    function pubShareCard(btn, e) {
      if (window.scsShareCard) { window.scsShareCard(btn, e); return; }
      e.stopPropagation();
      e.preventDefault();
      var prev = document.getElementById("pub-sp");
      if (prev) {
        prev.remove();
        if (window._pubSPBtn === btn) { window._pubSPBtn = null; return; }
      }
      window._pubSPBtn = btn;
      var url = btn.getAttribute("data-url");
      var r = btn.getBoundingClientRect();

      var panel = document.createElement("div");
      panel.id = "pub-sp";
      panel.className = "b1-share-panel open";
      panel.style.position = "fixed";
      panel.style.top = "auto";
      panel.style.bottom = window.innerHeight - r.top + 6 + "px";
      panel.style.right = window.innerWidth - r.right + "px";
      panel.style.zIndex = "99999";

      function mkA(bg, href, svgHtml, label) {
        var a = document.createElement("a");
        a.className = "b1-share-btn";
        a.style.background = bg;
        if (href) { a.href = href; a.target = "_blank"; a.rel = "noopener noreferrer"; } else { a.href = "#"; }
        a.innerHTML = svgHtml + "<span>" + label + "</span>";
        return a;
      }
      function closePanel() {
        var p = document.getElementById("pub-sp");
        if (p) p.remove();
        window._pubSPBtn = null;
      }

      var LI = '<svg fill="white" height="14" width="14"><use href="#spj-ico-li"></use></svg>';
      var FB = '<svg fill="white" height="14" width="14"><use href="#spj-ico-fb"></use></svg>';
      var XTW = '<svg fill="white" height="14" width="14"><use href="#spj-ico-tw"></use></svg>';
      var WA = '<svg fill="white" height="14" width="14"><use href="#spj-ico-wa"></use></svg>';
      var TG = '<svg fill="white" height="14" width="14"><use href="#spj-ico-tg"></use></svg>';
      var RD = '<svg fill="white" height="14" width="14"><use href="#spj-ico-rd"></use></svg>';
      var WC_SVG = '<svg fill="white" height="14" width="14"><use href="#spj-ico-wc"></use></svg>';
      var CP = '<svg fill="none" height="14" stroke="white" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" width="14"><use href="#spj-ico-cp"></use></svg>';

      var liA = mkA("#0a66c2", "https://www.linkedin.com/sharing/share-offsite/?url=" + encodeURIComponent(url), LI, "LinkedIn");
      liA.onclick = function () { setTimeout(closePanel, 100); };
      panel.appendChild(liA);
      var fbA = mkA("#1877f2", "https://www.facebook.com/sharer/sharer.php?u=" + encodeURIComponent(url), FB, "Facebook");
      fbA.onclick = function () { setTimeout(closePanel, 100); };
      panel.appendChild(fbA);
      var xA = mkA("#111", "https://twitter.com/intent/tweet?url=" + encodeURIComponent(url), XTW, "X (Twitter)");
      xA.onclick = function () { setTimeout(closePanel, 100); };
      panel.appendChild(xA);
      var waA = mkA("#25d366", "https://wa.me/?text=" + encodeURIComponent(url), WA, "WhatsApp");
      waA.onclick = function () { setTimeout(closePanel, 100); };
      panel.appendChild(waA);
      var tgA = mkA("#26a5e4", "https://t.me/share/url?url=" + encodeURIComponent(url), TG, "Telegram");
      tgA.onclick = function () { setTimeout(closePanel, 100); };
      panel.appendChild(tgA);
      var rdA = mkA("#ff4500", "https://www.reddit.com/submit?url=" + encodeURIComponent(url), RD, "Reddit");
      rdA.onclick = function () { setTimeout(closePanel, 100); };
      panel.appendChild(rdA);
      var wcA = mkA("#07c160", null, WC_SVG, "WeChat");
      wcA.setAttribute("data-u", url);
      wcA.onclick = function (ev) {
        ev.preventDefault();
        ev.stopPropagation();
        if (window.b1WC) window.b1WC(this);
        return false;
      };
      panel.appendChild(wcA);
      var cpA = mkA("#607d8b", null, CP, "Copy Link");
      cpA.onclick = function (ev) {
        ev.preventDefault();
        ev.stopPropagation();
        if (navigator.clipboard) {
          navigator.clipboard.writeText(url);
        } else {
          try {
            var t = document.createElement("textarea");
            t.value = url;
            document.body.appendChild(t);
            t.select();
            document.execCommand("copy");
            document.body.removeChild(t);
          } catch (err) {}
        }
        cpA.querySelector("span").textContent = "Copied!";
        setTimeout(closePanel, 1200);
        return false;
      };
      panel.appendChild(cpA);

      document.body.appendChild(panel);
      setTimeout(function () {
        function handler(ev) {
          if (!panel.contains(ev.target) && ev.target !== btn) {
            closePanel();
            document.removeEventListener("click", handler);
          }
        }
        document.addEventListener("click", handler);
      }, 50);
    }
    window.pubShareCard = pubShareCard;

    function cardHTML(p) {
      var thumbInner = p.thumb
        ? '<div aria-label="' + escAttr(p.title) + '" class="pub-card-thumb" role="img" style="background-image:url(\'' + escAttr(p.thumb) + "');\"></div>"
        : '<div class="pub-card-thumb pub-card-noimg"></div>';
      var readBadge = readSet[normUrl(p.link)] ? '<span class="pub-card-read-badge">✓ Read</span>' : "";
      var verifyHTML = verifyBadgeHTML(p.labels, "pub-card-verify-badge");
      var thumbHTML = '<div class="pub-card-thumb-wrap">' + thumbInner + readBadge + verifyHTML + "</div>";

      var descHTML = p.summary ? '<div class="pub-card-desc">' + escHTML(p.summary) + "…</div>" : "";

      var tagsHTML = "";
      if (p.labels && p.labels.length) {
        var MAX_TAGS = 3; /* keeps the row on a single line at typical card widths */
        var visibleLabels = p.labels.slice(0, MAX_TAGS);
        var moreHTML = p.labels.length > MAX_TAGS ? '<span class="pub-card-tag-more" title="' + escAttr(p.labels.slice(MAX_TAGS).join(", ")) + '">…</span>' : "";
        tagsHTML =
          '<div class="pub-card-tags">' +
          visibleLabels
            .map(function (l) {
              return (
                '<span class="pub-card-tag" data-label="' + escAttr(l) + '" ' +
                'onclick="event.preventDefault();event.stopPropagation();location.href=\'/search/label/\'+encodeURIComponent(this.getAttribute(\'data-label\'));">' +
                escHTML(l) +
                "</span>"
              );
            })
            .join("") +
          moreHTML +
          "</div>";
      }

      var authorHTML = "";
      if (p.authorImg) authorHTML += '<img alt="' + escAttr(p.author) + '" class="pub-card-avatar" loading="lazy" src="' + escAttr(p.authorImg) + '" />';
      if (p.author) authorHTML += '<span class="pub-card-author-name">' + escHTML(p.author) + "</span>";

      var commentsHTML =
        '<span class="pub-card-comments" onclick="event.preventDefault();event.stopPropagation();location.href=this.closest(\'a\').href+\'#comment-form\';">💬 ' +
        (p.comments || 0) +
        "</span>";

      var shareHTML =
        '<button class="pub-card-share spj-card-share" data-url="' + escAttr(p.link) + '" data-title="' + escAttr(p.title) + '" ' +
        'onclick="pubShareCard(this,event)" type="button">' +
        SHARE_SVG +
        "</button>";

      return (
        '<a class="pub-card" href="' + escAttr(p.link) + '" rel="noopener" target="_blank">' +
        thumbHTML +
        '<div class="pub-card-body">' +
        '<h4 class="pub-card-title">' + escHTML(p.title) + "</h4>" +
        descHTML +
        tagsHTML +
        '<div class="pub-card-footer">' +
        '<div class="pub-card-author-row">' + authorHTML + '<span class="pub-card-date">' + fmtCardDate(p.published) + "</span></div>" +
        '<div class="pub-card-footer-right">' + commentsHTML + shareHTML + "</div>" +
        "</div></div></a>"
      );
    }

    /*── Card list markup (one per topic group) — vertical stack, top to
         bottom, instead of the horizontal carousel the other MAIN MENU hub
         pages use. ──*/
    function cardListHTML(posts) {
      return '<div class="pub-card-list">' + posts.map(cardHTML).join("") + "</div>";
    }

    function renderArchive(items) {
      refreshReadSet();
      var archiveEl = document.getElementById("pub-archive");
      var emptyEl = document.getElementById("pub-empty");
      var sortBarEl = document.getElementById("pub-sort-bar");
      var tagJumpEl = document.getElementById("pub-tag-jump");

      if (!items.length) {
        archiveEl.style.display = "none";
        if (sortBarEl) sortBarEl.style.display = "none";
        emptyEl.style.display = "block";
        return;
      }

      var groups = buildGroups(items);
      var tagsSorted = GROUP_MAP.map(function(g){ return g.name; })
        .filter(function(n){ return groups[n] && groups[n].length; });

      var MAX_PILLS = 5;
      var pillTags = tagsSorted.slice(0, MAX_PILLS);
      var morePills = tagsSorted.slice(MAX_PILLS);
      var pillsHTML = pillTags
        .map(function (t) {
          return '<a class="pub-tag-pill" data-tag="' + escAttr(t) + '" href="#pub-tag-' + slugTag(t) + '">' + escHTML(t) + ' <span class="pub-cnt">' + groups[t].length + "</span></a>";
        })
        .join("");
      if (morePills.length) {
        pillsHTML += '<span class="pub-tag-pill-more" title="' + escAttr(morePills.join(", ")) + '">… +' + morePills.length + "</span>";
      }
      tagJumpEl.innerHTML = pillsHTML;

      archiveEl.innerHTML = tagsSorted
        .map(function (t, idx) {
          var posts = groups[t].slice().sort(function (a, b) {
            return new Date(b.published).getTime() - new Date(a.published).getTime();
          });
          return (
            '<details class="pub-tag-block" id="pub-tag-' + slugTag(t) + '"' + (idx === 0 ? " open" : "") + '>' +
            '<summary class="pub-tag-summary"><span class="pub-tag-chevron">▶</span><h2 class="pub-tag-title">' + escHTML(t) + '</h2><span class="pub-tag-badge">' + posts.length + " posts</span></summary>" +
            '<div class="pub-tag-body">' + cardListHTML(posts) + "</div>" +
            "</details>"
          );
        })
        .join("");

      archiveEl.style.display = "block";
      if (sortBarEl) sortBarEl.style.display = "none";
      emptyEl.style.display = "none";
    }

    /*── Live search filter (client-side, over already-loaded data) ──*/
    function applySearch(q) {
      q = (q || "").trim().toLowerCase();
      if (!q) {
        renderArchive(filterByPeriod(allItems));
        return;
      }
      var filtered = filterByPeriod(allItems).filter(function (p) {
        return (p.title + " " + p.summary).toLowerCase().indexOf(q) !== -1;
      });
      renderArchive(filtered);
    }

    /*── Top Ranked (real view counts via abacus, read-only) ──*/
    function keyFor(url) {
      try {
        var u = new URL(url);
        return u.pathname.replace(/\/+$/, "").replace(/[^a-zA-Z0-9]+/g, "-").replace(/^-+|-+$/g, "");
      } catch (e) {
        return (url || "").replace(/[^a-zA-Z0-9]+/g, "-");
      }
    }

    function fetchViewCount(url, cb) {
      var key = keyFor(url);
      if (!key) { cb(0); return; }
      fetch("https://abacus.jasoncameron.dev/get/" + VIEW_NS + "/" + key)
        .then(function (r) { return r.json(); })
        .then(function (d) { cb(d && typeof d.value === "number" ? d.value : 0); })
        .catch(function () { cb(null); });
    }

    function loadTopRanked(items) {
      var loadingEl = document.getElementById("pub-ranked-loading");
      var listEl = document.getElementById("pub-ranked-list");
      if (!items.length) {
        loadingEl.textContent = "No posts to display.";
        return;
      }

      var candidates = items
        .slice()
        .sort(function (a, b) { return new Date(b.published).getTime() - new Date(a.published).getTime(); })
        .slice(0, RANK_CANDIDATE_POOL);

      var results = [];
      var pending = candidates.length;
      var failed = 0;
      var CONCURRENCY = 6;
      var idx = 0;

      function next() {
        if (idx >= candidates.length) return;
        var p = candidates[idx++];
        fetchViewCount(p.link, function (views) {
          if (views === null) failed++;
          results.push({ post: p, views: views || 0 });
          pending--;
          if (pending === 0) done();
          else next();
        });
      }
      function done() {
        if (failed === candidates.length) {
          loadingEl.textContent = "Couldn't load view-count data. Please try again shortly.";
          return;
        }
        results.sort(function (a, b) { return b.views - a.views; });
        var top = results.slice(0, RANK_SHOW);
        listEl.innerHTML = top
          .map(function (r, i) {
            var thumbHTML = r.post.thumb
              ? '<span class="pub-rank-thumb" style="background-image:url(\'' + escAttr(r.post.thumb) + "');\"></span>"
              : '<span class="pub-rank-thumb pub-rank-noimg"></span>';
            var avatarHTML = r.post.authorImg
              ? '<span class="pub-rank-avatar" style="background-image:url(\'' + escAttr(r.post.authorImg) + "');\"></span>"
              : "";
            var authorHTML = r.post.author ? avatarHTML + '<span class="pub-rank-author">' + escHTML(r.post.author) + "</span>" : "";
            var metaHTML =
              authorHTML +
              '<span class="pub-rank-date">' + fmtCardDate(r.post.published) + "</span>" +
              '<span class="pub-rank-comments">💬 ' + r.post.comments + "</span>";
            var verifyHTML = verifyBadgeHTML(r.post.labels, "pub-rank-verify-badge");
            return (
              '<a class="pub-rank-row" href="' + escAttr(r.post.link) + '" rel="noopener" target="_blank">' +
              '<span class="pub-rank-num">' + (i + 1) + "</span>" +
              thumbHTML +
              '<span class="pub-rank-body"><div class="pub-rank-title-row"><h4 class="pub-rank-title">' + escHTML(r.post.title) + "</h4>" + verifyHTML + '</div><div class="pub-rank-meta">' + metaHTML + "</div></span>" +
              "</a>"
            );
          })
          .join("");
        loadingEl.style.display = "none";
      }

      for (var c = 0; c < Math.min(CONCURRENCY, candidates.length); c++) next();
    }

    /*── Init ──*/
    function onData(items) {
      items.sort(function (a, b) { return new Date(b.published).getTime() - new Date(a.published).getTime(); });
      allItems = items;
      document.getElementById("pub-loading").style.display = "none";
      renderArchive(filterByPeriod(allItems));
      loadTopRanked(allItems);
    }

    var cached = loadCache();
    if (cached) {
      onData(cached);
      fetchAllPosts(function (fresh) { if (fresh.length) saveCache(fresh); }); /* Background refresh (applied on next visit) */
    } else {
      fetchAllPosts(function (fresh) {
        if (fresh.length) saveCache(fresh);
        onData(fresh);
      });
    }

    document.getElementById("pub-search-input").addEventListener("input", function () {
      applySearch(this.value);
    });

    /*── Sort toggle buttons ──*/
    document.getElementById("pub-sort-bar").addEventListener("click", function (e) {
      var btn = e.target.closest(".pub-sort-btn");
      if (!btn) return;
      var mode = btn.getAttribute("data-sort");
      if (mode && mode !== pubSortMode) {
        pubSortMode = mode;
        renderArchive(filterByPeriod(allItems));
      }
    });

    /*── Topic pills (under the search box): clicking one opens only that
         topic's <details> and collapses every other topic, then scrolls to
         it. Delegated on the wrapper (not the pills themselves) since
         #pub-tag-jump's innerHTML is regenerated on every renderArchive
         call — a listener bound directly to a pill would be lost on the
         next re-render. ──*/
    document.getElementById("pub-tag-jump").addEventListener("click", function (e) {
      var pill = e.target.closest(".pub-tag-pill");
      if (!pill) return;
      e.preventDefault();
      var tag = pill.getAttribute("data-tag");
      var targetId = "pub-tag-" + slugTag(tag);
      document.querySelectorAll("#pub-archive .pub-tag-block").forEach(function (details) {
        details.open = details.id === targetId;
      });
      var target = document.getElementById(targetId);
      if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
    });

    /*── Force-hide comments section (theme's #comments renders outside this page's content, so handle via JS) ──*/
    document.addEventListener("DOMContentLoaded", function () {
      ["comments", "comment-holder"].forEach(function (id) {
        var el = document.getElementById(id);
        if (el) el.style.display = "none";
      });
      document.querySelectorAll(".comments, .comments-widget-container").forEach(function (el) {
        el.style.display = "none";
      });
    });
  
    document.getElementById("pub-period-bar").addEventListener("click", function(e) {
      var btn = e.target.closest(".spj-period-btn");
      if (!btn) return;
      document.querySelectorAll("#pub-period-bar .spj-period-btn").forEach(function(b) { b.classList.remove("active"); });
      btn.classList.add("active");
      periodMode = btn.getAttribute("data-period");
      renderArchive(filterByPeriod(allItems));
    });
  })();