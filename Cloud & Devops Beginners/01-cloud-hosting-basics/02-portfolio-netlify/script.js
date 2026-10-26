/**
 * Portfolio Site - Interactive Features
 * Handles:
 *   1. Mobile navigation toggle
 *   2. Smooth scrolling
 *   3. Contact form validation & submission
 *   4. Skill bar animation on scroll
 */

(function() {
  'use strict';

  // ─── Mobile Navigation Toggle ────────────────
  const navToggle = document.getElementById('nav-toggle');
  const navMenu = document.getElementById('nav-menu');

  if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
      navMenu.classList.toggle('active');
    });

    // Close menu when clicking a link
    document.querySelectorAll('.nav__link').forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('active');
      });
    });
  }

  // ─── Smooth Scrolling ────────────────────────
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

  // ─── Skill Bar Animation ────────────────────
  const skillBars = document.querySelectorAll('.skill-progress');

  const animateSkills = () => {
    skillBars.forEach(bar => {
      const rect = bar.getBoundingClientRect();
      const isVisible = rect.top < window.innerHeight - 100;

      if (isVisible && !bar.classList.contains('animated')) {
        const targetWidth = bar.style.width;
        bar.style.width = '0';
        bar.classList.add('animated');
        setTimeout(() => {
          bar.style.width = targetWidth;
        }, 100);
      }
    });
  };

  // Run on scroll and on load
  window.addEventListener('scroll', animateSkills);
  window.addEventListener('load', animateSkills);

  // ─── Contact Form Handling ──────────────────
  const contactForm = document.getElementById('contactForm');
  const formStatus = document.getElementById('formStatus');

  if (contactForm) {
    contactForm.addEventListener('submit', async function(e) {
      e.preventDefault();

      // Get form data
      const formData = new FormData(contactForm);
      const data = Object.fromEntries(formData);

      // Validate
      if (!data.name || !data.email || !data.message) {
        showStatus('Please fill in all fields.', 'error');
        return;
      }

      // Email validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(data.email)) {
        showStatus('Please enter a valid email address.', 'error');
        return;
      }

      // Simulate submission (replace with Formspree, Netlify Forms, etc.)
      showStatus('Sending...', 'success');
      setTimeout(() => {
        contactForm.reset();
        showStatus('Thank you! Your message has been sent successfully.', 'success');
      }, 1000);
    });
  }

  function showStatus(message, type) {
    if (!formStatus) return;
    formStatus.textContent = message;
    formStatus.className = `form-status ${type}`;
    formStatus.style.display = 'block';

    if (type === 'success' && message.includes('sent')) {
      setTimeout(() => {
        formStatus.style.opacity = '0';
      }, 3000);
    }
  }

  // ─── Project Card Hover Effects ─────────────
  document.querySelectorAll('.project-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
      const img = this.querySelector('.project-card__image img');
      if (img) {
        img.style.transform = 'scale(1.05)';
        img.style.transition = 'transform 0.3s ease';
      }
    });
    card.addEventListener('mouseleave', function() {
      const img = this.querySelector('.project-card__image img');
      if (img) {
        img.style.transform = 'scale(1)';
      }
    });
  });

  console.log('Portfolio site loaded. Ready for deployment to Netlify!');
})();
