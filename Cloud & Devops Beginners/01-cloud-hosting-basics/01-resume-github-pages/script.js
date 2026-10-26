/**
 * Resume Theme Toggle & Animations
 * Handles:
 *   1. Dark/light mode toggle (persisted in localStorage)
 *   2. Smooth scroll behavior
 *   3. Animation triggers on scroll
 */

(function() {
  'use strict';

  // ─── Theme Toggle ─────────────────────────────────
  const themeToggleBtn = document.getElementById('themeToggle');
  const themeIcon = document.getElementById('themeIcon');
  const body = document.body;

  // Check for saved theme preference
  const savedTheme = localStorage.getItem('theme');

  if (savedTheme === 'dark') {
    body.setAttribute('data-theme', 'dark');
    themeIcon.textContent = '☀️';
  }

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', function() {
      const currentTheme = body.getAttribute('data-theme');
      if (currentTheme === 'dark') {
        body.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
        themeIcon.textContent = '🌙';
      } else {
        body.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
        themeIcon.textContent = '☀️';
      }
    });
  }

  // ─── Smooth Scroll ─────────────────────────────────
  // Enable smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // ─── Scroll Animations ─────────────────────────────
  // Add 'visible' class to sections when they enter viewport
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target); // Stop observing once visible
      }
    });
  }, observerOptions);

  // Observe all sections
  document.querySelectorAll('.resume-section').forEach(section => {
    observer.observe(section);
  });

  // ─── Profile Image Error Handling ──────────────────
  const profileImg = document.getElementById('profileImage');
  if (profileImg) {
    profileImg.addEventListener('error', function() {
      // If the image fails to load, hide it gracefully
      this.style.display = 'none';
    });
  }

  // ─── Console Greeting ──────────────────────────────
  console.log('Resume loaded successfully!');
  console.log('Theme: ' + (body.getAttribute('data-theme') || 'light'));
})();
