/**
 * Project Showcase - JavaScript
 * Features: Project list rendering, deploy timestamp, mobile nav
 */
(function() {
  'use strict';

  // ─── Mobile Navigation ──────────────────────────
  const navToggle = document.getElementById('navToggle');
  const navList = document.getElementById('navList');

  if (navToggle && navList) {
    navToggle.addEventListener('click', () => {
      navList.classList.toggle('active');
    });

    document.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        navList.classList.remove('active');
      });
    });
  }

  // ─── Smooth Scrolling ────────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ─── Render Projects ─────────────────────────────
  const projectsGrid = document.getElementById('projectsGrid');
  const CATEGORIES = {
    frontend: '🎨 Frontend',
    backend: '⚙️ Backend',
    devops: '🚀 DevOps',
    cloud: '☁️ Cloud'
  };

  function renderProjects() {
    if (!projectsGrid) return;

    projectsGrid.innerHTML = PROJECTS.map(project => `
      <div class="project-card">
        <h3>${project.title}</h3>
        <p>${project.description}</p>
        <div class="project-card__tags">
          ${project.tech.map(tech => `<span class="tag">${tech}</span>`).join('')}
          <span class="tag" style="background: #e0f2fe; color: #0369a1;">
            ${CATEGORIES[project.category] || project.category}
          </span>
        </div>
      </div>
    `).join('');
  }

  // ─── Deploy Timestamp ─────────────────────────────
  function updateDeployTime() {
    const deployEl = document.getElementById('lastDeploy');
    if (!deployEl) return;

    const now = new Date();
    const timeStr = now.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    });
    const dateStr = now.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });

    deployEl.textContent = `Last deployed: ${dateStr} at ${timeStr}`;
  }

  // ─── Active Nav Link on Scroll ────────────────────
  function updateActiveNav() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = entry.target.getAttribute('id');
          navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${id}`) {
              link.classList.add('active');
            }
          });
        }
      });
    }, { threshold: 0.5 });

    sections.forEach(section => observer.observe(section));
  }

  // ─── Initialize ───────────────────────────────────
  renderProjects();
  updateDeployTime();
  updateActiveNav();

  // Update deploy time every 30 seconds (simulating CI/CD)
  setInterval(updateDeployTime, 30000);

  console.log('Project Showcase loaded.');
  console.log('Deployed via: GitHub Actions → GitHub Pages');
})();
