/**
 * Pokhara Studio INN - Interactive Client Logic
 * Enhanced with Hero Carousel, Card Photo Sliders & Lightbox Modal
 */

// Filter out any stray platform assets, review icons, or user avatars defensively
if (typeof APARTMENTS_DATA !== 'undefined' && Array.isArray(APARTMENTS_DATA)) {
  const FORBIDDEN_PATTERNS = [
    'platform', 'platformassets', 'airbnbplatformassets', '/user/',
    'favicon', 'icon', 'search-bar-icons', 'review-ai-synthesis', 'userprofile'
  ];
  APARTMENTS_DATA.forEach(apt => {
    if (Array.isArray(apt.images)) {
      apt.images = apt.images.filter(url => {
        if (!url || typeof url !== 'string') return false;
        const lower = url.toLowerCase();
        return !FORBIDDEN_PATTERNS.some(pat => lower.includes(pat));
      });
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initHeroSlider();
  renderApartments(APARTMENTS_DATA);
  renderReviews(REVIEWS_DATA);
  setupFilters();
  setupSearch();
  setupModal();
  setupFAQs();
  setupScrollEffects();
  setupMobileNav();
  initAutoScroll();
});

/* ===================================================================
   1. HERO BACKGROUND CAROUSEL
   =================================================================== */
let currentHeroIndex = 0;
let heroTimer = null;
let heroContentTimer = null;

function initHeroSlider() {
  const container = document.getElementById('hero-slider');
  const dotsContainer = document.getElementById('hero-indicators');
  if (!container || !HERO_SLIDES || HERO_SLIDES.length === 0) return;

  // Build slide elements
  container.innerHTML = HERO_SLIDES.map((slide, i) => `
    <a class="hero-slide ${i === 0 ? 'active' : ''}"
       style="background-image: url('${slide.image}')"
       href="${slide.airbnb_url}"
       target="_blank"
       rel="noopener noreferrer"
       aria-label="View ${slide.badge} on Airbnb"
       aria-hidden="${i === 0 ? 'false' : 'true'}"
       tabindex="${i === 0 ? '0' : '-1'}"
       data-index="${i}">
    </a>
  `).join('');

  // Build dots
  if (dotsContainer) {
    dotsContainer.innerHTML = HERO_SLIDES.map((_, i) => `
      <button class="hero-dot ${i === 0 ? 'active' : ''}" onclick="goToHeroSlide(${i})" aria-label="Show slide ${i + 1}" aria-current="${i === 0 ? 'true' : 'false'}"></button>
    `).join('');
  }

  // Set initial content
  updateHeroContent(0);

  // Auto advance every 5.5 seconds
  startHeroTimer();

  // Pause on hover
  container.addEventListener('mouseenter', () => clearInterval(heroTimer));
  container.addEventListener('mouseleave', () => startHeroTimer());
  container.addEventListener('focusin', () => clearInterval(heroTimer));
  container.addEventListener('focusout', () => startHeroTimer());
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) clearInterval(heroTimer);
    else startHeroTimer();
  });
}

