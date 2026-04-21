(function () {
  const NEW_DAYS = 7;

  document.addEventListener("DOMContentLoaded", function () {
    const now = new Date();

    // Chirpy v7 の実際のDOM構造に対応した複数セレクター
    const selectors = [
      'time[datetime]',
      '[data-ts]',
      'span.date',
      '.post-meta time',
      '.card-footer span',
      'span.timeago'
    ];

    let found = false;

    selectors.forEach(function(sel) {
      const elements = document.querySelectorAll(sel);
      if (elements.length > 0) {
        console.log('[new-badge] セレクター発見:', sel, elements.length + '件');
        found = true;
      }
    });

    if (!found) {
      console.log('[new-badge] 日付要素が見つかりません。全記事カードを確認します');
      // フォールバック：記事カード内のテキストから日付を探す
      const articles = document.querySelectorAll('article, .card-wrapper, li.post-item, .post-preview');
      console.log('[new-badge] 記事要素数:', articles.length);
      articles.forEach(function(art, i) {
        console.log('[new-badge] 記事' + i + ' クラス:', art.className, '| HTML先頭:', art.innerHTML.substring(0, 200));
      });
      return;
    }

    // 日付要素が見つかった場合はバッジを追加
    selectors.forEach(function(sel) {
      document.querySelectorAll(sel).forEach(function(el) {
        let postDate;
        if (el.hasAttribute('data-ts')) {
          postDate = new Date(parseInt(el.getAttribute('data-ts')));
        } else if (el.getAttribute('datetime')) {
          postDate = new Date(el.getAttribute('datetime'));
        } else {
          postDate = new Date(el.textContent.trim());
        }

        if (isNaN(postDate)) return;

        const diffDays = (now - postDate) / (1000 * 60 * 60 * 24);
        if (diffDays <= NEW_DAYS) {
          const card = el.closest('article, li, .card-wrapper, .card, div');
          if (!card) return;
          const titleEl = card.querySelector('h1, h2, h3, a.card-title, .card-title, a');
          if (titleEl && !titleEl.querySelector('.new-badge')) {
            const badge = document.createElement('span');
            badge.className = 'new-badge';
            badge.textContent = '🆕 New!';
            titleEl.appendChild(badge);
          }
        }
      });
    });
  });
})();
