/**
 * Photo Gallery - Interactive Features
 * Lazy loading, lightbox modal, filtering, view toggle
 */
(function() {
  'use strict';

  const galleryGrid = document.getElementById('galleryGrid');
  const photoCount = document.getElementById('photoCount');
  const galleryCaption = document.getElementById('galleryCaption');
  const modal = document.getElementById('photoModal');
  const modalImage = document.getElementById('modalImage');
  const modalCaption = document.getElementById('modalCaption');
  const modalMeta = document.getElementById('modalMeta');
  const modalClose = document.getElementById('modalClose');
  const loadMoreBtn = document.getElementById('loadMoreBtn');
  const viewBtns = document.querySelectorAll('.view-btn');
  const navToggle = document.getElementById('navToggle');
  const navList = document.getElementById('navList');

  // Mobile nav
  if (navToggle && navList) {
    navToggle.addEventListener('click', () => navList.classList.toggle('active'));
    document.querySelectorAll('.nav-link').forEach(l => l.addEventListener('click', () => navList.classList.remove('active')));
  }

  // Gallery state
  let displayedCount = 0;
  let currentFilter = 'all';
  const itemsPerPage = 8;

  function getFilteredPhotos(filter) {
    return filter === 'all' ? PHOTOS : PHOTOS.filter(p => p.category === filter);
  }

  function renderPhotos(photos, startIndex = 0, count = itemsPerPage) {
    const slice = photos.slice(startIndex, startIndex + count);
    galleryGrid.innerHTML = slice.map(photo => `
      <div class="gallery-item" onclick="openModal(${photo.id})">
        <span class="gallery-badge">${photo.category}</span>
        <img src="${photo.thumb}" alt="${photo.title}" loading="lazy" />
        <div class="gallery-item__info">
          <div class="gallery-item__title">${photo.title}</div>
          <div class="gallery-item__desc">${photo.desc}</div>
          <div class="gallery-item__meta">
            <span>${photo.location}</span>
            <span>${photo.date}</span>
          </div>
        </div>
      </div>
    `).join('');
  }

  function updateGalleryInfo() {
    const filtered = getFilteredPhotos(currentFilter);
    photoCount.textContent = `${filtered.length} photos`;
    galleryCaption.textContent = `Showing ${currentFilter === 'all' ? 'all' : currentFilter} photos`;
  }

  function renderFiltered(filter) {
    currentFilter = filter;
    displayedCount = 0;
    const filtered = getFilteredPhotos(filter);
    renderPhotos(filtered);
    updateGalleryInfo();
  }

  // Category filtering
  document.querySelectorAll('[data-filter]').forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
      this.classList.add('active');
      renderFiltered(this.dataset.filter);
    });
  });

  // View toggle
  viewBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      viewBtns.forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      const view = this.dataset.view;
      galleryGrid.className = `gallery-grid ${view}-view`;
    });
  });

  // Load more
  if (loadMoreBtn) {
    loadMoreBtn.addEventListener('click', function() {
      displayedCount += itemsPerPage;
      const filtered = getFilteredPhotos(currentFilter);
      const existingItems = galleryGrid.children.length;
      const newSlice = filtered.slice(existingItems, existingItems + itemsPerPage);

      if (newSlice.length === 0) {
        loadMoreBtn.style.display = 'none';
        return;
      }

      const html = newSlice.map(photo => `
        <div class="gallery-item" onclick="openModal(${photo.id})">
          <span class="gallery-badge">${photo.category}</span>
          <img src="${photo.thumb}" alt="${photo.title}" loading="lazy" />
          <div class="gallery-item__info">
            <div class="gallery-item__title">${photo.title}</div>
            <div class="gallery-item__desc">${photo.desc}</div>
            <div class="gallery-item__meta">${photo.location} · ${photo.date}</div>
          </div>
        </div>
      `).join('');

      galleryGrid.insertAdjacentHTML('beforeend', html);

      if (displayedCount + itemsPerPage >= filtered.length) {
        loadMoreBtn.style.display = 'none';
      }
    });
  }

  // Open modal
  window.openModal = function(photoId) {
    const photo = PHOTOS.find(p => p.id === photoId);
    if (!photo || !modal) return;

    modalImage.src = photo.src;
    modalImage.alt = photo.title;
    modalCaption.innerHTML = `<strong>${photo.title}</strong> — ${photo.desc}`;
    modalMeta.innerHTML = `
      📍 ${photo.location} · 📅 ${photo.date} · 📷 ${photo.camera || 'N/A'}
    `;
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
  };

  function closeModal() {
    if (modal) {
      modal.classList.remove('show');
      document.body.style.overflow = '';
    }
  }

  if (modalClose) modalClose.addEventListener('click', closeModal);
  if (modal) modal.addEventListener('click', e => {
    if (e.target === modal) closeModal();
  });

  // ESC key
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && modal && modal.classList.contains('show')) {
      closeModal();
    }
  });

  // Check if load more button needed
  function checkLoadMore() {
    const filtered = getFilteredPhotos(currentFilter);
    if (filtered.length <= itemsPerPage) {
      if (loadMoreBtn) loadMoreBtn.style.display = 'none';
    } else {
      if (loadMoreBtn) loadMoreBtn.style.display = 'block';
    }
  }

  // Init
  renderFiltered('all');
  checkLoadMore();
  console.log('Photo Gallery ready. Upload photos to AWS S3 and update photo-data.js with S3 URLs.');
})();
