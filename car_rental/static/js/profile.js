/* FastCars profile: Save is enabled only after a change, and guards against double submit. */
(function () {
  var form = document.querySelector('.prof-form');
  if (!form) return;

  var submit = form.querySelector('button[type="submit"]');
  var label = submit.textContent;

  function snapshot() {
    return new URLSearchParams(new FormData(form)).toString();
  }

  var initial = snapshot();
  var hasErrors = !!form.querySelector('.has-error, .form-alert');

  function sync() {
    submit.disabled = !hasErrors && snapshot() === initial;
  }

  sync();
  form.addEventListener('input', sync);
  form.addEventListener('change', sync);

  form.addEventListener('submit', function () {
    submit.disabled = true;
    submit.textContent = 'Saving…';
  });

  // Restore the button if the user returns with the browser's back button
  window.addEventListener('pageshow', function () {
    submit.textContent = label;
    initial = snapshot();
    sync();
  });
})();