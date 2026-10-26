/* RW Company — interações do site.
   Sem bibliotecas: Intersection Observer, Web Animations e CSS.
   Tudo respeita prefers-reduced-motion e nada anima fora da tela. */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  // Página de case aberta direto: sempre começa no topo (sem herdar a rolagem anterior)
  if ("scrollRestoration" in history) history.scrollRestoration = "manual";
  if (!location.hash) window.scrollTo(0, 0);

  /* ---------- reveal ao entrar na tela (uma vez) ---------- */
  var revealIO = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add("is-in");
      revealIO.unobserve(e.target);
    });
  }, { rootMargin: "0px 0px -10% 0px", threshold: 0.12 });
  function initReveal(root) {
    $$("[data-reveal], .mask-group, .connector", root).forEach(function (el) { revealIO.observe(el); });
  }

  /* ---------- cabeçalho, progresso de rolagem e botão flutuante ---------- */
  var header = $(".header");
  var bar = $(".progress");
  var waFloat = $(".wa-float");
  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      var y = window.scrollY;
      var max = doc.scrollHeight - window.innerHeight;
      if (bar) bar.style.transform = "scaleX(" + (max > 0 ? y / max : 0) + ")";
      if (header) header.classList.toggle("is-solid", y > 24);
      if (waFloat) waFloat.classList.toggle("is-on", y > window.innerHeight * 0.8);
      updateTimeline();
      ticking = false;
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });

  /* ---------- menu mobile ---------- */
  var menuBtn = $(".menu-btn");
  var nav = $("#nav");
  if (menuBtn && nav) {
    var setMenu = function (open) {
      menuBtn.setAttribute("aria-expanded", String(open));
      nav.classList.toggle("is-open", open);
      menuBtn.setAttribute("aria-label", open ? "Fechar menu" : "Abrir menu");
    };
    menuBtn.addEventListener("click", function () { setMenu(menuBtn.getAttribute("aria-expanded") !== "true"); });
    $$("a", nav).forEach(function (a) { a.addEventListener("click", function () { setMenu(false); }); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") setMenu(false); });
  }

  /* ---------- link ativo no menu conforme a seção ---------- */
  var navLinks = $$('.nav__link[href^="#"]');
  if (navLinks.length) {
    var secIO = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        navLinks.forEach(function (a) { a.setAttribute("aria-current", String(a.getAttribute("href") === "#" + e.target.id)); });
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    navLinks.forEach(function (a) { var s = $(a.getAttribute("href")); if (s) secIO.observe(s); });
  }

  /* ---------- vídeo do hero: só desktop, depois do carregamento ---------- */
  var heroVideo = $(".hero__video");
  if (heroVideo && !reduce && window.matchMedia("(min-width: 900px)").matches &&
      !(navigator.connection && navigator.connection.saveData)) {
    window.addEventListener("load", function () {
      setTimeout(function () {
        $$("source[data-src]", heroVideo).forEach(function (s) { s.src = s.dataset.src; });
        heroVideo.load();
        heroVideo.addEventListener("canplay", function () {
          heroVideo.play().then(function () { heroVideo.classList.add("is-ready"); }).catch(function () {});
        }, { once: true });
        new IntersectionObserver(function (en) {
          if (!heroVideo.classList.contains("is-ready")) return;
          if (en[0].isIntersecting) heroVideo.play().catch(function () {}); else heroVideo.pause();
        }).observe(heroVideo);
      }, 600);
    });
  }

  /* ---------- luz que acompanha o cursor nos cards ---------- */
  if (finePointer && !reduce) {
    $$(".tile").forEach(function (t) {
      t.addEventListener("pointermove", function (e) {
        var r = t.getBoundingClientRect();
        t.style.setProperty("--mx", (e.clientX - r.left) + "px");
        t.style.setProperty("--my", (e.clientY - r.top) + "px");
      });
    });
  }

  /* ---------- filtros do portfólio ---------- */
  var filters = $$(".filter");
  filters.forEach(function (f) {
    f.addEventListener("click", function () {
      var cat = f.dataset.filter;
      filters.forEach(function (x) { x.setAttribute("aria-pressed", String(x === f)); });
      $$(".case[data-cat]").forEach(function (c) {
        var show = cat === "all" || c.dataset.cat.split(" ").indexOf(cat) !== -1;
        c.classList.toggle("is-hidden", !show);
        if (show && !reduce && c.animate) c.animate([{ opacity: 0, transform: "translateY(12px)" }, { opacity: 1, transform: "none" }], { duration: 420, easing: "cubic-bezier(0.16,1,0.3,1)" });
      });
      var live = $("#filter-status");
      if (live) live.textContent = f.textContent.trim() + ": " + $$(".case[data-cat]:not(.is-hidden)").length + " projetos";
    });
  });

  /* ---------- contadores (uma vez, ao entrar na tela) ---------- */
  var fmt = new Intl.NumberFormat("pt-BR");
  var countIO = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      countIO.unobserve(e.target);
      var el = e.target, to = Number(el.dataset.to), from = Number(el.dataset.from || 0);
      if (reduce) { el.textContent = fmt.format(to); return; }
      var t0 = performance.now(), dur = 1400;
      (function frame(now) {
        var p = Math.min(1, (now - t0) / dur);
        var eased = 1 - Math.pow(1 - p, 4);
        el.textContent = fmt.format(Math.round(from + (to - from) * eased));
        if (p < 1) requestAnimationFrame(frame);
      })(t0);
    });
  }, { threshold: 0.6 });
  $$("[data-to]").forEach(function (el) { countIO.observe(el); });

  /* ---------- linha do tempo acompanha a rolagem ---------- */
  var timeline = $(".timeline");
  var steps = $$(".step");
  var tlVisible = false;
  if (timeline) {
    new IntersectionObserver(function (en) { tlVisible = en[0].isIntersecting; if (tlVisible) updateTimeline(); }).observe(timeline);
  }
  function updateTimeline() {
    if (!timeline || !tlVisible) return;
    var r = timeline.getBoundingClientRect();
    var mid = window.innerHeight * 0.6;
    var p = Math.max(0, Math.min(1, (mid - r.top) / r.height));
    timeline.style.setProperty("--p", p.toFixed(3));
    steps.forEach(function (s) {
      var sr = s.getBoundingClientRect();
      s.classList.toggle("is-active", sr.top + 24 < mid);
    });
  }

  /* ---------- conversa do agente no WhatsApp (igual ao Reels) ---------- */
  function createChat(box) {
    var script = (window.RW_CHAT || []).map(function (m) { return { from: m.from, html: m.html, wait: m.wait }; });
    var i = 0, timer = null, running = false, done = false;
    function typing(on) {
      var t = $(".wa__typing", box);
      if (on && !t) { t = document.createElement("div"); t.className = "wa__typing is-new"; t.setAttribute("aria-hidden", "true"); t.innerHTML = "<i></i><i></i><i></i>"; box.appendChild(t); }
      if (!on && t) t.remove();
    }
    function step() {
      if (!running) return;
      if (i >= script.length) { running = false; done = true; return; }
      var m = script[i];
      if (m.from === "bot" && !m.typed) {
        m.typed = true; typing(true);
        timer = setTimeout(step, reduce ? 0 : 900);
        return;
      }
      typing(false);
      var el = document.createElement("div");
      el.className = "wa__msg is-new" + (m.from === "me" ? " wa__msg--me" : "");
      el.innerHTML = m.html;
      box.appendChild(el);
      i++;
      timer = setTimeout(step, reduce ? 0 : (m.wait || 1200));
    }
    return {
      start: function () { if (running || done) return; running = true; step(); },
      pause: function () { running = false; clearTimeout(timer); },
      replay: function () {
        clearTimeout(timer); running = false; done = false; i = 0;
        script.forEach(function (m) { m.typed = false; });
        box.innerHTML = "";
        this.start();
      }
    };
  }

  /* ---------- palco do agente: abas, conversa e vídeo do Instagram ---------- */
  var observers = [];
  function watch(el, fn, opts) {
    var io = new IntersectionObserver(fn, opts);
    io.observe(el);
    observers.push(io);
    return io;
  }
  function initStage(stageEl) {
    var phone = $(".phone", stageEl);
    var box = $(".wa__chat", stageEl);
    if (!phone || !box) return;
    var chat = createChat(box);
    var waPanel = $('[id^="panel-wa"]', stageEl);
    var igPanel = $('[id^="panel-ig"]', stageEl);
    var igVideo = igPanel && $("video", igPanel);
    var tabs = $$('[role="tab"]', stageEl);
    var visible = false;
    function sync() {
      if (igVideo) {
        if (igPanel && !igPanel.hidden && visible) {
          if (!igVideo.dataset.loaded) {
            $$("source[data-src]", igVideo).forEach(function (s) { s.src = s.dataset.src; });
            igVideo.load(); igVideo.dataset.loaded = "1";
          }
          igVideo.play().catch(function () {});
        } else igVideo.pause();
      }
      if (waPanel && !waPanel.hidden && visible) chat.start(); else chat.pause();
    }
    function select(tab) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute("aria-selected", String(on));
        t.tabIndex = on ? 0 : -1;
        var p = document.getElementById(t.getAttribute("aria-controls"));
        if (p) p.hidden = !on;
      });
      sync();
    }
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { select(t); });
      t.addEventListener("keydown", function (e) {
        if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
        var n = tabs[(i + (e.key === "ArrowRight" ? 1 : tabs.length - 1)) % tabs.length];
        n.focus(); select(n);
      });
    });
    var replay = $(".replay", stageEl);
    if (replay) replay.addEventListener("click", function () {
      if (waPanel && waPanel.hidden && tabs[0]) select(tabs[0]);
      chat.replay();
    });
    watch(phone, function (en) { visible = en[0].isIntersecting; sync(); }, { threshold: 0.35 });
  }

  /* ---------- vídeos dos cases: tocam só visíveis ---------- */
  function initVideos(root) {
    $$("video[data-inview]", root).forEach(function (v) {
      watch(v, function (en) {
        if (en[0].isIntersecting) {
          if (!v.dataset.loaded) { $$("source[data-src]", v).forEach(function (s) { s.src = s.dataset.src; }); v.load(); v.dataset.loaded = "1"; }
          if (!reduce) v.play().catch(function () {});
        } else v.pause();
      }, { threshold: 0.3 });
    });
  }

  initReveal(document);
  $$(".ia__stage").forEach(initStage);
  initVideos(document);

  /* ---------- modal do vídeo institucional ---------- */
  var modal = $("#vmodal");
  if (modal && modal.showModal) {
    var mv = $("video", modal);
    $$("[data-open-video]").forEach(function (b) {
      b.addEventListener("click", function (e) {
        e.preventDefault();
        if (!mv.dataset.loaded) { mv.src = mv.dataset.src; mv.dataset.loaded = "1"; }
        modal.showModal();
        mv.play().catch(function () {});
      });
    });
    var closeModal = function () { mv.pause(); modal.close(); };
    $(".vmodal__close", modal).addEventListener("click", closeModal);
    modal.addEventListener("click", function (e) { if (e.target === modal) closeModal(); });
    modal.addEventListener("close", function () { mv.pause(); });
  }

  /* =========================================================
     Case em camada sobre a home
     Abre sempre no topo, sem trocar de página; fechar volta
     ao card de onde saiu. A página própria de cada case
     continua existindo para links diretos e buscadores.
     ========================================================= */
  var casesGrid = $(".cases");
  if (casesGrid && window.fetch && window.DOMParser) {
    var sheet = null, sheetScroll = null, sheetTitle = null, lastFocus = null, openUrl = null, homeUrl = location.href;
    var background = $$("body > header, body > main, body > footer, body > .wa-float");

    // URLs relativas da página do case passam a ser absolutas na home
    function absolutize(root, base) {
      $$("[src],[href],[poster],[data-src],[srcset]", root).forEach(function (el) {
        ["src", "href", "poster", "data-src"].forEach(function (attr) {
          var v = el.getAttribute(attr);
          if (v && !/^(#|https?:|mailto:|tel:|data:)/.test(v)) el.setAttribute(attr, new URL(v, base).href);
        });
        var ss = el.getAttribute("srcset");
        if (ss) el.setAttribute("srcset", ss.split(",").map(function (part) {
          var bits = part.trim().split(/\s+/);
          bits[0] = new URL(bits[0], base).href;
          return bits.join(" ");
        }).join(", "));
      });
    }

    function buildSheet() {
      sheet = document.createElement("div");
      sheet.className = "sheet";
      sheet.setAttribute("role", "dialog");
      sheet.setAttribute("aria-modal", "true");
      sheet.setAttribute("aria-labelledby", "sheet-title");
      sheet.innerHTML =
        '<div class="sheet__bar">' +
          '<button class="sheet__back" type="button"><svg aria-hidden="true"><use href="#i-arrow"/></svg>Voltar aos cases</button>' +
          '<span class="sheet__title" id="sheet-title"></span>' +
          '<button class="sheet__close" type="button" aria-label="Fechar case"><svg aria-hidden="true"><use href="#i-close"/></svg></button>' +
        "</div>" +
        '<div class="sheet__scroll" tabindex="-1"><div class="sheet__loading" role="status">Carregando case…</div></div>';
      document.body.appendChild(sheet);
      sheetScroll = $(".sheet__scroll", sheet);
      sheetTitle = $(".sheet__title", sheet);
      $(".sheet__back", sheet).addEventListener("click", function () { closeCase(true); });
      $(".sheet__close", sheet).addEventListener("click", function () { closeCase(true); });
      sheet.addEventListener("keydown", function (e) {
        if (e.key === "Escape") { e.stopPropagation(); closeCase(true); }
        if (e.key !== "Tab") return;
        var f = $$('a[href], button:not([disabled]), video[controls], [tabindex]:not([tabindex="-1"])', sheet).filter(function (x) { return x.offsetParent !== null; });
        if (!f.length) return;
        if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
        else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
      });
      // links dentro do case: outro case troca o conteúdo; início/cases fecha a camada
      sheet.addEventListener("click", function (e) {
        var a = e.target.closest("a[href]");
        if (!a || e.metaKey || e.ctrlKey || e.shiftKey || a.target === "_blank") return;
        var url = new URL(a.href, location.href);
        if (url.origin !== location.origin) return;
        if (/\/cases\//.test(url.pathname)) { e.preventDefault(); loadCase(url.href, true); return; }
        e.preventDefault();
        closeCase(true);
        if (url.hash) { var t = $(url.hash); if (t) t.scrollIntoView({ behavior: reduce ? "auto" : "smooth" }); }
      });
    }

    function loadCase(url, push) {
      openUrl = url;
      sheetScroll.innerHTML = '<div class="sheet__loading" role="status">Carregando case…</div>';
      sheetScroll.scrollTop = 0;
      observers.forEach(function (io) { io.disconnect(); });
      observers = [];
      return fetch(url, { credentials: "same-origin" }).then(function (r) {
        if (!r.ok) throw new Error(r.status);
        return r.text();
      }).then(function (html) {
        if (openUrl !== url) return;
        var page = new DOMParser().parseFromString(html, "text/html");
        var main = $("main", page);
        if (!main) throw new Error("sem conteúdo");
        absolutize(main, url);
        var h1 = $("h1", main);
        sheetTitle.textContent = h1 ? h1.textContent.trim() : "";
        sheetScroll.innerHTML = "";
        var wrap = document.createElement("div");
        wrap.className = "sheet__content";
        while (main.firstChild) wrap.appendChild(document.adoptNode(main.firstChild));
        sheetScroll.appendChild(wrap);
        sheetScroll.scrollTop = 0;
        initReveal(wrap);
        $$(".ia__stage", wrap).forEach(initStage);
        initVideos(wrap);
        if (push) history.pushState({ rwCase: url }, "", url);
        document.title = (sheetTitle.textContent || "Case") + " | Case RW Company";
        sheetScroll.focus({ preventScroll: true });
      }).catch(function () {
        // se algo falhar, segue para a página do case normalmente
        location.href = url;
      });
    }

    function openCase(url, trigger) {
      if (!sheet) buildSheet();
      lastFocus = trigger || document.activeElement;
      background.forEach(function (el) { el.setAttribute("inert", ""); });
      doc.classList.add("has-sheet");
      sheet.classList.add("is-open");
      if (!reduce && sheet.animate) {
        sheet.animate([{ opacity: 0, transform: "translateY(32px)" }, { opacity: 1, transform: "none" }], { duration: 480, easing: "cubic-bezier(0.16,1,0.3,1)" });
      }
      $(".sheet__close", sheet).focus({ preventScroll: true });
      loadCase(url, true);
    }

    function closeCase(viaUi) {
      if (!sheet || !sheet.classList.contains("is-open")) return;
      observers.forEach(function (io) { io.disconnect(); });
      observers = [];
      $$("video", sheet).forEach(function (v) { v.pause(); });
      var finish = function () {
        sheet.classList.remove("is-open");
        sheetScroll.innerHTML = "";
        doc.classList.remove("has-sheet");
        background.forEach(function (el) { el.removeAttribute("inert"); });
        document.title = homeTitle;
        if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
      };
      if (!reduce && sheet.animate) {
        sheet.animate([{ opacity: 1, transform: "none" }, { opacity: 0, transform: "translateY(24px)" }], { duration: 240, easing: "cubic-bezier(0.55,0,1,0.45)" }).onfinish = finish;
      } else finish();
      openUrl = null;
      if (viaUi && history.state && history.state.rwCase) history.back();
    }

    var homeTitle = document.title;
    casesGrid.addEventListener("click", function (e) {
      var card = e.target.closest(".case");
      if (!card || e.metaKey || e.ctrlKey || e.shiftKey || e.button > 0) return;
      var link = $(".case__link", card);
      if (!link) return;
      e.preventDefault();
      openCase(link.href, link);
    });
    window.addEventListener("popstate", function (e) {
      if (e.state && e.state.rwCase) {
        if (!sheet || !sheet.classList.contains("is-open")) openCase(e.state.rwCase); else loadCase(e.state.rwCase, false);
      } else closeCase(false);
    });
    history.replaceState(history.state || {}, "", homeUrl);
  }

  onScroll();
})();
