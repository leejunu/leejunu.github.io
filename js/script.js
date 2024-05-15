// Updates only the main content and not side and top nav
document.addEventListener('DOMContentLoaded', function() {
  const links = document.querySelectorAll('.nav-link');
  const mainContent = document.getElementById('main-content');

  links.forEach(link => {
    link.addEventListener('click', function(event) {
      console.log(link)
      if (!link.href.endsWith('cv.pdf')) {
        event.preventDefault();

        fetch(link.href)
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
function showAbstract(abstractId) {
  var paragraph = document.getElementById(abstractId);

  if (paragraph.style.display === "none") {
    paragraph.style.display = "block";
  } else {
    paragraph.style.display = "none";
  }
}
