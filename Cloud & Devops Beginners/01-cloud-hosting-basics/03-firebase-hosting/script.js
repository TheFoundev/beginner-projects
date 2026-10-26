/**
 * DevLog - Firebase Hosted Site
 * Features: Mobile nav, header scroll effect, dynamic blog posts, smooth scroll
 */

// Blog Post Data (normally fetched from an API)
const BLOG_POSTS = [
  {
    title: "Getting Started with Docker",
    excerpt: "Docker is revolutionizing how we package applications. Here's my first week of learning containers, from writing Dockerfiles to running my first container.",
    tags: ["Docker", "Containers", "Beginner"],
    date: "Jan 15, 2026"
  },
  {
    title: "Understanding Cloud Deployment Models",
    excerpt: "IaaS, PaaS, and SaaS — three acronyms you'll see everywhere in the cloud. Here's a beginner-friendly breakdown with real-world analogies.",
    tags: ["Cloud", "IaaS", "PaaS", "SaaS"],
    date: "Jan 10, 2026"
  },
  {
    title: "My CI/CD Journey with GitHub Actions",
    excerpt: "Automated testing and deployment transformed how I ship code. This guide walks through setting up your first pipeline from scratch.",
    tags: ["CI/CD", "GitHub Actions", "DevOps"],
    date: "Jan 5, 2026"
  }
];

// Mobile Navigation
(function() {
  'use strict';

  const navToggle = document.getElementById('navToggle');
  const navList = document.getElementById('navList');

  if (navToggle && navList) {
    navToggle.addEventListener('click', () => {
      navList.classList.toggle('active');
    });

    document.querySelectorAll('.nav__link').forEach(link => {
      link.addEventListener('click', () => {
        navList.classList.remove('active');
      });
    });
  }

  // Header Scroll Effect
  const header = document.getElementById('header');

  window.addEventListener('scroll', () => {
    if (header) {
      if (window.scrollY > 50) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    }
  });

  // Render Blog Posts
  function renderPosts() {
    const grid = document.getElementById('postsGrid');
    if (!grid) return;

    grid.innerHTML = BLOG_POSTS.map(post => `
      <article class="post-card">
        <span class="post-card__date">${post.date}</span>
        <h3>${post.title}</h3>
        <p>${post.excerpt}</p>
        <div class="post-card__tags">
          ${post.tags.map(tag => `<span class="post-tag">${tag}</span>`).join('')}
        </div>
      </article>
    `).join('');
  }

  // Smooth Scroll
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // Init
  document.addEventListener('DOMContentLoaded', () => {
    renderPosts();
    console.log('DevLog: Deployed with Firebase. Run "firebase deploy" to update.');
  });
})();
