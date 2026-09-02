
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

    var LABEL = "Maritime Industry Insights";
    var FEED_BASE = "https://www.shippauljobs.com/feeds/posts/summary/-/" + encodeURIComponent(LABEL) + "?alt=json";
    /* Versioned so that adding fields to mapEntry() (author/comments/labels)
       automatically invalidates any visitor's stale cached items instead of
       rendering "undefined" for the new fields — same pattern as apl_cache_v5
       in Main.html's Explore All Posts widget. */
    var CACHE_KEY = "mii_cache_v2"; /* bumped: v1 could have cached a truncated (45-post) result from the pagination bug */
    var CACHE_TTL = 30 * 60 * 1000;
    var VIEW_NS = "shippauljobs-views"; /* shared sitewide counter — same namespace Maritime Weekly.html uses */
    var MONTHS_SHORT = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    var RANK_CANDIDATE_POOL = 40; /* Compare view counts only among the N most recent posts (limits API call volume) */
    var RANK_SHOW = 6;
    var FALLBACK_GROUP = "General"; /* posts tagged only "Maritime Industry Insights" with no other topic tag */
    var GROUP_MAP = [
      { name: "Maritime News Analysis", labels: ["Maritime News Analysis","Maritime Trend","Maritime","Maritime Solution"] },
      { name: "Maritime Market",        labels: ["Maritime Market","Industry and Market","Marine Insurance","claims management","loss prevention","Marine","shipowner"] },
      { name: "Industry Trends",        labels: ["A.I in Marine","AI Product","AI and Automation","AICyberLab","CRSI","Cyber Security","Security Assessment","Threats and Attacks","risk assessment","JOBS","Maritime Jobs & Careers","IACS UR E26 E27","IACS UR E26","IACS UR E27","IACS E26","IACS E27","Compliances","Regulatory Compliance","Rules and Compliance","Compliance","Classification"] },
      { name: "USCG",                   labels: ["USCG"] },
      { name: "IMO",                    labels: ["IMO","IMO MSC"] },
      { name: "Shipbuilding Market",    labels: ["Shipbuilding","Shipbuilding Market"] },
      { name: "General",                labels: [] }
    ];
    var miiSortMode = "alpha"; /* 'alpha' = A-Z (default) | 'count' = most posts first */

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

    function fetchAllPosts(cb) {
      var collected = [];
      function page(start) {
        fetch(FEED_BASE + "&max-results=150&start-index=" + start)
          .then(function (r) {
            return r.json();
          })
          .then(function (d) {
            var entries = (d.feed && d.feed.entry) || [];
            entries.forEach(function (e) {
              collected.push(mapEntry(e));
            });
            /* Blogger's public summary feed silently caps each response at
               ~45 entries regardless of max-results=150, so
               entries.length===150 is never true and this always stopped
               after page 1. Advance by however many entries actually came
               back instead; start<1500 stays as a sane runaway ceiling. */
            if (entries.length > 0 && start < 1500) {
              page(start + entries.length);
            } else {
              cb(collected);
            }
          })
          .catch(function () {
            cb(collected);
          });
      }
      page(1);
    }

    /*── Grouping: fixed semantic order defined by GROUP_MAP.
         Each post is placed in every group whose labels[] intersects the post's
         own labels. Posts matching no group go to the catch-all "General" entry. ──*/
    function buildGroups(items) {
      var labelToGroup = {};
      var catchAll = null;
      GROUP_MAP.forEach(function(g) {
        if (!g.labels.length) { catchAll = g.name; return; }
        g.labels.forEach(function(l) { labelToGroup[l] = g.name; });
      });
      var groups = {};
      GROUP_MAP.forEach(function(g) { groups[g.name] = []; });
      items.forEach(function(p) {
        var matched = {};
        (p.labels || []).forEach(function(l) {
          if (l === LABEL) return;
          var gname = labelToGroup[l];
          if (gname && !matched[gname]) { matched[gname] = true; groups[gname].push(p); }
        });
        if (!Object.keys(matched).length && catchAll !== null) {
          groups[catchAll].push(p);
        }
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
    function miiShareCard(btn, e) {
      if (window.scsShareCard) { window.scsShareCard(btn, e); return; }
      e.stopPropagation();
      e.preventDefault();
      var prev = document.getElementById("mii-sp");
      if (prev) {
        prev.remove();
        if (window._miiSPBtn === btn) { window._miiSPBtn = null; return; }
      }
      window._miiSPBtn = btn;
      var url = btn.getAttribute("data-url");
      var r = btn.getBoundingClientRect();

      var panel = document.createElement("div");
      panel.id = "mii-sp";
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
        var p = document.getElementById("mii-sp");
        if (p) p.remove();
        window._miiSPBtn = null;
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
    window.miiShareCard = miiShareCard;

    function cardHTML(p) {
      var thumbInner = p.thumb
        ? '<div aria-label="' + escAttr(p.title) + '" class="mii-card-thumb" role="img" style="background-image:url(\'' + escAttr(p.thumb) + "');\"></div>"
        : '<div class="mii-card-thumb mii-card-noimg"></div>';
      var readBadge = readSet[normUrl(p.link)] ? '<span class="mii-card-read-badge">✓ Read</span>' : "";
      var verifyHTML = verifyBadgeHTML(p.labels, "mii-card-verify-badge");
      var thumbHTML = '<div class="mii-card-thumb-wrap">' + thumbInner + readBadge + verifyHTML + "</div>";

      var descHTML = p.summary ? '<div class="mii-card-desc">' + escHTML(p.summary) + "…</div>" : "";

      var tagsHTML = "";
      if (p.labels && p.labels.length) {
        var MAX_TAGS = 3; /* keeps the row on a single line at typical card widths */
        var visibleLabels = p.labels.slice(0, MAX_TAGS);
        var moreHTML = p.labels.length > MAX_TAGS ? '<span class="mii-card-tag-more" title="' + escAttr(p.labels.slice(MAX_TAGS).join(", ")) + '">…</span>' : "";
        tagsHTML =
          '<div class="mii-card-tags">' +
          visibleLabels
            .map(function (l) {
              return (
                '<span class="mii-card-tag" data-label="' + escAttr(l) + '" ' +
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
      if (p.authorImg) authorHTML += '<img alt="' + escAttr(p.author) + '" class="mii-card-avatar" loading="lazy" src="' + escAttr(p.authorImg) + '" />';
      if (p.author) authorHTML += '<span class="mii-card-author-name">' + escHTML(p.author) + "</span>";

      var commentsHTML =
        '<span class="mii-card-comments" onclick="event.preventDefault();event.stopPropagation();location.href=this.closest(\'a\').href+\'#comment-form\';">💬 ' +
        (p.comments || 0) +
        "</span>";

      var shareHTML =
        '<button class="mii-card-share spj-card-share" data-url="' + escAttr(p.link) + '" data-title="' + escAttr(p.title) + '" ' +
        'onclick="miiShareCard(this,event)" type="button">' +
        SHARE_SVG +
        "</button>";

      return (
        '<a class="mii-card" href="' + escAttr(p.link) + '" rel="noopener" target="_blank">' +
        thumbHTML +
        '<div class="mii-card-body">' +
        '<h4 class="mii-card-title">' + escHTML(p.title) + "</h4>" +
        descHTML +
        tagsHTML +
        '<div class="mii-card-footer">' +
        '<div class="mii-card-author-row">' + authorHTML + '<span class="mii-card-date">' + fmtCardDate(p.published) + "</span></div>" +
        '<div class="mii-card-footer-right">' + commentsHTML + shareHTML + "</div>" +
        "</div></div></a>"
      );
    }

    /*── Carousel row markup (one per topic group — 3.5 cards per line,
         matching the main page's "Introduction to Marine Solutions" widget) ──*/
    function carouselHTML(posts) {
      var indicator = posts.length > 1 ? "1 / " + posts.length : "";
      return (
        '<div class="mii-carousel-wrap">' +
        '<button class="mii-car-btn mii-car-prev" disabled type="button" aria-label="Previous"><span class="mii-car-arrow"></span></button>' +
        '<div class="mii-car-outer"><div class="mii-car-track">' + posts.map(cardHTML).join("") + "</div></div>" +
        '<button class="mii-car-btn mii-car-next" disabled type="button" aria-label="Next"><span class="mii-car-arrow"></span></button>' +
        "</div>" +
        '<div class="mii-car-indicator">' + indicator + "</div>"
      );
    }

    function renderArchive(items) {
      refreshReadSet();
      var archiveEl = document.getElementById("mii-archive");
      var emptyEl = document.getElementById("mii-empty");
      var sortBarEl = document.getElementById("mii-sort-bar");
      var tagJumpEl = document.getElementById("mii-tag-jump");

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
          return '<a class="mii-tag-pill" data-tag="' + escAttr(t) + '" href="#mii-tag-' + slugTag(t) + '">' + escHTML(t) + ' <span class="mii-cnt">' + groups[t].length + "</span></a>";
        })
        .join("");
      if (morePills.length) {
        pillsHTML += '<span class="mii-tag-pill-more" title="' + escAttr(morePills.join(", ")) + '">… +' + morePills.length + "</span>";
      }
      tagJumpEl.innerHTML = pillsHTML;

      archiveEl.innerHTML = tagsSorted
        .map(function (t, idx) {
          var posts = groups[t].slice().sort(function (a, b) {
            return new Date(b.published).getTime() - new Date(a.published).getTime();
          });
          return (
            '<details class="mii-tag-block" id="mii-tag-' + slugTag(t) + '"' + (idx === 0 ? " open" : "") + '>' +
            '<summary class="mii-tag-summary"><span class="mii-tag-chevron">▶</span><h2 class="mii-tag-title">' + escHTML(t) + '</h2><span class="mii-tag-badge">' + posts.length + " posts</span></summary>" +
            '<div class="mii-tag-body">' + carouselHTML(posts) + "</div>" +
            "</details>"
          );
        })
        .join("");

      archiveEl.style.display = "block";
      if (sortBarEl) sortBarEl.style.display = "none";
      emptyEl.style.display = "none";
      initAllCarousels();
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

    /*══════════════════════════════════════════════════════════
       Carousel engine — generalized version of the main page's
       "Introduction to Marine Solutions" (#ms-*) carousel, supporting
       many simultaneous instances (one per topic row) with a single
       shared drag/resize dispatcher.
    ══════════════════════════════════════════════════════════*/
    var carousels = [];
    var drag = { active: false, inst: null, startX: 0, baseX: 0, moved: false };
    var SNAP_RATIO = 0.18;

    function carStep(inst) {
      var first = inst.track.children[0];
      return first ? first.offsetWidth + 10 : 0;
    }
    function carMaxIndex(inst) {
      var step = carStep(inst);
      if (!step) return 0;
      var visible = Math.max(1, Math.round((inst.outer.offsetWidth + 10) / step));
      return Math.max(0, inst.track.children.length - visible);
    }
    function carApply(inst, animate) {
      inst.track.style.transition = animate ? "transform .42s cubic-bezier(.25,.46,.45,.94)" : "none";
      inst.track.style.transform = "translateX(-" + inst.index * carStep(inst) + "px)";
    }
    function carUpdateBtns(inst) {
      var max = carMaxIndex(inst);
      inst.prevBtn.disabled = inst.index <= 0;
      inst.nextBtn.disabled = inst.index >= max;
    }
    function carUpdateIndicator(inst) {
      var total = inst.track.children.length;
      if (inst.indEl) inst.indEl.textContent = total > 1 ? inst.index + 1 + " / " + total : "";
    }
    function carGoTo(inst, idx, animate) {
      inst.index = Math.max(0, Math.min(idx, carMaxIndex(inst)));
      carApply(inst, animate);
      carUpdateBtns(inst);
      carUpdateIndicator(inst);
    }

    function initAllCarousels() {
      carousels = [];
      document.querySelectorAll("#mii-archive .mii-carousel-wrap").forEach(function (wrap) {
        var track = wrap.querySelector(".mii-car-track");
        var outer = wrap.querySelector(".mii-car-outer");
        var prevBtn = wrap.querySelector(".mii-car-prev");
        var nextBtn = wrap.querySelector(".mii-car-next");
        var indEl = wrap.nextElementSibling && wrap.nextElementSibling.classList.contains("mii-car-indicator") ? wrap.nextElementSibling : null;
        var inst = { wrap: wrap, track: track, outer: outer, prevBtn: prevBtn, nextBtn: nextBtn, indEl: indEl, index: 0, animating: false };
        carousels.push(inst);

        prevBtn.addEventListener("click", function () {
          if (inst.animating || inst.index <= 0) return;
          inst.animating = true;
          carGoTo(inst, inst.index - 1, true);
          setTimeout(function () { inst.animating = false; }, 450);
        });
        nextBtn.addEventListener("click", function () {
          if (inst.animating || inst.index >= carMaxIndex(inst)) return;
          inst.animating = true;
          carGoTo(inst, inst.index + 1, true);
          setTimeout(function () { inst.animating = false; }, 450);
        });

        outer.addEventListener("mousedown", function (e) {
          if (inst.animating) return;
          drag = { active: true, inst: inst, startX: e.clientX, baseX: -(inst.index * carStep(inst)), moved: false };
          track.style.transition = "none";
          e.preventDefault();
        });
        outer.addEventListener("touchstart", function (e) {
          if (inst.animating) return;
          drag = { active: true, inst: inst, startX: e.touches[0].clientX, baseX: -(inst.index * carStep(inst)), moved: false };
          track.style.transition = "none";
        }, { passive: true });
        wrap.addEventListener("click", function (e) { if (drag.moved) e.preventDefault(); }, true);

        carUpdateBtns(inst);
        carUpdateIndicator(inst);
      });

      /* Collapsed <details> topics render their content at 0 width (the
         browser doesn't lay out hidden content), so any carousel measured
         at init time inside a closed group got carStep()=0 → carMaxIndex()=0
         → both prev/next buttons stuck permanently disabled, even after the
         user opens that group. Recompute every carousel inside a group the
         moment it's expanded so the buttons/track catch up to their real
         width. */
      document.querySelectorAll("#mii-archive .mii-tag-block").forEach(function (details) {
        details.addEventListener("toggle", function () {
          if (!details.open) return;
          carousels.forEach(function (inst) {
            if (details.contains(inst.wrap)) {
              carApply(inst, false);
              carUpdateBtns(inst);
              carUpdateIndicator(inst);
            }
          });
        });
      });
    }

    function dragMove(clientX) {
      if (!drag.active) return;
      var inst = drag.inst;
      var delta = clientX - drag.startX;
      if (Math.abs(delta) > 4) drag.moved = true;
      var max = carMaxIndex(inst), minTx = -(max * carStep(inst));
      var tx = drag.baseX + delta;
      if (tx > 0) tx = tx * 0.25;
      if (tx < minTx) tx = minTx + (tx - minTx) * 0.25;
      inst.track.style.transform = "translateX(" + tx + "px)";
    }
    function dragEnd(clientX) {
      if (!drag.active) return;
      var inst = drag.inst;
      drag.active = false;
      if (!drag.moved) { carApply(inst, true); return; }
      var delta = clientX - drag.startX;
      var step = carStep(inst), max = carMaxIndex(inst);
      if (Math.abs(delta) > step * SNAP_RATIO) {
        if (delta < 0 && inst.index < max) inst.index++;
        else if (delta > 0 && inst.index > 0) inst.index--;
      }
      inst.animating = true;
      carGoTo(inst, inst.index, true);
      setTimeout(function () { inst.animating = false; }, 450);
    }
    document.addEventListener("mousemove", function (e) { if (drag.active) { e.preventDefault(); dragMove(e.clientX); } });
    document.addEventListener("mouseup", function (e) { if (drag.active) dragEnd(e.clientX); });
    document.addEventListener("touchmove", function (e) { if (drag.active) dragMove(e.touches[0].clientX); }, { passive: true });
    document.addEventListener("touchend", function (e) { if (drag.active) dragEnd(e.changedTouches[0].clientX); }, { passive: true });
    window.addEventListener("resize", function () {
      carousels.forEach(function (inst) {
        if (inst.index > carMaxIndex(inst)) inst.index = carMaxIndex(inst);
        carApply(inst, false);
        carUpdateBtns(inst);
      });
    });

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
      var loadingEl = document.getElementById("mii-ranked-loading");
      var listEl = document.getElementById("mii-ranked-list");
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
              ? '<span class="mii-rank-thumb" style="background-image:url(\'' + escAttr(r.post.thumb) + "');\"></span>"
              : '<span class="mii-rank-thumb mii-rank-noimg"></span>';
            var avatarHTML = r.post.authorImg
              ? '<span class="mii-rank-avatar" style="background-image:url(\'' + escAttr(r.post.authorImg) + "');\"></span>"
              : "";
            var authorHTML = r.post.author ? avatarHTML + '<span class="mii-rank-author">' + escHTML(r.post.author) + "</span>" : "";
            var metaHTML =
              authorHTML +
              '<span class="mii-rank-date">' + fmtCardDate(r.post.published) + "</span>" +
              '<span class="mii-rank-comments">💬 ' + r.post.comments + "</span>";
            var verifyHTML = verifyBadgeHTML(r.post.labels, "mii-rank-verify-badge");
            return (
              '<a class="mii-rank-row" href="' + escAttr(r.post.link) + '" rel="noopener" target="_blank">' +
              '<span class="mii-rank-num">' + (i + 1) + "</span>" +
              thumbHTML +
              '<span class="mii-rank-body"><div class="mii-rank-title-row"><h4 class="mii-rank-title">' + escHTML(r.post.title) + "</h4>" + verifyHTML + '</div><div class="mii-rank-meta">' + metaHTML + "</div></span>" +
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
      document.getElementById("mii-loading").style.display = "none";
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

    document.getElementById("mii-search-input").addEventListener("input", function () {
      applySearch(this.value);
    });

    /*── Sort toggle buttons ──*/
    document.getElementById("mii-sort-bar").addEventListener("click", function (e) {
      var btn = e.target.closest(".mii-sort-btn");
      if (!btn) return;
      var mode = btn.getAttribute("data-sort");
      if (mode && mode !== miiSortMode) {
        miiSortMode = mode;
        renderArchive(filterByPeriod(allItems));
      }
    });

    /*── Topic pills (under the search box): clicking one opens only that
         topic's <details> and collapses every other topic, then scrolls to
         it. Delegated on the wrapper (not the pills themselves) since
         #mii-tag-jump's innerHTML is regenerated on every renderArchive
         call — a listener bound directly to a pill would be lost on the
         next re-render. ──*/
    document.getElementById("mii-tag-jump").addEventListener("click", function (e) {
      var pill = e.target.closest(".mii-tag-pill");
      if (!pill) return;
      e.preventDefault();
      var tag = pill.getAttribute("data-tag");
      var targetId = "mii-tag-" + slugTag(tag);
      document.querySelectorAll("#mii-archive .mii-tag-block").forEach(function (details) {
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
  
    document.getElementById("mii-period-bar").addEventListener("click", function(e) {
      var btn = e.target.closest(".spj-period-btn");
      if (!btn) return;
      document.querySelectorAll("#mii-period-bar .spj-period-btn").forEach(function(b) { b.classList.remove("active"); });
      btn.classList.add("active");
      periodMode = btn.getAttribute("data-period");
      renderArchive(filterByPeriod(allItems));
    });
  })();