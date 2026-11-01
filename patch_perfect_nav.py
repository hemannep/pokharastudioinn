with open('css/styles.css', 'r') as f:
    css = f.read()

# Replace the header and navbar section with the ultra-refined styling
start_target = "/* ================= HEADER / NAVBAR ================= */"
end_target = "/* ================= HERO SECTION & SLIDER ================= */"

s_idx = css.find(start_target)
e_idx = css.find(end_target)

if s_idx != -1 and e_idx != -1:
    perfect_navbar_css = """/* ================= HEADER / NAVBAR ================= */
.header {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.96);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(226, 232, 240, 0.85);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.header.scrolled {
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.06);
  border-bottom-color: #cbd5e1;
}
.header .container {
  max-width: 1360px;
  padding: 0 1.5rem;
}
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 70px;
  gap: 1.25rem;
}

/* Brand Logo */
.logo-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-shrink: 0;
  text-decoration: none;
}
.nav-brand-logo {
  width: 44px;
  height: 44px;
  border-radius: 11px;
  object-fit: contain;
  box-shadow: 0 3px 10px rgba(15, 23, 42, 0.15);
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  display: block;
}
.logo-container:hover .nav-brand-logo {
  transform: scale(1.06);
}
.logo-text h1 {
  font-family: var(--font-serif);
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: -0.015em;
  color: #0f172a;
  line-height: 1.1;
  white-space: nowrap;
}
.logo-text span {
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: #d97706;
  font-weight: 700;
  display: block;
  margin-top: 1px;
}

/* Nav Menu: Modern Pill Hover */
.nav-menu {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  margin: 0 auto;
}
.nav-link {
  font-size: 0.85rem;
  font-weight: 600;
  color: #475569;
  padding: 0.45rem 0.85rem;
  border-radius: var(--radius-full);
  white-space: nowrap;
  letter-spacing: -0.01em;
  transition: all 0.2s ease;
  position: relative;
}
.nav-link:hover {
  color: #0f172a;
  background: #f1f5f9;
}
.nav-link.active {
  color: #d97706;
  background: #fef3c7;
  font-weight: 700;
}
.nav-link::after {
  display: none;
}

/* Nav Action Buttons */
.nav-actions {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex-shrink: 0;
}
.btn-nav {
  padding: 0.55rem 1.15rem;
  font-size: 0.84rem;
  font-weight: 600;
  border-radius: var(--radius-full);
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  transition: all 0.25s ease;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.btn-nav-whatsapp {
  background: #25d366;
  color: #ffffff;
}
.btn-nav-whatsapp:hover {
  background: #1ebc57;
  color: #ffffff;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(37, 211, 102, 0.3);
}
.btn-nav-airbnb {
  background: #ff385c;
  color: #ffffff;
}
.btn-nav-airbnb:hover {
  background: #e00b41;
  color: #ffffff;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 56, 92, 0.3);
}

.mobile-toggle {
  display: none;
  font-size: 1.35rem;
  color: #0f172a;
  padding: 0.4rem;
  border-radius: 8px;
}

"""
    css = css[:s_idx] + perfect_navbar_css + css[e_idx:]
    with open('css/styles.css', 'w') as f:
        f.write(css)
    print('Updated navbar CSS to perfect modern pill design!')
else:
    print('Failed to find navbar markers')

# Also update class in index.html to btn-nav
with open('index.html', 'r') as f:
    html = f.read()

old_actions = """      <div class="nav-actions">
        <a href="https://wa.me/9779856043981?text=Hello%20Pokhara%20Studio%20INN,%20I%20would%20like%20to%20inquire%20about%20apartment%20rates%20and%20availability." target="_blank" rel="noopener noreferrer" class="btn btn-whatsapp">
          <i class="fa-brands fa-whatsapp"></i> Chat WhatsApp
        </a>
        <a href="#apartments" class="btn btn-airbnb">
          <i class="fa-brands fa-airbnb"></i> View on Airbnb
        </a>
        <button class="mobile-toggle" id="mobile-toggle" aria-label="Toggle navigation menu">
          <i class="fa-solid fa-bars"></i>
        </button>
      </div>"""

new_actions = """      <div class="nav-actions">
        <a href="https://wa.me/9779856043981?text=Hello%20Pokhara%20Studio%20INN,%20I%20would%20like%20to%20inquire%20about%20apartment%20rates%20and%20availability." target="_blank" rel="noopener noreferrer" class="btn-nav btn-nav-whatsapp">
          <i class="fa-brands fa-whatsapp"></i> WhatsApp
        </a>
        <a href="#apartments" class="btn-nav btn-nav-airbnb">
          <i class="fa-brands fa-airbnb"></i> View on Airbnb
        </a>
        <button class="mobile-toggle" id="mobile-toggle" aria-label="Toggle navigation menu">
          <i class="fa-solid fa-bars"></i>
        </button>
      </div>"""

html = html.replace(old_actions, new_actions)
with open('index.html', 'w') as f:
    f.write(html)

print('Updated index.html button classes!')
