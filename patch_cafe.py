# 1. Update index.html
with open('index.html', 'r') as f:
    html = f.read()

# Add Cafe to navigation
old_nav = """      <nav class="nav-menu" id="nav-menu">
        <a href="#home" class="nav-link active">Home</a>
        <a href="#apartments" class="nav-link">Apartments</a>
        <a href="#hosts" class="nav-link">Hosts</a>
        <a href="#amenities" class="nav-link">Amenities</a>
        <a href="#location" class="nav-link">Location</a>
        <a href="#reviews" class="nav-link">Reviews</a>
        <a href="#contact" class="nav-link">Contact</a>
      </nav>"""

new_nav = """      <nav class="nav-menu" id="nav-menu">
        <a href="#home" class="nav-link active">Home</a>
        <a href="#apartments" class="nav-link">Apartments</a>
        <a href="#cafe" class="nav-link">In-House Cafe</a>
        <a href="#hosts" class="nav-link">Hosts</a>
        <a href="#amenities" class="nav-link">Amenities</a>
        <a href="#location" class="nav-link">Location</a>
        <a href="#reviews" class="nav-link">Reviews</a>
        <a href="#contact" class="nav-link">Contact</a>
      </nav>"""

html = html.replace(old_nav, new_nav)

# Add trust bar item / mention
old_trust = """      <div class="trust-card">
        <div class="trust-icon"><i class="fa-solid fa-utensils"></i></div>
        <div class="trust-info">
          <h4>Fully Equipped Kitchens</h4>
          <p>Gas stove, fridge, cookware &amp; dining</p>
        </div>
      </div>"""

new_trust = """      <div class="trust-card">
        <div class="trust-icon"><i class="fa-solid fa-mug-hot"></i></div>
        <div class="trust-info">
          <h4>Pokhara Java Coffee</h4>
          <p>Fresh in-house café &amp; artisan brews</p>
        </div>
      </div>"""

html = html.replace(old_trust, new_trust)

# Add dedicated Cafe Section right before amenities
cafe_section = """  <!-- In-House Cafe Spotlight Section -->
  <section class="section cafe-section" id="cafe">
    <div class="container">
      <div class="cafe-card-wrapper">
        <div class="cafe-content">
          <span class="section-tag" style="background: rgba(217, 119, 6, 0.15); color: #d97706;">
            <i class="fa-solid fa-mug-saucer"></i> On-Premise Coffee Experience
          </span>
          <h2 class="section-title">Pokhara Java Coffee — Right Inside Your Apartment Compound</h2>
          <p class="section-desc" style="text-align: left; margin-bottom: 1.5rem;">
            You don't even need to leave the building to enjoy world-class artisanal Himalayan coffee! <strong>Pokhara Java Coffee</strong> is our in-house café located right on-site at Pokhara Studio INN. Wake up to freshly brewed espresso, cappuccino, locally sourced Nepali organic beans, and delicious breakfast treats steps from your studio door.
          </p>

          <div class="cafe-features-grid">
            <div class="cafe-feature-item">
              <i class="fa-solid fa-seedling"></i>
              <div>
                <h5>Locally Sourced Organic Coffee</h5>
                <p>Specialty grade Himalayan Arabica beans roasted to perfection.</p>
              </div>
            </div>
            <div class="cafe-feature-item">
              <i class="fa-solid fa-laptop-code"></i>
              <div>
                <h5>Work &amp; Chill Friendly</h5>
                <p>Peaceful ambiance, power outlets &amp; fast fiber Wi-Fi for remote work.</p>
              </div>
            </div>
            <div class="cafe-feature-item">
              <i class="fa-solid fa-bread-slice"></i>
              <div>
                <h5>Breakfast &amp; Bakery Items</h5>
                <p>Fresh toasts, bakery bites, smoothies, teas, and healthy breakfast bowls.</p>
              </div>
            </div>
            <div class="cafe-feature-item">
              <i class="fa-solid fa-door-open"></i>
              <div>
                <h5>Zero Walking Commute</h5>
                <p>Located on the apartment grounds — step straight downstairs from your room.</p>
              </div>
            </div>
          </div>

          <div class="cafe-cta-wrap">
            <a href="https://share.google/vMG6krHgbNpJV7Kwg" target="_blank" rel="noopener noreferrer" class="btn btn-gold">
              <i class="fa-brands fa-google"></i> View Pokhara Java Coffee on Google
            </a>
            <a href="https://wa.me/9779856043981?text=Hello!%20I%20would%20love%20to%20know%20more%20about%20Pokhara%20Java%20Coffee%20and%20the%20apartments." target="_blank" rel="noopener noreferrer" class="btn btn-whatsapp">
              <i class="fa-brands fa-whatsapp"></i> Inquire on WhatsApp
            </a>
          </div>
        </div>

        <div class="cafe-media-col">
          <div class="cafe-image-card">
            <img src="images/apartments/23583417_1.png" alt="Pokhara Java Coffee at Pokhara Studio INN" class="cafe-img-hero">
            <div class="cafe-badge-float">
              <i class="fa-solid fa-star" style="color: #fbbf24;"></i>
              <div>
                <strong>Pokhara Java Coffee</strong>
                <span>In-House Artisanal Cafe</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
"""

