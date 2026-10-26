/**
 * Visitor Counter - Frontend JavaScript
 * Fetches visitor count from serverless API backed by Upstash Redis
 */
(function() {
  'use strict';

  const visitorCountEl = document.getElementById('visitorCount');
  const countValueEl = document.querySelector('.count-value');
  const redisStatusEl = document.getElementById('redisStatus');
  const responseTimeEl = document.getElementById('responseTime');
  const refreshBtn = document.getElementById('refreshBtn');
  const resetLocalBtn = document.getElementById('resetLocalBtn');

  let currentCount = 0;

  // ─── Fetch Visitor Count ──────────────────────
  async function fetchVisitorCount(showAnimation = false) {
    const start = performance.now();

    try {
      if (showAnimation && countValueEl) {
        countValueEl.style.transform = 'scale(1.1)';
        countValueEl.style.color = '#22c55e';
      }

      const response = await fetch('/api/count', { cache: 'no-store' });
      const data = await response.json();
      const newCount = data.count || 0;

      const elapsed = Math.round(performance.now() - start);

      animateCount(currentCount, newCount);
      currentCount = newCount;

      if (redisStatusEl) {
        redisStatusEl.textContent = data.online !== false ? 'Online' : 'Offline';
        redisStatusEl.style.color = data.online !== false ? '#22c55e' : '#ef4444';
      }

      if (responseTimeEl) {
        responseTimeEl.textContent = `${elapsed}ms`;
      }
    } catch (err) {
      console.error('Failed to fetch count:', err);
      if (redisStatusEl) {
        redisStatusEl.textContent = 'Offline';
        redisStatusEl.style.color = '#ef4444';
      }
      if (countValueEl) {
        countValueEl.textContent = '0';
      }
    } finally {
      if (countValueEl) {
        setTimeout(() => {
          countValueEl.style.transform = '';
          countValueEl.style.color = '';
        }, 300);
      }
    }
  }

  // ─── Animate Count ─────────────────────────────
  function animateCount(from, to) {
    if (!countValueEl) return;

    const duration = 1000;
    const steps = 30;
    const stepTime = duration / steps;
    const increment = (to - from) / steps;

    let current = from;
    let step = 0;

    const timer = setInterval(() => {
      step++;
      current = from + increment * step;
      countValueEl.textContent = Math.round(current).toLocaleString();

      if (step >= steps) {
        clearInterval(timer);
        countValueEl.textContent = to.toLocaleString();
      }
    }, stepTime);
  }

  // ─── Event Listeners ──────────────────────────
  if (refreshBtn) {
    refreshBtn.addEventListener('click', () => fetchVisitorCount(true));
  }

  if (resetLocalBtn) {
    resetLocalBtn.addEventListener('click', async function() {
      this.disabled = true;
      this.textContent = 'Resetting...';

      try {
        // Reset by calling the count endpoint with a fresh request
        // Note: In a real app, the server handles counter increments
        await fetch('/api/count', { cache: 'no-store' });
        fetchVisitorCount(true);
        this.textContent = 'Reset';
      } catch (err) {
        this.textContent = 'Try Again';
      } finally {
        this.disabled = false;
      }
    });
  }

  // ─── Initialize ─────────────────────────────────
  fetchVisitorCount(true);

  // Refresh every 10 seconds
  setInterval(() => fetchVisitorCount(false), 10000);

  console.log('Visitor Counter loaded.');
  console.log('Backend: Vercel Functions + Upstash Redis');
})();
