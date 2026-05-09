/* =========================================================
   Student Hub – Main JS
   Multi-step form, validations, micro-interactions
   ========================================================= */

'use strict';

// ── Nav scroll effect ────────────────────────────────────
const nav = document.querySelector('.nav');
if (nav) {
  window.addEventListener('scroll', () => {
    nav.classList.toggle('nav--scrolled', window.scrollY > 10);
  }, { passive: true });
}

// ── Flash auto-dismiss ───────────────────────────────────
document.querySelectorAll('.flash').forEach(el => {
  setTimeout(() => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(-6px)';
    el.style.transition = 'opacity 0.4s, transform 0.4s';
    setTimeout(() => el.remove(), 400);
  }, 5000);
});

// ── Multi-step Registration Form ─────────────────────────
(function initMultiStep() {
  const panels = document.querySelectorAll('.form-panel');
  const steps  = document.querySelectorAll('.step');
  const form   = document.getElementById('registration-form');
  if (!form || panels.length === 0) return;

  let currentStep = 0;

  // If server returned step errors (form re-render after submit),
  // jump to the first step that has errors.
  const serverErrors = document.querySelectorAll('.form-control.is-invalid');
  if (serverErrors.length > 0) {
    const firstErr = serverErrors[0];
    const panel = firstErr.closest('.form-panel');
    if (panel) {
      currentStep = [...panels].indexOf(panel);
    }
  }

  function showStep(idx) {
    panels.forEach((p, i) => p.classList.toggle('active', i === idx));
    steps.forEach((s, i) => {
      s.classList.remove('active', 'completed');
      if (i < idx)  s.classList.add('completed');
      if (i === idx) s.classList.add('active');
    });
    window.scrollTo({ top: 0, behavior: 'smooth' });
    currentStep = idx;
  }

  showStep(currentStep);

  // Step-specific field lists for inline validation
  const stepFields = [
    ['first_name', 'last_name', 'dob', 'gender', 'email', 'phone'],
    ['street', 'city', 'state', 'zip_code', 'country'],
    ['high_school', 'graduation_year', 'major', 'enrollment_type'],
    ['password', 'confirm_password', 'terms'],
  ];

  function validateField(el) {
    if (!el) return true;
    let valid = true;
    const val = el.value.trim();

    // Required
    if (el.required && val === '') valid = false;

    // Min-length
    if (el.minLength > 0 && val.length < el.minLength) valid = false;

    // Email
    if (el.type === 'email' && val && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)) valid = false;

    // Tel – allow +, digits, spaces, dashes, parens
    if (el.type === 'tel' && val && !/^\+?[\d\s\-\(\)]{7,20}$/.test(val)) valid = false;

    // Number range
    if (el.type === 'number' || el.tagName === 'INPUT' && el.dataset.type === 'year') {
      const n = parseInt(val, 10);
      if (el.min && n < parseInt(el.min, 10)) valid = false;
      if (el.max && n > parseInt(el.max, 10)) valid = false;
    }

    el.classList.toggle('is-invalid', !valid);
    el.classList.toggle('is-valid', valid && val !== '');
    return valid;
  }

  function validateStep(idx) {
    const names = stepFields[idx] || [];
    let ok = true;
    names.forEach(name => {
      const el = form.querySelector(`[name="${name}"]`);
      if (!validateField(el)) ok = false;
    });

    // Password confirmation cross-check
    if (idx === 3) {
      const pw  = form.querySelector('[name="password"]');
      const cpw = form.querySelector('[name="confirm_password"]');
      if (pw && cpw && pw.value !== cpw.value) {
        cpw.classList.add('is-invalid');
        cpw.classList.remove('is-valid');
        ok = false;
      }
      const toggle = form.querySelector('[name="terms"]');
      if (toggle && !toggle.checked) ok = false;
    }
    return ok;
  }

  // Next buttons
  document.querySelectorAll('[data-next]').forEach(btn => {
    btn.addEventListener('click', () => {
      if (validateStep(currentStep) && currentStep < panels.length - 1) {
        showStep(currentStep + 1);
      }
    });
  });

  // Back buttons
  document.querySelectorAll('[data-prev]').forEach(btn => {
    btn.addEventListener('click', () => {
      if (currentStep > 0) showStep(currentStep - 1);
    });
  });

  // Live validation on blur
  form.querySelectorAll('.form-control').forEach(el => {
    el.addEventListener('blur', () => validateField(el));
    el.addEventListener('input', () => {
      if (el.classList.contains('is-invalid')) validateField(el);
    });
  });

  // Final submit validation
  form.addEventListener('submit', e => {
    let firstBad = -1;
    stepFields.forEach((_, i) => {
      if (!validateStep(i) && firstBad === -1) firstBad = i;
    });
    if (firstBad >= 0) {
      e.preventDefault();
      showStep(firstBad);
    }
  });
})();

// ── Password strength meter ───────────────────────────────
(function initPasswordStrength() {
  const pw  = document.querySelector('[name="password"]');
  const bar = document.querySelector('.password-strength__bar');
  const lbl = document.querySelector('.strength-label');
  if (!pw || !bar) return;

  const levels = [
    { max: 0,  color: '#FF3B30', text: '' },
    { max: 1,  color: '#FF3B30', text: 'Weak' },
    { max: 2,  color: '#FF9500', text: 'Fair' },
    { max: 3,  color: '#007AFF', text: 'Good' },
    { max: 4,  color: '#34C759', text: 'Strong' },
  ];

  pw.addEventListener('input', () => {
    const v = pw.value;
    let score = 0;
    if (v.length >= 8) score++;
    if (/[A-Z]/.test(v)) score++;
    if (/[0-9]/.test(v)) score++;
    if (/[^A-Za-z0-9]/.test(v)) score++;

    const pct = (score / 4) * 100;
    const lvl = levels[score];
    bar.style.width = pct + '%';
    bar.style.background = lvl.color;
    if (lbl) { lbl.textContent = lvl.text; lbl.style.color = lvl.color; }
  });
})();

// ── iOS toggle (checkbox) clicks ─────────────────────────
document.querySelectorAll('.toggle-track').forEach(track => {
  track.addEventListener('click', () => {
    const input = track.previousElementSibling;
    if (input && input.type === 'checkbox') {
      input.checked = !input.checked;
      input.dispatchEvent(new Event('change'));
    }
  });
});

// ── Admin table – column sort arrows ─────────────────────
(function initSortArrows() {
  const headers = document.querySelectorAll('.data-table th[data-sort]');
  headers.forEach(th => {
    const col = th.dataset.sort;
    const url = new URL(window.location.href);
    const cur = url.searchParams.get('sort');
    const ord = url.searchParams.get('order') || 'desc';
    if (cur === col) {
      th.querySelector('a').innerHTML += ord === 'asc' ? ' ↑' : ' ↓';
    }
  });
})();

// ── Profile completion ring animation ────────────────────
(function initProgressRing() {
  const fill = document.querySelector('.progress-ring__fill');
  if (!fill) return;
  const pct = parseInt(fill.dataset.pct, 10) || 0;
  const r   = parseFloat(fill.getAttribute('r')) || 40;
  const circ = 2 * Math.PI * r;
  fill.style.strokeDasharray  = circ;
  fill.style.strokeDashoffset = circ;
  requestAnimationFrame(() => {
    fill.style.strokeDashoffset = circ * (1 - pct / 100);
  });
})();
