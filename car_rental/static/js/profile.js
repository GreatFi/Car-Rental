/* FastCars profile: time-of-day greeting, completeness meter, save/discard on change. */
(function () {
  // Greeting (server-rendered text is "Welcome back" if JS is off)
  var greet = document.querySelector('[data-greeting]');
  if (greet) {
    var h = new Date().getHours();
    greet.textContent = h < 12 ? 'Good morning' : h < 17 ? 'Good afternoon' : 'Good evening';
  }

  var form = document.querySelector('.prof-form');
  if (!form) return;

  var submit = form.querySelector('button[type="submit"]');
  var discard = form.querySelector('[data-discard]');
  var label = submit.textContent;

  function snapshot() {
    return new URLSearchParams(new FormData(form)).toString();
  }

  var initial = snapshot();
  var hasErrors = !!form.querySelector('.has-error, .form-alert');

  // Completeness meter: how many of the editable fields have a value
  var meter = document.querySelector('[data-meter]');
  var fields = [].slice.call(form.querySelectorAll('input:not([type="hidden"]):not([type="checkbox"]):not([type="radio"]), select, textarea'));

  function updateMeter() {
    if (!meter || !fields.length) return;
    var done = fields.filter(function (f) { return f.value.trim() !== ''; }).length;
    meter.querySelector('.prof-meter-text').textContent =
      done === fields.length ? 'All details added' : done + ' of ' + fields.length + ' details added';
    meter.querySelector('.prof-meter-bar span').style.width = Math.round((done / fields.length) * 100) + '%';
    meter.hidden = false;
  }

  // Save is only enabled after a change; Discard appears with it
  function sync() {
    var dirty = snapshot() !== initial;
    submit.disabled = !hasErrors && !dirty;
    if (discard) discard.hidden = !dirty;
    updateMeter();
  }

  sync();
  form.addEventListener('input', sync);
  form.addEventListener('change', sync);
  form.addEventListener('reset', function () { setTimeout(sync, 0); });

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