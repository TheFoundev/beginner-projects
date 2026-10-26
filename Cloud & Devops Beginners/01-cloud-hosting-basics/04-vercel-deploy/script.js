/**
 * Fun Facts Website - Interactive Features
 * Features:
 *   1. Theme toggle (dark/light mode) with localStorage
 *   2. Random fact generator with animation
 *   3. Category filtering
 *   4. Mobile navigation
 */
(function() {
  'use strict';

  // ─── DOM Elements ───────────────────────────────
  const themeToggle = document.getElementById('themeToggle');
  const newFactBtn = document.getElementById('newFactBtn');
  const anotherFactBtn = document.getElementById('anotherFactBtn');
  const factText = document.getElementById('factText');
  const factSource = document.getElementById('factSource');
  const factIcon = document.querySelector('.fact-icon');
  const navLinks = document.querySelectorAll('.nav-link');

  // ─── Theme Toggle ───────────────────────────────
  function initTheme() {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const currentTheme = savedTheme || (prefersDark ? 'dark' : 'light');

    if (currentTheme === 'dark') {
      document.body.setAttribute('data-theme', 'dark');
      if (themeToggle) themeToggle.textContent = '☀️';
    }
  }

  if (themeToggle) {
    themeToggle.addEventListener('click', function() {
      const isDark = document.body.getAttribute('data-theme') === 'dark';
      if (isDark) {
        document.body.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
        this.textContent = '🌙';
      } else {
        document.body.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
        this.textContent = '☀️';
      }
    });
  }

  // ─── Random Fact Generator ──────────────────────
  function getRandomFact(categoryFilter) {
    let facts = ALL_FACTS;
    if (categoryFilter && categoryFilter !== 'all') {
      facts = FUN_FACTS[categoryFilter] || ALL_FACTS;
    }
    const randomIndex = Math.floor(Math.random() * facts.length);
    return facts[randomIndex];
  }

  function displayFact(fact, category) {
    if (!factText || !factSource || !factIcon) return;

    factIcon.textContent = getCategoryEmoji(category || fact.category || 'science');
    factText.textContent = fact.text;
    factSource.textContent = `Source: ${fact.source}`;

    // Animate the text
    factText.style.opacity = '0';
    factSource.style.opacity = '0';
    factIcon.style.transform = 'scale(0.5)';

    setTimeout(() => {
      factText.style.opacity = '1';
      factSource.style.opacity = '1';
      factIcon.style.transform = 'scale(1)';
    }, 150);
  }

  function getCategoryEmoji(category) {
    const emojis = {
      science: '🔬',
      history: '🏛️',
      nature: '🌿',
      tech: '💻',
      food: '🍕'
    };
    return emojis[category] || '🤔';
  }

  function showNewFact() {
    if (!ALL_FACTS || ALL_FACTS.length === 0) return;
    const fact = getRandomFact();
    displayFact(fact, fact.category);
  }

  // Attach button events
  if (newFactBtn) newFactBtn.addEventListener('click', showNewFact);
  if (anotherFactBtn) anotherFactBtn.addEventListener('click', showNewFact);

  // ─── Category Filtering ────────────────────────
  const categoryCards = document.querySelectorAll('.category-card');

  categoryCards.forEach(card => {
    card.addEventListener('click', function() {
      const category = this.dataset.category;
      const facts = FUN_FACTS[category] || [];

      if (facts.length > 0) {
        const randomIndex = Math.floor(Math.random() * facts.length);
        displayFact(facts[randomIndex], category);
      }

      // Update active nav link
      navLinks.forEach(link => link.classList.remove('active'));
      const categoryLink = document.querySelector(`.nav-link[href="#${category}"]`) ||
                           document.querySelector('.nav-link');
      if (categoryLink) categoryLink.classList.add('active');
    });
  });

  // ─── Mobile Navigation ────────────────────────
  const navToggle = document.getElementById('navToggle');
  const navList = document.querySelector('.nav-list');

  if (navToggle && navList) {
    navToggle.addEventListener('click', () => {
      navList.classList.toggle('active');
    });

    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        if (navList.classList.contains('active')) {
          navList.classList.remove('active');
        }
      });
    });
  }

  // ─── Smooth Scrolling ─────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ─── Init ─────────────────────────────────────
  initTheme();
  console.log('Fun Facts site ready. Deploy with: vercel --prod');
})();
