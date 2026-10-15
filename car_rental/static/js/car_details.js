/* FastCars car details: photo viewer. No dependencies. */
(function () {
  var items = [].slice.call(document.querySelectorAll('.gallery-item'));
  var dialog = document.getElementById('lightbox');
  if (!items.length || !dialog) return;

  var img = dialog.querySelector('.lb-img');
  var count = dialog.querySelector('.lb-count');
  var prev = dialog.querySelector('.lb-prev');
  var next = dialog.querySelector('.lb-next');
  var close = dialog.querySelector('.lb-close');
  var current = 0;

  function show(i) {
    current = (i + items.length) % items.length;
    img.src = items[current].getAttribute('data-full');
    img.alt = items[current].querySelector('img').alt;
    count.textContent = (current + 1) + ' / ' + items.length;
  }

  function open(i) {
    show(i);
    if (!dialog.open) dialog.showModal();
  }

  items.forEach(function (el, i) {
    el.addEventListener('click', function () { open(i); });
  });

  var all = document.querySelector('.gallery-all');
  if (all) all.addEventListener('click', function () { open(0); });

  prev.addEventListener('click', function () { show(current - 1); });
  next.addEventListener('click', function () { show(current + 1); });
  close.addEventListener('click', function () { dialog.close(); });

  // Clicking the dark area around the photo closes the viewer
  dialog.addEventListener('click', function (e) {
    if (e.target === dialog) dialog.close();
  });

  dialog.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') show(current - 1);
    if (e.key === 'ArrowRight') show(current + 1);
  });

  if (items.length < 2) { prev.hidden = true; next.hidden = true; }
})();