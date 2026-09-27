/**
 * PADEV Project Main JavaScript
 * Handles responsive navbar, scroll animations, counters, and UI triggers.
 */

document.addEventListener('DOMContentLoaded', () => {
  initMobileMenu();
  initStickyHeader();
  initCounters();
  initModals();
  initHeadlineRotator();
});

/**
 * Hero Headline Rotator
 * Cross-fades the headline lines stored in Site Settings -> Hero Text,
 * one blank line per headline, at a deliberately slow pace.
 */
function initHeadlineRotator() {
  const rotator = document.querySelector('[data-headline-rotator]');
  if (!rotator) return;

  const items = Array.from(rotator.querySelectorAll('.hero-headline'));
  if (items.length < 2) return;

  // Respect visitors who ask for reduced motion: the first line simply stays.
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const interval = parseInt(rotator.dataset.interval, 10) || 7000;
  let index = 0;

  window.setInterval(() => {
    if (document.hidden) return;

    items[index].classList.add('is-hidden');
    items[index].setAttribute('aria-hidden', 'true');

    index = (index + 1) % items.length;

    items[index].classList.remove('is-hidden');
    items[index].removeAttribute('aria-hidden');
  }, interval);
}

/**
 * Mobile Drawer Menu Handler
 */
function initMobileMenu() {
  const menuToggle = document.getElementById('mobile-menu-toggle');
  const menuClose = document.getElementById('mobile-menu-close');
  const mobileDrawer = document.getElementById('mobile-drawer');
  const mobileOverlay = document.getElementById('mobile-overlay');

  if (menuToggle && mobileDrawer && mobileOverlay) {
    const openMenu = () => {
      mobileDrawer.classList.remove('translate-x-full');
      mobileOverlay.classList.remove('hidden');
      document.body.classList.add('overflow-hidden');
    };

    const closeMenu = () => {
      mobileDrawer.classList.add('translate-x-full');
      mobileOverlay.classList.add('hidden');
      document.body.classList.remove('overflow-hidden');
    };

    menuToggle.addEventListener('click', openMenu);
    if (menuClose) menuClose.addEventListener('click', closeMenu);
    mobileOverlay.addEventListener('click', closeMenu);
  }
}

/**
 * Sticky Header Scroll State
 */
function initStickyHeader() {
  const header = document.getElementById('main-header');
  if (!header) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 40) {
      header.classList.add('shadow-md', 'py-2');
      header.classList.remove('py-4');
    } else {
      header.classList.remove('shadow-md', 'py-2');
      header.classList.add('py-4');
    }
  });
}

/**
 * Scroll Triggered Counter Increment
 */
function initCounters() {
  const counters = document.querySelectorAll('.counter-val');
  if (!counters.length) return;

  let animated = false;

  const animateCounters = () => {
    counters.forEach(counter => {
      const target = +counter.getAttribute('data-target');
      const duration = 2000;
      const stepTime = 30;
      const steps = duration / stepTime;
      const increment = target / steps;
      let current = 0;

      const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
          counter.textContent = target.toLocaleString() + (counter.getAttribute('data-suffix') || '');
          clearInterval(timer);
        } else {
          counter.textContent = Math.ceil(current).toLocaleString() + (counter.getAttribute('data-suffix') || '');
        }
      }, stepTime);
    });
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !animated) {
        animateCounters();
        animated = true;
      }
    });
  }, { threshold: 0.3 });

  const counterSection = document.getElementById('counter-section');
  if (counterSection) {
    observer.observe(counterSection);
  }
}

/**
 * Modal Popup Utilities
 */
function initModals() {
  const modalTriggers = document.querySelectorAll('[data-modal-target]');
  const modalCloses = document.querySelectorAll('[data-modal-close]');

  modalTriggers.forEach(trigger => {
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = trigger.getAttribute('data-modal-target');
      const modal = document.getElementById(targetId);
      if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        document.body.classList.add('overflow-hidden');
      }
    });
  });

  modalCloses.forEach(closeBtn => {
    closeBtn.addEventListener('click', () => {
      const modal = closeBtn.closest('.modal-container');
      if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
        document.body.classList.remove('overflow-hidden');
      }
    });
  });
}
