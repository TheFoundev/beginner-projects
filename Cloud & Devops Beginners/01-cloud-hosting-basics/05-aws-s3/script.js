/**
 * Photo Gallery - Interactive Features
 * Handles: Lazy loading, lightbox modal, filtering, view toggle, counter
 */
(function() {
  'use strict';

  // DOM Elements
  const galleryGrid = document.getElementById('galleryGrid');
  const photoCountEl = document.getElementById('photoCount');
  const galleryCaption = document.getElementById('galleryCaption');
  const modal = document.getElementById('photoModal');
  const modalImage = document.getElementById('modalImage');
  const modalCaption = document.getElementById('modalCaption');
  const modalClose = document.getElementById('modalClose');
  const downloadBtn = document.getElementById('downloadBtn');
  const shareBtn = document.getElementById('shareBtn');
  const viewBtns = document.querySelectorAll('.view-btn');
  const addPhotoBtn = document.getElementById('addPhotoBtn');
  const shuffleBtn = document.getElementById('shuffleBtn');
  const categoryLinks = document.querySelectorAll('[data-filter]');

  let currentFilter = 'all';
  let currentView = 'grid';
  let displayedPhotos = [];

  // ─── Render Gallery ─────────────────────────────
  function renderGallery(photos, view = 'grid') {
    galleryGrid.className = `gallery-grid ${view}-view`;
    galleryGrid.innerHTML = photos.map(photo => `
      <div class="gallery-item" onclick="openModal(${photo.id})">
        <span class="gallery-badge">${photo.category}</span>
        <img src="${photo.thumb}" alt="${photo.title}" loading="lazy" />
        <div class="gallery-item__info">
          <div class="gallery-item__title">${photo.title}</div>
          <div class="gallery-item__desc">${photo.description}</div>
          <div class="gallery-item__meta">
            <span>${photo.location}</span>
            <span>${photo.date}</span>
          </div>
        </div>
      </div>
    `).join('');
  }

  // ─── Filter ─────────────────────────────────────
  function filterPhotos(category) {
    currentFilter = category;
    displayedPhotos = currentFilter === 'all'
      ? [...PHOTOS]
      : PHOTOS.filter(p => p.category === currentFilter);

    renderGallery(displayedPhotos, currentView);
    updateGalleryInfo();

    // Update active link
    categoryLinks.forEach(link => link.classList.remove('active'));
    const activeLink = document.querySelector(`[data-filter="${category}"]`) ||
                       document.querySelector('.nav-link');
    if (activeLink) activeLink.classList.add('active');
  }

  // ─── Gallery Info ───────────────────────────────
  function updateGalleryInfo() {
    if (photoCountEl) {
      photoCountEl.textContent = `${displayedPhotos.length} photos`;
    }
    if (galleryCaption) {
      galleryCaption.textContent = currentFilter === 'all'
        ? 'Showing all photos'
        : `Showing ${currentFilter} photos`;
    }
  }

  // ─── View Toggle ────────────────────────────────
  viewBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      viewBtns.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      currentView = this.dataset.view;
      renderGallery(displayedPhotos, currentView);
    });
  });

  // ─── Category Filtering ────────────────────────
  categoryLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const category = this.dataset.filter || 'all';
      filterPhotos(category);
    });
  });

  // ─── Modal (Lightbox) ───────────────────────────
  window.openModal = function(photoId) {
    const photo = PHOTOS.find(p => p.id === photoId);
    if (!photo || !modal) return;

    modalImage.src = photo.src;
    modalImage.alt = photo.title;
    modalCaption.innerHTML = `
      <strong>${photo.title}</strong> — ${photo.description}<br>
      📍 ${photo.location} · 📷 ${photo.camera} · 📏 ${photo.focal} · ISO ${photo.iso}
    `;
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  };

  function closeModal() {
    if (modal) {
      modal.style.display = 'none';
      document.body.style.overflow = '';
    }
  }

  if (modalClose) modalClose.addEventListener('click', closeModal);
  if (modal) modal.addEventListener('click', function(e) {
    if (e.target === modal) closeModal();
  });

  // Close modal with Escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && modal && modal.style.display === 'flex') {
      closeModal();
    }
  });

  // ─── Action Buttons ─────────────────────────────
  if (downloadBtn) {
    downloadBtn.addEventListener('click', function() {
      if (modalImage.src) {
        window.open(modalImage.src, '_blank');
      }
    });
  }

  if (shareBtn) {
    shareBtn.addEventListener('click', function() {
      const photoSrc = modalImage.src;
      navigator.clipboard.writeText(photoSrc).then(() => {
        alert('Photo URL copied to clipboard!');
      }).catch(() => {
        alert('Copy this URL: ' + photoSrc);
      });
    });
  }

  if (shuffleBtn) {
    shuffleBtn.addEventListener('click', function() {
      const shuffled = [...displayedPhotos].sort(() => Math.random() - 0.5);
      displayedPhotos = shuffled;
      renderGallery(displayedPhotos, currentView);
    });
  }

  if (addPhotoBtn) {
    addPhotoBtn.addEventListener('click', function() {
      alert('To add photos: Upload images to your AWS S3 bucket, then add entries to photo-data.js.');
    });
  }

  // ─── Initialize ─────────────────────────────────
  filterPhotos('all');
  console.log('Photo Gallery ready. Upload images to AWS S3 to replace placeholders.');
})();