function startHeroTimer() {
  clearInterval(heroTimer);
  if (document.hidden || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  heroTimer = setInterval(() => {
    changeHeroSlide(1);
  }, 5500);
}

function changeHeroSlide(direction) {
  if (!HERO_SLIDES || HERO_SLIDES.length === 0) return;
  let nextIndex = currentHeroIndex + direction;
  if (nextIndex < 0) nextIndex = HERO_SLIDES.length - 1;
  if (nextIndex >= HERO_SLIDES.length) nextIndex = 0;
  goToHeroSlide(nextIndex);
}

function goToHeroSlide(index) {
  if (!HERO_SLIDES || HERO_SLIDES.length === 0) return;
  index = ((index % HERO_SLIDES.length) + HERO_SLIDES.length) % HERO_SLIDES.length;
  currentHeroIndex = index;
  const slides = document.querySelectorAll('.hero-slide');
  const dots = document.querySelectorAll('.hero-dot');

  slides.forEach((slide, i) => {
    const isActive = i === index;
    slide.classList.toggle('active', isActive);
    slide.setAttribute('aria-hidden', String(!isActive));
    slide.tabIndex = isActive ? 0 : -1;
  });

  dots.forEach((dot, i) => {
    dot.classList.toggle('active', i === index);
    dot.setAttribute('aria-current', String(i === index));
  });

  updateHeroContent(index);
  startHeroTimer();
}

function updateHeroContent(index) {
  const badgeEl = document.getElementById('hero-slide-badge');
  const titleEl = document.getElementById('hero-title');
  const subEl = document.getElementById('hero-subtitle');
  const airbnbHeroBtn = document.getElementById('hero-airbnb-link');

  const slide = HERO_SLIDES[index];
  if (!slide) return;

  if (badgeEl) {
    badgeEl.innerHTML = `<i class="fa-solid fa-house-chimney"></i> ${slide.badge}`;
  }
  if (titleEl) {
    titleEl.style.opacity = '0';
    clearTimeout(heroContentTimer);
    heroContentTimer = setTimeout(() => {
      titleEl.textContent = slide.title;
      titleEl.style.opacity = '1';
      if (subEl) {
        subEl.textContent = slide.subtitle;
        subEl.style.opacity = '1';
      }
    }, 200);
  }
  if (subEl && !titleEl) {
    subEl.style.opacity = '0';
    clearTimeout(heroContentTimer);
    heroContentTimer = setTimeout(() => {
      subEl.textContent = slide.subtitle;
      subEl.style.opacity = '1';
    }, 200);
  } else if (subEl) {
    subEl.style.opacity = '0';
  }
  if (airbnbHeroBtn) {
    airbnbHeroBtn.href = slide.airbnb_url;
  }
}

/* ===================================================================
   2. APARTMENTS LISTING GRID & PER-CARD PHOTO SLIDERS
   =================================================================== */
// Track current slide per apartment card
const cardSliderState = {};
const cardImageErrorCount = {};
let activeApartmentFilter = 'all';
let apartmentSearchQuery = '';

function getVisibleApartments() {
  let apartments = [...APARTMENTS_DATA];

  if (activeApartmentFilter === 'top-rated') {
    apartments.sort((a, b) => parseFloat(b.rating) - parseFloat(a.rating));
  } else if (activeApartmentFilter === 'family') {
    const familyIds = new Set(['37218276', '1039685991315991696', '27266098']);
    apartments = apartments.filter(a => familyIds.has(a.id));
  } else if (activeApartmentFilter === 'popular') {
    apartments.sort((a, b) => parseInt(b.reviews, 10) - parseInt(a.reviews, 10));
  }

  if (apartmentSearchQuery) {
    apartments = apartments.filter(apt =>
      apt.name.toLowerCase().includes(apartmentSearchQuery) ||
      apt.tagline.toLowerCase().includes(apartmentSearchQuery) ||
      apt.description.toLowerCase().includes(apartmentSearchQuery) ||
      apt.amenities.some(am => am.toLowerCase().includes(apartmentSearchQuery))
    );
  }

  return apartments;
}

function renderApartments(apartments) {
  const container = document.getElementById('apartments-grid');
  if (!container) return;

  if (apartments.length === 0) {
    container.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 4rem 1rem;">
        <i class="fa-solid fa-hotel" style="font-size: 3rem; color: #cbd5e1; margin-bottom: 1rem;"></i>
        <h3 style="color: #334155; font-size: 1.25rem;">No apartments found matching your criteria</h3>
        <p style="color: #94a3b8; font-size: 0.95rem;">Try clearing your search query or switching filters.</p>
      </div>
    `;
    updateApartmentResultsStatus(0);
    return;
  }

  container.innerHTML = apartments.map((apt, cardIndex) => {
    const totalPhotos = apt.images.length;
    const firstImage = apt.images[0] || '';
    cardSliderState[apt.id] = 0;
    cardImageErrorCount[apt.id] = 0;

    const amenitiesChips = apt.amenities.slice(0, 4).map(item => `
      <span class="amenity-chip">${item}</span>
    `).join('');

    return `
      <article class="apartment-card" id="apartment-${apt.id}" data-id="${apt.id}" aria-labelledby="title-${apt.id}">
        <!-- Photo Slidebar -->
        <div class="card-media-wrap">
          <div class="card-slider" id="slider-${apt.id}">
            <button class="card-slider-slide" type="button" onclick="openDetailsModal('${apt.id}')" aria-label="Open photo gallery for ${apt.name}">
              <img src="${firstImage}" alt="${apt.name} - Photo 1" class="card-slider-img" loading="${cardIndex < 4 ? 'eager' : 'lazy'}" decoding="async" width="800" height="800" onerror="handleCardImageError('${apt.id}', this)">
            </button>
          </div>
          
          <button class="card-slider-btn card-slider-prev" onclick="slideCard('${apt.id}', -1)" aria-label="Previous photo">
            <i class="fa-solid fa-chevron-left"></i>
          </button>
          <button class="card-slider-btn card-slider-next" onclick="slideCard('${apt.id}', 1)" aria-label="Next photo">
            <i class="fa-solid fa-chevron-right"></i>
          </button>

          <!-- Clean Floating Photo Badge (e.g. 1 / 35 photos) -->
          <button class="card-photo-counter" id="counter-${apt.id}" onclick="openDetailsModal('${apt.id}')" aria-label="View all ${totalPhotos} photos of ${apt.name}">
            <i class="fa-regular fa-image"></i> 1 / ${totalPhotos}
          </button>

          <span class="card-badge">
            <i class="fa-solid fa-star"></i> ${apt.badge}
          </span>

          <a href="${apt.url}" target="_blank" rel="noopener noreferrer" class="card-airbnb-redirect-icon" title="Open on Airbnb">
            <i class="fa-brands fa-airbnb"></i>
          </a>
        </div>

        <div class="card-body">
          <div class="card-header-row">
            <h3 class="card-title" id="title-${apt.id}">
              <a href="${apt.url}" target="_blank" rel="noopener noreferrer">${apt.name}</a>
            </h3>
            <div class="card-rating">
              <i class="fa-solid fa-star"></i>
              <span>${apt.rating}</span>
              <span style="color: var(--stone); font-weight: 500;">(${apt.reviews})</span>
            </div>
          </div>

          <div class="card-tagline">${apt.tagline}</div>
          <p class="card-desc">${apt.description}</p>

          <div class="card-specs">
            <span class="spec-item"><i class="fa-solid fa-user-group"></i> ${apt.guests}</span>
            <span class="spec-item"><i class="fa-solid fa-bed"></i> ${apt.beds}</span>
            <span class="spec-item"><i class="fa-solid fa-bath"></i> ${apt.baths}</span>
            <span class="spec-item"><i class="fa-solid fa-wifi"></i> Fast WiFi</span>
          </div>

          <div class="card-amenities">
            ${amenitiesChips}
            <span class="amenity-chip" style="color: var(--accent); font-weight: 600;" onclick="openDetailsModal('${apt.id}')">+more</span>
          </div>

          <div class="card-actions">
            <button class="btn-card-details" onclick="openDetailsModal('${apt.id}')">
              <i class="fa-regular fa-images"></i> All ${totalPhotos} Photos
            </button>
            <a href="${apt.url}" target="_blank" rel="noopener noreferrer" class="btn-card-airbnb">
              <i class="fa-brands fa-airbnb"></i> Book on Airbnb
            </a>
          </div>
        </div>
      </article>
    `;
  }).join('');

  updateApartmentResultsStatus(apartments.length);
}

function slideCard(id, direction) {
  const slider = document.getElementById(`slider-${id}`);
  const counter = document.getElementById(`counter-${id}`);
  const apt = APARTMENTS_DATA.find(a => a.id === id);
  if (!slider || !apt || apt.images.length === 0) return;

  const totalSliderImgs = apt.images.length;
  if (cardSliderState[id] === undefined) cardSliderState[id] = 0;

  cardSliderState[id] += direction;
  if (cardSliderState[id] < 0) cardSliderState[id] = totalSliderImgs - 1;
  if (cardSliderState[id] >= totalSliderImgs) cardSliderState[id] = 0;

  const idx = cardSliderState[id];
  const image = slider.querySelector('.card-slider-img');
  if (image) {
    image.src = apt.images[idx];
    image.alt = `${apt.name} - Photo ${idx + 1}`;
  }

  if (counter) {
    counter.innerHTML = `<i class="fa-regular fa-image"></i> ${idx + 1}/${apt.images.length}`;
  }
}

function setCardSlide(id, targetIndex) {
  const apt = APARTMENTS_DATA.find(a => a.id === id);
  if (!apt || apt.images.length === 0) return;
  const current = cardSliderState[id] ?? 0;
  const normalized = ((targetIndex % apt.images.length) + apt.images.length) % apt.images.length;
  slideCard(id, normalized - current);
}

function handleCardImageError(id, image) {
  const apt = APARTMENTS_DATA.find(a => a.id === id);
  if (!apt || !image) return;
  cardImageErrorCount[id] = (cardImageErrorCount[id] || 0) + 1;
  if (cardImageErrorCount[id] < apt.images.length) {
    slideCard(id, 1);
  } else {
    image.onerror = null;
    image.alt = `${apt.name} photo unavailable`;
  }
}

function updateApartmentResultsStatus(count) {
  const status = document.getElementById('apartments-results-status');
  if (status) status.textContent = `${count} apartment${count === 1 ? '' : 's'} shown`;
}

/* ===================================================================
   3. FILTER & SEARCH LOGIC
   =================================================================== */
function setupFilters() {
  const buttons = document.querySelectorAll('.filter-btn');
  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      buttons.forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-pressed', 'false');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-pressed', 'true');
      activeApartmentFilter = btn.getAttribute('data-filter') || 'all';
      renderApartments(getVisibleApartments());
    });
  });
}

function setupSearch() {
  const searchInput = document.getElementById('search-apartments');
  if (!searchInput) return;

  searchInput.addEventListener('input', (e) => {
    apartmentSearchQuery = e.target.value.toLowerCase().trim();
    renderApartments(getVisibleApartments());
  });
}

/* ===================================================================
   4. LIGHTBOX MODAL WITH FULL AIRBNB IMAGE GALLERY
   =================================================================== */
let activeModalApt = null;
let activeModalImgIndex = 0;
let lastModalFocus = null;

function setPageInert(inert) {
  document.querySelectorAll('.header, main, .footer, .floating-actions, #autoscroll-toggle, #back-to-top')
    .forEach(element => {
      if (inert) element.setAttribute('inert', '');
      else element.removeAttribute('inert');
    });
}

function trapModalFocus(event, overlay) {
  if (event.key !== 'Tab') return;
  const focusable = [...overlay.querySelectorAll(
    'a[href], button:not([disabled]), input:not([disabled]), [tabindex]:not([tabindex="-1"])'
  )].filter(element => element.offsetParent !== null);
  if (focusable.length === 0) return;
  const first = focusable[0];
  const last = focusable[focusable.length - 1];
  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault();
    last.focus();
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault();
    first.focus();
  }
}

function setupModal() {
  const overlay = document.getElementById('details-modal');
  const closeBtn = document.getElementById('modal-close-btn');

  if (closeBtn && overlay) {
    closeBtn.addEventListener('click', closeModal);
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) closeModal();
    });
  }

  document.addEventListener('keydown', (e) => {
    if (!overlay || !overlay.classList.contains('active')) return;
    if (e.key === 'Escape') {
      e.preventDefault();
      closeModal();
    } else if (e.key === 'ArrowRight') {
      e.preventDefault();
      nextModalImage();
    } else if (e.key === 'ArrowLeft') {
      e.preventDefault();
      prevModalImage();
    } else {
      trapModalFocus(e, overlay);
    }
  });
}

function openDetailsModal(id) {
  const apt = APARTMENTS_DATA.find(a => a.id === id);
  if (!apt || apt.images.length === 0) return;

  activeModalApt = apt;
  activeModalImgIndex = 0;

  const modal = document.getElementById('details-modal');
  const mainImg = document.getElementById('modal-main-img');
  const thumbsWrap = document.getElementById('modal-thumbs');
  const title = document.getElementById('modal-title');
  const tagline = document.getElementById('modal-tagline');
  const rating = document.getElementById('modal-rating');
  const reviews = document.getElementById('modal-reviews');
  const specs = document.getElementById('modal-specs');
  const desc = document.getElementById('modal-description');
  const amenities = document.getElementById('modal-amenities');
  const airbnbBtn = document.getElementById('modal-airbnb-btn');
  const whatsappBtn = document.getElementById('modal-whatsapp-btn');
  const photoCounter = document.getElementById('modal-photo-counter');
  const closeBtn = document.getElementById('modal-close-btn');

  if (!modal) return;
  lastModalFocus = document.activeElement;

  if (title) title.innerText = apt.name;
  if (tagline) tagline.innerText = apt.tagline;
  if (rating) rating.innerText = apt.rating;
  if (reviews) reviews.innerText = `(${apt.reviews} Airbnb reviews)`;
  if (desc) desc.innerText = apt.description;

  if (specs) {
    specs.innerHTML = `
      <span><i class="fa-solid fa-home"></i> ${apt.type}</span>
      <span><i class="fa-solid fa-user-group"></i> ${apt.guests}</span>
      <span><i class="fa-solid fa-bed"></i> ${apt.beds}</span>
      <span><i class="fa-solid fa-bath"></i> ${apt.baths}</span>
      <span><i class="fa-solid fa-kitchen-set"></i> ${apt.kitchen}</span>
      <span><i class="fa-solid fa-wifi"></i> ${apt.wifi}</span>
    `;
  }

  if (amenities) {
    amenities.innerHTML = apt.amenities.map(am => `
      <div class="modal-amenity-item">
        <i class="fa-solid fa-circle-check"></i>
        <span>${am}</span>
      </div>
    `).join('');
  }

  if (airbnbBtn) {
    airbnbBtn.href = apt.url;
  }
  if (whatsappBtn) {
    whatsappBtn.href = `https://wa.me/9779856043981?text=Namaste!%20I%20am%20interested%20in%20booking%20${encodeURIComponent(apt.name)}%20at%20Pokhara%20Studio%20INN.%20Could%20you%20share%20availability%3F`;
  }

  // Load Main Image
  if (mainImg) {
    mainImg.src = apt.images[0];
    mainImg.alt = `${apt.name} - Photo 1`;
  }

  if (photoCounter) {
    photoCounter.innerText = `Photo 1 of ${apt.images.length}`;
  }

  // Thumbnails Gallery
  if (thumbsWrap) {
    thumbsWrap.innerHTML = apt.images.map((img, i) => `
      <button type="button" class="modal-thumb ${i === 0 ? 'active' : ''}" onclick="selectModalImage(${i})" aria-label="Show photo ${i + 1} of ${apt.name}" aria-current="${i === 0 ? 'true' : 'false'}">
        <img src="${img}" alt="" loading="lazy" decoding="async" width="152" height="108">
      </button>
    `).join('');
  }

  modal.classList.add('active');
  modal.setAttribute('aria-hidden', 'false');
  setPageInert(true);
  document.body.style.overflow = 'hidden';
  requestAnimationFrame(() => closeBtn?.focus());
}

function selectModalImage(index) {
  if (!activeModalApt) return;
  index = ((index % activeModalApt.images.length) + activeModalApt.images.length) % activeModalApt.images.length;
  activeModalImgIndex = index;
  const mainImg = document.getElementById('modal-main-img');
  const photoCounter = document.getElementById('modal-photo-counter');

  if (mainImg) {
    mainImg.src = activeModalApt.images[index];
    mainImg.alt = `${activeModalApt.name} - Photo ${index + 1}`;
  }

  if (photoCounter) {
    photoCounter.innerText = `Photo ${index + 1} of ${activeModalApt.images.length}`;
  }

  const thumbs = document.querySelectorAll('.modal-thumb');
  thumbs.forEach((th, i) => {
    th.classList.toggle('active', i === index);
    th.setAttribute('aria-current', String(i === index));
    if (i === index) {
      th.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
    }
  });
}

function nextModalImage() {
  if (!activeModalApt) return;
  let next = activeModalImgIndex + 1;
  if (next >= activeModalApt.images.length) next = 0;
  selectModalImage(next);
}

function prevModalImage() {
  if (!activeModalApt) return;
  let prev = activeModalImgIndex - 1;
  if (prev < 0) prev = activeModalApt.images.length - 1;
  selectModalImage(prev);
}

function closeModal() {
  const modal = document.getElementById('details-modal');
  if (modal && modal.classList.contains('active')) {
    modal.classList.remove('active');
    modal.setAttribute('aria-hidden', 'true');
    setPageInert(false);
    document.body.style.overflow = '';
    activeModalApt = null;
    activeModalImgIndex = 0;
    if (lastModalFocus && document.contains(lastModalFocus)) lastModalFocus.focus();
    lastModalFocus = null;
  }
}

/* ===================================================================
   5. FAQS ACCORDION
   =================================================================== */
function setupFAQs() {
  const faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach((item, index) => {
    const question = item.querySelector('.faq-question');
    const answer = item.querySelector('.faq-answer');
    if (question) {
      const questionId = `faq-question-${index + 1}`;
      const answerId = `faq-answer-${index + 1}`;
      const isInitiallyOpen = item.classList.contains('open');
      question.id = questionId;
      question.setAttribute('aria-controls', answerId);
      question.setAttribute('aria-expanded', String(isInitiallyOpen));
      if (answer) {
        answer.id = answerId;
        answer.setAttribute('role', 'region');
        answer.setAttribute('aria-labelledby', questionId);
        answer.setAttribute('aria-hidden', String(!isInitiallyOpen));
      }
      question.addEventListener('click', () => {
        const isOpen = item.classList.contains('open');
        faqItems.forEach(i => {
          i.classList.remove('open');
          i.querySelector('.faq-question')?.setAttribute('aria-expanded', 'false');
          i.querySelector('.faq-answer')?.setAttribute('aria-hidden', 'true');
        });
        if (!isOpen) {
          item.classList.add('open');
          question.setAttribute('aria-expanded', 'true');
          answer?.setAttribute('aria-hidden', 'false');
        }
      });
    }
  });
}

/* ===================================================================
   6. SCROLL & MOBILE NAVBAR
   =================================================================== */
function setupScrollEffects() {
  const header = document.querySelector('.header');
  const backToTop = document.getElementById('back-to-top');

  window.addEventListener('scroll', () => {
    const scrollY = window.scrollY;

    if (header) {
      header.classList.toggle('scrolled', scrollY > 40);
    }

    if (backToTop) {
      backToTop.classList.toggle('visible', scrollY > 400);
    }
  });

  if (backToTop) {
    backToTop.addEventListener('click', () => {
      const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      window.scrollTo({ top: 0, behavior: reducedMotion ? 'auto' : 'smooth' });
    });
  }
}

function setupMobileNav() {
  const toggleBtn = document.getElementById('mobile-toggle');
  const navMenu = document.getElementById('nav-menu');
  const header = document.querySelector('.header');

  if (toggleBtn && navMenu) {
    const setMenuOpen = (isOpen, restoreFocus = false) => {
      navMenu.classList.toggle('open', isOpen);
      navMenu.inert = !isOpen && window.innerWidth <= 960;
      header?.classList.toggle('menu-open', isOpen);
      toggleBtn.setAttribute('aria-expanded', String(isOpen));
      toggleBtn.innerHTML = isOpen ? '<i class="fa-solid fa-xmark"></i>' : '<i class="fa-solid fa-bars"></i>';
      if (isOpen) navMenu.querySelector('.nav-link')?.focus();
      else if (restoreFocus) toggleBtn.focus();
    };

    setMenuOpen(false);
    toggleBtn.addEventListener('click', () => setMenuOpen(!navMenu.classList.contains('open')));

    const links = navMenu.querySelectorAll('.nav-link');
    links.forEach(l => {
      l.addEventListener('click', () => setMenuOpen(false));
    });

    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && navMenu.classList.contains('open')) {
        setMenuOpen(false, true);
      }
    });

    window.addEventListener('resize', () => {
      if (window.innerWidth > 960) setMenuOpen(false);
      else if (!navMenu.classList.contains('open')) navMenu.inert = true;
    });
  }
}

