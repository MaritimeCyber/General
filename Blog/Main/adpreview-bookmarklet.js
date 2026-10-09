// ShipPaulJobs 광고 영역 미리보기 북마클릿 (원본 소스)
// - 테마를 수정하지 않고, 현재 보고 있는 페이지에만 광고 자리 박스를 그립니다.
// - 다시 누르면 박스가 사라집니다(토글). 새로고침해도 사라집니다.
// - 설치용 링크는 adpreview-bookmarklet.html 에 있습니다. 이 파일을 고친 뒤에는
//   build-bookmarklet.sh 를 실행해 설치 페이지를 다시 만드세요.
(function () {
  var ID = 'spj-adph-style';
  var old = document.getElementById(ID);
  if (old) {
    old.remove();
    document.querySelectorAll('[data-adph]').forEach(function (e) { e.remove(); });
    return;
  }

  var st = document.createElement('style');
  st.id = ID;
  st.textContent =
    '.spj-adph{box-sizing:border-box;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;width:100%;margin:16px auto;padding:10px;' +
    'border:2px dashed #e0a100;border-radius:8px;background:repeating-linear-gradient(45deg,#fff8e1,#fff8e1 10px,#fff3cd 10px,#fff3cd 20px);' +
    "color:#7a5600;font:600 13px/1.4 'Roboto',sans-serif;text-align:center;position:relative;z-index:5}" +
    '.spj-adph b{background:#e0a100;color:#fff;font-size:10px;letter-spacing:.1em;padding:2px 8px;border-radius:3px}' +
    '.spj-adph i{font-style:normal;font-weight:400;font-size:11.5px;opacity:.8}';
  document.head.appendChild(st);

  var count = 0;
  function box(key, name, size, minH, maxW) {
    var d = document.createElement('div');
    d.className = 'spj-adph';
    d.setAttribute('data-adph', key);
    d.style.minHeight = minH + 'px';
    if (maxW) d.style.maxWidth = maxW + 'px';
    d.innerHTML = '<b>AD</b><span>' + name + '</span><i>' + size + '</i>';
    count++;
    return d;
  }
  function before(ref, el) { if (ref && ref.parentNode) ref.parentNode.insertBefore(el, ref); }
  function after(ref, el) { if (ref && ref.parentNode) ref.parentNode.insertBefore(el, ref.nextSibling); }

  // 1) 헤더 아래
  after(document.querySelector('header.centered-top-container'),
    box('header-below', '헤더 아래 배너', '728×90 / 반응형', 90, 970));

  // 2) 글 본문 상단/하단 (개별 글 페이지에서만)
  var body = document.querySelector('.post-body.entry-content[id^="post-body-"]');
  if (body) {
    body.insertBefore(box('post-top', '글 본문 상단', '반응형 (권장 728×90)', 100), body.firstChild);
    var cta = [].slice.call(body.children).filter(function (e) {
      return /Join the ShipPaulJobs Community/.test(e.textContent);
    })[0];
    var bottom = box('post-bottom', '글 본문 하단', '336×280 / 반응형', 250);
    cta ? before(cta, bottom) : body.appendChild(bottom);
  }

  // 3) 메인 피드 중간 (목록 페이지): 3번째 포스트 뒤, 글이 적으면 그 앞
  var posts = document.querySelectorAll('.blog-posts .post-outer-container');
  if (posts.length >= 2) {
    var idx = Math.min(2, posts.length - 2);
    after(posts[idx], box('feed-middle', '메인 피드 중간 (In-feed)', '반응형 · ' + (idx + 1) + '번째 포스트 뒤', 120));
  }

  // 4) 사이드바 맨 위
  var side = document.querySelector('aside.sidebar-container .sidebar_top_wrapper') ||
             document.querySelector('aside.sidebar-container');
  if (side) side.insertBefore(box('sidebar', '사이드바', '300×250', 250, 300), side.firstChild);

  // 5) 푸터 위
  after(document.querySelector('main#main'), box('footer-above', '푸터 위 배너', '728×90 / 반응형', 90, 970));

  if (!count) alert('이 페이지에서는 광고 자리를 찾지 못했습니다.');
})();
