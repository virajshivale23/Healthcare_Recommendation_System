/* ============================================================
   HealthAI+  —  script.js
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ---------- Navbar shadow + mobile toggle ---------- */
  const navbar = document.getElementById('navbar');
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');

  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 30);
    toggleBackToTop();
  });

  if (navToggle) {
    navToggle.addEventListener('click', () => {
      navLinks.classList.toggle('open');
    });
  }

  document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => navLinks.classList.remove('open'));
  });

  /* ---------- Scroll reveal ---------- */
  const revealEls = document.querySelectorAll('.reveal');
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });
  revealEls.forEach(el => revealObserver.observe(el));

  /* ---------- Counter animation ---------- */
  const counters = document.querySelectorAll('[data-count]');
  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        counterObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });
  counters.forEach(c => counterObserver.observe(c));

  function animateCounter(el) {
    const target = parseInt(el.dataset.count, 10);
    const suffix = el.dataset.suffix || '';
    const duration = 1400;
    const start = performance.now();

    function tick(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.round(eased * target) + suffix;
      if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  /* ---------- Back to top ---------- */
  const backToTop = document.getElementById('backToTop');
  function toggleBackToTop() {
    if (!backToTop) return;
    backToTop.classList.toggle('show', window.scrollY > 500);
  }
  if (backToTop) {
    backToTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ---------- Symptom search filter ---------- */
  const searchInput = document.getElementById('symptomSearch');
  const chips = document.querySelectorAll('.symptom-chip');

  if (searchInput) {
    searchInput.addEventListener('keyup', () => {
      const query = searchInput.value.toLowerCase().trim();
      chips.forEach(chip => {
        const label = chip.dataset.label.toLowerCase();
        chip.classList.toggle('hidden-chip', !label.includes(query));
      });
    });
  }

  /* ---------- Symptom chip select + counter ---------- */
  const selectedCountEl = document.getElementById('selectedCount');

  function updateSelectedCount() {
    const checked = document.querySelectorAll('.symptom-chip input:checked').length;
    if (selectedCountEl) {
      selectedCountEl.querySelector('b').textContent = checked;
    }
  }

  chips.forEach(chip => {
    const input = chip.querySelector('input');
    input.addEventListener('change', () => {
      chip.classList.toggle('checked', input.checked);
      updateSelectedCount();
    });
  });

  /* ---------- Predict form: loading spinner ---------- */
  const predictForm = document.getElementById('predictForm');
  const spinnerOverlay = document.getElementById('spinnerOverlay');

  if (predictForm) {
    predictForm.addEventListener('submit', (e) => {
      const checked = document.querySelectorAll('.symptom-chip input:checked').length;
      if (checked === 0) {
        e.preventDefault();
        shakeCard();
        return;
      }
      if (spinnerOverlay) spinnerOverlay.classList.add('active');
    });
  }

  function shakeCard() {
    const card = document.querySelector('.predict-card');
    if (!card) return;
    card.animate(
      [
        { transform: 'translateX(0)' },
        { transform: 'translateX(-8px)' },
        { transform: 'translateX(8px)' },
        { transform: 'translateX(-6px)' },
        { transform: 'translateX(6px)' },
        { transform: 'translateX(0)' }
      ],
      { duration: 400 }
    );
  }

  /* ---------- Ripple effect on buttons ---------- */
  document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('click', function (e) {
      const rect = this.getBoundingClientRect();
      const ripple = document.createElement('span');
      const size = Math.max(rect.width, rect.height);
      ripple.className = 'ripple';
      ripple.style.width = ripple.style.height = size + 'px';
      ripple.style.left = (e.clientX - rect.left - size / 2) + 'px';
      ripple.style.top = (e.clientY - rect.top - size / 2) + 'px';
      this.appendChild(ripple);
      setTimeout(() => ripple.remove(), 600);
    });
  });

});