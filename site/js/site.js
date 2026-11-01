/* seovisi.com.tr — site betiği (derleme yok, dış kaynak yok).
   1) Dar ekranda menü   2) Kaydırınca üst bölüm   3) Fareyle ışık ve eğim efektleri
   Betik çalışmazsa site eksiksiz çalışır; yalnızca bu efektler olmaz. */
(function () {
  "use strict";

  var kok = document.documentElement;
  var hareketAzalt = window.matchMedia("(prefers-reduced-motion: reduce)");

  /* 1) Menü */
  var dugme = document.querySelector("[data-menu-dugme]");
  var menu = document.getElementById("ana-menu");
  if (dugme && menu) {
    var yazi = dugme.querySelector(".menu-yazi");
    dugme.setAttribute("role", "button");
    dugme.setAttribute("aria-controls", "ana-menu");
    dugme.setAttribute("aria-expanded", "false");

    var ayarla = function (acik) {
      dugme.setAttribute("aria-expanded", acik ? "true" : "false");
      menu.classList.toggle("acik", acik);
      kok.classList.toggle("menu-acik", acik);
      if (yazi) yazi.textContent = acik ? "Kapat" : "Menü";
      if (acik) {
        var ilk = menu.querySelector("a");
        if (ilk) ilk.focus();
      }
    };

    dugme.addEventListener("click", function (olay) {
      olay.preventDefault();
      ayarla(dugme.getAttribute("aria-expanded") !== "true");
    });
    dugme.addEventListener("keydown", function (olay) {
      if (olay.key === " ") {
        olay.preventDefault();
        dugme.click();
      }
    });
    document.addEventListener("keydown", function (olay) {
      if (olay.key === "Escape" && menu.classList.contains("acik")) {
        ayarla(false);
        dugme.focus();
      }
    });
    menu.addEventListener("click", function (olay) {
      if (olay.target.closest("a")) ayarla(false);
    });
    window.matchMedia("(min-width: 1024px)").addEventListener("change", function (olay) {
      if (olay.matches) ayarla(false);
    });
  }

  /* 2) Kaydırınca üst bölüm belirginleşir */
  var ust = document.querySelector(".ust");
  if (ust) {
    var kaydi = null;
    var bak = function () {
      var simdi = window.scrollY > 12;
      if (simdi !== kaydi) {
        kaydi = simdi;
        ust.classList.toggle("kaydi", simdi);
      }
    };
    window.addEventListener("scroll", bak, { passive: true });
    bak();
  }

  /* 3) Fareyle ışık takibi ve giriş panelinin hafif eğimi (yalnızca fare kullananlarda) */
  if (!window.matchMedia("(hover: hover) and (pointer: fine)").matches || hareketAzalt.matches) return;

  document.addEventListener("pointermove", function (olay) {
    var kart = olay.target.closest ? olay.target.closest(".isikli") : null;
    if (!kart) return;
    var r = kart.getBoundingClientRect();
    kart.style.setProperty("--mx", (olay.clientX - r.left) + "px");
    kart.style.setProperty("--my", (olay.clientY - r.top) + "px");
  }, { passive: true });

  var sahne = document.querySelector("[data-egim]");
  var panel = sahne ? sahne.querySelector(".panel") : null;
  if (!panel) return;
  var genisEkran = window.matchMedia("(min-width: 1080px)");
  var bekleyen = 0;
  sahne.addEventListener("pointermove", function (olay) {
    if (!genisEkran.matches || bekleyen) return;
    var r = sahne.getBoundingClientRect();
    var x = (olay.clientX - r.left) / r.width - 0.5;
    var y = (olay.clientY - r.top) / r.height - 0.5;
    bekleyen = window.requestAnimationFrame(function () {
      bekleyen = 0;
      panel.style.setProperty("--ry", (-11 + x * 12).toFixed(2) + "deg");
      panel.style.setProperty("--rx", (5 - y * 9).toFixed(2) + "deg");
    });
  }, { passive: true });
  sahne.addEventListener("pointerleave", function () {
    panel.style.removeProperty("--ry");
    panel.style.removeProperty("--rx");
  });
})();
