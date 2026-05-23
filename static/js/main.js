'use strict';

// ── Dark Mode Toggle ─────────────────────────────────────────────
(function initDarkMode() {
  const toggle = document.getElementById('theme-toggle');
  const icon   = document.getElementById('theme-icon');
  if (!toggle) return;

  // Restore saved preference or respect system
  const saved = localStorage.getItem('theme');
  if (saved) {
    document.documentElement.setAttribute('data-theme', saved);
  } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    document.documentElement.setAttribute('data-theme', 'dark');
  }
  updateIcon();

  toggle.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    updateIcon();
  });

  function updateIcon() {
    if (!icon) return;
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    icon.textContent = isDark ? 'light_mode' : 'dark_mode';
    icon.style.transform = `rotate(${isDark ? '180' : '0'}deg)`;
  }
})();

// ── Toast Flash Auto-dismiss ─────────────────────────────────────
(function initToasts() {
  setTimeout(() => {
    document.querySelectorAll('[data-flash]').forEach(el => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(-8px)';
      el.style.transition = 'opacity 0.4s, transform 0.4s';
      setTimeout(() => el.remove(), 400);
    });
  }, 5000);
})();

// ── Multi-step registration form ─────────────────────────────────
(function initMultiStep() {
  const panels = document.querySelectorAll('.form-panel');
  const dots   = document.querySelectorAll('.step-dot');
  const form   = document.getElementById('registration-form');
  if (!form || panels.length === 0) return;

  const titles = ['Personal Information', 'Address Details', 'Academic Details', 'Create Account'];
  let current  = 0;

  // Jump to first panel that has server-side errors
  document.querySelectorAll('.field-error').forEach(el => {
    const panel = el.closest('.form-panel');
    if (panel) {
      const idx = [...panels].indexOf(panel);
      if (idx < current || current === 0) current = idx;
    }
  });

  function showStep(idx) {
    panels.forEach((p, i) => p.classList.toggle('hidden', i !== idx));

    dots.forEach((d, i) => {
      d.className = 'step-dot w-7 h-7 rounded-full flex items-center justify-center text-caption font-bold transition-all duration-300 ';
      if (i < idx) {
        d.classList.add('bg-secondary', 'text-on-secondary');
        d.innerHTML = '<span class="material-symbols-outlined text-[14px]">check</span>';
      } else if (i === idx) {
        d.classList.add('bg-primary', 'text-on-primary');
        d.textContent = i + 1;
      } else {
        d.classList.add('bg-surface-container-highest', 'text-on-surface-variant');
        d.textContent = i + 1;
      }
    });

    const pct = Math.round(((idx + 1) / panels.length) * 100);
    const bar = document.getElementById('progress-bar');
    if (bar) bar.style.width = pct + '%';

    const lbl = document.getElementById('step-label');
    if (lbl) lbl.textContent = `Step ${idx + 1} of ${panels.length}`;

    const pctEl = document.getElementById('step-pct');
    if (pctEl) pctEl.textContent = pct + '% Complete';

    const titleEl = document.getElementById('step-title');
    if (titleEl) titleEl.textContent = titles[idx] || '';

    current = idx;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  showStep(current);

  const stepFields = [
    ['first_name','last_name','dob','gender','email','phone'],
    ['street','city','state','zip_code','country'],
    ['high_school','graduation_year','major','enrollment_type'],
    ['password','confirm_password','terms'],
  ];

  function validateStep(idx) {
    let ok = true;
    (stepFields[idx] || []).forEach(name => {
      const el = form.querySelector(`[name="${name}"]`);
      if (!el) return;
      if (el.type === 'checkbox') { if (!el.checked) ok = false; return; }
      const v = el.value.trim();
      if (el.required && !v) { ok = false; return; }
      if (el.type === 'email' && v && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) ok = false;
      if (el.type === 'tel' && v && !/^\+?[\d\s\-\(\)]{7,20}$/.test(v)) ok = false;
    });
    if (idx === 3) {
      const pw  = form.querySelector('[name="password"]');
      const cpw = form.querySelector('[name="confirm_password"]');
      if (pw && cpw && pw.value !== cpw.value) ok = false;
    }
    return ok;
  }

  document.querySelectorAll('[data-next]').forEach(btn =>
    btn.addEventListener('click', () => { if (current < panels.length - 1) showStep(current + 1); })
  );
  document.querySelectorAll('[data-prev]').forEach(btn =>
    btn.addEventListener('click', () => { if (current > 0) showStep(current - 1); })
  );

  form.addEventListener('submit', e => {
    let firstBad = -1;
    stepFields.forEach((_, i) => { if (!validateStep(i) && firstBad === -1) firstBad = i; });
    if (firstBad >= 0) { e.preventDefault(); showStep(firstBad); }
  });
})();

// ── Password strength meter ───────────────────────────────────────
(function initPasswordStrength() {
  const pw  = document.querySelector('[name="password"]');
  const bar = document.getElementById('password-strength-bar');
  const lbl = document.getElementById('strength-label');
  if (!pw || !bar) return;

  pw.addEventListener('input', () => {
    const v = pw.value;
    let score = 0;
    if (v.length >= 8)           score++;
    if (/[A-Z]/.test(v))         score++;
    if (/[0-9]/.test(v))         score++;
    if (/[^A-Za-z0-9]/.test(v))  score++;

    const colors = ['', '#ba1a1a', '#f97316', '#2559bf', '#2c694e'];
    const labels = ['', 'Weak', 'Fair', 'Good', 'Strong'];
    bar.style.width      = (score / 4 * 100) + '%';
    bar.style.background = colors[score] || '';
    if (lbl) { lbl.textContent = labels[score]; lbl.style.color = colors[score]; }
  });
})();

// ── Scroll-driven nav shadow ──────────────────────────────────────
(function initNavScroll() {
  const nav = document.getElementById('main-nav');
  if (!nav) return;
  window.addEventListener('scroll', () => {
    if (window.scrollY > 10) {
      nav.style.boxShadow = '0 4px 20px rgba(0,0,0,0.08)';
    } else {
      nav.style.boxShadow = '0 1px 3px rgba(0,0,0,0.05)';
    }
  }, { passive: true });
})();
