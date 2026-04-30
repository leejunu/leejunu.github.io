// Updates only the main content and not side and top nav
document.addEventListener('DOMContentLoaded', function() {
  const links = document.querySelectorAll('.nav-link');
  const mainContent = document.getElementById('main-content');

  links.forEach(link => {
    link.addEventListener('click', function(event) {
      if (!link.href.endsWith('cv.pdf')) {
        event.preventDefault();
        const url = new URL(link.href);
        url.searchParams.set('_ts', Date.now().toString());

        fetch(url.toString(), { cache: 'no-store' })
          .then(response => response.text())
          .then(html => {
            mainContent.innerHTML = html;
          })
          .catch(error => console.error('Error fetching page:', error));
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
