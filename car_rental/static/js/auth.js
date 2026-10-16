/* FastCars password forms (login, register, recover, change password).
   Show/hide toggle, strength hint, match check, double-submit guard. No dependencies. */
(function () {
  var EYE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"/><circle cx="12" cy="12" r="3"/></svg>';
  var EYE_OFF = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10.733 5.076a10.744 10.744 0 0 1 11.205 6.575 1 1 0 0 1 0 .696 10.747 10.747 0 0 1-1.444 2.49"/><path d="M14.084 14.158a3 3 0 0 1-4.242-4.242"/><path d="M17.479 17.499a10.75 10.75 0 0 1-15.417-5.151 1 1 0 0 1 0-.696 10.75 10.75 0 0 1 4.446-5.143"/><path d="m2 2 20 20"/></svg>';
  var LABELS = ['', 'Weak', 'Fair', 'Good', 'Strong'];

  // A hint, not a rule: the server-side password validators still decide
  function level(v) {
    var points = 0;
    if (v.length >= 8) points++;
    if (v.length >= 12) points++;
    if (/[a-z]/.test(v) && /[A-Z]/.test(v)) points++;
    if (/\d/.test(v)) points++;
    if (/[^A-Za-z0-9]/.test(v)) points++;
    if (v.length < 8) return 1;
    return Math.min(4, Math.max(1, points - 1));
  }

  function enhance(form) {
    var first = null;   // the "new password" input
    var second = null;  // the "confirm password" input

    [].slice.call(form.querySelectorAll('input[type="password"]')).forEach(function (input) {
      var wrap = document.createElement('div');
      wrap.className = 'pw';
      input.parentNode.insertBefore(wrap, input);
      wrap.appendChild(input);

      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'pw-toggle';
      btn.setAttribute('aria-label', 'Show password');
      btn.setAttribute('aria-pressed', 'false');
      btn.innerHTML = EYE;
      wrap.appendChild(btn);

      btn.addEventListener('click', function () {
        var show = input.type === 'password';
        input.type = show ? 'text' : 'password';
        btn.innerHTML = show ? EYE_OFF : EYE;
        btn.setAttribute('aria-label', show ? 'Hide password' : 'Show password');
        btn.setAttribute('aria-pressed', String(show));
      });

      var name = input.name || '';
      if (/password1$/.test(name)) first = { input: input, wrap: wrap };
      else if (/password2$/.test(name)) second = { input: input, wrap: wrap };
    });

    if (first) {
      var meter = document.createElement('div');
      meter.className = 'pw-meter';
      meter.hidden = true;
      meter.innerHTML = '<div class="pw-meter-bar"><span></span><span></span><span></span><span></span></div><span class="pw-meter-text"></span>';
      first.wrap.insertAdjacentElement('afterend', meter);

      first.input.addEventListener('input', function () {
        var v = first.input.value;
        if (!v) { meter.hidden = true; return; }
        var lvl = level(v);
        meter.hidden = false;
        meter.setAttribute('data-level', lvl);
        meter.querySelector('.pw-meter-text').textContent = 'Password strength: ' + LABELS[lvl];
      });
    }

    if (first && second) {
      var match = document.createElement('p');
      match.className = 'pw-match';
      match.hidden = true;
      match.setAttribute('aria-live', 'polite');
      second.wrap.insertAdjacentElement('afterend', match);

      var check = function () {
        var a = first.input.value;
        var b = second.input.value;
        if (!b) { match.hidden = true; return; }
        var ok = a === b;
        match.hidden = false;
        match.className = 'pw-match ' + (ok ? 'is-ok' : 'is-bad');
        match.textContent = ok ? 'Passwords match' : "Passwords don't match";
      };
      first.input.addEventListener('input', check);
      second.input.addEventListener('input', check);
    }

    var submit = form.querySelector('button[type="submit"]');
    if (!submit) return;
    var label = submit.textContent;

    form.addEventListener('submit', function () {
      submit.disabled = true;
      submit.textContent = 'Please wait…';
    });

    // Restore the button if the user comes back with the browser's back button
    window.addEventListener('pageshow', function () {
      submit.disabled = false;
      submit.textContent = label;
    });
  }

  [].slice.call(document.querySelectorAll('.auth-form, .pw-form')).forEach(enhance);
})();