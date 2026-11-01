/* seovisi.com.tr — site betiği (derleme yok, dış kaynak yok).
   1) Üst menü: kaydırınca belirginleşir, altındaki zemine göre koyu/açık cam olur
   2) Dar ekranda menü   3) Fareyle ışık ve eğim efektleri
   Betik çalışmazsa site eksiksiz çalışır; menü koyu cam kalır, yalnızca bu efektler olmaz. */
(function () {
  "use strict";

  var kok = document.documentElement;
  var hareketAzalt = window.matchMedia("(prefers-reduced-motion: reduce)");

  /* 1) Üst menü */
  var ust = document.querySelector(".ust");
  var iste = function () {};
  if (ust) {
    var yapraklar = Array.prototype.slice.call(document.querySelectorAll(".yaprak"));
    var bekliyor = false;
    var guncelle = function () {
      bekliyor = false;
      ust.classList.toggle("kaydi", window.scrollY > 12);
      var acik = false;
      if (!kok.classList.contains("menu-acik")) {
        var kapsul = ust.firstElementChild;
        var k = kapsul ? kapsul.getBoundingClientRect() : null;
        var orta = k ? k.top + k.height / 2 : 43;
        for (var i = 0; i < yapraklar.length; i++) {
          var r = yapraklar[i].getBoundingClientRect();
          if (r.top <= orta && r.bottom >= orta) {
            acik = true;
            break;
          }
        }
      }
      ust.classList.toggle("acik-zemin", acik);
    };
    iste = function () {
      if (!bekliyor) {
        bekliyor = true;
        window.requestAnimationFrame(guncelle);
      }
    };
    window.addEventListener("scroll", iste, { passive: true });
    window.addEventListener("resize", iste, { passive: true });
    iste();
  }

  /* 2) Dar ekranda menü */
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
      iste();
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

  /* 3) Fareyle ışık takibi ve giriş panelinin hafif eğimi (yalnızca fare kullananlarda) */
  if (!window.matchMedia("(hover: hover) and (pointer: fine)").matches || hareketAzalt.matches) return;

  document.addEventListener("pointermove", function (olay) {
    var kart = olay.target.closest ? olay.target.closest(".isikli") : null;
    if (!kart) return;
    var r = kart.getBoundingClientRect();
    kart.style.setProperty("--mx", (olay.clientX - r.left) + "px");
    kart.style.setProperty("--my", (olay.clientY - r.top) + "px");
  }, { passive: true });

  // Giriş bölümünde fareyi izleyen yumuşak ışık
  var kahraman = document.querySelector("[data-isik]");
  var isik = kahraman ? kahraman.querySelector(".isik-takip") : null;
  if (kahraman && isik) {
    var isikBekliyor = 0;
    var isikX = 0;
    var isikY = 0;
    kahraman.addEventListener("pointermove", function (olay) {
      var r = kahraman.getBoundingClientRect();
      isikX = olay.clientX - r.left;
      isikY = olay.clientY - r.top;
      if (isikBekliyor) return;
      isikBekliyor = window.requestAnimationFrame(function () {
        isikBekliyor = 0;
        isik.style.setProperty("--tx", isikX + "px");
        isik.style.setProperty("--ty", isikY + "px");
        kahraman.classList.add("isik-acik");
      });
    }, { passive: true });
    kahraman.addEventListener("pointerleave", function () {
      kahraman.classList.remove("isik-acik");
    });
  }

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
