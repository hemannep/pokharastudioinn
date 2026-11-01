with open('css/styles.css', 'r') as f:
    css = f.read()

# 1. Update header and navbar
old_navbar = """.header {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border-color);
  transition: var(--transition);
}
.header.scrolled {
  box-shadow: var(--shadow-sm);
  background: rgba(255, 255, 255, 0.98);
}
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 76px;
}
.logo-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.logo-icon {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #0f172a, #334155);
  color: #fbbf24;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.35rem;
  box-shadow: 0 4px 10px rgba(15, 23, 42, 0.2);
}
.logo-text h1 {
  font-family: var(--font-serif);
  font-size: 1.35rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--primary);
  line-height: 1.1;
}
.logo-text span {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--accent);
  font-weight: 700;
  display: block;
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 2rem;
}
.nav-link {
  font-size: 0.925rem;
  font-weight: 600;
  color: var(--text-muted);
  position: relative;
  padding: 0.25rem 0;
}
.nav-link:hover, .nav-link.active {
  color: var(--primary);
}
.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--accent);
  transition: var(--transition);
}
.nav-link:hover::after, .nav-link.active::after {
  width: 100%;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}"""

new_navbar = """.header {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-bottom: 1px solid rgba(226, 232, 240, 0.9);
  transition: var(--transition);
}
.header.scrolled {
  box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.08);
  background: rgba(255, 255, 255, 0.99);
}
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 72px;
  gap: 1.5rem;
}
.logo-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-shrink: 0;
}
.logo-icon {
  width: 42px;
  height: 42px;
  background: linear-gradient(135deg, #0f172a, #334155);
  color: #fbbf24;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  box-shadow: 0 3px 8px rgba(15, 23, 42, 0.18);
}
.logo-text h1 {
  font-family: var(--font-serif);
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--primary);
  line-height: 1.1;
  white-space: nowrap;
}
.logo-text span {
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--accent);
  font-weight: 700;
  display: block;
}

.nav-menu {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.6rem;
  margin: 0 auto;
}
.nav-link {
  font-size: 0.88rem;
  font-weight: 600;
  color: #475569;
  position: relative;
  padding: 0.4rem 0.2rem;
  white-space: nowrap;
  letter-spacing: -0.01em;
}
.nav-link:hover {
  color: var(--primary);
}
.nav-link.active {
  color: var(--accent);
  font-weight: 700;
}
.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--accent);
  border-radius: 2px;
  transition: var(--transition);
}
.nav-link:hover::after, .nav-link.active::after {
  width: 100%;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  flex-shrink: 0;
}"""

if old_navbar in css:
    css = css.replace(old_navbar, new_navbar)
    print("Replaced navbar CSS successfully!")
else:
    print("Warning: old_navbar not exact match, checking partial...")

# 2. Update card-photo-counter and remove card-dots
old_counter = """.card-dots {
  position: absolute;
  bottom: 12px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 5px;
  z-index: 8;
  background: rgba(15, 23, 42, 0.55);
  padding: 4px 8px;
  border-radius: var(--radius-full);
  backdrop-filter: blur(4px);
  max-width: 80%;
  overflow-x: hidden;
}
.card-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  transition: var(--transition);
  cursor: pointer;
}
.card-dot.active {
  background: #ffffff;
  width: 16px;
  border-radius: 10px;
}

/* Photo Counter Badge (e.g. 1/35) */
.card-photo-counter {
  position: absolute;
  bottom: 12px;
  right: 12px;
  z-index: 8;
  background: rgba(15, 23, 42, 0.75);
  color: #ffffff;
  font-size: 0.72rem;
  font-weight: 600;
  padding: 0.2rem 0.55rem;
  border-radius: var(--radius-full);
  backdrop-filter: blur(4px);
  pointer-events: none;
}"""

new_counter = """/* Photo Counter Badge (Clean Minimal Pill) */
.card-photo-counter {
  position: absolute;
  bottom: 12px;
  right: 12px;
  z-index: 8;
  background: rgba(15, 23, 42, 0.8);
  color: #ffffff;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.3rem 0.65rem;
  border-radius: var(--radius-full);
  backdrop-filter: blur(6px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  pointer-events: none;
  display: flex;
  align-items: center;
  gap: 0.35rem;
}"""

if old_counter in css:
    css = css.replace(old_counter, new_counter)
    print("Replaced card dots & counter CSS successfully!")

# 3. Add Auto-scroll toggle and clickable review card styles
reviews_and_autoscroll_css = """
/* ================= AUTO-SCROLL FLOATING TOGGLE ================= */
.autoscroll-toggle-btn {
  position: fixed;
  bottom: 24px;
  left: 80px;
  z-index: 990;
  background: #ffffff;
  color: var(--primary);
  border: 1px solid var(--border-color);
  padding: 0.55rem 1rem;
  border-radius: var(--radius-full);
  font-size: 0.8rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.45rem;
  box-shadow: var(--shadow-md);
  transition: var(--transition);
  cursor: pointer;
}
.autoscroll-toggle-btn:hover {
  border-color: var(--accent);
  color: var(--accent);
  transform: translateY(-2px);
}
.autoscroll-toggle-btn.active {
  background: var(--primary);
  color: #ffffff;
  border-color: var(--primary);
}
.autoscroll-toggle-btn.active i {
  color: #fbbf24;
}

/* ================= CLICKABLE REVIEWS CARD ENHANCEMENT ================= */
.review-card-link {
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
  height: 100%;
}
.review-card {
  padding: 2rem;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  background: #ffffff;
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
  transition: var(--transition);
  position: relative;
  overflow: hidden;
}
.review-card:hover {
  transform: translateY(-5px);
  border-color: #ff385c;
  box-shadow: 0 12px 24px -4px rgba(255, 56, 92, 0.12), 0 4px 10px -2px rgba(0,0,0,0.04);
}
.review-header-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.9rem;
}
.review-airbnb-tag {
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--airbnb);
  background: #fff0f3;
  padding: 0.25rem 0.55rem;
  border-radius: var(--radius-full);
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  border: 1px solid #ffd1d9;
}
.review-apt-badge {
  font-size: 0.75rem;
  color: var(--accent);
  font-weight: 600;
  margin-bottom: 0.75rem;
  display: block;
}
.review-text {
  font-size: 0.925rem;
  color: #334155;
  line-height: 1.6;
  font-style: italic;
  margin-bottom: 1.5rem;
  flex-grow: 1;
}
.review-redirect-hint {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--airbnb);
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  margin-top: 0.75rem;
  transition: var(--transition);
}
.review-card:hover .review-redirect-hint {
  transform: translateX(3px);
}
"""

css += reviews_and_autoscroll_css

with open('css/styles.css', 'w') as f:
    f.write(css)

print('Updated css/styles.css successfully!')
