/* FastCars booking history: status filter tabs with counts. No dependencies. */
(function () {
  var tabs = document.querySelector('.hist-tabs');
  var cards = [].slice.call(document.querySelectorAll('.hist-card'));
  var none = document.querySelector('.hist-none');
  if (!tabs || !cards.length) return;

  var buttons = [].slice.call(tabs.querySelectorAll('.hist-tab'));

  // Counts per status; hide tabs for statuses the user has none of
  buttons.forEach(function (btn) {
    var key = btn.getAttribute('data-filter');
    var n = key === 'all'
      ? cards.length
      : cards.filter(function (c) { return c.getAttribute('data-status') === key; }).length;
    btn.querySelector('.hist-count').textContent = n;
    if (key !== 'all' && n === 0) btn.hidden = true;
  });

  // Only worth showing if there is something to filter between
  var visibleTabs = buttons.filter(function (b) { return !b.hidden; });
  if (visibleTabs.length < 3) return;
  tabs.hidden = false;

  function apply(key) {
    var shown = 0;
    cards.forEach(function (card) {
      var match = key === 'all' || card.getAttribute('data-status') === key;
      card.hidden = !match;
      if (match) shown++;
    });
    if (none) none.hidden = shown > 0;
    buttons.forEach(function (b) {
      var on = b.getAttribute('data-filter') === key;
      b.classList.toggle('is-active', on);
      b.setAttribute('aria-pressed', String(on));
    });
  }

  buttons.forEach(function (btn) {
    btn.addEventListener('click', function () { apply(btn.getAttribute('data-filter')); });
  });
})();