/* ===================================================================
   REVIEWS RENDERING WITH DIRECT AIRBNB REDIRECTS
   =================================================================== */
function renderReviews(reviews) {
  const container = document.getElementById('reviews-grid');
  if (!container || !reviews) return;

  container.innerHTML = reviews.map(rev => `
    <a href="${rev.airbnb_url}" target="_blank" rel="noopener noreferrer" class="review-card-link" title="Click to view this review on Airbnb">
      <div class="review-card">
        <div>
          <div class="review-header-meta">
            <div class="review-stars">
              ${'<i class="fa-solid fa-star"></i>'.repeat(rev.rating)}
            </div>
            <span class="review-airbnb-tag">
              <i class="fa-brands fa-airbnb"></i> Airbnb
            </span>
          </div>

          <span class="review-apt-badge">
            <i class="fa-solid fa-hotel"></i> ${rev.date}
          </span>

          <p class="review-text">"${rev.text}"</p>
        </div>

        <div>
          <div class="review-author">
            <div class="author-avatar">${rev.avatar}</div>
            <div class="author-details">
              <h5>${rev.author}</h5>
              <span>${rev.country} · Airbnb Guest</span>
            </div>
          </div>
          <span class="review-redirect-hint">
            View on Airbnb <i class="fa-solid fa-arrow-up-right-from-square"></i>
          </span>
        </div>
      </div>
    </a>
  `).join('');
}

