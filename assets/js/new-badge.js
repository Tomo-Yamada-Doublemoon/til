(function () {
  const NEW_DAYS = 7;

  document.addEventListener("DOMContentLoaded", function () {
    const now = new Date();

    // Chirpy v7 の構造: .post-meta の中に time 要素がある
    document.querySelectorAll('.post-meta time').forEach(function (el) {
      const datetime = el.getAttribute('datetime') || el.getAttribute('data-ts') || el.textContent.trim();
      const postDate = new Date(datetime);

      if (isNaN(postDate)) return;

      const diffDays = (now - postDate) / (1000 * 60 * 60 * 24);
      if (diffDays > NEW_DAYS) return;

      // .post-meta → 親をたどって article まで上がる
      const article = el.closest('article');
      if (!article) return;

      // article の中から h1 または タイトルリンクを探す
      const titleEl = article.querySelector('h1, h2, .card-title, a[href] h1, a[href] h2');
      if (!titleEl || titleEl.querySelector('.new-badge')) return;

      const badge = document.createElement('span');
      badge.className = 'new-badge';
      badge.textContent = '🆕 New!';
      titleEl.appendChild(badge);
    });
  });
})();
