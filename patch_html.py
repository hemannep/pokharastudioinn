with open('index.html', 'r') as f:
    html = f.read()

# 1. Update nav labels to be clean and compact
old_nav = """      <nav class="nav-menu" id="nav-menu">
        <a href="#home" class="nav-link active">Home</a>
        <a href="#apartments" class="nav-link">Our 9 Apartments</a>
        <a href="#hosts" class="nav-link">Meet Superhosts</a>
        <a href="#amenities" class="nav-link">Amenities</a>
        <a href="#location" class="nav-link">Location &amp; Map</a>
        <a href="#reviews" class="nav-link">Reviews</a>
        <a href="#contact" class="nav-link">Contact</a>
      </nav>"""

new_nav = """      <nav class="nav-menu" id="nav-menu">
        <a href="#home" class="nav-link active">Home</a>
        <a href="#apartments" class="nav-link">Apartments</a>
        <a href="#hosts" class="nav-link">Hosts</a>
        <a href="#amenities" class="nav-link">Amenities</a>
        <a href="#location" class="nav-link">Location</a>
        <a href="#reviews" class="nav-link">Reviews</a>
        <a href="#contact" class="nav-link">Contact</a>
      </nav>"""

html = html.replace(old_nav, new_nav)

# 2. Update reviews section with id="reviews-grid" and click hint
old_reviews = """      <div class="reviews-grid">
        <div class="review-card">
          <div>
            <div class="review-stars">
              <i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i>
            </div>
            <p class="review-text">
              "Ekraj and Heman are wonderful hosts! The apartment was sparkling clean, quiet, and had everything needed to cook our own meals. Fast internet made remote working seamless. 10/10 recommended!"
            </p>
          </div>
          <div class="review-author">
            <div class="author-avatar">SM</div>
            <div class="author-details">
              <h5>Sarah M.</h5>
              <span>United Kingdom · 1-Month Stay</span>
            </div>
          </div>
        </div>

        <div class="review-card">
          <div>
            <div class="review-stars">
              <i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i>
            </div>
            <p class="review-text">
              "We loved the peaceful surroundings away from Lakeside party noise, yet only a quick stroll when we wanted food or coffee. Ekraj helped store our extra bags while we trekked Mardi Himal."
            </p>
          </div>
          <div class="review-author">
            <div class="author-avatar">DL</div>
            <div class="author-details">
              <h5>David &amp; Lisa</h5>
              <span>Germany · Trekking Vacation</span>
            </div>
          </div>
        </div>

        <div class="review-card">
          <div>
            <div class="review-stars">
              <i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i><i class="fa-solid fa-star"></i>
            </div>
            <p class="review-text">
              "Hot showers with great water pressure, comfortable bed, sunny balcony, and Superhost hospitality at its finest. Whenever we needed anything, WhatsApp response was instant. Truly our home in Pokhara!"
            </p>
          </div>
          <div class="review-author">
            <div class="author-avatar">KT</div>
            <div class="author-details">
              <h5>Kenji Tanaka</h5>
              <span>Japan · Studio Guest</span>
            </div>
          </div>
        </div>
      </div>"""

new_reviews = """      <div class="reviews-grid" id="reviews-grid">
        <!-- Rendered dynamically from REVIEWS_DATA with direct Airbnb review redirects -->
      </div>"""

html = html.replace(old_reviews, new_reviews)

# 3. Add Auto-scroll floating button right beside back to top
old_btt = """  <!-- Back to Top Button -->
  <button class="back-to-top" id="back-to-top" aria-label="Back to top">
    <i class="fa-solid fa-arrow-up"></i>
  </button>"""

new_btt = """  <!-- Auto Scroll Floating Toggle -->
  <button class="autoscroll-toggle-btn active" id="autoscroll-toggle" aria-label="Toggle Auto Scroll">
    <i class="fa-solid fa-pause"></i> Auto-Scroll: On
  </button>

  <!-- Back to Top Button -->
  <button class="back-to-top" id="back-to-top" aria-label="Back to top">
    <i class="fa-solid fa-arrow-up"></i>
  </button>"""

html = html.replace(old_btt, new_btt)

with open('index.html', 'w') as f:
    f.write(html)

print('Updated index.html successfully!')