/* ===================================================================
   SMOOTH AUTOMATIC PAGE SCROLLING (WITHOUT USER NEEDING TO SCROLL)
   =================================================================== */
let autoScrollInterval = null;
let isAutoScrolling = false;

function initAutoScroll() {
  const toggleBtn = document.getElementById('autoscroll-toggle');

  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      if (isAutoScrolling) {
        stopAutoScroll();
      } else {
        startAutoScroll();
      }
    });
  }

  // Manual input always wins; automatic scrolling is explicitly opt-in.
  const handleUserInteraction = () => {
    if (isAutoScrolling) stopAutoScroll();
  };

  window.addEventListener('wheel', handleUserInteraction, { passive: true });
  window.addEventListener('touchmove', handleUserInteraction, { passive: true });
  window.addEventListener('keydown', handleUserInteraction);
  document.addEventListener('visibilitychange', () => {
    if (document.hidden && isAutoScrolling) stopAutoScroll();
  });
}

function startAutoScroll() {
  if (isAutoScrolling) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  isAutoScrolling = true;
  updateAutoScrollBtn(true);
  beginAutoScrollInterval();
}

function stopAutoScroll() {
  isAutoScrolling = false;
  clearInterval(autoScrollInterval);
  updateAutoScrollBtn(false);
}

function beginAutoScrollInterval() {
  clearInterval(autoScrollInterval);
  autoScrollInterval = setInterval(() => {
    const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
    if (window.scrollY >= maxScroll - 5) {
      stopAutoScroll();
    } else {
      window.scrollBy({ top: 1.2, behavior: 'auto' });
    }
  }, 32);
}

function updateAutoScrollBtn(active) {
  const toggleBtn = document.getElementById('autoscroll-toggle');
  if (!toggleBtn) return;
  toggleBtn.classList.toggle('active', active);
  toggleBtn.setAttribute('aria-pressed', String(active));
  toggleBtn.innerHTML = active 
    ? '<i class="fa-solid fa-pause"></i> Auto-Scroll: On' 
    : '<i class="fa-solid fa-play"></i> Auto-Scroll: Off';
}

/* ===================================================================
   SCROLL REVEAL (premium fade-in)
   =================================================================== */
document.addEventListener('DOMContentLoaded', () => {
  const els = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) { els.forEach(e => e.classList.add('in')); return; }
  const io = new IntersectionObserver(entries => {
    entries.forEach(en => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
  }, { threshold: 0.12 });
  els.forEach(e => io.observe(e));
});
