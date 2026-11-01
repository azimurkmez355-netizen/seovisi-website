/* seovisi.com.tr — tek betik: dar ekranda menüyü açıp kapatır.
   Betik çalışmazsa "Menü" bağlantısı sayfanın altındaki menüye götürür. */
(function () {
  var dugme = document.querySelector("[data-menu-dugme]");
  var menu = document.getElementById("ana-menu");
  if (!dugme || !menu) return;

  dugme.setAttribute("role", "button");
  dugme.setAttribute("aria-controls", "ana-menu");
  dugme.setAttribute("aria-expanded", "false");

  function ayarla(acik) {
    dugme.setAttribute("aria-expanded", acik ? "true" : "false");
    menu.classList.toggle("acik", acik);
  }

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
    if (olay.key === "Escape" && dugme.getAttribute("aria-expanded") === "true") {
      ayarla(false);
      dugme.focus();
    }
  });

  menu.addEventListener("click", function (olay) {
    if (olay.target.closest("a")) ayarla(false);
  });

  window.matchMedia("(min-width: 1024px)").addEventListener("change", function (e) {
    if (e.matches) ayarla(false);
  });
})();
