with open('index.html', 'r') as f:
    html = f.read()

# Update Navbar logo
old_logo = """      <a href="#home" class="logo-container" aria-label="Pokhara Studio INN Homepage">
        <div class="logo-icon">
          <i class="fa-solid fa-mountain-sun"></i>
        </div>
        <div class="logo-text">
          <h1>Pokhara Studio INN</h1>
          <span>Apartments &amp; Suites</span>
        </div>
      </a>"""

new_logo = """      <a href="#home" class="logo-container" aria-label="Pokhara Studio INN Homepage">
        <img src="assets/logo.svg" alt="Pokhara Studio INN Luxury Emblem" class="nav-brand-logo" width="46" height="46">
        <div class="logo-text">
          <h1>Pokhara Studio INN</h1>
          <span>Apartments &amp; Cafe</span>
        </div>
      </a>"""

html = html.replace(old_logo, new_logo)

# Update Footer logo
old_footer_logo = """          <div class="logo-container" style="margin-bottom: 0.5rem;">
            <div class="logo-icon">
              <i class="fa-solid fa-mountain-sun"></i>
            </div>
            <div class="logo-text">
              <h1>Pokhara Studio INN</h1>
              <span>Apartments &amp; Suites</span>
            </div>
          </div>"""

new_footer_logo = """          <div class="logo-container" style="margin-bottom: 0.5rem;">
            <img src="assets/logo.svg" alt="Pokhara Studio INN Luxury Emblem" class="nav-brand-logo" width="50" height="50">
            <div class="logo-text">
              <h1>Pokhara Studio INN</h1>
              <span>Apartments &amp; Cafe</span>
            </div>
          </div>"""

html = html.replace(old_footer_logo, new_footer_logo)

# Update favicon link
old_favicon = """  <!-- Favicon -->
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23d97706'><path d='M12 3L2 12h3v8h6v-5h2v5h6v-8h3L12 3z'/></svg>">"""

new_favicon = """  <!-- Favicon -->
  <link rel="icon" type="image/svg+xml" href="assets/logo.svg">"""

html = html.replace(old_favicon, new_favicon)

with open('index.html', 'w') as f:
    f.write(html)

print('Updated index.html with new logo!')

# Update css/styles.css
with open('css/styles.css', 'r') as f:
    css = f.read()

logo_css = """
.nav-brand-logo {
  width: 46px;
  height: 46px;
  border-radius: 12px;
  object-fit: contain;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.2);
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  display: block;
}
.logo-container:hover .nav-brand-logo {
  transform: scale(1.08) rotate(-3deg);
}
"""

if '.nav-brand-logo' not in css:
    css += logo_css
    with open('css/styles.css', 'w') as f:
        f.write(css)
    print('Added .nav-brand-logo to styles.css!')
