(function () {
  // ★ここを変えると「何日以内をNEWにするか」が変わります
  const NEW_DAYS = 7;

  document.addEventListener("DOMContentLoaded", function () {
    const now = new Date();

    const timeElements = document.querySelectorAll("time[datetime], [data-ts]");

    timeElements.forEach(function (el) {
      let postDate;

      if (el.hasAttribute("data-ts")) {
        postDate = new Date(parseInt(el.getAttribute("data-ts")));
      } else {
        postDate = new Date(el.getAttribute("datetime"));
      }

      if (isNaN(postDate)) return;

      const diffDays = (now - postDate) / (1000 * 60 * 60 * 24);

      if (diffDays <= NEW_DAYS) {
        const card = el.closest("article, li, .post-preview, div");
        if (!card) return;

        const titleEl = card.querySelector("h1, h2, h3, a.post-title, a");
        if (titleEl && !titleEl.querySelector(".new-badge")) {
          const badge = document.createElement("span");
          badge.className = "new-badge";
          badge.textContent = "🆕 New!";
          titleEl.appendChild(badge);
        }
      }
    });
  });
})();
