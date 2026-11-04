// Francês da Thaís: áudio inline, menu no celular e checkboxes que lembram o progresso.
(function () {
  // 🔊 Áudio: cada link para .mp3 vira um botão que toca na própria página.
  var atual = null, botaoAtual = null;
  document.querySelectorAll('a[href$=".mp3"]').forEach(function (a) {
    a.classList.add("audio");
    a.setAttribute("role", "button");
    a.setAttribute("title", "Ouvir");
    a.addEventListener("click", function (ev) {
      ev.preventDefault();
      if (botaoAtual === a && atual && !atual.paused) { atual.pause(); a.classList.remove("tocando"); return; }
      if (atual) { atual.pause(); if (botaoAtual) botaoAtual.classList.remove("tocando"); }
      atual = new Audio(a.getAttribute("href"));
      botaoAtual = a;
      a.classList.add("tocando");
      atual.addEventListener("ended", function () { a.classList.remove("tocando"); });
      atual.play().catch(function () { a.classList.remove("tocando"); });
    });
  });

  // ☰ Menu no celular
  var btn = document.querySelector(".abrir-menu");
  if (btn) btn.addEventListener("click", function () {
    var aberto = document.body.classList.toggle("menu-aberto");
    btn.setAttribute("aria-expanded", aberto ? "true" : "false");
  });

  // ✅ Checkboxes: ficam salvos neste navegador (localStorage).
  var pagina = document.body.getAttribute("data-pagina") || location.pathname;
  document.querySelectorAll("li.task input[type=checkbox]").forEach(function (cb, i) {
    var chave = "frances-thais:" + pagina + ":" + i;
    var salvo = localStorage.getItem(chave);
    if (salvo !== null) cb.checked = salvo === "1";
    cb.addEventListener("change", function () { localStorage.setItem(chave, cb.checked ? "1" : "0"); });
  });
})();
