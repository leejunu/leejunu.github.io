// Updates only the main content and not side and top nav
document.addEventListener('DOMContentLoaded', function() {
  const links = document.querySelectorAll('.nav-link');
  const mainContent = document.getElementById('main-content');
  const navbar = document.getElementById('navbarNav');

  function closeNavbar() {
    if (!navbar) {
      return;
    }

    navbar.classList.remove('show');
    navbar.classList.remove('collapsing');
    navbar.classList.add('collapse');
    navbar.removeAttribute('style');

    const toggle = document.querySelector('.navbar-toggler');
    if (toggle) {
      toggle.classList.add('collapsed');
      toggle.setAttribute('aria-expanded', 'false');
    }
  }

  function scheduleNavbarClose() {
    closeNavbar();
    window.setTimeout(closeNavbar, 350);
  }

  links.forEach(link => {
    link.addEventListener('click', function(event) {
      if (!link.href.endsWith('cv.pdf')) {
        event.preventDefault();
        scheduleNavbarClose();
        const url = new URL(link.href);
        url.searchParams.set('_ts', Date.now().toString());

        fetch(url.toString(), { cache: 'no-store' })
          .then(response => response.text())
          .then(html => {
            mainContent.innerHTML = html;
            document.body.classList.remove('home-view');
            document.body.classList.add('section-view');
            scheduleNavbarClose();
            window.scrollTo({ top: 0, behavior: 'auto' });
          })
          .catch(error => console.error('Error fetching page:', error));
      } else {
        scheduleNavbarClose();
      }
    });
  });
});

// Abstract button handling
function showAbstract(abstractId, button) {
  const paragraph = document.getElementById(abstractId);

  if (!paragraph) {
    return;
  }

  const isOpen = paragraph.classList.toggle('is-open');

  if (button) {
    button.classList.toggle('is-open', isOpen);
    button.setAttribute('aria-expanded', String(isOpen));
  }
}
