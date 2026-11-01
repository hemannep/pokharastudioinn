with open('js/main.js', 'r') as f:
    js = f.read()

# 1. Update DOMContentLoaded to include renderReviews and initAutoScroll
old_ready = """document.addEventListener('DOMContentLoaded', () => {
  initHeroSlider();
  renderApartments(APARTMENTS_DATA);
  setupFilters();
  setupSearch();
  setupModal();
  setupFAQs();
  setupScrollEffects();
  setupMobileNav();
});"""

new_ready = """document.addEventListener('DOMContentLoaded', () => {
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
});"""

js = js.replace(old_ready, new_ready)

# 2. Add renderReviews implementation and AutoScroll implementation
additional_js = """
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
              <i class="fa-brands fa-airbnb"></i> Verified Review
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
let userInterruptedTimeout = null;

function initAutoScroll() {
  const toggleBtn = document.getElementById('autoscroll-toggle');
  
  // Start automatic tour smoothly after initial 3.5 seconds
  setTimeout(() => {
    startAutoScroll();
  }, 3500);

  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      if (isAutoScrolling) {
        stopAutoScroll();
      } else {
        startAutoScroll();
      }
    });
  }

  // If user scrolls manually or touches screen, pause auto-scroll temporarily then resume
  const handleUserInteraction = () => {
    if (isAutoScrolling) {
      pauseAutoScrollTemporarily();
    }
  };

  window.addEventListener('wheel', handleUserInteraction, { passive: true });
  window.addEventListener('touchmove', handleUserInteraction, { passive: true });
}

function startAutoScroll() {
  if (isAutoScrolling) return;
  isAutoScrolling = true;
  updateAutoScrollBtn(true);

  clearInterval(autoScrollInterval);
  autoScrollInterval = setInterval(() => {
    const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
    if (window.scrollY >= maxScroll - 5) {
      // Loop smoothly back to top when reaching bottom
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
      window.scrollBy({ top: 1.2, behavior: 'auto' });
    }
  }, 22); // ~45px per second smooth steady reading speed
}

function stopAutoScroll() {
  isAutoScrolling = false;
  clearInterval(autoScrollInterval);
  clearTimeout(userInterruptedTimeout);
  updateAutoScrollBtn(false);
}

function pauseAutoScrollTemporarily() {
  clearInterval(autoScrollInterval);
  clearTimeout(userInterruptedTimeout);
  
  // Resume auto-scroll after 7 seconds of user inactivity
  userInterruptedTimeout = setTimeout(() => {
    if (isAutoScrolling) {
      startAutoScroll();
    }
  }, 7000);
}

function updateAutoScrollBtn(active) {
  const toggleBtn = document.getElementById('autoscroll-toggle');
  if (!toggleBtn) return;
  toggleBtn.classList.toggle('active', active);
  toggleBtn.innerHTML = active 
    ? '<i class="fa-solid fa-pause"></i> Auto-Scroll: On' 
    : '<i class="fa-solid fa-play"></i> Auto-Scroll: Off';
}
"""

# Clean slideCard function of any dots logic
old_slide = """  if (dotsContainer) {
    const dots = dotsContainer.querySelectorAll('.card-dot');
    dots.forEach((dot, i) => {
      dot.classList.toggle('active', i === (idx % dots.length));
    });
  }"""
js = js.replace(old_slide, "")

js += additional_js

with open('js/main.js', 'w') as f:
    f.write(js)

print('Updated js/main.js successfully with reviews & smooth auto-scroll!')