html = html.replace('<!-- Amenities Highlights Section -->', cafe_section + '\n  <!-- Amenities Highlights Section -->')

# Also add in FAQ
old_faq = """        <div class="faq-item">
          <button class="faq-question">
            <span>Do all 9 apartments have private kitchens and bathrooms?</span>
            <i class="fa-solid fa-chevron-down"></i>
          </button>
          <div class="faq-answer">
            <p>Yes. Every single one of our 9 studio apartments has its own private attached bathroom with 24/7 hot shower and its own fully equipped private kitchen (gas stove, refrigerator, utensils, kettle, and cookware).</p>
          </div>
        </div>"""

new_faq = """        <div class="faq-item">
          <button class="faq-question">
            <span>Is there a café or breakfast available on site?</span>
            <i class="fa-solid fa-chevron-down"></i>
          </button>
          <div class="faq-answer">
            <p>Yes! We have our own on-site café, <strong>Pokhara Java Coffee</strong> (<a href="https://share.google/vMG6krHgbNpJV7Kwg" target="_blank" style="color: var(--accent); font-weight: 600;">View on Google</a>), located right in the apartment property. Guests can enjoy freshly roasted specialty Nepali coffee, breakfast, bakery items, and drinks without leaving the premises.</p>
          </div>
        </div>

        <div class="faq-item">
          <button class="faq-question">
            <span>Do all 9 apartments have private kitchens and bathrooms?</span>
            <i class="fa-solid fa-chevron-down"></i>
          </button>
          <div class="faq-answer">
            <p>Yes. Every single one of our 9 studio apartments has its own private attached bathroom with 24/7 hot shower and its own fully equipped private kitchen (gas stove, refrigerator, utensils, kettle, and cookware).</p>
          </div>
        </div>"""

html = html.replace(old_faq, new_faq)

with open('index.html', 'w') as f:
    f.write(html)

print('Updated index.html with Cafe section and Google link!')

# 2. Append CSS for Cafe Section
with open('css/styles.css', 'r') as f:
    css = f.read()

cafe_css = """
/* ================= IN-HOUSE CAFE SECTION ================= */
.cafe-section {
  background: #fdfbf7;
  border-top: 1px solid #f1ece1;
  border-bottom: 1px solid #f1ece1;
  padding: 5rem 0;
}
.cafe-card-wrapper {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 3.5rem;
  align-items: center;
  background: #ffffff;
  padding: 3.5rem;
  border-radius: var(--radius-lg);
  border: 1px solid #ebdccb;
  box-shadow: 0 10px 30px -10px rgba(180, 83, 9, 0.08);
}
.cafe-content h2 {
  font-size: 2.3rem;
  margin-bottom: 1rem;
}
.cafe-features-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
  margin-bottom: 2rem;
}
.cafe-feature-item {
  display: flex;
  align-items: flex-start;
  gap: 0.85rem;
}
.cafe-feature-item i {
  color: #b45309;
  background: #fef3c7;
  width: 38px;
  height: 38px;
  min-width: 38px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
}
.cafe-feature-item h5 {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--primary);
  margin-bottom: 0.2rem;
}
.cafe-feature-item p {
  font-size: 0.825rem;
  color: var(--text-muted);
  line-height: 1.4;
}
.cafe-cta-wrap {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}
.cafe-media-col {
  position: relative;
}
.cafe-image-card {
  position: relative;
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  border: 4px solid #ffffff;
}
.cafe-img-hero {
  width: 100%;
  height: 380px;
  object-fit: cover;
  transition: transform 0.5s ease;
}
.cafe-image-card:hover .cafe-img-hero {
  transform: scale(1.03);
}
.cafe-badge-float {
  position: absolute;
  bottom: 20px;
  left: 20px;
  right: 20px;
  background: rgba(15, 23, 42, 0.88);
  backdrop-filter: blur(10px);
  color: #ffffff;
  padding: 1rem 1.25rem;
  border-radius: var(--radius-md);
  border: 1px solid rgba(255, 255, 255, 0.15);
  display: flex;
  align-items: center;
  gap: 1rem;
}
.cafe-badge-float strong {
  display: block;
  font-size: 1.05rem;
  color: #fbbf24;
}
.cafe-badge-float span {
  font-size: 0.8rem;
  color: #cbd5e1;
}

@media (max-width: 900px) {
  .cafe-card-wrapper {
    grid-template-columns: 1fr;
    padding: 2rem 1.5rem;
    gap: 2rem;
  }
  .cafe-features-grid {
    grid-template-columns: 1fr;
  }
  .cafe-img-hero {
    height: 280px;
  }
}
"""

if '.cafe-section' not in css:
    css += cafe_css
    with open('css/styles.css', 'w') as f:
        f.write(css)
    print('Updated css/styles.css with cafe styles!')
