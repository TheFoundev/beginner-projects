/**
 * Fortune Cookie App - Interactive Features
 * Fetches fortunes from serverless API, tracks request count
 */
(function() {
  'use strict';

  let requestCount = parseInt(localStorage.getItem('requestCount') || '0');
  const requestCountEl = document.getElementById('requestCount');
  const getFortuneBtn = document.getElementById('getFortuneBtn');
  const fortuneText = document.getElementById('fortuneText');
  const fortuneMeta = document.getElementById('fortuneMeta');

  function updateRequestCount() {
    requestCount += 1;
    localStorage.setItem('requestCount', requestCount);
    if (requestCountEl) requestCountEl.textContent = `Requests: ${requestCount}`;
  }

  function setLoading(isLoading) {
    if (!getFortuneBtn) return;
    getFortuneBtn.disabled = isLoading;
    const btnText = getFortuneBtn.querySelector('.btn-text');
    const btnLoading = getFortuneBtn.querySelector('.btn-loading');
    if (btnText) btnText.style.display = isLoading ? 'none' : 'inline';
    if (btnLoading) btnLoading.style.display = isLoading ? 'inline' : 'none';
  }

  async function getFortune() {
    updateRequestCount();
    setLoading(true);

    // Show loading state
    if (fortuneText) {
      fortuneText.textContent = 'Fetching your fortune...';
      fortuneText.style.opacity = '0.5';
    }

    try {
      const response = await fetch('/.netlify/functions/fortune');
      const data = await response.json();

      if (data.fortune) {
        // Animate the fortune change
        if (fortuneText) {
          fortuneText.style.opacity = '0';
          setTimeout(() => {
            fortuneText.textContent = data.fortune;
            fortuneText.style.opacity = '1';
          }, 150);
        }
        if (fortuneMeta) {
          fortuneMeta.textContent = `Fortune #${Math.floor(Math.random() * 1000)} of ${data.totalFortunes || 10}`;
        }
      } else {
        throw new Error('No fortune returned');
      }
    } catch (err) {
      console.error('Failed to get fortune:', err);
      // Fallback fortunes for offline/demo
      const fallback = [
        "A new adventure is about to begin.",
        "Your curiosity will lead you to great discoveries.",
        "Great things never came from comfort zones."
      ];
      const random = fallback[Math.floor(Math.random() * fallback.length)];

      if (fortuneText) {
        fortuneText.style.opacity = '0';
        setTimeout(() => {
          fortuneText.textContent = random;
          fortuneText.style.opacity = '1';
        }, 150);
      }
      if (fortuneMeta) fortuneMeta.textContent = '(Demo mode — deploy the full function)';
    } finally {
      setLoading(false);
    }
  }

  if (getFortuneBtn) {
    getFortuneBtn.addEventListener('click', getFortune);
  }

  updateRequestCount();
  console.log('Fortune Cookie app loaded. API: /.netlify/functions/fortune');
})();
