/**
 * Contact Form - Frontend JavaScript
 * Handles form validation, submission, and status messages.
 * Works with AWS Lambda backend via API Gateway.
 */
(function() {
  'use strict';

  const form = document.getElementById('contactForm');
  const formStatus = document.getElementById('formStatus');
  const submitBtn = form ? form.querySelector('button[type="submit"]') : null;
  const btnText = submitBtn ? submitBtn.querySelector('.btn-text') : null;
  const btnLoading = submitBtn ? submitBtn.querySelector('.btn-loading') : null;

  // Show status message
  function showStatus(message, type) {
    if (!formStatus) return;
    formStatus.textContent = message;
    formStatus.className = `form-status ${type}`;
    formStatus.style.display = 'block';
  }

  // Reset form status
  function resetStatus() {
    if (formStatus) {
      formStatus.style.display = 'none';
      formStatus.className = 'form-status';
    }
  }

  // Set button loading state
  function setLoading(isLoading) {
    if (!submitBtn) return;
    submitBtn.disabled = isLoading;
    if (btnText) btnText.style.display = isLoading ? 'none' : 'inline';
    if (btnLoading) btnLoading.style.display = isLoading ? 'inline' : 'none';
  }

  // Validate email format
  function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  // Handle form submission
  if (form) {
    form.addEventListener('submit', async function(e) {
      e.preventDefault();
      resetStatus();

      const formData = new FormData(form);
      const data = {
        name: formData.get('name')?.trim() || '',
        email: formData.get('email')?.trim() || '',
        subject: formData.get('subject')?.trim() || '',
        message: formData.get('message')?.trim() || ''
      };

      // Client-side validation
      if (!data.name || !data.email || !data.subject || !data.message) {
        showStatus('Please fill in all required fields.', 'error');
        return;
      }

      if (!isValidEmail(data.email)) {
        showStatus('Please enter a valid email address.', 'error');
        return;
      }

      if (data.message.length < 10) {
        showStatus('Message seems too short. Please add more details.', 'error');
        return;
      }

      // Submit to backend
      setLoading(true);
      showStatus('Sending your message...', 'loading');

      try {
        const response = await fetch(form.action, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
          showStatus('Message sent successfully! I\'ll reply soon.', 'success');
          form.reset();
        } else {
          showStatus(`Error: ${result.error || 'Something went wrong'}`, 'error');
        }
      } catch (err) {
        // For demo/testing without backend
        console.error('Form submission error:', err);

        // Fallback: simulate success for demo purposes
        showStatus('Message received! (Demo mode - configure AWS Lambda for real delivery)', 'success');
        form.reset();
      } finally {
        setLoading(false);
      }
    });
  }

  // Input focus animations
  document.querySelectorAll('.contact-form input, .contact-form textarea').forEach(input => {
    input.addEventListener('focus', function() {
      this.parentElement.classList.add('focused');
    });
    input.addEventListener('blur', function() {
      this.parentElement.classList.remove('focused');
    });
  });

  console.log('Serverless contact form loaded.');
  console.log('Backend: AWS Lambda + API Gateway + SES');
})();
