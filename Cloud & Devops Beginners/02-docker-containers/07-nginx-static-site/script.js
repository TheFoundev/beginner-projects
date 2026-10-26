/**
 * Multi-Page Site - Shared JavaScript
 * Handles: Mobile nav toggle, smooth scroll, visitor counter, form validation
 */
(function() {
  'use strict';

  // ─── Mobile Navigation Toggle ───────────────────
  const navToggle = document.getElementById('navToggle');
  const navList = document.getElementById('navList');

  if (navToggle && navList) {
    navToggle.addEventListener('click', () => {
      navList.classList.toggle('active');
    });
  }

  // ─── Smooth Scrolling ───────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        if (navList && navList.classList.contains('active')) {
          navList.classList.remove('active');
        }
      }
    });
  });

  // ─── Visitor Counter (localStorage) ─────────────
  function initVisitorCounter() {
    const counterEl = document.getElementById('counter');
    if (!counterEl) return;

    let count = parseInt(localStorage.getItem('visitorCount') || '0');
    count += 1;
    localStorage.setItem('visitorCount', count);
    counterEl.textContent = count;

    // Animate the counter
    counterEl.style.transform = 'scale(1.2)';
    setTimeout(() => {
      counterEl.style.transform = 'scale(1)';
    }, 200);
  }

  // Initialize counter on home page only
  if (window.location.pathname.includes('index.html') || window.location.pathname === '/') {
    initVisitorCounter();
  }

  // ─── Contact Form Validation ───────────────────
  const contactForm = document.getElementById('contactForm');
  const formStatus = document.getElementById('formStatus');

  if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
      e.preventDefault();

      const formData = new FormData(contactForm);
      const data = Object.fromEntries(formData);

      // Validate required fields
      const requiredFields = ['name', 'email', 'subject', 'message'];
      const missing = requiredFields.filter(f => !data[f]);

      if (missing.length > 0) {
        showStatus(`Missing: ${missing.join(', ')}`, 'error');
        return;
      }

      // Email validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(data.email)) {
        showStatus('Please enter a valid email address.', 'error');
        return;
      }

      // Simulate submission
      showStatus('Sending message...', 'success');
      setTimeout(() => {
        contactForm.reset();
        showStatus('Thank you! Your message has been sent.', 'success');
      }, 800);
    });
  }

  function showStatus(message, type) {
    if (!formStatus) return;
    formStatus.textContent = message;
    formStatus.className = `form-status ${type}`;
    formStatus.style.display = 'block';
    setTimeout(() => {
      if (formStatus.classList.contains('success') && !message.includes('Sending')) {
        formStatus.style.display = 'none';
      }
    }, 3000);
  }

  // ─── Active Nav Link ───────────────────────────
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-link').forEach(link => {
    link.classList.remove('active');
    if (link.getAttribute('href') === currentPage) {
      link.classList.add('active');
    }
  });

  console.log('Multi-page site JavaScript loaded. Hosted with Nginx in Docker.');
})();
