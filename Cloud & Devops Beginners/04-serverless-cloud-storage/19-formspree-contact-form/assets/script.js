/**
 * Formspree Contact Form - Frontend JavaScript
 * Real-time validation, submission, and status messages.
 */
(function() {
  'use strict';

  const form = document.getElementById('contactForm');
  const formStatus = document.getElementById('formStatus');
  const submitBtn = form ? form.querySelector('button[type="submit"]') : null;

  // Input validation patterns
  const patterns = {
    email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    name: /^[\w\s.'-]{2,50}$/,
    phone: /^[\d\s+\-()]{10,20}$/
  };

  // Show status
  function showStatus(message, type) {
    if (!formStatus) return;
    formStatus.textContent = message;
    formStatus.className = `form-status ${type}`;
  }

  // Real-time validation
  const inputs = form ? form.querySelectorAll('input, textarea') : [];

  inputs.forEach(input => {
    input.addEventListener('input', function() {
      validateInput(this);
    });

    input.addEventListener('blur', function() {
      validateInput(this);
    });
  });

  function validateInput(input) {
    const value = input.value.trim();
    const name = input.name;
    let isValid = true;
    let message = '';

    if (input.hasAttribute('required') && !value) {
      isValid = false;
      input.style.borderColor = '#ef4444';
      return;
    }

    if (name === 'email' && value && !patterns.email.test(value)) {
      isValid = false;
      message = 'Invalid email format';
    }

    if (name === 'name' && value && !patterns.name.test(value)) {
      isValid = false;
      message = 'Name contains invalid characters';
    }

    input.style.borderColor = isValid ? '#22c55e' : '#ef4444';
  }

  // Handle form submission
  if (form) {
    form.addEventListener('submit', async function(e) {
      e.preventDefault();

      const formData = new FormData(form);
      const data = Object.fromEntries(formData);

      // Validate all fields
      let hasErrors = false;
      inputs.forEach(input => {
        validateInput(input);
        if (input.hasAttribute('required') && !input.value.trim()) {
          hasErrors = true;
        }
        if (input.name === 'email' && input.value && !patterns.email.test(input.value)) {
          hasErrors = true;
        }
      });

      if (hasErrors) {
        showStatus('Please fix the errors and try again.', 'error');
        return;
      }

      // Disable button and show loading
      if (submitBtn) {
        submitBtn.disabled = true;
        const btnText = submitBtn.querySelector('.btn-text');
        const btnLoading = submitBtn.querySelector('.btn-loading');
        if (btnText) btnText.style.display = 'none';
        if (btnLoading) btnLoading.style.display = 'inline';
      }

      showStatus('Sending your message...', 'loading');

      // Submit via fetch (Formspree API)
      try {
        const response = await fetch(form.action, {
          method: 'POST',
          body: formData,
          headers: {
            'Accept': 'application/json'
          }
        });

        if (response.ok) {
          form.reset();
          inputs.forEach(i => { i.style.borderColor = ''; });
          showStatus('Thank you! Your message has been sent successfully.', 'success');
        } else {
          const errorData = await response.json().catch(() => ({}));
          showStatus(`Error: ${errorData.error || 'Failed to send message'}`, 'error');
        }
      } catch (err) {
        // For local testing without Formspree account
        console.log('Demo mode - form would submit to Formspree');
        showStatus('Demo mode: Form would submit to your Formspree endpoint. Configure YOUR_FORM_ID in the HTML.', 'success');
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          const btnText = submitBtn.querySelector('.btn-text');
          const btnLoading = submitBtn.querySelector('.btn-loading');
          if (btnText) btnText.style.display = 'inline';
          if (btnLoading) btnLoading.style.display = 'none';
        }
      }
    });
  }

  console.log('Formspree contact form loaded.');
  console.log('Replace YOUR_FORM_ID in index.html with your actual Formspree form ID.');
})();
